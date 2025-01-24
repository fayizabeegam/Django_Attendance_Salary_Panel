from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self,username,mobile,password=None,**extra_fields):
        if not username and not mobile:
            raise ValueError("The username or mobile field must be set")
        
        user = self.model(username=username, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self,username,mobile,password=None,**extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username=username, mobile=mobile, password=password, **extra_fields)
        