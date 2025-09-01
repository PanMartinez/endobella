from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager

from endobella.auth.models import User
from endobella.common.models import BaseModel, SeoGaioBase


class Article(BaseModel, SeoGaioBase):
    class Category(models.TextChoices):
        KNOWLEDGE_BASE = "knowledge_base", _("Knowledlege Base")
        WELL_BEING = "well_being", _("Well Being")
        DIET = "Diet", _("Diet")

    class Type(models.TextChoices):
        ARTICLE = "Article", _("Article")
        BLOG_POSTING = "BlogPosting", _("Blog Post")
        NEWS_ARTICLE = "NewsArticle", _("News Article")
        GUIDE = "Guide", _("Guide")

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="articles"
    )
    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        default=Category.KNOWLEDGE_BASE,
        help_text=_("Article category"),
    )
    featured_image = models.ImageField(
        upload_to="uploads/",
        help_text=_("Featured image displayed at the top of the article"),
    )
    excerpt = models.TextField(
        max_length=300, help_text=_("Short excerpt shown in article")
    )
    content = CKEditor5Field(help_text=_("Full article content"), blank=True)

    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    publish_date = models.DateTimeField(
        help_text=_("When this article should be published"), null=True, blank=True
    )

    tags = TaggableManager(blank=True)
    article_type = models.CharField(
        max_length=50,
        choices=Type.choices,
        default=Type.ARTICLE,
        help_text=_("Schema.org article type for structured data"),
    )

    show_table_of_contents = models.BooleanField(
        default=True, help_text=_("Display auto-generated table of contents")
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_published"]),
            models.Index(fields=["publish_date"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/{self.slug}/"
