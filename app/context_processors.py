from askme_fetisov.settings import MEDIA_URL
import os
import time, jwt
from django.conf import settings

def get_centrifugo_info(user_id):
    secret = settings.CENTRIFUGO_SECRET
    ws_url = settings.CENTRIFUGO_WS_URL
    claims = {"sub": str(user_id), "exp": int(time.time()) + 5 * 60}
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM3MjIiLCJleHAiOjE3MzU3NDQzOTQsImlhdCI6MTczNTEzOTU5NH0.av6TVQnidqtiCdxczRib5dnYSPY7kjjA29T89OoFzGg"
    return {"token": token, "ws_url": ws_url}

def topbar_default_staff(request):
    default_profile_image = os.path.join(MEDIA_URL, 'images/profile_default.jpg')

    return {
        'default_profile_image': default_profile_image,
        **get_centrifugo_info(request.user.id)
    }
