# Django
from django.urls import path, include
# Project
from .views import RegisterFormView, LoginView, LogoutView, activate_user_view

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterFormView, name="register"),
    path("login/", LoginView, name="login"),
    path("logout/", LogoutView, name="logout"),
    path("activate/<str:code>", activate_user_view, name="activate"),
    # path('', post_list_view, name="list"),
    # path('create/', post_create_view, name="create"),
    # path('<int:id>/', post_detail_view, name="detail"),
    # path('<int:id>/update', post_update_view, name="update"),
    # path('<int:id>/delete', posts_delete_view, name="delete"),
]