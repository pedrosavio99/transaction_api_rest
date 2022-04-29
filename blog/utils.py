import bcrypt
from blog.models import UserPayer


def bcrypt_password_login(psw):
    psw = str(psw).encode('utf8')
    hashed = bcrypt.hashpw(psw, bcrypt.gensalt(10))
    return hashed.decode()

