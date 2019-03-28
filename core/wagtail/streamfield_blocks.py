from __future__ import absolute_import, unicode_literals

from django.utils.functional import cached_property

from wagtail.core.blocks import ChooserBlock
from wagtail.core.models import Collection
from wagtail.images.shortcuts import get_rendition_or_not_found
import json

from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.widgets import AdminChooser


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
