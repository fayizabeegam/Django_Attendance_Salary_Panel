from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()

class UsernameOrMobileBackend(ModelBackend):
    """
    Custom backend to allow authentication using either username or mobile.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
        except User.DoesNotExist:
            return None
        if user and user.check_password(password):
            return user
        return None


# class CustomBackend(ModelBackend):
#     """
#     An additional custom backend for specific authentication requirements (if needed).
#     """
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         # Implement custom logic here if required
#         return super().authenticate(request, username=username, password=password)