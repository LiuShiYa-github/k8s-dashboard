from django.shortcuts import render
from django.http import JsonResponse,QueryDict
from devops import k8s
from kubernetes import client

# Create your views here.
@k8s.self_login_required
def pvc(request):
    return render(request, 'storage/pvc.html')

@k8s.self_login_required
def pvc_api(request):
    # 获取当前用户登录凭据，调用k8s api操作命名空间
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    k8s.load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()

    if request.method == "GET":
        data = []
        search_key = request.GET.get("search_key")
        namespace = request.GET.get("namespace")
        try:
            for pvc in core_api.list_namespaced_persistent_volume_claim(namespace=namespace).items:
                name = pvc.metadata.name
                namespace = pvc.metadata.namespace
                labels = pvc.metadata.labels
                storage_class_name = pvc.spec.storage_class_name
                access_modes = pvc.spec.access_modes
                capacity = (pvc.status.capacity if pvc.status.capacity is None else pvc.status.capacity["storage"])
                volume_name = pvc.spec.volume_name
                status = pvc.status.phase
                create_time = pvc.metadata.creation_timestamp

                pvc = {"name": name, "namespace": namespace, "lables": labels,
                       "storage_class_name": storage_class_name, "access_modes": access_modes, "capacity": capacity,
                       "volume_name": volume_name, "status": status, "create_time": create_time}
                # 根据查询关键字返回数据
                if search_key:
                    if search_key in name:
                        data.append(pvc)
                else:
                    data.append(pvc)
            code = 0
            msg = "查询成功."
        except Exception as e:
            print(e)
            status = getattr(e, 'status')
            if status == 403:
                msg = "没有访问权限！"
            else:
                msg = "查询失败！"
            code = 1

        # 分页
        count = len(data)  # 要在切片之前获取总数

        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        # data = data[0:10]
        start = (page - 1) * limit  # 切片的起始值
        end = page * limit  # 切片的末值
        data = data[start:end]  # 返回指定数据范围

        result = {'code': code, 'msg': msg, 'data': data, 'count': count}
        return JsonResponse(result)

    elif request.method == "DELETE":
        request_data = QueryDict(request.body)
        name = request_data.get("name")
        namespace = request_data.get("namespace")
        print(request_data)
        try:
            core_api.delete_namespaced_persistent_volume_claim(namespace=namespace, name=name)
            code = 0
            msg = "删除成功."
        except Exception as e:
            status = getattr(e, 'status')
            if status == 403:
                msg = "没有访问权限！"
            else:
                msg = "删除失败！"
            code = 1

        result = {'code': code, 'msg': msg}
        return JsonResponse(result)

@k8s.self_login_required
def configmap(request):
    return render(request, 'storage/configmap.html')

@k8s.self_login_required
def configmap_api(request):
    # 获取当前用户登录凭据，调用k8s api操作命名空间
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    k8s.load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()

    if request.method == "GET":
        data = []
        search_key = request.GET.get("search_key")
        namespace = request.GET.get("namespace")
        try:
            for cm in core_api.list_namespaced_config_map(namespace=namespace).items:
                name = cm.metadata.name
                namespace = cm.metadata.namespace
                data_length = ("0" if cm.data is None else len(cm.data))
                create_time = cm.metadata.creation_timestamp

                cm = {"name": name, "namespace": namespace, "data_length": data_length, "create_time": create_time}
                # 根据查询关键字返回数据
                if search_key:
                    if search_key in name:
                        data.append(cm)
                else:
                    data.append(cm)
            code = 0
            msg = "查询成功."
        except Exception as e:
            print(e)
            status = getattr(e, 'status')
            if status == 403:
                msg = "没有访问权限！"
            else:
                msg = "查询失败！"
            code = 1

        # 分页
        count = len(data)  # 要在切片之前获取总数

        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        # data = data[0:10]
        start = (page - 1) * limit  # 切片的起始值
        end = page * limit  # 切片的末值
        data = data[start:end]  # 返回指定数据范围

        result = {'code': code, 'msg': msg, 'data': data, 'count': count}
        return JsonResponse(result)

    elif request.method == "DELETE":
        request_data = QueryDict(request.body)
        name = request_data.get("name")
        namespace = request_data.get("namespace")
        print(request_data)
        try:
            core_api.delete_namespaced_config_map(name=name,namespace=namespace)
            code = 0
            msg = "删除成功."
        except Exception as e:
            status = getattr(e, 'status')
            if status == 403:
                msg = "没有访问权限！"
            else:
                msg = "删除失败！"
            code = 1

        result = {'code': code, 'msg': msg}
        return JsonResponse(result)

@k8s.self_login_required
def secret(request):
    return render(request, 'storage/secret.html')

@k8s.self_login_required
def secret_api(request):
    # 获取当前用户登录凭据，调用k8s api操作命名空间
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    k8s.load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()

    if request.method == "GET":
        data = []
        search_key = request.GET.get("search_key")
        namespace = request.GET.get("namespace")
        try:
            for secret in core_api.list_namespaced_secret(namespace=namespace).items:
                name = secret.metadata.name
                namespace = secret.metadata.namespace
                data_length = ("空" if secret.data is None else len(secret.data))
                create_time = secret.metadata.creation_timestamp

                se = {"name": name, "namespace": namespace, "data_length": data_length, "create_time": create_time}
                # 根据查询关键字返回数据
                if search_key:
                    if search_key in name:
                        data.append(se)
                else:
                    data.append(se)
            code = 0
            msg = "查询成功."
        except Exception as e:
            print(e)
            status = getattr(e, 'status')
            if status == 403:
                msg = "没有访问权限！"
            else:
                msg = "查询失败！"
            code = 1

        # 分页
        count = len(data)  # 要在切片之前获取总数

        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        # data = data[0:10]
        start = (page - 1) * limit  # 切片的起始值
        end = page * limit  # 切片的末值
        data = data[start:end]  # 返回指定数据范围

        result = {'code': code, 'msg': msg, 'data': data, 'count': count}
        return JsonResponse(result)

    elif request.method == "DELETE":
        request_data = QueryDict(request.body)
        name = request_data.get("name")
        namespace = request_data.get("namespace")
        print(request_data)
        try:
            core_api.delete_namespaced_secret(namespace=namespace, name=name)
            code = 0
            msg = "删除成功."
        except Exception as e:
            status = getattr(e, 'status')
            if status == 403:
                msg = "没有访问权限！"
            else:
                msg = "删除失败！"
            code = 1

        result = {'code': code, 'msg': msg}
        return JsonResponse(result)