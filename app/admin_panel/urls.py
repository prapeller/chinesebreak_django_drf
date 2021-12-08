from django.contrib import admin
from django.urls import path, include
from .views import index

appname = 'admin_panel'

urlpatterns = [
    path('', index),

]
