from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.files.images import get_image_dimensions

from .models import Profile

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                            'class': 'form-control',
                                                            }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                            'class': 'form-control',
                                                            }))
    username = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                            'class': 'form-control',
                                                            }))
    email = forms.EmailField(required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                            'class': 'form-control',
                                                            }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                    'class': 'form-control',
                                                                    'data-toggle': 'password',
                                                                    'id': 'password',
                                                                    }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                    'class': 'form-control',
                                                                    'data-toggle': 'password',
                                                                    'id': 'password',
                                                                    }))

    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name',
            'username', 
            'email', 
            'password1', 
            'password2', 
            ]

        def save(self, commit=True):
            user = super(SignUpForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(
                                    attrs={'placeholder': 'Username',
                                            'class': 'form-control',
                                            }))
    
    password = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Password',
                                            'class': 'form-control',
                                            'data-toggle': 'password',
                                            'id': 'password',
                                            'name': 'password',
                                            }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            #validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    f'Please use an image that is '
                    '{max_width} x {max_height} pixels or smaller.')

            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            #validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    f'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar
    
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']

class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

'''
class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'first_name', 
            'last_name', 
            'email',
            ]
'''   