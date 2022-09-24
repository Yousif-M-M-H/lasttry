from django.contrib import admin
from django.urls import path, include
from . import views
from .views import ShowProfilePageView, EditProfilePageView

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name="home"),
    path('delete/<int:id>', views.delete, name='delete'),
    path('update/<int:id>', views.update, name='update'),
    path('', include("django.contrib.auth.urls")),
    path('add', views.add, name="add"),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(),
         name="show_profile_page"),
    path('<int:pk>/edit_profile_page/', EditProfilePageView.as_view(),
         name="edit_profile_page"),
    path("password_reset", views.password_reset_request, name="password_reset")

]
