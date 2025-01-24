from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from AttendanceAndSalaryPanel.accounts import models

User = get_user_model()

class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(models.Q(username=username) | models.Q(mobile=username))
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
