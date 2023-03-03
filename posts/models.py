from django.db import models
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    # class Meta: 
    #     ordering = ["-updated"]
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)])