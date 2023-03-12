from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post, Comment

# Create your tests here.

class PostCreateViewTest(TestCase):
    def test_post_create_stores_user(self):
        user1 = get_user_model().objects.create_user(
            username='user1', email='user1@gmail.com', password='1234'
        )
        
        post_data = {
            'title': 'test post',
            'content': 'Hello world',
        }
        self.client.force_login(user1)
        self.client.post(reverse('post_create'), post_data)

        self.assertTrue(Post.objects.filter(author=user1).exists())

class PostUpdateViewTest(TestCase):
    def test_post_update_returns_404(self):
        user1 = get_user_model().objects.create_user(
            username='user1', email='user1@gmail.com', password='1234'
        )
        user2 = get_user_model().objects.create_user(
            username='user2', email='user2@gmail.com', password='1234'
        )

        post = Post.objects.create(
            author=user1, title='test post', content='Hello world')

        self.client.force_login(user2)
        response = self.client.post(
            reverse('post_edit', kwargs=({'pk': post.id})),
            {'title': 'change title'}
        )
        self.assertEqual(response.status_code, 404)
        
""" 

class PostTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='qwerty'
        )

        cls.post = Post.objects.create(
            title ='Some title',
            content = 'Some post content',
            author = cls.user,
        )
        
        '''
        cls.user_2 = get_user_model().objects.create_user(
            username='testuser_2',
            email='test_2@email.com',
            password='secret'
        )
        
        cls.comment = Comment.objects.create(
            post = cls.post,
            body = 'Test comment',
            author = cls.user_2  
        )
        '''
    
    def test_string_representation(self):
        post = Post(title='Some title')
        self.assertEqual(str(post), post.title)
        # comment = Comment(comment='Test comment')
        # self.assertEqual(str(comment), comment.comment)
    
    def test_post_content(self):
        self.assertEqual(self.post.title, 'Some title')
        self.assertEqual(self.post.author.username, 'testuser')
        self.assertEqual(self.post.content, 'Some post content')
        self.assertEqual(str(self.post), 'Some title')
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")
    
    '''
    def test_comment_content(self):
        self.assertEqual(self.comment.post, 'Some post content')
        self.assertEqual(self.comment.comment, 'Test comment')
        self.assertEqual(self.comment.author, 'testuser_2')
        self.assertEqual(str(self.comment), 'Test comment')
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")
    '''
    
    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Some post content')
        self.assertTemplateUsed(response, 'posts/home.html')
    
    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
    def test_post_detail_view(self):
        response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
        no_response = self.client.get('/post/50000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Some title')
        # self.assertContains(response, 'Some post content')
        # self.assertContains(response, 'Test comment')
        # self.assertContains(response, 'testuser')
        self.assertTemplateUsed(response, 'posts/detail.html')
        
    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)
        
    def test_post_create_view(self):
        response = self.client.post(
            reverse('post_new'), 
            {
                'title': 'New title',
                'content': 'New text',
                'author': self.user.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertContains(Post.objects.last().title, "New title")
        self.assertContains(Post.objects.last().content, "New text")
    
    def test_post_update_view(self):
        response = self.client.post(
            reverse('post_edit', args='1'),
            {
                'title': 'Updated title',
                'content': 'Updated text',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertContains(Post.objects.last().title, "Updated title")
        self.assertContains(Post.objects.last().content, "Updated text")
        
    def test_post_delete_view(self):
        response = self.client.post(
            reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 302)

        
    '''
    # Tests with comments 
    
    def test_submit_comment_logged_in(self):
        self.client.login(username='testuser_2', password='secret')
        url = reverse('post_detail', args=[1])
        response = self.client.post(url, {
            'author': self.user_2,
            'comment': 'Test comment'
        })
        self.assertEqual(response.status_code, 302)  # Found redirect
        self.assertEqual(Comment.objects.last().author, self.user_2 )
        self.assertEqual(Comment.objects.last().comment, 'Test comment')
        
    def test_submit_comment_logged_out_fail(self):
        self.client.logout()
        last_comment = Comment.objects.last()
        url = reverse('post_detail', args=[1])
        response = self.client.post(url, {
            'name': 'Samuel', 
            'comment': 'I am not the real author',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, you cannot use this name.")
        self.assertEqual(last_comment, Comment.objects.last())
        
    def test_submit_comment_logged_out_success(self):
        self.client.logout()
        url = reverse('post_detail', args=[1])
        response = self.client.post(url, {
            'author': self.user_2,
            'comment': "I definitely have to try this!"
        })
        self.assertEqual(response.status_code, 302)  # Found redirect
        self.assertEqual(Comment.objects.last().author, self.user_2)
        self.assertEqual(Comment.objects.last().comment, "I definitely have to try this!")
    '''
    
        
class HomePageTests(SimpleTestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/home.html')
        
'''

"""
