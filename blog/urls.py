# Django
from django.urls import path, include
# Project
from .views import Blog_Detail_View, Blog_List_View, Blog_Create_View, Blog_Update_View, Blog_Delete_View

app_name = "posts"

urlpatterns = [
    path('', Blog_List_View.as_view(), name="list"),
    path('create/', Blog_Create_View.as_view(), name="create"),
    path('<int:pk>/', Blog_Detail_View.as_view(), name="detail"),
    path('<int:pk>/update', Blog_Update_View.as_view(), name="update"),
    path('<int:pk>/delete', Blog_Delete_View.as_view(), name="delete"),
]