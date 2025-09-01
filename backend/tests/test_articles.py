import pytest
from django.utils import timezone
from django.urls import reverse
from rest_framework import status

from endobella.articles.models import Article


@pytest.mark.django_db
class TestArticleViewSet:
    article_list_url = reverse("article-list")

    def test_list_articles(self, client, test_article):
        response = client.get(self.article_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["slug"] == test_article.slug
        assert response.data["results"][0]["title"] == test_article.title

    def test_retrieve_article(self, client, test_article):
        url = reverse("article-detail", kwargs={"slug": test_article.slug})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["slug"] == test_article.slug
        assert response.data["title"] == test_article.title

    def test_retrieve_nonexistent_article(self, client):
        url = reverse("article-detail", kwargs={"slug": "nonexistent-article"})
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize(
        "filter_param, filter_value, expected_count",
        [
            ("slug", "test-article", 1),
            ("title", "Test Article", 1),
            ("is_featured", "true", 1),
            ("is_published", "true", 1),
            ("article_type", Article.Type.ARTICLE, 1),
            ("category", "test-category", 1),
        ],
    )
    def test_filter_articles(
        self,
        client,
        test_article,
        filter_param,
        filter_value,
        expected_count,
    ):
        response = client.get(self.article_list_url, {filter_param: filter_value})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == expected_count

    @pytest.mark.parametrize(
        "search_term, expected_count",
        [
            ("Test Article", 1),
            ("Test excerpt", 1),
            ("test content", 1),
            ("nonexistent", 0),
        ],
    )
    def test_search_articles(self, client, test_article, search_term, expected_count):
        response = client.get(self.article_list_url, {"search": search_term})

        assert response.status_code == status.HTTP_200_OK
        for article in response.data["results"]:
            print(article)
        assert len(response.data["results"]) == expected_count

    @pytest.mark.parametrize(
        "ordering, expected_first_slug",
        [
            ("created_at", "test-article"),
            ("-created_at", "second-article"),
            ("updated_at", "test-article"),
            ("-updated_at", "second-article"),
            ("publish_date", "test-article"),
            ("-publish_date", "second-article"),
            ("title", "second-article"),
            ("-title", "test-article"),
        ],
    )
    def test_ordering_articles(
        self, client, test_article, dummy_article, ordering, expected_first_slug
    ):
        dummy_article(
            slug="second-article",
            title="Another Article",
            excerpt="Another excerpt",
            content="Another content",
            is_featured=False,
            is_published=True,
            article_type=Article.Type.ARTICLE,
            publish_date=timezone.now(),
        )
        response = client.get(self.article_list_url, {"ordering": ordering})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"][0]["slug"] == expected_first_slug

    def test_unpublished_article_not_shown(
        self, client, test_article_unpublished, dummy_article
    ):
        response = client.get(self.article_list_url)
        assert response.status_code == status.HTTP_200_OK
        for article in response.data["results"]:
            assert article["slug"] != test_article_unpublished.slug

    def test_unpublished_article_not_retrievable(
        self, client, test_article_unpublished
    ):
        url = reverse("article-detail", kwargs={"slug": test_article_unpublished.slug})
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
