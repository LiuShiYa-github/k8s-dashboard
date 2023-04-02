from django.urls import path, re_path, include
from dashboard import views

urlpatterns = [
    re_path('^$', views.index),
    re_path('login/', views.login),
    re_path('logout/', views.logout),
    re_path('k8s/', include('k8s.urls')),
    re_path('workload/', include('workload.urls')),
    re_path('loadbalancer/', include('loadbalancer.urls')),
    re_path('storage/', include('storage.urls')),
    re_path('ace_editor/', views.ace_editor, name="ace_editor"),
    re_path('export_resource_api/', views.export_resource_api, name="export_resource_api"),
    re_path('apply_yaml/', views.apply_yaml, name="apply_yaml"),
    re_path('node_resource/', views.node_resource, name="node_resource"),
]
