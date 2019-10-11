#A custom django has_group conditional tag
#  usage:
#
#      {% if request.user|has_group:"Manager" %}  {% endif %}
#
# Developer: Thanos Vassilakis, 2002


import re, string
from django import template

register = template.Library()


from django.contrib.auth.models import Group


@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
        return True if group in user.groups.all() else False
    except Group.DoesNotExist:
        return False
