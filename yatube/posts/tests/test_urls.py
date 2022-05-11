from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from http import HTTPStatus

from ..models import Post, Group

User = get_user_model()


class GroupURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Тестовое описание',
            slug='slug',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост больше 15 симовлов',
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.create_url = '/create/'
        self.unexisting_url = '/unexisting/'

    def get_update_url(self, id):
        return f'/posts/{id}/edit/'

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/slug/': 'posts/group_list.html',
            '/profile/auth/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_create_url_uses_correct_template(self):
        """Страница создания поста использует верный шаблон."""
        response = self.authorized_client.get(self.create_url)
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_urls_exists_at_desired_location(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = [
            '/',
            '/group/slug/',
            '/profile/auth/',
            '/posts/1/',
        ]
        for address in templates_url_names:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_exists_at_desired_location_authorized(self):
        """Страница создания поста доступна авторизованному
        пользователю."""
        response = self.authorized_client.get(self.create_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_redirect_anonymous_on_admin_login(self):
        """Страница создания поста перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get(self.create_url, follow=True)
        self.assertRedirects(
            response, ('/auth/login/?next=/create/'))

    def test_post_edit_url_exists_at_desired_location_authorized(self):
        """Страница редактирования поста доступна авторизованному
        пользователю."""
        response = self.authorized_client.get(
            self.get_update_url(self.post.id)
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_url_uses_correct_template(self):
        """Страница редактирования поста использует верный шаблон."""
        response = self.authorized_client.get(
            self.get_update_url(self.post.id)
        )
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_unexisting_page_exists_at_desired_location(self):
        """Несуществующая страница доступна любому пользователю."""
        response = self.guest_client.get(self.unexisting_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
