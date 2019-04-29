# Django
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
# Project
from .models import PostModel
from .forms import PostModelForm

# CRUD

# Create
# @login_required(login_url='/login/')
def post_create_view(request):
    template_name = 'blog/create.html'
    form = PostModelForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.save()
        messages.success(request, "Felicidades!!! creaste el POST: %s" % instance.title)
        try:
            return HttpResponseRedirect(instance.get_absolute_url())
        except:
            return redirect("posts:list")
    context = {
        "title_header": 'Create',
        "title": "Crear Post",
        "form": form
    }
    return render(request, template_name, context)

# Retrive
def post_detail_view(request, id):
	template_name = 'blog/detail.html'
	try:
		instance = PostModel.objects.get(id=id)
	except:
		template_names 	= "404.html"
		detail_comment = "El Post que buscas no existe"
		contextdata = {
			"detail_comment": detail_comment,
			}
		return render(request, template_names, contextdata, status = 404)
	context = {
		'article': instance,
	}
	return render(request, template_name, context)

# Update
# @login_required(login_url='/login/')
def post_update_view(request, id=None):
    template_name = 'blog/create.html'
    
    try:
    	instance = PostModel.objects.get(id=id)
    except:
    	template_names 	= "404.html"
    	detail_comment = "El post que deseas editar no existe"
    	contextdata = {
    		"detail_comment": detail_comment,
    	}
    	return render(request, template_names, contextdata, status = 404)
    # Formulario
    form = PostModelForm(request.POST or None, instance=instance)
    # Verificamos que el formulario es valido
    if form.is_valid():
        instance = form.save(commit = False)
        instance.save()
        messages.success(request, "Actualizaste el POST: %s" % instance.title)
        return redirect("posts:detail", id=id)
    # Contexto
    context = {
        "title_header": 'Update',
    	"title":'Actualizar post',
    	"articles": instance,
    	"form": form
    }
    return render(request, template_name, context)

# Delete
def posts_delete_view(request, id=None):
    template_name = 'blog/delete.html'
    try:
        obj = PostModel.objects.get(id=id)
    except:
        template_names 	= "404.html"
        detail_comment = "El post que deseas Eliminar no existe"
        contextdata = { 
            "detail_comment": detail_comment,
        }
        return render(request, template_names, contextdata, status = 404)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Eliminaste el Post: %s" % obj.title)
        return redirect("posts:list")
    context = {
        "object": obj,
    }
    return render(request, template_name, context)

# List
def post_list_view(request):
    if request.user.is_authenticated:
        qs = PostModel.objects.all()
        template_name = 'blog/list.html'
        users_qs = request.user
    else:
        qs = PostModel.objects.filter(publish='publish')
        template_name = 'blog/list_public.html'
        users_qs = 'Desconocido'
    # Buscador en la lista de post
    query = request.GET.get("q", None)
    if query is not None:
        qs = qs.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query))
    context = {
        "objects": qs,
        "users_qs": users_qs,
    }
    return render(request, template_name, context)

@login_required(login_url='/login/')
def post_list_login_view(request):
    qs = PostModel.objects.all()
    if request.user.is_authenticated:
        template_name = 'blog/list.html'
        users_qs = request.user
    else:
        template_name = 'blog/list_public.html'
        users_qs = 'Desconocido'
    context = {
        "objects": qs,
        "users_qs": users_qs,
    }
    return render(request, template_name, context)
