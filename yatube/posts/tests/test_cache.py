# from django.test import TestCase, Client, override_settings
# from django.contrib.auth import get_user_model

# from django.core.cache import cache

# from ..models import Post


# User = get_user_model()


# class GroupViewTests(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.user = User.objects.create_user(username='auth')
#         cls.post = Post.objects.create(
#             author=cls.user,
#             text='Тестовый пост больше 15 символов',
#         )

#     # @classmethod
#     # def tearDownClass(cls):

#     def setUp(self):
#         self.guest_client = Client()
#         self.authorized_client = Client()
#         self.authorized_client.force_login(self.user)
   
   
#     def test_new_group_has_no_posts(self):
#             """В новой группе не было постов"""
            
#             cache_ind = cache.get('index_page')
#             self.assertEqual((Post.objects), cache_ind)
       
#         # self.assertTrue(
#         #     cache.filter(
#         #         text='Тестовый пост больше 15 символов',
#         #     ).exists()
#         # )
            