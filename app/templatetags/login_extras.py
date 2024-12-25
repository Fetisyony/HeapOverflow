from urllib.parse import urlencode
from django import template
from django.urls import reverse
from askme_fetisov.settings import MEDIA_URL
import os

register = template.Library()

@register.simple_tag(takes_context=True)
def get_login_url_with_continue(context):
    request = context['request']
    current_path = request.path
    login_url = reverse('login') 
    query_string = urlencode({'continue': current_path})
    return f"{login_url}?{query_string}"
