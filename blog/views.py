# Django
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView,ListView

# Project
from .models import PostModel
from .forms import PostModelForm

# Create
class Blog_Create_View(CreateView):
	template_name = "blog/create.html"
	form_class = PostModelForm

	# Context Data
	def get_context_data(self, *args,**kwargs):
		context = super(Blog_Create_View,self).get_context_data(*args,**kwargs)
		context["title"] = "Crear Post"
		return context

	# Formulario valido
	def form_valid(self, form):
		return super(Blog_Create_View,self).form_valid(form)

# Retrive
class Blog_Detail_View(DetailView):
    model = PostModel
    template_name = "blog/detail.html"
    
    # Context Data
    def get_context_data(self, **kwargs):
        qs = super(Blog_Detail_View,self).get_context_data(**kwargs)
        return qs

# Update
class Blog_Update_View(UpdateView):
	queryset = PostModel.objects.all()
	form_class = PostModelForm
	template_name = "blog/create.html"

	# Context Data
	def get_context_data(self, *args,**kwargs):
		context = super(Blog_Update_View,self).get_context_data(*args,**kwargs)
		context["title"] = "Editar Post"
		return context
    
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
