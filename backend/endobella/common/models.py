from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SeoGaioBase(models.Model):
    meta_title = models.CharField(
        max_length=70,
        blank=True,
        help_text=_(
            "Custom meta title for SEO (max 70 characters). Leave blank to use the default title."
        ),
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text=_("Custom meta description for SEO (max 160 characters)."),
    )
    focus_keyword = models.CharField(
        max_length=100,
        blank=True,
        help_text=_("Main keyword or phrase for this content."),
    )
    canonical_url = models.URLField(
        blank=True, help_text=_("Canonical URL to prevent duplicate content issues.")
    )
    no_index = models.BooleanField(
        default=False, help_text=_("Prevent search engines from indexing this page.")
    )
    content_abstract = models.TextField(
        max_length=500,
        blank=True,
        help_text=_(
            "A factual, concise summary of the content for AI models (max 500 characters)."
        ),
    )
    key_questions_answered = models.TextField(
        blank=True,
        help_text=_(
            "List key questions this content answers, one per line. Used for FAQ snippets and conversational AI."
        ),
    )

    class Meta:
        abstract = True
