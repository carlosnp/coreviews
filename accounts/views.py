# Django
from django.shortcuts import render, redirect
# Django Translation
from django.utils.translation import gettext as _
from django.utils.translation import ugettext_lazy as _l
# Autentification django
from django.contrib.auth import authenticate, get_user_model, login, logout

# Project
from .forms import UserCreationForm, UserChangeForm, UserLoginForm

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
        user	 = authenticate(username=username, password=password)
        login(request, user)
        return redirect("dashboards:home")
    context = {
        "title": _("Login"),
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
        return redirect("dashboards:home")
    context = {
        "title": _("Sign in"),
        "form": form
    }
    return render(request, template_name, context)
