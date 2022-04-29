from functools import wraps
from http.client import BAD_REQUEST

from blog.models import Auth_token
from rest_framework.response import Response 


def is_auth_token_transaction(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        token = request.headers['Authorization']
        auth_is_autenticated = Auth_token.objects.filter(token=token).first()
        if auth_is_autenticated is not None:
            request.logged_user = auth_is_autenticated.user_payer
            return function(request, *args, **kwargs)
        else:
            response = {'message': 'NOT ALLOWED ACCESS!!'}
            return Response(response, status=400)

    wrapper.__name__ = function.__name__
    wrapper.__doc__ = function.__doc__
    return wrapper


