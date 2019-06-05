from __future__ import absolute_import, unicode_literals

from django.db import models
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField

from wagtail.core.models import Page

from core.wagtail.stream_block import ARTICLE_STREAM_BLOCK


class HomePage(Page):
    content = StreamField(ARTICLE_STREAM_BLOCK, blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('content')
    ]

