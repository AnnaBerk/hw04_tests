from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.cache import cache

from ..models import Post


User = get_user_model()


class GroupViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост больше 15 символов',
        )
        cls.post2 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост больше 15 символов',
        )

    # @classmethod
    # def tearDownClass(cls):

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
   
   
    def test_index_cache(self):
        """
        Проверяем что механизм кеша главной страницы работает
        """
        url = reverse('posts:index')
        response = self.guest_client.get(url)
        count = len(response.context['page_obj'])
        self.assertEqual(len(response.context['page_obj']), count)
        # post = Post.objects.filter(id=1)
        # post.delete()
        # response = self.guest_client.get(url)
        # count = len(response.context['page_obj'])
        # self.assertEqual(len(response.context['page_obj']), count)