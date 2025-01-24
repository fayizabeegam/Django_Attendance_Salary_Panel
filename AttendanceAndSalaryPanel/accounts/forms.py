from typing import Any
from django import forms
from .models import*
from attendance.models import Employee
from .validators import CustomPasswordValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm


class UserRegistrationForm(forms.ModelForm):
    Password = forms.CharField(widget=forms.PasswordInput)
    ConfirmPassword = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['IFID','username','email','mobile']

    def clean(self):
        cleaned_data =  super().clean()

        mobile = cleaned_data.get('mobile')
        IFID = cleaned_data.get('IFID')

        # Check if the Mobile and IFID exist in the Employee model
        employee = Employee.objects.filter(Mobile=mobile, IFID=IFID).first()
        if not employee:
            raise forms.ValidationError("The Mobile and IFID do not match any employee record.")

        # Check if the Mobile is already registered to another user
        existing_user = User.objects.filter(mobile=mobile).exclude(IFID=IFID).first()
        if existing_user:
            raise forms.ValidationError("This Mobile number is already associated with another registered employee.")
        
        password = cleaned_data.get('Password')
        confirm_password = cleaned_data.get('ConfirmPassword')

        if password != confirm_password:
            raise ValidationError("Password do not matching")
        
        password_validator = CustomPasswordValidator()
        if password:
            password_validator.validate(password)
        return cleaned_data
    
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not Employee.objects.filter(Mobile=mobile).exists():
            raise ValidationError('This mobile number not registered')
        return mobile
    
    def clean_IFID(self):
        IFID = self.cleaned_data.get('IFID')
        if not Employee.objects.filter(IFID=IFID).exists():
            raise ValidationError('This IFID not registered')
        return IFID



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username/Mobile", max_length=150, widget=forms.TextInput(attrs={
        'id': 'form3Example1cg'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'typePasswordX'
    }))



class PasswordResetForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email not found")
        return email
    
