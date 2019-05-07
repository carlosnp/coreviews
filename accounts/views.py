# Django
from django.shortcuts import render, redirect
# Django Translation
from django.utils.translation import gettext as _
from django.utils.translation import ugettext_lazy as _l

# Project
from .forms import UserCreationForm, UserChangeForm

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
        "title": _("Register"),
        "form": form
    }
    return render(request, template_name, context)
