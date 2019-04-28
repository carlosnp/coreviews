from django.contrib import admin

# Register your models here.
from .models import PostModel

class PostModelAdmin(admin.ModelAdmin):
    list_display = ('active','title','publish','publish_date','updated','timestamp')
    list_display_links  = ['title']
    list_editable       = ['active','publish','publish_date']
    readonly_fields 	= ['updated','timestamp']
    class Meta:
        model = PostModel

admin.site.register(PostModel, PostModelAdmin)