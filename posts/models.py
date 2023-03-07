from datetime import datetime
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import utc

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

    class Meta: 
        ordering = ["-date_created"]
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)])
    
    @property 
    def post_preview(self):
        return ' '.join(self.content.split(' ')[:10]) + " ..."
    
    @property
    def cap_author(self):
        return f'{self.author}'.capitalize()
    
    # @property
    # def time_diff(self):
    #     return timezone.now() - self.updated
    
    # def time_from_last_update(self):
    #     if self.updated:
    #         now = datetime.utcnow().replace(tzinfo=utc)
    #         timediff = now - self.updated
    #         return timediff.days()