from askme_fetisov.settings import MEDIA_URL
import os


def topbar_default_staff(request):
    default_profile_image = os.path.join(MEDIA_URL, 'images/profile_default.jpg')

    return {
        'default_profile_image': default_profile_image,
    }
