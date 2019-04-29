# Django
from django.shortcuts import render
from django.views.generic import TemplateView

# Home Page
class HomeView(TemplateView):
    template_name = "home.html"

    # Context Data
    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args,**kwargs)
        context["title"] = "Home Page" 
        return context
    