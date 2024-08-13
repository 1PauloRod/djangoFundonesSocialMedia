from django.contrib.auth.backends import BaseBackend
from .models import CustomUser

class EmailOrPhoneBackend(BaseBackend):
    def authenticate(self, request, email_or_phone=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=email_or_phone)
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(phone_number=email_or_phone)
            except CustomUser.DoesNotExist:
                return None
            
        if user.check_password(password):
            return user
        return None
    
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None