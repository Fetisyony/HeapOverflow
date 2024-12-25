from app.models import Profile, Tag
from askme_fetisov.settings import MEDIA_URL
import os
import time, jwt
from django.conf import settings
from django.core.cache import cache


def get_cache(request):
    popular_tags = cache.get('popular_tags')
    if not popular_tags:
        popular_tags = Tag.objects.get_popular_n_tags()
        cache.set('popular_tags', popular_tags, 60)
    
    top_users = cache.get('top_users')
    if not top_users:
        top_users = Profile.objects.get_top_n_users_by_number_of_answers(10)
        cache.set('top_users', top_users, 60)
    return {'popular_tags': popular_tags, 'top_users': top_users}

def get_centrifugo_info(user_id):
    secret = settings.CENTRIFUGO_SECRET
    ws_url = settings.CENTRIFUGO_WS_URL
    claims = {"sub": str(user_id), "exp": int(time.time()) + 5 * 60}
    token = jwt.encode(claims, secret, algorithm="HS256")
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM3MjIiLCJleHAiOjE3MzU3NDQzOTQsImlhdCI6MTczNTEzOTU5NH0.av6TVQnidqtiCdxczRib5dnYSPY7kjjA29T89OoFzGg"
    return {"token": token, "ws_url": ws_url}

def topbar_default_staff(request):
    default_profile_image = os.path.join(MEDIA_URL, 'images/profile_default.jpg')

    cached_data = get_cache(request)

    return {
        'default_profile_image': default_profile_image,
        **get_centrifugo_info(request.user.id),
        **cached_data
    }
