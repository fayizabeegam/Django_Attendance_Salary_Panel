from django.shortcuts import render,redirect
from .models import*
from .forms import*
from django.core.mail import send_mail,EmailMultiAlternatives
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView,FormView,View
from django.contrib.auth import login,authenticate
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
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
            existing_user = User.objects.filter(mobile=mobile).first()
            if existing_user:
                # Allow registration if the user matches the employee (e.g., same mobile and IFID)
                form.add_error(None, "You are already registered. Please log in.")
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
    



class CustomPasswordResetView(PasswordResetView):
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = render_to_string(email_template_name, context)

        # Use EmailMultiAlternatives to send HTML and plain text
        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name:
            html_email = render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")
        email_message.send()