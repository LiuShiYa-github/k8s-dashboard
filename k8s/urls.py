from django.urls import re_path
from k8s import views

urlpatterns = [
    re_path('node', views.node, name='node'),
    re_path('namespace', views.namespace, name='namespace'),
]