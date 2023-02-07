from django.urls import re_path
from workload import views

urlpatterns = [
    re_path('deployment/$', views.deployment, name='deployment'),
    re_path('deployment_api/$', views.deployment_api, name='deployment_api'),
    re_path('deployment_create/$', views.deployment_create, name='deployment_create'),
    re_path('deployment_details/$', views.deployment_details, name='deployment_details'),
    re_path('^replicaset_api/$', views.replicaset_api, name='replicaset_api'),
    re_path('daemonset/', views.daemonset, name='daemonset'),
    re_path('daemonset_api/$', views.daemonset_api, name='daemonset_api'),
    re_path('statefulset/', views.statefulset, name='statefulset'),
    re_path('statefulset_api/$', views.statefulset_api, name='statefulset_api'),
    re_path('pod/', views.pod, name='pod'),
    re_path('pod_api/$', views.pod_api, name='pod_api'),
    re_path('terminal/$', views.terminal, name='terminal'),
    re_path('container_log/$', views.container_log, name='container_log')
]