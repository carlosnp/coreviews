# Django
from django.urls import path, include
# Project
from .views import post_list_view, post_detail_view, post_create_view, post_update_view, posts_delete_view

app_name = "posts"

urlpatterns = [
    path('', post_list_view, name="list"),
    path('create/', post_create_view, name="create"),
    path('<int:id>/', post_detail_view, name="detail"),
    path('<int:id>/update', post_update_view, name="update"),
    path('<int:id>/delete', posts_delete_view, name="delete"),
]