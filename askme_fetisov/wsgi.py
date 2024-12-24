"""
WSGI config for askme_fetisov project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

from io import BytesIO
import os

from django.core.wsgi import get_wsgi_application
from urllib.parse import parse_qs

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askme_fetisov.settings')

application_core = get_wsgi_application()

def application(environ, start_response):
    get_params = parse_qs(environ.get('QUERY_STRING', ''))

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size)
    except (ValueError, TypeError):
        request_body = b""

    environ['wsgi.input'] = BytesIO(request_body)

    print("============================")
    print("GET params:")
    print(get_params)
    if request_body:
        try:
            post_data = request_body.decode('utf-8')
            print("POST params:")
            print(post_data)
        except UnicodeDecodeError:
            print("POST data is not UTF-8 encoded.")
    else:
        print("No POST params")
    print("============================")

    return application_core(environ, start_response)

