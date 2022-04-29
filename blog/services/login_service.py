import uuid
import bcrypt
from rest_framework.response import Response
from blog.models import UserPayer, Auth_token
from blog.serializers import Auth_tokenSerializer


def bcrypt_password_login_check(password_request, email):
    try:
        user_query = UserPayer.objects.get(email=email)
        if user_query:
            user_query_password = user_query.password.encode('utf8')
            password_request = str(password_request).encode('utf8')
            return bcrypt.checkpw(password_request, user_query_password)
        else:
            return False
    except Exception:
        return False


def login_services(request):
    try:
        email = request.data['email']
        password = request.data['password']
    except Exception as error:
        response = {"Fields Error": str(error)}
        return Response(response, status=400)

    try:
        password_authenticate = bcrypt_password_login_check(password, email)
        if password_authenticate:
            user_request = UserPayer.objects.get(email=email)

            if user_request is None:
                response = {'message': 'User not found'}
                return Response(response, status=400)

            auth = Auth_token()
            auth.user_payer = user_request
            auth.token = uuid.uuid4()
            auth.save()

            auth_token_serializer = Auth_tokenSerializer(auth, many=False)
            
            response = {'message': 'welcome', 'newToken': auth_token_serializer.data}
            return Response(response, status=200)
        else:
            response = {'message': 'Incorrect email or password'}
            return Response(response, status=400)
    except Exception as error:
        response = {"Error": str(error)}
        return Response(response, status=400)

