import uuid
from django.test import Client,TestCase
from django.shortcuts import redirect
from blog.models import UserPayer, Wallet, Auth_token
from blog.utils import bcrypt_password_login
from blog.views import register


class TestTransactionsUtils(TestCase):
    client = Client()

    def get_token(self, email, password):
        payload_login_correct = {"email": f'{email}', "password": f'{password}'}
        response_login = self.client.post('/login/', payload_login_correct, content_type='application/json')
        token = response_login.json()['newToken']['token']
        return token
        pass


def create_user(document, name, email, psw):
    user = UserPayer()
    user.document = document
    user.name = name
    user.email = email
    user.psw = bcrypt_password_login(psw)
    user.save()
    auth = Auth_token()
    auth.id_user = user
    auth.token = uuid.uuid4()
    auth.save()


def register_user(request):
    print(request)
    register(request)
    

def create_wallet(user):
    wallet = Wallet()
    wallet.user_id = user
    wallet.save()


def get_token(payload_login_correct):
    user_token = UserPayer.objects.get(email=payload_login_correct["email"])
    token = Auth_token.objects.get(id_user=user_token)
    print(token)



