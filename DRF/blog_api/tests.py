from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from blog.models import Post, Category
from django.contrib.auth.models import User


class PostTest(APITestCase):
    listcreate_url = reverse('blog_api:listcreate')

    def setUp(self):
        self.client = APIClient()
        self.post_payload = {'title': 'new',
                             'author': 1,
                             'category': 1,
                             'excerpt': 'new',
                             'content': 'new',
                             'slug': 'test_slug'}
        self.test_user_1 = User.objects.create_user(username='test_user1', password='123456789')
        self.test_user_2 = User.objects.create_user(username='test_user2', password='123456789')
        self.test_category = Category.objects.create(name='django')

    def test_view_post(self):
        response = self.client.get(self.listcreate_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        # Login required
        self.client.login(username=self.test_user_1.username, password='123456789')

        response = self.client.post(self.listcreate_url, self.post_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_update(self):
        """Specific user can update only own post"""
        self.client.login(username=self.test_user_1.username, password='123456789')
        test_post = self.client.post(self.listcreate_url, self.post_payload, format='json')
        post_url = reverse('blog_api:detailcreate', kwargs={'pk': 1})
        response = self.client.put( post_url, self.post_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)





