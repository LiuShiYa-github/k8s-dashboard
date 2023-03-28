from django.shortcuts import render


# Create your views here.


def daemonset(request):
    return render(request, 'workload/daemonset.html')


def deployment(request):
    return render(request, 'workload/deployment.html')
