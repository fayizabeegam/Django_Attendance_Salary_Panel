from django.shortcuts import render,redirect
from .models import*
from .forms import*
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView,FormView
from django.contrib.auth import login,authenticate
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
# Create your views here.

"""
    HR and Employee Registration View
"""

class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('accounts:signin')

    def form_valid(self, form):
        try:
            
            mobile = form.cleaned_data.get('mobile')
            IFID = form.cleaned_data.get('IFID')

            # Check if the Employee exists
            employee = Employee.objects.filter(Mobile=mobile, IFID=IFID).first()
            if not employee:
                form.add_error(None, "No employee record found with the given Mobile and IFID.")
                return self.form_invalid(form)

            # Check if the User already exists
            if User.objects.filter(mobile=mobile).exists():
                form.add_error(None, "A user with this mobile number already exists.")
                return self.form_invalid(form)
                
            user = form.save(commit=False)
            user.role = 'HR' if self.request.POST.get('role') == 'HR' else 'Employee'
            user.set_password(form.cleaned_data['Password'])
            user.save()

            messages.success(self.request, 'Registration successful!')
            return HttpResponseRedirect(self.success_url)
        
        except ValidationError as e:
            form.add_error(None, str(e))
            messages.error(self.request, "There was an error with your registration. Please try again.")
            # return super().form_valid(form)
            return self.render_to_response(self.get_context_data(form=form))
        
        except Exception as e:
            form.add_error(None, "An unexpected error occurred. Please try again.")
            messages.error(self.request, "An unexpected error occurred.")
            # return super().form_valid(form)
            return self.render_to_response(self.get_context_data(form=form))
    
    # Set this to True for the signup page and Hide the navbar on the signup page
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_signup_page'] = True  
        context['show_navbar'] = False   
        return context

"""
    User Login View  
"""

class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = 'signin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_signin_page'] = True
        context['show_navbar'] = False  
        return context


    def form_valid(self, form):
        username_or_mobile = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # user = None
        try:
            user = authenticate(self.request, username=username_or_mobile, password=password)
            if user is None:
                try:
                    user_obj = User.objects.get(mobile=username_or_mobile)
                    user = authenticate(self.request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
                    
            if user is None:
                raise ValidationError('Invalid credentials')
            
            login(self.request, user)
            if user.is_superuser:
                return redirect(reverse_lazy('adminapp:admin-dashboard'))
            else:
                raise ValidationError('Invalid role assigned to the user')
        
        except ValidationError as e:
            form.add_error(None, str(e))
            messages.error(self.request, "Invalid login credentials. Please try again.")
            return self.form_invalid(form)
        except Exception as e:
            form.add_error(None, "An unexpected error occurred. Please try again.")
            messages.error(self.request, "An unexpected error occurred.")
            return self.form_invalid(form)


    def form_invalid(self, form):
        # Re-render the form with errors
        return self.render_to_response(self.get_context_data(form=form)) 
    



class PasswordResetView(FormView):
    template_name = 'password_reset_request.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('accounts:signin')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(self.request, "This email address is not registered.")
            return self.form_invalid(self, form)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(user.pk.encode())

        reset_url = f"{get_current_site(self.request).domain}/accounts/reset_password/{uid}/{token}/"

        # Send password reset email
        subject = "Password Reset Request"
        message = render_to_string("password_reset_email.html", {
            "reset_url": reset_url,
            "user": user
        })
        send_mail(subject, message, "no-reply@example.com", [email])
        
        messages.success(self.request, "Password reset email has been sent.")
        return redirect(self.success_url)
