import json

from django.utils.functional import cached_property
from wagtail.admin.widgets import AdminChooser
from wagtail.core import blocks
from wagtail.core.blocks import ChooserBlock, render_to_string
from wagtail.core.models import Collection
from wagtail.images.blocks import ImageChooserBlock
from django.utils.translation import ugettext_lazy as _
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.images.shortcuts import get_rendition_or_not_found
from wagtailstreamforms.blocks import WagtailFormBlock

new_table_options = {
    'colHeaders': False,
}
ARTICLE_STREAM_BLOCK = [
    ('heading', blocks.StructBlock([
        ('heading_type', blocks.ChoiceBlock(choices=[
            ('h2', 'H2'),
            ('h3', 'H3'),
            ('h4', 'H4'),
            ('h5', 'H5'),
            ('h6', 'H6'),
        ])),
        ('heading_text', blocks.CharBlock(required=True)),
    ], icon='title')),
    ('paragraph', blocks.RichTextBlock()),
    ('table', TableBlock(table_options=new_table_options)),
    ('embed', EmbedBlock()),
    ('button', blocks.StructBlock([
        ('button_name', blocks.CharBlock(required=True)),
        ('button_url', blocks.CharBlock(required=True)),
        ('button_color', blocks.ChoiceBlock(choices=[
            ('btn--green', 'Green'),
            ('btn--olive', 'Olive'),
            ('btn--dark-green', 'Dark green'),
            ('btn--lime', 'Lime'),
            ('btn--light-green', 'Light green'),
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
    ('accordion', blocks.StructBlock([
        ('accordion_heading', blocks.CharBlock(required=True)),
        ('accordion_content', blocks.RichTextBlock()),
    ], icon='arrows-up-down')),
    ('quote', blocks.StructBlock([
        ('quote', blocks.RichTextBlock(required=False)),
    ], icon='openquote')),
    ('banner', blocks.StructBlock([
        ('banner_heading', blocks.CharBlock(required=False)),
        ('banner_text', blocks.RichTextBlock(required=False)),
        ('banner_button_name', blocks.CharBlock(required=False)),
        ('banner_button_url', blocks.CharBlock(required=False)),
        ('banner_image', ImageChooserBlock(required=True)),
        ('banner_image_position', blocks.ChoiceBlock(choices=[
            ('bannerimage-bg', 'Image as background'),
            ('bannerimage-section', 'Image in a section')
        ])),
    ], icon='placeholder')),
    ('info_block', blocks.StructBlock([
        ('info_block_heading', blocks.CharBlock(required=False)),
        ('info_block_text', blocks.RichTextBlock(required=False)),
        ('info_block_button_name', blocks.CharBlock(required=False)),
        ('info_block_button_url', blocks.CharBlock(required=False)),
        ('info_block_image', ImageChooserBlock(required=False)),
        ('info_block_image_position', blocks.ChoiceBlock(choices=[
            ('left', 'Image on the left'),
            ('right', 'Image on the right')
        ])),
        ('info_block_icon_section', blocks.ListBlock(blocks.StructBlock([
            ('info_block_icon_text', blocks.CharBlock(required=False)),
            ('info_block_icon_image', ImageChooserBlock(required=False)),
        ]))),
    ], icon='plus')),
    ('multi_blocks', blocks.StructBlock([
        ('multi_blocks_heading', blocks.CharBlock(required=False)),
        ('multi_blocks_section', blocks.ListBlock(blocks.StructBlock([
            ('multi_block_heading', blocks.CharBlock(required=False)),
            ('multi_block_text', blocks.RichTextBlock(required=False)),
            ('multi_block_image', ImageChooserBlock(required=False)),
        ]))),
        ('multi_block_url_text', blocks.CharBlock(required=False)),
        ('multi_block_url', blocks.CharBlock(required=False)),
    ], icon='grip')),
    ('info_banner', blocks.StructBlock([
        ('info_banner_heading', blocks.CharBlock(required=False)),
        ('info_banner_text', blocks.RichTextBlock(required=False)),
        ('info_banner_button_name', blocks.CharBlock(required=False)),
        ('info_banner_button_url', blocks.CharBlock(required=False)),
    ], icon='plus-inverse')),
    ('progress_steps', blocks.StructBlock([
        ('progress_steps_image', ImageChooserBlock(required=False)),
        ('progress_steps_blocks', blocks.ListBlock(blocks.StructBlock([
            ('progress_steps_block_heading', blocks.CharBlock(required=False, label="Step Heading")),
            ('progress_steps_block_text', blocks.RichTextBlock(required=False, label="Step Text")),
            ('progress_steps_block_image', ImageChooserBlock(required=False, label="Step Image")),
        ]))),
    ], icon='order')),
    ('checklist', blocks.StructBlock([
        ('checklist_heading', blocks.CharBlock(required=False)),
        ('checklist_image', ImageChooserBlock(required=False)),
        ('checklist_text', blocks.RichTextBlock(required=False)),
        ('checklist_lists', blocks.ListBlock(blocks.StructBlock([
            ('checklist_list', blocks.CharBlock(required=False, label="Checklist")),
        ]))),
        ('checklist_button_name', blocks.CharBlock(required=False)),
        ('checklist_button_url', blocks.CharBlock(required=False)),
        ('checklist_style', blocks.ChoiceBlock(choices=[
            ('full-checklist', 'Full checklist without image'),
            ('image-checklist', 'Image and checklist side by side'),
        ], blank=False)),
    ], icon='list-ul')),
    ('testimonial', blocks.StructBlock([
        ('testimonial_image', ImageChooserBlock(required=False)),
        ('testimonial_text', blocks.RichTextBlock(required=False)),
        ('testimonial_name', blocks.CharBlock(required=False, label="Name")),
        ('testimonial_position', blocks.CharBlock(required=False, label="Position")),
    ], icon='user')),
    ('multi_testimonials', blocks.StructBlock([
        ('title', blocks.CharBlock(required=False)),
        ('testimonials', blocks.ListBlock(blocks.StructBlock([
            ('testimonial_image', ImageChooserBlock(required=False)),
            ('testimonial_text', blocks.RichTextBlock(required=False)),
            ('testimonial_name', blocks.CharBlock(required=False, label="Name")),
            ('testimonial_position', blocks.CharBlock(required=False, label="Position")),
        ]))),
    ], icon='user')),
    ('form', WagtailFormBlock()),
]


class CollectionChooser(AdminChooser):
    add_one_text = _('Add a collection')
    choose_one_text = _('Choose an collection')
    link_to_chosen_text = _('Edit this collection')

    def __init__(self, **kwargs):
        super(CollectionChooser, self).__init__(**kwargs)
        self.image_model = Collection

    def render_html(self, name, value, attrs):
        collections = Collection.objects.all()
        original_field_html = super(CollectionChooser, self).render_html(name, value, attrs)

        collection_items = []
        for collection in collections:
            if value == collection.id:
                collection_items.append(
                    '<option selected="true" value="%s">%s</option>' % (collection.id, collection.name))
            else:
                collection_items.append('<option value="%s">%s</option>' % (collection.id, collection.name))

        collection_selector = '''
        <select name="%s" id="%s_select" placeholder="%s">
            <option value="" selected="">---------</option>
                %s
        </select>
        ''' % (
            attrs['id'],
            attrs['id'],
            attrs['placeholder'],
            '\n'.join(collection_items)
        )

        return render_to_string("articles/widgets/collection_chooser.html", {
            'widget': self,
            'original_field_html': original_field_html,
            'attrs': attrs,
            'value': value,
            'collection_selector': collection_selector,
        })

    def render_js_init(self, id_, name, value):
        return "createCollectionChooser({0});".format(json.dumps(id_))


class CollectionChooserBlock(ChooserBlock):
    @cached_property
    def target_model(self):
        return Collection

    @cached_property
    def widget(self):
        return CollectionChooser

    def render_basic(self, value, context=None):
        if value:
            return get_rendition_or_not_found(value, 'original').img_tag()
        else:
            return ''

    class Meta:
        icon = "picture"
