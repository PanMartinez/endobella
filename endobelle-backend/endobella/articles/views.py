from django_filters import FilterSet
from endobella.articles.models import Article
from endobella.articles.serializers import ArticleSerializer
from endobella.common.mixins import PublicItemViewMixin


class ArticleFilterSet(FilterSet):
    class Meta:
        model = Article
        fields = [
            "slug",
            "title",
            "excerpt",
            "publish_date",
            "is_featured",
            "is_published",
            "article_type",
            "author",
        ]


class ArticleViewSet(PublicItemViewMixin):
    queryset = Article.objects.filter(is_published=True)
    serializer_class = ArticleSerializer
    lookup_field = "slug"
    search_fields = ["title", "excerpt", "content"]
    ordering_fields = ["created_at", "updated_at", "publish_date", "title"]
    ordering = ["-created_at"]
    filterset_class = ArticleFilterSet
