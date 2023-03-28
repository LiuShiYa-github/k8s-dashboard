from django.urls import re_path
from workload import views

urlpatterns = [
    re_path('daemonset', views.daemonset, name='daemonset'),
    re_path('deployment', views.deployment, name='deployment'),
]