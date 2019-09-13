from django.urls import path
from . import views

urlpatterns = [
    path('', views.msgproc),
    path('register/', views.register),
    path('login/', views.login)
]