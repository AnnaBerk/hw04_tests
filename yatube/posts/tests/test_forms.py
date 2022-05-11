from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Post, Group

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='group',
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

    def test_can_create_post(self):
        """Авторизированный пользователь может создавать пост"""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст из формы',
            'group.title': 'group',
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': 'auth'})
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Текст из формы',
            ).exists()
        )

    def test_can_edit_post(self):
        """Авторизированный пользователь может редактировать пост"""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст из формы',
            'group.title': 'group',
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': '1'}),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': '1'})
        )
        self.assertEqual(Post.objects.count(), posts_count)
        new_post = Post.objects.get(id='1')
        self.assertEqual(new_post.id, self.post.id)
        self.assertNotEqual(new_post.text, self.post.text)

    def test_cant_create_post(self):
        """Неавторизированный пользователь не может создавать пост"""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст из формы',
            'group.title': 'group',
        }
        response = self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, '/auth/login/?next=/create/')
        self.assertEqual(Post.objects.count(), posts_count)
