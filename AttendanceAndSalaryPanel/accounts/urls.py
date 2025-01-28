from django.urls import path,re_path
from .views import*
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path('signup/',UserRegistrationView.as_view(),name='signup'),
    path('signin/',UserLoginView.as_view(),name='signin'),
    path('logout/',LogoutView.as_view(),name='logout'),

    # path('forgot_password/', PasswordResetView.as_view(), name='forgot-password'),
    # path('reset_password/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='reset-password'),

     path('password_reset/', CustomPasswordResetView.as_view(
        template_name='password_reset_form.html',
        email_template_name='password_reset_email.txt',
        html_email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt',
        success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset'),
    
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
