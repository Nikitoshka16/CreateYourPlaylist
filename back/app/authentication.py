from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from app.models import Users

class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # Получаем токен из заголовка Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1] 
        try:
            user = Users.objects.get(token=token)
            return (user, token)  # Возвращаем пользователя, если токен найден
        except Users.DoesNotExist:
            raise AuthenticationFailed("Неверный токен")