from urllib.parse import urlparse
from flask import request, url_for


def err_response(msg, status_code):
    return {
        "success": False,
        "error": msg,
        "statusCode": status_code
    }, status_code

def absolute_url(url_name, **value):
    endpoint_uri = urlparse(request.host_url)
    return endpoint_uri._replace(
        path=url_for(url_name, **value)
    ).geturl()
