from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post

# Create your tests here.
class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'test@email.com',
            password = 'secret'
        )
        self.post = Post.objects.create(
            title = 'a good title',
            body = 'nice body content',
            author = self.user,
        )
        
    def test_string_representation(self):
        post = Post(title = 'sample titel')
        self.assertEqual(str(post), post.title)
        
    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'a good title')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'nice body content')
        
    def test_post_list_view(self):
        respone = self.client.get(reverse('home'))
        self.assertEqual(respone.status_code, 200)
        self.assertContains(respone, 'a good title')
        self.assertTemplateUsed(respone, 'home.html')
        
    def test_post_detail_view(self):
        respone = self.client.get('/post/1/')
        no_respone = self.client.get('/post/100000/')
        self.assertEqual(respone.status_code, 200)
        self.assertEqual(no_respone.status_code, 404)
        self.assertContains(respone, 'a good title')
        self.assertTemplateUsed(respone, 'post_detail.html')
        