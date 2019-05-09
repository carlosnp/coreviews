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
    else:
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
