from asyncio import exceptions
import jwt
import datetime
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model

def generate_access_token(user):
    payload = {
        'user_id':user.id,
        'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat' : datetime.datetime.utcnow()
    }
    return jwt.encode(payload,settings.SECRET_KEY,algorithm='HS256').decode('utf-8')

class JWTAuthentification(BaseAuthentication):
    def authenticate(self,request):
        token = request.COOKIES.get('token')

        if not token:
            return None

        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithm=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('unauthorized')

        user = get_user_model().objects.filter(id=payload['user_id']).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User Not Found')
        return (user,None)