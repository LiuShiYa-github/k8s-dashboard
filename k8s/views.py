from django.shortcuts import render
from kubernetes import client
from django.http import JsonResponse, QueryDict
from dashboard import auth_check


# Create your views here.


def node(request):
    return render(request, 'k8s/node.html')


def namespace(request):
    return render(request, 'k8s/namespace.html')


@auth_check.self_login_required
def namespace_api(request):
    # 获取当前用户登录凭据，调用k8s api操作命名空间
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    auth_check.load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()
    if request.method == "GET":
        data = []
        search_key = request.GET.get("search_key")
        try:
            # items返回一个对象，类LIST（[{命名空间属性},{命名空间属性}] ），每个元素是一个类字典（命名空间属性），操作类字典
            for ns in core_api.list_namespace().items:
                name = ns.metadata.name
                labels = ns.metadata.labels
                create_time = ns.metadata.creation_timestamp
                namespace = {"name": name, "labels": labels, "create_time": create_time}
                # 根据查询关键字返回数据
                if search_key:
                    if search_key in name:
                        data.append(namespace)
                else:
                    data.append(namespace)
            code = 0
            msg = "查询成功."
        except Exception as e:
            status = getattr(e, 'status')
            if status == 403:
                msg = "没有访问权限！"
            else:
                msg = "查询失败！"
            code = 1
            msg = "查询成功"
            result = {'code': code, 'msg': msg, 'data': data}
            return JsonResponse(result)
        # 分页
        count = len(data)  # 要在切片之前获取总数

        if request.GET.get('page'):  # 如果为真说明数据表格带有分页（适配首页命名空间选择）
            page = int(request.GET.get('page'))
            limit = int(request.GET.get('limit'))
            # data = data[0:10]
            start = (page - 1) * limit  # 切片的起始值
            end = page * limit  # 切片的末值
            data = data[start:end]  # 返回指定数据范围

        result = {'code': code, 'msg': msg, 'data': data, 'count': count}
        return JsonResponse(result)
    elif request.method == "POST":
        ns_name = request.POST.get("name")

        # 判断命名空间是否存在
        for ns in core_api.list_namespace().items:
            if ns_name == ns.metadata.name:
                result = {'code': 1, 'msg': "命名空间已经存在！"}
                return JsonResponse(result)

        body = client.V1Namespace(
            api_version="v1",
            kind="Namespace",
            metadata=client.V1ObjectMeta(
                name=ns_name
            )
        )
        try:
            core_api.create_namespace(body=body)
            code = 0
            msg = "创建成功."
        except Exception as e:
            status = getattr(e, 'status')
            if status == 403:
                msg = "没有创建权限！"
            else:
                msg = "创建失败！"
            code = 1

        result = {'code': code, 'msg': msg}
        return JsonResponse(result)
    elif request.method == "DELETE":
        # django对于GET和POST请求进行了封装，即可以通过request.GET/request.POST获取里面的值
        # 对PUT和DELETE并没有封装，所以需要自己封装，从request.body里获取
        request_data = QueryDict(request.body)
        name = request_data.get("name")

        try:
            core_api.delete_namespace(name=name)
            code = 0
            msg = "删除命名空间成功."
        except Exception as e:
            status = getattr(e, 'status')
            if status == 403:
                msg = "没有访问命名空间权限！"
            else:
                msg = "删除命名空间失败！"
            code = 1

        result = {'code': code, 'msg': msg}
        return JsonResponse(result)


@auth_check.self_login_required
def node_api(request):
    # 获取当前用户登录凭据，调用k8s api操作命名空间
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    auth_check.load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()

    if request.method == "GET":
        data = []
        search_key = request.GET.get("search_key")
        try:
            for node in core_api.list_node_with_http_info()[0].items:
                name = node.metadata.name
                labels = node.metadata.labels
                status = node.status.conditions[-1].status
                scheduler = ("是" if node.spec.unschedulable is None else "否")
                cpu = node.status.capacity['cpu']
                memory = node.status.capacity['memory']
                kebelet_version = node.status.node_info.kubelet_version
                cri_version = node.status.node_info.container_runtime_version
                create_time = auth_check.timestamp_format(node.metadata.creation_timestamp)
                node = {"name": name, "labels": labels, "status": status,
                        "scheduler": scheduler, "cpu": cpu, "memory": memory,
                        "kebelet_version": kebelet_version, "cri_version": cri_version,
                        "create_time": create_time}
                # 根据查询关键字返回数据
                if search_key:
                    if search_key in name:
                        data.append(node)
                else:
                    data.append(node)
            code = 0
            msg = "查询节点成功."
        except Exception as e:
            status = getattr(e, 'status')
            if status == 403:
                msg = "没有访问节点权限！"
            else:
                msg = "查询节点失败！"
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
        pass


