# Django
from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView

# Project
from .models import PostModel
from .forms import PostModelForm

# Create
class Blog_Create_View(CreateView):
	template_name = "blog/create.html"
	model = PostModel
	fields = ["title","content", "publish"]

	# Context Data
	def get_context_data(self, *args,**kwargs):
		context = super(Blog_Create_View,self).get_context_data(*args,**kwargs)
		context["title"] = "Crear Post"
		return context

# Retrive
class Blog_Detail_View(DetailView):
    model = PostModel
    template_name = "blog/detail.html"
    
    # Context Data
    def get_context_data(self, **kwargs):
        qs = super(Blog_Detail_View,self).get_context_data(**kwargs)
        return qs
    
# List
class Blog_List_View(ListView):
    model = PostModel
    template_name = "blog/list.html"

    def get_queryset(self, *args,**kwargs):
        qs = super(Blog_List_View, self).get_queryset(*args,**kwargs)
        qs = qs.order_by("-publish_date")
        return qs
    
    # Context Data
    def get_context_data(self, *args,**kwargs):
        context = super(Blog_List_View,self).get_context_data(*args,**kwargs)
        context["users_qs"] = self.request.user
        return context
