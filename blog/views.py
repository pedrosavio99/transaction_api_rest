from rest_framework.decorators import  api_view
from blog.decorator import is_auth_token_transaction
from blog.services.login_service import login_services
from blog.services.register_services import register_services
from blog.services.transaction_services import make_transaction_services, status_transaction_services


@api_view(['POST', 'GET'])
def login(request):
    return login_services(request)


@api_view(['POST'])
def register(request):
    return register_services(request)


@api_view(['POST', 'GET'])
@is_auth_token_transaction
def make_transaction(request):
    return make_transaction_services(request)


@api_view(['POST', 'GET'])
@is_auth_token_transaction
def status_transaction_auth(request):
    return status_transaction_services(request)