@auth_check.self_login_required
def pv(request):
    return render(request, 'k8s/pv.html')


@auth_check.self_login_required
def pv_api(request):
    # 获取当前用户登录凭据，调用k8s api操作命名空间
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    auth_check.load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()

    if request.method == "GET":
        data = []
        search_key = request.GET.get("search_key")
        try:
            for pv in core_api.list_persistent_volume().items:
                name = pv.metadata.name
                capacity = pv.spec.capacity["storage"]
                access_modes = pv.spec.access_modes
                reclaim_policy = pv.spec.persistent_volume_reclaim_policy
                status = pv.status.phase
                if pv.spec.claim_ref is not None:
                    pvc_ns = pv.spec.claim_ref.namespace
                    pvc_name = pv.spec.claim_ref.name
                    pvc = "%s / %s" % (pvc_ns, pvc_name)
                else:
                    pvc = "未绑定"
                storage_class = pv.spec.storage_class_name
                create_time = pv.metadata.creation_timestamp
                pv = {"name": name, "capacity": capacity, "access_modes": access_modes,
                      "reclaim_policy": reclaim_policy, "status": status, "pvc": pvc,
                      "storage_class": storage_class, "create_time": create_time}

                # 根据查询关键字返回数据
                if search_key:
                    if search_key in name:
                        data.append(pv)
                else:
                    data.append(pv)
            code = 0
            msg = "查询成功."
        except Exception as e:
            status = getattr(e, 'status')
            if status == 403:
                msg = "没有访问权限！"
            else:
                msg = "查询失败！"
            code = 1

        # 分页
        count = len(data)  # 要在切片之前获取总数

        if request.GET.get('page'):  # 如果为真说明数据表格带有分页（适配首页命名空间选择）
            page = int(request.GET.get('page'))
            limit = int(request.GET.get('limit'))
            # data = data[0:10]
            start = (page - 1) * limit  # 切片的起始值
            end = page * limit  # 切片的末值
            data = data[start:end]  # 返回指定数据范围

        code = 0
        msg = "查询成功"
        result = {'code': code, 'msg': msg, 'data': data, 'count': count}
        return JsonResponse(result)
    elif request.method == "POST":

        name = request.POST.get("name", None)
        capacity = request.POST.get("capacity", None)
        access_mode = request.POST.get("access_mode", None)
        storage_type = request.POST.get("storage_type", None)
        server_ip = request.POST.get("server_ip", None)
        mount_path = request.POST.get("mount_path", None)

        for pv in core_api.list_persistent_volume().items:
            if name == pv.metadata.name:
                result = {'code': 1, 'msg': "PV已经存在！"}
                return JsonResponse(result)

        body = client.V1PersistentVolume(
            api_version="v1",
            kind="PersistentVolume",
            metadata=client.V1ObjectMeta(name=name),
            spec=client.V1PersistentVolumeSpec(
                capacity={'storage': capacity},
                access_modes=[access_mode],
                nfs=client.V1NFSVolumeSource(
                    server=server_ip,
                    path="/ifs/kubernetes/%s" % mount_path
                )
            )
        )
        try:
            core_api.create_persistent_volume(body=body)
            code = 0
            msg = "创建PV成功."
        except Exception as e:
            status = getattr(e, 'status')
            if status == 403:
                msg = "没有创建权限！"
            else:
                msg = "创建PV失败！"
            code = 1
        result = {'code': code, 'msg': msg}
        return JsonResponse(result)

    elif request.method == "DELETE":
        request_data = QueryDict(request.body)
        name = request_data.get("name")

        try:
            core_api.delete_persistent_volume(name=name)
            code = 0
            msg = "删除持久卷成功."
        except Exception as e:
            status = getattr(e, 'status')
            if status == 403:
                msg = "没有访问持久卷权限！"
            else:
                msg = "删除持久卷失败！"
            code = 1

        result = {'code': code, 'msg': msg}
        return JsonResponse(result)


@auth_check.self_login_required
def pv_create(request):
    return render(request, 'k8s/pv_create.html')
