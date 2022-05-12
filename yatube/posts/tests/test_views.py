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

    def get_first_object(self, response):
        return response.context['page_obj'][0]    

    def test_context(self, url, **kwargs):
        response = self.guest_client.get(reverse(url, **kwargs))
        first_object = self.get_first_object(response)
        contexts = {
            first_object.author.username: self.post.author.username,
            first_object.text: self.post.text,
            first_object.group.title: self.post.group.title
        }
        for obj_ctx, self_ctx in contexts.items():
            with self.subTest():
                self.assertEqual(obj_ctx, self_ctx)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        self.test_context('posts:index')

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        self.test_context('posts:group_list', kwargs={'slug': 'slug'})

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        self.test_context('posts:profile', kwargs={'username': 'auth'})

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': '1'}
        ))
        first_object = response.context['post']
        self.assertEqual(
            first_object.author.username, self.post.author.username
        )
        self.assertEqual(first_object.text, self.post.text)
        self.assertEqual(first_object.group.title, self.post.group.title)

    def test_post_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': '1'})
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)


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

    def test_first_page_contains_ten_records(self):
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_eight_records(self):
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 8)

    def test_group_list_page_contains_ten_records(self):
        response = self.client.get(reverse(
            'posts:group_list', kwargs={'slug': 'slug'})
        )
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_group2_list_page_contains_five_records(self):
        response = self.client.get(reverse(
            'posts:group_list', kwargs={'slug': 'slug2'})
        )
        self.assertEqual(len(response.context['page_obj']), 5)

    def test_first_page_profile_contains_ten_records(self):
        response = self.client.get(reverse(
            'posts:profile', kwargs={'username': 'auth'})
        )
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_profile_contains_eight_records(self):
        response = self.client.get(reverse(
            'posts:profile', kwargs={'username': 'auth'}) + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 8)
