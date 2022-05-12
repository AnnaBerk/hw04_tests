from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms

from ..models import Post, Group

User = get_user_model()


class GroupViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='group',
            description='Тестовое описание',
            slug='slug',
        )
        cls.group2 = Group.objects.create(
            title='group2',
            description='Тестовое описание2',
            slug='slug2',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост больше 15 символов',
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_group_list_page_show_correct_context(self):
        """Пост group2 не попал на страницу записей group."""
        response = self.authorized_client.get(reverse(
            'posts:group_list', kwargs={'slug': 'slug'}
        ))
        first_object = response.context['page_obj'][0]
        post_group_0 = first_object.group.title
        self.assertNotEqual(post_group_0, 'group2')

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': 'slug'}): (
                'posts/group_list.html'
            ),
            reverse('posts:profile', kwargs={'username': 'auth'}): (
                'posts/profile.html'
            ),
            reverse('posts:post_detail', kwargs={'post_id': '1'}): (
                'posts/post_detail.html'
            ),
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit', kwargs={'post_id': '1'}): (
                'posts/create_post.html'
            ),
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def get_object(self, response,):
        res = response.context
        if 'page_obj' not in res:
            return response.context['post']
        return response.context['page_obj'][0]

    def test_context(func):
        def wrapper(self):
            response = func(self)
            object = self.get_object(response)
            contexts = {
                object.author.username: self.post.author.username,
                object.text: self.post.text,
                object.group.title: self.post.group.title
            }
            for obj_ctx, self_ctx in contexts.items():
                with self.subTest():
                    self.assertEqual(obj_ctx, self_ctx)
        return wrapper

    @test_context
    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        return self.guest_client.get(reverse('posts:index'))

    @test_context
    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        return self.guest_client.get(reverse(
            'posts:group_list', kwargs={'slug': 'slug'})
        )

    @test_context
    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        return self.guest_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': '1'}
        ))

    def test_post_create_and_edit_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response_create_pg = self.authorized_client.get(
            reverse('posts:post_create')
        )
        response_edit_pg = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': '1'})
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response_create_pg.context.get(
                    'form').fields.get(value)
                self.assertIsInstance(form_field, expected)

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response_edit_pg.context.get(
                    'form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_new_group_has_no_posts(self):
        """В новой группе не было постов"""
        form_data = {
            'text': 'Текст из формы',
            'group.title': 'newgroup',
        }
        self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        post_cnt = self.group.posts_group.all().count()
        self.assertEqual(post_cnt, 1)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='group',
            description='Тестовое описание',
            slug='slug',
        )
        cls.group2 = Group.objects.create(
            title='group2',
            description='Тестовое описание2',
            slug='slug2',
        )
        for _ in range(0, 13):
            cls.post = Post.objects.create(
                author=cls.user,
                text='Тестовый пост',
                group=cls.group,
            )
        for _ in range(0, 5):
            cls.post = Post.objects.create(
                author=cls.user,
                text='Тестовый пост',
                group=cls.group2,
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
            '/group/slug/': TEN_POSTS,
            '/group/slug2/': FIVE_POSTS,
            '/profile/auth/': TEN_POSTS,
            '/profile/auth/?page=2': EIGHT_POSTS,
        }
        for url, cnt in urls_posts.items():
            with self.subTest(cnt=cnt):
                response = self.client.get(url)
                self.assertEqual(len(response.context['page_obj']), cnt)
