# Django
from django import forms
# Validadores
from django.core.validators import RegexValidator
# Django Translation
from django.utils.translation import gettext as _
from django.utils.translation import ugettext_lazy as _l
# Django Example
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Project
from .models import RegisterUser, USERNMAE_REDEX, message_register

User = get_user_model()

# Formulario para iniciar sesion
class UserLoginForm(forms.Form):
    username = forms.CharField(
        label=_l("User Name"), 
        max_length=150,
        validators = [RegexValidator(
            regex = USERNMAE_REDEX,
            message = message_register,
            code = "invalid_username",
            )
        ],
        required=True)
    password = forms.CharField(
        label=_l('Password'), 
        widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': _('User Name')})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Password')})

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user_obj = User.objects.filter(username=username).first()
        # Si el usuario no existe
        if not user_obj:
            print("usuario no existe")
            raise forms.ValidationError(_l("This user not exist"))
        else:
            print(user_obj.check_password(password))
            # Si la contraseña es incorrecta
            if not user_obj.check_password(password):
                print("Hola")
                raise forms.ValidationError(_l("Invalid password"))
        return super(UserLoginForm, self).clean(*args, **kwargs)
    
    # def clean_username(self):
    #     username = self.cleaned_data.get("username")
    #     user_qs = User.objects.filter(username=username)
    #     user_exists = user_qs.exists()
    #     if not user_exists and user_qs.count() != 1:
    #         raise forms.ValidationError(_l("This user not exist"))
    #     return username
    
# Crear usuario
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label=_l('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_l('Password confirmation'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': _('User Name')})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Email')})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Password')})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Password')})

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("Username '%s' is already in use.") % username.upper())
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(_("Email <%s> is already in use.") % email.lower())

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_l("Passwords don't match"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password','is_active', 'is_staff', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]