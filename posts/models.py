from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

# from django.conf import settings

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True, max_length=140)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    tags = models.CharField(max_length=100, blank=True)
    likes = models.ManyToManyField(User, related_name='post_like', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta: 
        ordering = ['-date_created']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        if self.date_updated is None:
            self.date_updated = timezone.now()
        self.date_updated = None
        return super().save(*args, **kwargs)
    
    def update(self, *args, **kwargs):
        kwargs.update({'date_updated': timezone.now})
        super().update(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[self.pk])
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.CharField(max_length=140)
    author = models.ForeignKey(
        User,
        # settings.AUTH_USER_MODEL,
        editable=False,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    likes = models.ManyToManyField(User, related_name='comment_like', blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-date_created').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    
    class Meta:
        ordering = ['-date_created']
    
    def __str__(self):
        return self.body[:50]

    def get_absolute_url(self):
        return reverse("post_list")
    
'''
class Like(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='likes',
        on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post,
        related_name='likes',
        on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name="unique_like"),
        ]
'''
# https://www.agiliq.com/books/djenofdjango/chapter4.html