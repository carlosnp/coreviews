# Django
from django.urls import path, include
# Project
from .views import HomeView, AboutView

app_name = "dashboards"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about")
    # path('', post_list_view, name="list"),
    # path('create/', post_create_view, name="create"),
    # path('<int:id>/', post_detail_view, name="detail"),
    # path('<int:id>/update', post_update_view, name="update"),
    # path('<int:id>/delete', posts_delete_view, name="delete"),
]