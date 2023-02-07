from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def node(request):
    return render(request, 'node.html')


def namespace(request):
    return render(request, 'namespace.html')


def deployment(request):
    return render(request, 'deployment.html')


def daemonset(request):
    return render(request, 'daemonset.html')
