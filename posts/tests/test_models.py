from django.test import TestCase

from ..models import Post, Comment

class TestModels(TestCase):
    def test_model_str(self):
        post = Post.objects.create(
            title="",
            author=self.request.user,
            content="",
        )
        
        comment = Comment.objects.create(
            post=post,
            body="",
            author=self.request.user,
        )
        self.assertEqual(str(post.title), "")
        self.assertEqual(str(comment.body), "")