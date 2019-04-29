# Django
from django.shortcuts import render
from django.views.generic import DetailView, ListView

# Project
from .models import PostModel
from .forms import PostModelForm

# Retrive
class Blog_Detail_View(DetailView):
    model = PostModel
    template_name = "blog/detail.html"

    def get_context_data(self, **kwargs):
        context = super(Blog_Detail_View,self).get_context_data(**kwargs)
        return context
    
# List
class Blog_List_View(ListView):
    model = PostModel
    template_name = "blog/list.html"

    def get_context_data(self, *args,**kwargs):
        context = super(Blog_List_View,self).get_context_data(*args,**kwargs)
        context["users_qs"] = self.request.user
        return context
