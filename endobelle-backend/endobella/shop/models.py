from django.db import models

from endobella.common.models import BaseModel

import json
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class SlugModelBase(BaseModel):
    class Meta:
        abstract = True

    name = models.CharField(max_length=255, help_text="The name of the object.")
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text="A URL-friendly version of the name. Auto-generated if left blank.",
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(SlugModelBase):
    """
    Represents a product category, supporting a hierarchical structure.
    e.g., Clothing > Mens > T-Shirts
    """

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        help_text="The parent category, for creating a hierarchy.",
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]


class Tag(SlugModelBase):
    """
    Represents a non-hierarchical tag for grouping products.
    e.g., "eco-friendly", "best-seller", "new-arrival"
    """

    class Meta:
        ordering = ["name"]


class Product(SlugModelBase):
    """
    The main product model, acting as a "template" for its variants.
    It holds all the shared information across different versions of a product.
    """

    # --- Core and Commerce Fields ---
    short_description = models.TextField(
        blank=True, help_text="A concise, punchy summary for list views."
    )
    long_description = models.TextField(
        blank=True,
        help_text="The detailed, comprehensive description for the product page.",
    )

    # --- Taxonomy and Relationships ---
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        help_text="The primary category for this product.",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="products",
        help_text="Tags for non-hierarchical classification.",
    )

    # --- Status and Timestamps ---
    is_available = models.BooleanField(
        default=True, help_text="Is this product available for purchase?"
    )

    # --- Advanced SEO Fields ---
    meta_title = models.CharField(
        max_length=255,
        blank=True,
        help_text="Custom <title> tag for SEO. If blank, the product name will be used.",
    )
    meta_description = models.CharField(
        max_length=300,
        blank=True,
        help_text="Custom <meta name='description'> tag for SEO.",
    )

    # --- Generative AI Optimization (GAIO) Fields ---
    class BrandVoiceChoices(models.TextChoices):
        PLAYFUL = "PLAYFUL", "Playful & Witty"
        PROFESSIONAL = "PROFESSIONAL", "Professional & Technical"
        MINIMALIST = "MINIMALIST", "Minimalist & Elegant"
        ADVENTUROUS = "ADVENTUROUS", "Adventurous & Bold"

    gaio_brand_voice = models.CharField(
        max_length=20,
        choices=BrandVoiceChoices.choices,
        default=BrandVoiceChoices.PROFESSIONAL,
        help_text="Defines the tone for AI-generated content.",
    )
    gaio_target_personas = models.JSONField(
        default=list,
        blank=True,
        help_text="Structured data on target audiences (e.g., [{'persona': '...', 'pain_point': '...'}]).",
    )
    gaio_key_features = models.JSONField(
        default=list,
        blank=True,
        help_text="Benefit-oriented features for AI input (e.g., [{'feature': '...', 'benefit': '...'}]).",
    )
    gaio_structured_facts = models.JSONField(
        default=dict,
        blank=True,
        help_text="Verifiable, citable product data points (e.g., {'Material': 'Organic Cotton'}).",
    )
    gaio_faq_data = models.JSONField(
        default=list,
        blank=True,
        help_text="Q&A pairs for conversational search (e.g., [{'q': '...', 'a': '...'}]).",
    )
    gaio_description_variants = models.JSONField(
        default=dict,
        blank=True,
        help_text="Stores A/B test variations of descriptions and their performance data.",
    )

    class Meta:
        ordering = ["-created_at"]

    def get_average_rating(self):
        """Calculates the average rating from all reviews."""
        return self.reviews.aggregate(Avg("rating"))["rating__avg"]

    def get_schema_json(self, request):
        """Generates a JSON-LD schema for the product, essential for rich results in Google."""
        default_variant = (
            self.variants.filter(is_default=True).first() or self.variants.first()
        )
        if not default_variant:
            return "{}"

        schema = {
            "@context": "https://schema.org/",
            "@type": "Product",
            "name": self.name,
            "image": [
                request.build_absolute_uri(img.image.url) for img in self.images.all()
            ],
            "description": self.short_description or self.long_description,
            "sku": default_variant.sku,
            "brand": {
                "@type": "Brand",
                "name": "YourBrandName",
            },  # Replace with a Brand model if you have one
            "offers": {
                "@type": "Offer",
                "url": request.build_absolute_uri(self.get_absolute_url()),
                "priceCurrency": "USD",  # Replace with your store's currency
                "price": str(default_variant.price),
                "availability": (
                    "https://schema.org/InStock"
                    if self.is_available and default_variant.stock_quantity > 0
                    else "https://schema.org/OutOfStock"
                ),
                "itemCondition": "https://schema.org/NewCondition",
            },
        }

        avg_rating = self.get_average_rating()
        review_count = self.reviews.count()
        if avg_rating and review_count > 0:
            schema = {
                "@type": "AggregateRating",
                "ratingValue": round(avg_rating, 2),
                "reviewCount": review_count,
            }

        return json.dumps(schema, indent=2)

    def get_absolute_url(self):
        # This requires you to have a URL pattern named 'product_detail'
        from django.urls import reverse

        return reverse("product_detail", kwargs={"slug": self.slug})


class ProductVariant(BaseModel):
    """
    Represents a specific, sellable version of a product.
    e.g., The "Large", "Blue" version of a T-Shirt.
    This model holds the unique SKU, price, and stock for each variation.
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    sku = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique Stock Keeping Unit for this specific variant.",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="The price of this specific variant."
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Optional promotional price.",
    )
    stock_quantity = models.PositiveIntegerField(
        default=0, help_text="Inventory level for this variant."
    )

    # Example attribute fields. Add more as needed for your products.
    size = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)

    is_default = models.BooleanField(
        default=False,
        help_text="Should this variant be shown by default on the product page?",
    )

    class Meta:
        # Ensure only one variant can be the default for a given product
        unique_together = ("product", "size", "color")  # Example constraint
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                condition=models.Q(is_default=True),
                name="unique_default_variant",
            )
        ]
        ordering = ["size", "color"]

    def __str__(self):
        attributes = filter(None, [self.size, self.color])
        return f"{self.product.name} ({', '.join(attributes)})"


class ProductImage(BaseModel):
    """
    Stores an image associated with a product.
    Allows for multiple images per product.
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Descriptive text for accessibility and SEO.",
    )

    def __str__(self):
        return f"Image for {self.product.name}"


class Review(BaseModel):
    """
    Stores a customer review for a product.
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5.",
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("product", "user")  # A user can only review a product once

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"
