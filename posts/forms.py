from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(label='Enter a title', max_length=50)
    content = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = Post
        fields = ['title', 'content']
        # ordering = ['-date_created']