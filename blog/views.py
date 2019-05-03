# Python
from datetime import datetime

# Django
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (CreateView, 
								  DetailView, 
								  UpdateView, 
								  DeleteView, 
								  ListView)
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _l
from django.contrib.messages.views import SuccessMessageMixin

# Project
from .models import PostModel
from .forms import PostModelForm

# Create
class Blog_Create_View(SuccessMessageMixin, CreateView):
	template_name = "blog/create.html"
	form_class = PostModelForm
	model = PostModel
	success_message = _l("Congratulations!!! Created the POST: %(title)s")

	# Context Data
	def get_context_data(self, *args,**kwargs):
		context = super(Blog_Create_View,self).get_context_data(*args,**kwargs)
		context["title"] = _("Create publication")
		return context

	# Formulario valido
	def form_valid(self, form):
		valid_form = super(Blog_Create_View,self).form_valid(form)
		return valid_form

# Retrive
class Blog_Detail_View(DetailView):
    template_name = "blog/detail.html"
    model = PostModel
	
	# Metodo que toma la solicitud y devuelve la respuesta   
    def dispatch(self, request, *args, **kwargs):
    	try:
		    # messages.success(self.request, _("Welcome to the publication: {}").format(self.get_object().title))
		    messages.success(self.request, _("{}").format(self.get_object().title))
		    return super(Blog_Detail_View, self).dispatch(request, *args, **kwargs)
    	except:
		    template_names 	= "404.html"
		    detail_comment = _l("The publication you are looking for does not exist")
		    contextdata = {"detail_comment": detail_comment,}
		    return render(request, template_names, contextdata, status = 404)

    # Context Data
    def get_context_data(self, **kwargs):
        context = super(Blog_Detail_View, self).get_context_data(**kwargs)
        context["title_header"] = _("Details")
        return context

# Update
class Blog_Update_View(SuccessMessageMixin, UpdateView):
	template_name = "blog/create.html"
	queryset = PostModel.objects.all()
	form_class = PostModelForm
	# success_message = _l("You updated the post")
	success_message = _l("You updated the post: %(title)s")

	def dispatch(self, request, *args, **kwargs):
		try:
			return super(Blog_Update_View, self).dispatch(request, *args, **kwargs)
		except:
			template_names 	= "404.html"
			detail_comment = _("The post you want edit not exist")
			contextdata = {"detail_comment": detail_comment,}
			return render(request, template_names, contextdata, status = 404)

	# Context Data
	def get_context_data(self, *args,**kwargs):
		context = super(Blog_Update_View,self).get_context_data(*args,**kwargs)
		context["title"] = _("Update post")
		return context

# Delete
class Blog_Delete_View(DeleteView):
	template_name = "blog/delete.html"
	model = PostModel
	# success_url = reverse_lazy("posts:list")

	def dispatch(self, request, *args, **kwargs):
		try:
			return super(Blog_Delete_View, self).dispatch(request, *args, **kwargs)
		except:
			template_names 	= "404.html"
			detail_comment = _("The post you want delete not exist")
			contextdata = {"detail_comment": detail_comment,}
			return render(request, template_names, contextdata, status = 404)
	
	def get_context_data(self, *args,**kwargs):
		context = super(Blog_Delete_View, self).get_context_data(*args,**kwargs)
		context["title_header"] = _("Delete")
		return context
	

	def get_success_url(self):
		messages.success(self.request, _("Deleted the post: {}").format(self.get_object().title))
		return reverse_lazy("posts:list")
    
# List
class Blog_List_View(ListView):
    template_name = "blog/list.html"
    model = PostModel

    def get_queryset(self, *args,**kwargs):
        qs = super(Blog_List_View, self).get_queryset(*args,**kwargs)
        qs = qs.order_by("-publish_date")
        return qs
    
    # Context Data
    def get_context_data(self, *args,**kwargs):
        context = super(Blog_List_View,self).get_context_data(*args,**kwargs)
        context["users_qs"] = self.request.user
        context["title_header"] = _("List")
        return context