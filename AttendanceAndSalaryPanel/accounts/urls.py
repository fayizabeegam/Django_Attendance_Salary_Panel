from django.urls import path,re_path
from .views import*
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path('signup/',UserRegistrationView.as_view(),name='signup'),
    path('signin/',UserLoginView.as_view(),name='signin'),
    path('logout/',LogoutView.as_view(),name='logout'),
    
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
