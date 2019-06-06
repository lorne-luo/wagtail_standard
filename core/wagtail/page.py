from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from core.wagtail.stream_block import SUPER_STREAM_BLOCKS


class StreamPage(Page):
    content = StreamField(SUPER_STREAM_BLOCKS, blank=True)

    class Meta:
        abstract = True
