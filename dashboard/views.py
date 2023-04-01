from django.shortcuts import render, redirect
from .auth_check import auth_check, self_login_required
from .models import User
from django.http import JsonResponse


# Create your views here.

@self_login_required
def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        token = request.POST.get("token")
        # 处理token登录
        if token:
            if auth_check("token", token):  # 如果token是有效登录成功
                request.session['is_login'] = True
                request.session['auth_type'] = 'token'  # 用于后期前端调用django，django拿着这个信息去请求k8s api
                request.session['token'] = token
                code = 0
                msg = "登录成功"
            else:
                code = 1
                msg = "Token无效！"
        else:
            # 处理kubeconfig文件登录
            file_obj = request.FILES.get("file")
            import random
            token_random = str(random.random()).split('.')[1]
            try:
                content = file_obj.read().decode()  # bytes to str
                User.objects.create(
                    auth_type="kubeconfig",
                    token=token_random,
                    content=content
                )
                code = 0
                msg = "上传文件成功."
            except Exception:
                code = 1
                msg = "文件类型错误！"
                result = {'code': code, 'msg': msg}
                return JsonResponse(result)

            # 上传文件成功，继续验证文件合法性
            if auth_check('kubeconfig', token_random):
                request.session['is_login'] = True
                request.session['auth_type'] = 'kubeconfig'  # 用于后期前端调用django，django拿着这个信息去请求k8s api
                request.session['token'] = token_random
                code = 0
                msg = "登录成功"
            else:
                User.objects.get(token=token_random).delete()
                code = 1
                msg = "kubeconfig文件无效！"

        result = {'code': code, 'msg': msg}
        return JsonResponse(result)


def node(request):
    return render(request, 'node.html')


def namespace(request):
    return render(request, 'namespace.html')


def deployment(request):
    return render(request, 'deployment.html')


def daemonset(request):
    return render(request, 'daemonset.html')


@self_login_required
def logout(request):
    request.session.flush()
    return redirect(login)
