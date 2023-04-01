from django.urls import re_path, include
from dashboard import views

urlpatterns = [
    re_path('^$', views.index),
    re_path('login/', views.login),
    re_path('logout/', views.logout),
    re_path('workload/', include('workload.urls')),
    re_path('k8s/', include('k8s.urls')),
]
