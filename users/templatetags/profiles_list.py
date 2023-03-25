from django import template

from ..models import Profile

register = template.Library()

@register.simple_tag
def get_profiles():
    profiles = Profile.objects.all()
    return profiles
    