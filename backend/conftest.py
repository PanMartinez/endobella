from __future__ import annotations

import pytest
from django.core.cache import cache
from django.utils import timezone
from rest_framework.test import APIClient

from endobella.articles.models import Article
from endobella.auth.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture()
def auth_client(client, test_user: User):
    client.force_login(test_user)
    return client


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()


@pytest.fixture
def dummy_user(db):
    def _create_dummy_user(**kwargs):
        user = User.objects.create(**kwargs)
        return user

    return _create_dummy_user


@pytest.fixture
def test_user(db, dummy_user):
    return dummy_user(
        email="test@user.com",
        first_name="John",
        last_name="Doe",
        password="TestUser123",
    )


@pytest.fixture
def dummy_article(db):
    def _create_dummy_article(**kwargs):
        article = Article.objects.create(**kwargs)
        return article

    return _create_dummy_article


@pytest.fixture
def test_article(db, dummy_article, test_user):
    article = dummy_article(
        title="Test Article",
        slug="test-article",
        author=test_user,
        featured_image="test-article.jpg",
        content="Test content",
        excerpt="Test excerpt",
        is_featured=True,
        is_published=True,
        publish_date=timezone.now(),
        article_type=Article.Type.ARTICLE,
        show_table_of_contents=True,
    )
    return article


@pytest.fixture
def test_article_unpublished(db, dummy_article, test_user):
    article = dummy_article(
        title="Test Article Unpublished",
        slug="test-article-unpublished",
        author=test_user,
        featured_image="test-article-unpublished.jpg",
        content="Test content",
        excerpt="Test excerpt",
        is_featured=True,
        is_published=False,
    )
    return article
