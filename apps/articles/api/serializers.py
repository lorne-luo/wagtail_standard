from rest_framework import serializers
from ..models import ArticlePage


class ArticlePageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
    next_article = serializers.SerializerMethodField()

    class Meta:
        model = ArticlePage
        fields = ('id', 'title', 'url', 'topic', 'go_live_at', 'next_article')

    def get_url(self, obj):
        return obj.full_url

    def get_topic(self, obj):
        return obj.get_topic()

    def get_next_article(self, obj):
        return obj.get_next_article()
