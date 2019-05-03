# Django
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
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
        msj = _("Congratulations!!! Created the POST")
        messages.success(request, msj+": %s" % instance.title)
        try:
            return HttpResponseRedirect(instance.get_absolute_url())
        except:
            return redirect("posts:list")
    context = {
        "title_header": _('Create'),
        "title": _("Create publication"),
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
		detail_comment = _("This post not exist")
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
    	detail_comment = _("The post you want edit not exist")
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
        msj = _("Updated the post")
        messages.success(request, msj+": %s" % instance.title)
        return redirect("posts:detail", id=id)
    # Contexto
    context = {
        "title_header": _('Update'),
    	"title":_('Update post'),
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
        detail_comment = _("The post you want delete not exist")
        contextdata = { 
            "detail_comment": detail_comment,
        }
        return render(request, template_names, contextdata, status = 404)
    if request.method == "POST":
        obj.delete()
        msj = _("Deleted the post")
        messages.success(request, msj+": %s" % obj.title)
        return redirect("posts:list")
    
    title_header = _("Delete")
    context = {
        "title_header": title_header,
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
        "title_header": _("List"), 
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
