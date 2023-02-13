from django import forms

from .models import Post

class PostFormNew(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        ordering = ['-date_created']

class PostForm(forms.Form):
    title = forms.CharField(label='Enter a title', max_length=50)
    content = forms.CharField(widget=forms.Textarea)