import uuid
from rest_framework.response import Response
from blog.models import UserPayer, Wallet, Auth_token
from blog.serializers import Auth_tokenSerializer, UserPayerSerializer
from blog.utils import bcrypt_password_login


def register_services(request):
    try:
        document = request.data['document']
        name = request.data['name']
        email = request.data['email']
        password = request.data['password']

        if len(document.strip()) == 0:
            response = {'message':
                        'complete the field: Valid Document(CNPJ must be 14 digits and CPF must be 11 digits)'}
            return Response(response, status=400)

        if len(name.strip()) == 0:
            response = {'message': 'complete the field: Valid Name'}
            return Response(response, status=400)

        if len(email.strip()) == 0:
            response = {'message': 'complete the field: Valid Email'}
            return Response(response, status=400)

        if len(password) < 8:
            response = {'message': 'password must be 8 characters'}
            return Response(response, status=400)

        if len(document) != 11 and len(document) != 14:
            response = {'message':
                        'complete the field: Valid Document(CNPJ must be 14 digits and CPF must be 11 digits)'}
            return Response(response, status=400)

        user_filter_email = UserPayer.objects.filter(email=email)
        if user_filter_email.count() > 0:
            response = {'message': 'user with the same email already registered'}
            return Response(response, status=400)

        user_filter_doc = UserPayer.objects.filter(document=document)
        if user_filter_doc.count() > 0:
            response = {'message': 'user with the same document already registered'}
            return Response(response, status=400)

        try:
            request.data['password'] = bcrypt_password_login(password)
            user_serializer = UserPayerSerializer(data=request.data)

            if user_serializer.is_valid() and user_serializer.save():
                wallet = Wallet()
                wallet.user_payer = user_serializer.instance
                wallet.save()
                auth = Auth_token()
                auth.user_payer = user_serializer.instance
                auth.token = uuid.uuid4()
                auth.save()

                auth_token_serializer = Auth_tokenSerializer(auth)
                response = {'message': 'user created', 'new user': f'{auth_token_serializer.data}'}
                return Response(response, status=200)
            else:
                response = {'message': 'Create Error', 'message_error': f'{user_serializer.errors}'}
                return Response(response, status=200)
        except Exception as error:
            response = {"Error": str(error)}
            return Response(response, status=400)
    except Exception as error:
        response = {"Error": str(error)}
        return Response(response, status=400)
