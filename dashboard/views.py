from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from kubernetes import client

from dashboard import auth_check
from dashboard import node_data
from dashboard.models import User


# Create your views here.

@auth_check.self_login_required
def index(request):
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    auth_check.load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()

    # 命名空间：前端通过ajax从namespace_api接口获取数据，动态渲染
    # 计算资源：准备一个计算资源的接口（node_resource），ajax访问这个接口获取数据，动态渲染（node_data.py）
    # 存储资源：模板渲染（node_data.py）
    # 节点状态：模板渲染（node_data.py）

    # 存储资源
    pv_list = []
    for pv in core_api.list_persistent_volume().items:
        pv_name = pv.metadata.name
        capacity = pv.spec.capacity["storage"]  # 返回字典对象
        access_modes = pv.spec.access_modes
        reclaim_policy = pv.spec.persistent_volume_reclaim_policy
        status = pv.status.phase
        if pv.spec.claim_ref is not None:
            pvc_ns = pv.spec.claim_ref.namespace
            pvc_name = pv.spec.claim_ref.name
            claim = "%s/%s" % (pvc_ns, pvc_name)
        else:
            claim = "未关联PVC"
        storage_class = pv.spec.storage_class_name
        create_time = auth_check.timestamp_format(pv.metadata.creation_timestamp)

        data = {"pv_name": pv_name, "capacity": capacity, "access_modes": access_modes,
                "reclaim_policy": reclaim_policy, "status": status,
                "claim": claim, "storage_class": storage_class, "create_time": create_time}
        pv_list.append(data)

    # 节点状态
    node_resource = node_data.node_resource(core_api)

    return render(request, 'index.html', {"pv_list": pv_list, "node_resource": node_resource})


# 计算资源接口
def node_resource(request):
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    auth_check.load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()

    result = node_data.node_resource(core_api)
    return JsonResponse(result)


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        token = request.POST.get("token")
        # 处理token登录
        if token:
            if auth_check.auth_check("token", token):  # 如果token是有效登录成功
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
            if auth_check.auth_check('kubeconfig', token_random):
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


def logout(request):
    request.session.flush()
    return redirect(login)


@xframe_options_exempt
def ace_editor(request):
    # 点击YAML，URL参数从接收再传递到编辑页面模板
    data = {}
    namespace = request.GET.get('namespace')
    resource = request.GET.get('resource')
    name = request.GET.get('name')
    data['namespace'] = namespace
    data['resource'] = resource
    data['name'] = name
    return render(request, 'ace_editor.html', {'data': data})


import json, yaml


def b_to_yaml(content):
    s = content.decode()  # bytes转字符串
    json_obj = json.loads(s)  # 字符串转json
    y = yaml.safe_dump(json_obj)  # json转yaml
    return y


def export_resource_api(request):
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    auth_check.load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()  # namespace,pod,service,pv,pvc
    apps_api = client.AppsV1Api()  # deployment
    networking_api = client.NetworkingV1beta1Api()  # ingress
    storage_api = client.StorageV1Api()  # storage_class

    namespace = request.GET.get("namespace")
    resource = request.GET.get("resource")
    name = request.GET.get("name")

    code = 0
    msg = "获取YAML内容成功."
    try:
        if resource == "node":
            content = core_api.read_node(name=name, _preload_content=False).read()
        elif resource == "namespace":
            content = core_api.read_namespace(name=name, _preload_content=False).read()
        elif resource == "pv":
            content = core_api.read_persistent_volume(name=name, _preload_content=False).read()
        elif resource == "deployment":
            content = apps_api.read_namespaced_deployment(name=name, namespace=namespace, _preload_content=False).read()
        elif resource == "daemonset":
            content = apps_api.read_namespaced_daemon_set(name=name, namespace=namespace, _preload_content=False).read()
        elif resource == "statefulset":
            content = apps_api.read_namespaced_stateful_set(name=name, namespace=namespace,
                                                            _preload_content=False).read()
        elif resource == "pod":
            content = core_api.read_namespaced_pod(name=name, namespace=namespace, _preload_content=False).read()
        elif resource == "service":
            content = core_api.read_namespaced_service(name=name, namespace=namespace, _preload_content=False).read()
        elif resource == "ingress":
            content = networking_api.read_namespaced_ingress(name=name, namespace=namespace,
                                                             _preload_content=False).read()
        elif resource == "pvc":
            content = core_api.read_namespaced_persistent_volume_claim(name=name, namespace=namespace,
                                                                       _preload_content=False).read()
        elif resource == "configmap":
            content = core_api.read_namespaced_config_map(name=name, namespace=namespace, _preload_content=False).read()
        elif resource == "secret":
            content = core_api.read_namespaced_secret(name=name, namespace=namespace, _preload_content=False).read()
        else:
            code = 1
            msg = "暂不支持该资源类型！"
    except Exception as e:
        status = getattr(e, "status")
        if status == 403:
            msg = "没有获取YAML权限！"
        else:
            msg = "获取YAML失败！"
        code = 1

    res = {"code": code, "msg": msg, "data": b_to_yaml(content)}
    return JsonResponse(res)


@auth_check.self_login_required
def apply_yaml(request):
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    auth_check.load_auth_config(auth_type, token)

    core_api = client.CoreV1Api()  # namespace,pod,service,pv,pvc
    apps_api = client.AppsV1Api()  # deployment
    networking_api = client.NetworkingV1beta1Api()  # ingress
    storage_api = client.StorageV1Api()  # storage_class

    yaml_content = request.POST.get("yaml_content")
    content = yaml.safe_load(yaml_content)  # yaml转字典
    kind = content['kind']
    namespace = content['metadata']['namespace']  # 集群资源没有命名空间，会异常
    name = content['metadata']['name']

    code = 0
    msg = "应用YAML成功."
    try:
        if kind == "PersistentVolume":
            core_api.patch_persistent_volume(body=content, name=name)
        elif kind == "Deployment":
            apps_api.patch_namespaced_deployment(body=content, namespace=namespace, name=name)
        elif kind == "DaemonSet":
            apps_api.patch_namespaced_daemon_set(body=content, namespace=namespace, name=name)
        elif kind == "Service":
            core_api.patch_namespaced_service(body=content, namespace=namespace, name=name)
        elif kind == "DaemonSet":
            apps_api.patch_namespaced_daemon_set(body=content, namespace=namespace, name=name)
        elif kind == "StatefulSet":
            apps_api.patch_namespaced_stateful_set(body=content, namespace=namespace, name=name)
        elif kind == "Pod":
            core_api.patch_namespaced_pod(body=content, namespace=namespace, name=name)
        elif kind == "Service":
            core_api.patch_namespaced_service(body=content, namespace=namespace, name=name)
        elif kind == "Ingress":
            networking_api.patch_namespaced_ingress(body=content, namespace=namespace, name=name)
        elif kind == "PersistentVolumeClaim":
            core_api.patch_namespaced_persistent_volume_claim(body=content, namespace=namespace, name=name)
        elif kind == "ConfigMap":
            core_api.patch_namespaced_config_map(body=content, namespace=namespace, name=name)
        elif kind == "Secret":
            core_api.patch_namespaced_secret(body=content, namespace=namespace, name=name)
        else:
            code = 1
            msg = "暂不支持该资源类型更新！"
    except Exception as e:
        status = getattr(e, 'status')
        if status == 403:
            msg = "没有更新权限！"
        else:
            print(e)
            msg = "更新失败！"
        code = 1

    res = {"code": code, "msg": msg}
    return JsonResponse(res)
