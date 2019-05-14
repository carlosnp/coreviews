# Django
from django.contrib import messages
from django.shortcuts import render, redirect
# Django Translation
from django.utils.translation import gettext as _
from django.utils.translation import ugettext_lazy as _l
# Autentification django
from django.contrib.auth import authenticate, get_user_model, login, logout

# Project
from .forms import UserCreationForm, UserChangeForm, UserLoginForm
from .models import ActivationProfile

User = get_user_model()

# Cerrar Sesion
def LogoutView(request):
	logout(request)
	return redirect("dashboards:about")

# Iniciar sesion
def LoginView(request, *args, **kwargs):
    template_name = "register.html"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        try:
            user_q = User.objects.filter(username=username)
        except User.DoesNotExist:
            user_q = None
        if user_q is not None and user_q:
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("dashboards:home")
        else:
            # messages.error(request, form['username'].errors)
            messages.warning(request, _('This user does not exist, please register'))
            # return redirect("accounts:register")
    else:
        if form['username'].errors:
            messages.error(request, form['username'].errors)
        if form['password'].errors:
            messages.error(request, form['password'].errors)
    context = {
        "title": _("Login"),
        "login" : True,
        "form": form
    }
    return render(request, template_name, context)

# Registro de usuarios
def RegisterFormView(request, *args, **kwargs):
    template_name = "register.html"
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        user.save()
        messages.info(request, _("Created user"))
        return redirect("dashboards:home")
    # Para que se muestren los errores  
    else:
        if form['username'].errors:
            messages.error(request, form['username'].errors)
        if form['email'].errors:
            messages.error(request, form['email'].errors)
        if form['password2'].errors:
            messages.error(request, form['password2'].errors)
    context = {
        "title": _("Sign in"),
        "login" : False,
        "form": form
    }
    return render(request, template_name, context)

# Activacion del perfil
def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        activate_profile_qs = ActivationProfile.objects.filter(key=code)
        if activate_profile_qs.exists() and activate_profile_qs.count() == 1:
            activate_obj = activate_profile_qs.first()
            if not activate_obj.expired:
                user_obj = activate_obj.user
                user_obj.is_active = True
                activate_obj.expired = True
                activate_obj.save()
                return redirect("accounts:login")
    return redirect("accounts:login")