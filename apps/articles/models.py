from __future__ import absolute_import, unicode_literals

import json
from collections import OrderedDict
from django.db.models import Q

from django.utils import timezone
from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtail.contrib.table_block.blocks import TableBlock
from django.template.defaultfilters import slugify

from apps.articles.forms import ArticleWagtailAdminModelForm
from core.wagtail.stream_block import CollectionChooserBlock


class Category(models.Model):
    name = models.CharField(
        max_length=80, unique=True, verbose_name=_('Category'))
    slug = models.SlugField(unique=True, max_length=80)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name="children",
        help_text=_(
            'Categories, unlike tags, can have a hierarchy. You might have a '
            'Jazz category, and under that have children categories for Bebop'
            ' and Big Band. Totally optional.')
    )
    description = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")

    panels = [
        FieldPanel('name'),
        FieldPanel('parent'),
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            count = Category.objects.filter(slug=slug).count()
            if count > 0:
                slug = '{}-{}'.format(slug, count)
            self.slug = slug
        return super(Category, self).save(*args, **kwargs)


class ArticlePageTag(TaggedItemBase):
    """
    many-to-many relationship between the ArticlePage object and tags.
    """
    content_object = ParentalKey('ArticlePage', related_name='article_tags', on_delete=models.CASCADE)


class ArticlePage(Page):
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)
    is_home_featured = models.BooleanField(_('is home featured'), default=False)
    topic = ParentalKey('topics.TopicPage', related_name='topic_articles', blank=True, null=True,
                        on_delete=models.SET_NULL)  # redundant of parent topicpage
    view_count = models.PositiveIntegerField('view count', blank=False, default=0)
    reading_mins = models.PositiveIntegerField('reading minutes', blank=True, null=True)
    short_description = models.TextField(_('short description'), max_length=512, blank=True)

    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content = StreamField([
        ('heading', blocks.StructBlock([
            ('heading_type', blocks.ChoiceBlock(choices=[
                ('h1', 'H1'),
                ('h2', 'H2'),
                ('h3', 'H3'),
                ('h4', 'H4'),
                ('h5', 'H5'),
                ('h6', 'H6'),
            ])),
            ('heading_text', blocks.CharBlock(required=True)),
        ], icon='title')),
        ('paragraph', blocks.RichTextBlock()),
        ('table', TableBlock(table_options={'colHeaders': False, })),
        ('embed', EmbedBlock()),
        ('download', DocumentChooserBlock(required=True)),
        ('button', blocks.StructBlock([
            ('button_name', blocks.CharBlock(required=True)),
            ('button_url', blocks.CharBlock(required=True)),
            ('button_color', blocks.ChoiceBlock(choices=[
                ('btn--green', 'Green'),
                ('btn--orange', 'Orange'),
                ('btn--yellow', 'Yellow'),
                ('btn--lime', 'Lime'),
                ('btn--blue', 'Blue'),
                ('btn--grey', 'Grey'),
            ], blank=False)),
        ], icon='form')),
        ('html', blocks.RawHTMLBlock()),
        ('image', blocks.StructBlock([
            ('image', ImageChooserBlock()),
            ('image_caption', blocks.CharBlock(required=False)),
            ('image_position', blocks.ChoiceBlock(choices=[
                ('center', 'Center'),
                ('left', 'Left'),
                ('right', 'Right'),
                ('full-width', 'Full width')
            ])),
        ], icon='image')),
        ('gallery', blocks.StructBlock([
            ('gallery_title', blocks.CharBlock(required=False)),
            ('gallery_collection', CollectionChooserBlock()),
        ], icon='picture')),
        ('accoordion', blocks.StructBlock([
            ('accoordion_heading', blocks.CharBlock(required=True)),
            ('accoordion_content', blocks.RichTextBlock()),
        ], icon='arrows-up-down')),
        ('quote', blocks.StructBlock([
            ('quote', blocks.RichTextBlock(required=False)),
        ], icon='openquote')),

    ])

    parent_page_types = ['home.Homepage']
    base_form_class = ArticleWagtailAdminModelForm

    search_fields = Page.search_fields + [
        index.SearchField('content', partial_match=True),
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('main_image'),
        FieldPanel('short_description'),
        StreamFieldPanel('content'),
    ]
    category_content_panels = [
        MultiFieldPanel(
            [
                FieldPanel('topic', widget=forms.Select),
            ],
            heading="Categories,tags Block",
            classname="collapsible"
        ),
        InlinePanel('article_tags', label="Tags", classname="collapsible"),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('is_home_featured'),
        FieldPanel('reading_mins'),
        FieldPanel('owner'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(category_content_panels, heading='Categories'),
        ObjectList(Page.promote_panels, heading='SEO settings'),
        ObjectList(settings_panels, heading='Article settings', classname="settings"),
    ])

    def save(self, *args, **kwargs):
        instance = super(ArticlePage, self).save(*args, **kwargs)

        # unfeature others before call super save
        if self.live and self.is_home_featured:
            root = self.get_root()
            ArticlePage.objects.descendant_of(root).exclude(id=self.id).update(is_home_featured=False)

        return instance

    def update_view_count(self):
        # total view counter
        self.view_count += 1

        self.save(update_fields=['view_count'])

    def serve(self, request, *args, **kwargs):
        self.update_view_count()
        return super(ArticlePage, self).serve(request, *args, **kwargs)
