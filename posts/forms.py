from django import forms

from .models import Post

class PostFormNew(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        ordering = ['-date_created']

class PostForm(forms.Form):
    title = forms.CharField(max_length=50)
    content = forms.CharField()