from django.urls import re_path
from workload import views

urlpatterns = [
    re_path('daemonset/$', views.daemonset, name='daemonset'),
    # re_path('daemonset_api/$', views.daemonset_api, name='daemonset_api'),
    re_path('deployment/$', views.deployment, name='deployment'),
    re_path('deployment_api/$', views.deployment_api, name='deployment_api'),
]