from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from ..models import Post, Group


User = get_user_model()


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='author')
        cls.grouppag = Group.objects.create(
            title='grouppag',
            description='Тестовое описание',
            slug='slugpag',
        )
        cls.grouppag2 = Group.objects.create(
            title='grouppag2',
            description='Тестовое описание2',
            slug='slugpag2',
        )
        for _ in range(0, 13):
            cls.post = Post.objects.create(
                author=cls.user,
                text='Тестовый пост',
                group=cls.grouppag,
            )
        for _ in range(0, 5):
            cls.post = Post.objects.create(
                author=cls.user,
                text='Тестовый пост',
                group=cls.grouppag2,
            )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_paginator(self):
        TEN_POSTS = 10
        EIGHT_POSTS = 8
        FIVE_POSTS = 5
        urls_posts = {
            '/': TEN_POSTS,
            '/?page=2': EIGHT_POSTS,
            '/group/slugpag/': TEN_POSTS,
            '/group/slugpag2/': FIVE_POSTS,
            '/profile/author/': TEN_POSTS,
            '/profile/author/?page=2': EIGHT_POSTS,
        }
        for url, cnt in urls_posts.items():
            with self.subTest(cnt=cnt):
                response = self.client.get(url)
                self.assertEqual(len(response.context['page_obj']), cnt)
