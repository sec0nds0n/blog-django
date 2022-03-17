from urllib import response
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
        
    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), {
            'title':'New title',
            'body':'New text',
            'author': self.user.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'New title')
        self.assertEqual(Post.objects.last().body, 'New text')
        
    def test_post_update_view(self):
        response = self.client.post(reverse('post_edit', args='1'),{
            'title':'Updated title',
            'body':'Updated text',
        })
        self.assertEqual(response.status_code, 302)
        
    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 302)