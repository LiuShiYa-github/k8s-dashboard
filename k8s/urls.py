from django.urls import re_path
from k8s import views

urlpatterns = [
    re_path('node/$', views.node, name='node'),
    re_path('node_api/$', views.node_api, name='node_api'),

    re_path('namespace/$', views.namespace, name='namespace'),
    re_path('namespace_api/$', views.namespace_api, name='namespace_api'),

    re_path('pv/$', views.pv, name='pv'),
    re_path('pv_api/$', views.pv_api, name='pv_api'),
]