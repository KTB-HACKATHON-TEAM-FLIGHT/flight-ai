from django.urls import path
from . import views

urlpatterns = [
    path('ppt', views.chatai, name='chatbot'),
] 