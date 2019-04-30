# Django
from django.contrib import admin

# Project
from .models import PostModel

class PostModelAdmin(admin.ModelAdmin):
    list_display = ['active','title',
                    'publish','publish_date',
                    'updated','timestamp',
                    'get_age'
                    ]
    list_display_links  = ['title']
    list_editable       = ['active','publish','publish_date']
    readonly_fields 	= ['updated','timestamp']

    class Meta:
        model = PostModel
    
    def get_age(self, obj, *args, **kwargs):
        return str(obj.age)

admin.site.register(PostModel, PostModelAdmin)