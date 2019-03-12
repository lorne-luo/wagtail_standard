from django.forms import HiddenInput
from wagtail.wagtailadmin.forms import WagtailAdminPageForm
from django import forms


class ArticleWagtailAdminModelForm(WagtailAdminPageForm):
    class Media:
        js = (
            'js/collection-chooser.js',
            'asset/jquery_chosen/chosen.jquery.min.js'
        )
        css = {
            'all': ('asset/jquery_chosen/chosen.min.css',)
        }
