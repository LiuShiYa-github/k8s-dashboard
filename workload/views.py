from django.shortcuts import render
from django.http import JsonResponse, QueryDict
from dashboard import auth_check
from kubernetes import client


# Create your views here.

@auth_check.self_login_required
def deployment(request):
    return render(request, 'workload/deployment.html')


@auth_check.self_login_required
def deployment_api(request):
    # 获取当前用户登录凭据，调用k8s api操作命名空间
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    auth_check.load_auth_config(auth_type, token)
    apps_api = client.AppsV1Api()

    if request.method == "GET":
        data = []
        search_key = request.GET.get("search_key")
        namespace = request.GET.get("namespace")
        try:
            for dp in apps_api.list_namespaced_deployment(namespace=namespace).items:
                name = dp.metadata.name
                namespace = dp.metadata.namespace
                replicas = dp.spec.replicas
                available_replicas = (0 if dp.status.available_replicas is None else dp.status.available_replicas)
                labels = dp.metadata.labels
                selector = dp.spec.selector.match_labels
                containers = {}
                for c in dp.spec.template.spec.containers:
                    containers[c.name] = c.image
                create_time = dp.metadata.creation_timestamp
                dp = {"name": name, "namespace": namespace, "replicas": replicas,
                      "available_replicas": available_replicas, "labels": labels, "selector": selector,
                      "containers": containers, "create_time": create_time}
                # 根据查询关键字返回数据
                if search_key:
                    if search_key in name:
                        data.append(dp)
                else:
                    data.append(dp)
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

    elif request.method == "POST":
        name = request.POST.get("name", None)
        namespace = request.POST.get("namespace", None)
        image = request.POST.get("image", None)
        replicas = int(request.POST.get("replicas", None))
        print(request.POST)
        # 处理标签
        labels = {}
        try:
            for l in request.POST.get("labels", None).split(","):
                k = l.split("=")[0]
                v = l.split("=")[1]
                labels[k] = v
        except Exception as e:
            res = {"code": 1, "msg": "标签格式错误！"}
            return JsonResponse(res)

        resources = request.POST.get("resources", None)
        health_liveness = request.POST.get("health[liveness]",
                                           None)  # {'health[liveness]': ['on'], 'health[readiness]': ['on']}
        health_readiness = request.POST.get("health[readiness]", None)

        if resources == "1c2g":
            resources = client.V1ResourceRequirements(limits={"cpu": "1", "memory": "1Gi"},
                                                      requests={"cpu": "0.9", "memory": "0.9Gi"})
        elif resources == "2c4g":
            resources = client.V1ResourceRequirements(limits={"cpu": "2", "memory": "4Gi"},
                                                      requests={"cpu": "1.9", "memory": "3.9Gi"})
        elif resources == "4c8g":
            resources = client.V1ResourceRequirements(limits={"cpu": "4", "memory": "8Gi"},
                                                      requests={"cpu": "3.9", "memory": "7.9Gi"})
        else:
            resources = client.V1ResourceRequirements(limits={"cpu": "500m", "memory": "1Gi"},
                                                      requests={"cpu": "450m", "memory": "900Mi"})
        liveness_probe = ""
        if health_liveness == "on":
            liveness_probe = client.V1Probe(http_get="/", timeout_seconds=30, initial_delay_seconds=30)
        readiness_probe = ""
        if health_readiness == "on":
            readiness_probe = client.V1Probe(http_get="/", timeout_seconds=30, initial_delay_seconds=30)

        for dp in apps_api.list_namespaced_deployment(namespace=namespace).items:
            if name == dp.metadata.name:
                result = {'code': 1, 'msg': "Deployment %s已经存在！" % name}
                return JsonResponse(result)

        body = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=name),
            spec=client.V1DeploymentSpec(
                replicas=replicas,
                selector={'matchLabels': labels},
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(labels=labels),
                    spec=client.V1PodSpec(
                        containers=[client.V1Container(
                            # https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Container.md
                            name="web",
                            image=image,
                            env=[{"name": "TEST", "value": "123"}, {"name": "DEV", "value": "456"}],
                            ports=[client.V1ContainerPort(container_port=80)],
                            # liveness_probe=liveness_probe,
                            # readiness_probe=readiness_probe,
                            resources=resources,
                        )]
                    )
                ),
            )
        )
        try:
            apps_api.create_namespaced_deployment(namespace=namespace, body=body)
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

    elif request.method == "PUT":
        request_data = QueryDict(request.body)
        name = request_data.get("name")
        namespace = request_data.get("namespace")
        replicas = int(request_data.get("replicas"))
        try:
            body = apps_api.read_namespaced_deployment(name=name, namespace=namespace)
            current_replicas = body.spec.replicas
            min_replicas = 0
            max_replicas = 20
            if replicas > current_replicas and replicas < max_replicas:
                # body = body.spec.template.spec.containers[0].image = "nginx:1.17"
                body.spec.replicas = replicas  # 更新对象内副本值
                apps_api.patch_namespaced_deployment(name=name, namespace=namespace, body=body)
                msg = "扩容成功！"
                code = 0
            elif replicas < current_replicas and replicas > min_replicas:
                body.spec.replicas = replicas
                apps_api.patch_namespaced_deployment(name=name, namespace=namespace, body=body)
                msg = "缩容成功！"
                code = 0
            elif replicas == current_replicas:
                msg = "副本数一致！"
                code = 1
            elif replicas > max_replicas:
                msg = "副本数设置过大！请联系管理员操作。"
                code = 1
            elif replicas == min_replicas:
                msg = "副本数不能设置0！"
                code = 1
        except Exception as e:
            status = getattr(e, "status")
            if status == 403:
                msg = "你没有扩容/缩容权限！"
            else:
                msg = "扩容/缩容失败！"
            code = 1
        res = {"code": code, "msg": msg}
        return JsonResponse(res)
    elif request.method == "DELETE":
        request_data = QueryDict(request.body)
        name = request_data.get("name")
        namespace = request_data.get("namespace")

        try:
            apps_api.delete_namespaced_deployment(name=name, namespace=namespace)
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


@auth_check.self_login_required
def deployment_create(request):
    return render(request, 'workload/deployment_create.html')


@auth_check.self_login_required
def deployment_details(request):
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    auth_check.load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()
    apps_api = client.AppsV1Api()
    networking_api = client.NetworkingV1beta1Api()

    dp_name = request.GET.get("name")
    namespace = request.GET.get("namespace")

    dp_info = []
    for dp in apps_api.list_namespaced_deployment(namespace=namespace).items:
        if dp_name == dp.metadata.name:
            name = dp.metadata.name
            namespace = dp.metadata.namespace
            replicas = dp.spec.replicas
            available_replicas = (
                0 if dp.status.available_replicas is None else dp.status.available_replicas)  # ready_replicas
            labels = dp.metadata.labels
            selector = dp.spec.selector.match_labels

            # 通过deployment反查对应service
            service = []
            svc_name = None
            for svc in core_api.list_namespaced_service(namespace=namespace).items:
                if svc.spec.selector == selector:
                    svc_name = svc.metadata.name  # 通过该名称筛选ingress
                    type = svc.spec.type
                    cluster_ip = svc.spec.cluster_ip
                    ports = svc.spec.ports

                    data = {"type": type, "cluster_ip": cluster_ip, "ports": ports}
                    service.append(data)

            # service没有创建，ingress也就没有  ingress->service->deployment->pod
            ingress = {"rules": None, "tls": None}
            for ing in networking_api.list_namespaced_ingress(namespace=namespace).items:
                for r in ing.spec.rules:
                    for b in r.http.paths:
                        if b.backend.service_name == svc_name:
                            ingress["rules"] = ing.spec.rules
                            ingress["tls"] = ing.spec.tls

            containers = []
            for c in dp.spec.template.spec.containers:
                c_name = c.name
                image = c.image
                liveness_probe = c.liveness_probe
                readiness_probe = c.readiness_probe
                resources = c.resources  # 在前端处理
                env = c.env
                ports = c.ports
                volume_mounts = c.volume_mounts
                args = c.args
                command = c.command

                container = {"name": c_name, "image": image, "liveness_probe": liveness_probe,
                             "readiness_probe": readiness_probe,
                             "resources": resources, "env": env, "ports": ports,
                             "volume_mounts": volume_mounts, "args": args, "command": command}
                containers.append(container)

            tolerations = dp.spec.template.spec.tolerations
            rolling_update = dp.spec.strategy.rolling_update
            volumes = []
            if dp.spec.template.spec.volumes is not None:
                for v in dp.spec.template.spec.volumes:  # 返回类似字典格式，不知道为啥不能遍历
                    volume = {}
                    if v.config_map is not None:
                        volume["config_map"] = v.config_map
                    elif v.secret is not None:
                        volume["secret"] = v.secret
                    elif v.empty_dir is not None:
                        volume["empty_dir"] = v.empty_dir
                    elif v.host_path is not None:
                        volume["host_path"] = v.host_path
                    elif v.config_map is not None:
                        volume["downward_api"] = v.downward_api
                    elif v.config_map is not None:
                        volume["glusterfs"] = v.glusterfs
                    elif v.cephfs is not None:
                        volume["cephfs"] = v.cephfs
                    elif v.rbd is not None:
                        volume["rbd"] = v.rbd
                    elif v.persistent_volume_claim is not None:
                        volume["persistent_volume_claim"] = v.persistent_volume_claim
                    else:
                        volume["unknown"] = "unknown"
                    volumes.append(volume)

            rs_number = dp.spec.revision_history_limit
            create_time = auth_check.timestamp_format(dp.metadata.creation_timestamp)

            dp_info = {"name": name, "namespace": namespace, "replicas": replicas,
                       "available_replicas": available_replicas, "labels": labels,
                       "selector": selector, "containers": containers, "rs_number": rs_number,
                       "rolling_update": rolling_update, "create_time": create_time, "volumes": volumes,
                       "tolerations": tolerations, "service": service, "ingress": ingress}
            print(dp_info)
        return render(request, 'workload/deployment_details.html',
                      {'dp_name': dp_name, 'namespace': namespace, 'dp_info': dp_info})


@auth_check.self_login_required
def replicaset_api(request):
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    auth_check.load_auth_config(auth_type, token)
    apps_api = client.AppsV1Api()

    if request.method == "GET":
        dp_name = request.GET.get("name", None)
        namespace = request.GET.get("namespace", None)
        data = []
        for rs in apps_api.list_namespaced_replica_set(namespace=namespace).items:
            current_dp_name = rs.metadata.owner_references[0].name
            rs_name = rs.metadata.name
            if dp_name == current_dp_name:
                namespace = rs.metadata.namespace
                replicas = rs.status.replicas
                available_replicas = rs.status.available_replicas
                ready_replicas = rs.status.ready_replicas
                revision = rs.metadata.annotations["deployment.kubernetes.io/revision"]
                create_time = auth_check.timestamp_format(rs.metadata.creation_timestamp)

                containers = {}
                for c in rs.spec.template.spec.containers:
                    containers[c.name] = c.image

                rs = {"name": rs_name, "namespace": namespace, "replicas": replicas,
                      "available_replicas": available_replicas, "ready_replicas": ready_replicas,
                      "revision": revision, 'containers': containers, "create_time": create_time}
                data.append(rs)
        count = len(data)  # 可选，rs默认保存10条，所以不用分页
        res = {"code": 0, "msg": "", "count": count, 'data': data}
        return JsonResponse(res)
    elif request.method == "POST":
        dp_name = request.POST.get("dp_name")  # deployment名称
        namespace = request.POST.get("namespace")
        revision = request.POST.get("revision")

        # 回滚，参考 https://github.com/kubernetes-client/python/issues/1232
        associated_replica_sets = apps_api.list_namespaced_replica_set(
            namespace=namespace,
        )
        revision_ordered_replica_sets = sorted(
            associated_replica_sets.items,
            key=lambda e: e.metadata.annotations['deployment.kubernetes.io/revision'],
            reverse=True
        )
        idx = 0
        for i in revision_ordered_replica_sets:
            idx += 1
            for k, v in i.metadata.annotations.items():
                if (k == "deployment.kubernetes.io/revision" and v == revision):
                    break
        rollback_replica_set = (
            revision_ordered_replica_sets[idx - 1]
        )
        patch = [
            {
                'op': 'replace',
                'path': '/spec/template',
                'value': rollback_replica_set.spec.template
            },
            {
                'op': 'replace',
                'path': '/metadata/annotations',
                'value': {
                    'deployment.kubernetes.io/revision': revision,
                }
            }
        ]

        try:
            apps_api.patch_namespaced_deployment(name=dp_name, namespace=namespace, body=patch)
            code = 0
            msg = "回滚成功！"
        except Exception as e:
            print(e)
            status = getattr(e, "status")
            if status == 403:
                msg = "你没有回滚权限！"
            else:
                msg = "回滚失败！"
            code = 1
        res = {"code": code, "msg": msg}
        return JsonResponse(res)


@auth_check.self_login_required
def daemonset(request):
    return render(request, 'workload/daemonset.html')


@auth_check.self_login_required
def daemonset_api(request):
    # 获取当前用户登录凭据，调用k8s api操作命名空间
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    auth_check.load_auth_config(auth_type, token)
    apps_api = client.AppsV1Api()

    if request.method == "GET":
        data = []
        search_key = request.GET.get("search_key")
        namespace = request.GET.get("namespace")
        try:
            for ds in apps_api.list_namespaced_daemon_set(namespace).items:
                name = ds.metadata.name
                namespace = ds.metadata.namespace
                desired_number = ds.status.desired_number_scheduled
                available_number = ds.status.number_available
                labels = ds.metadata.labels
                selector = ds.spec.selector.match_labels
                containers = {}
                for c in ds.spec.template.spec.containers:
                    containers[c.name] = c.image
                create_time = ds.metadata.creation_timestamp

                ds = {"name": name, "namespace": namespace, "labels": labels, "desired_number": desired_number,
                      "available_number": available_number,
                      "selector": selector, "containers": containers, "create_time": create_time}
                # 根据查询关键字返回数据
                if search_key:
                    if search_key in name:
                        data.append(ds)
                else:
                    data.append(ds)
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
            apps_api.delete_namespaced_daemon_set(namespace=namespace, name=name)
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


@auth_check.self_login_required
def statefulset(request):
    return render(request, 'workload/statefulset.html')


@auth_check.self_login_required
def statefulset_api(request):
    # 获取当前用户登录凭据，调用k8s api操作命名空间
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    auth_check.load_auth_config(auth_type, token)
    apps_api = client.AppsV1Api()

    if request.method == "GET":
        data = []
        search_key = request.GET.get("search_key")
        namespace = request.GET.get("namespace")
        try:
            for sts in apps_api.list_namespaced_stateful_set(namespace).items:
                name = sts.metadata.name
                namespace = sts.metadata.namespace
                labels = sts.metadata.labels
                selector = sts.spec.selector.match_labels
                replicas = sts.spec.replicas
                ready_replicas = ("0" if sts.status.ready_replicas is None else sts.status.ready_replicas)
                # current_replicas = sts.status.current_replicas
                service_name = sts.spec.service_name
                containers = {}
                for c in sts.spec.template.spec.containers:
                    containers[c.name] = c.image
                create_time = sts.metadata.creation_timestamp

                ds = {"name": name, "namespace": namespace, "labels": labels, "replicas": replicas,
                      "ready_replicas": ready_replicas, "service_name": service_name,
                      "selector": selector, "containers": containers, "create_time": create_time}
                # 根据查询关键字返回数据
                if search_key:
                    if search_key in name:
                        data.append(ds)
                else:
                    data.append(ds)
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
            apps_api.delete_namespaced_stateful_set(namespace=namespace, name=name)
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


@auth_check.self_login_required
def pod(request):
    return render(request, 'workload/pod.html')


@auth_check.self_login_required
def pod_api(request):
    # 获取当前用户登录凭据，调用k8s api操作命名空间
    auth_type = request.session.get("auth_type")
    token = request.session.get("token")
    auth_check.load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()

    if request.method == "GET":
        data = []
        search_key = request.GET.get("search_key")
        namespace = request.GET.get("namespace")
        try:
            for po in core_api.list_namespaced_pod(namespace).items:
                name = po.metadata.name
                namespace = po.metadata.namespace
                labels = po.metadata.labels
                pod_ip = po.status.pod_ip

                containers = []  # [{},{},{}]
                status = "None"
                # 只为None说明Pod没有创建（不能调度或者正在下载镜像）
                if po.status.container_statuses is None:
                    status = po.status.conditions[-1].reason
                else:
                    for c in po.status.container_statuses:
                        c_name = c.name
                        c_image = c.image

                        # 获取重启次数
                        restart_count = c.restart_count

                        # 获取容器状态
                        c_status = "None"
                        if c.ready is True:
                            c_status = "Running"
                        elif c.ready is False:
                            if c.state.waiting is not None:
                                c_status = c.state.waiting.reason
                            elif c.state.terminated is not None:
                                c_status = c.state.terminated.reason
                            elif c.state.last_state.terminated is not None:
                                c_status = c.last_state.terminated.reason

                        c = {'c_name': c_name, 'c_image': c_image, 'restart_count': restart_count, 'c_status': c_status}
                        containers.append(c)

                create_time = po.metadata.creation_timestamp

                po = {"name": name, "namespace": namespace, "pod_ip": pod_ip,
                      "labels": labels, "containers": containers, "status": status,
                      "create_time": create_time}
                # 根据查询关键字返回数据
                if search_key:
                    if search_key in name:
                        data.append(po)
                else:
                    data.append(po)
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
            core_api.delete_namespaced_pod(namespace=namespace, name=name)
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


from django.views.decorators.clickjacking import xframe_options_exempt


@xframe_options_exempt
@auth_check.self_login_required
def terminal(request):
    namespace = request.GET.get("namespace")
    pod_name = request.GET.get("pod_name")
    containers = request.GET.get("containers").split(',')  # 返回 nginx1,nginx2，转成一个列表方便前端处理
    auth_type = request.session.get(
        'auth_type')  # 认证类型和token，用于传递到websocket，websocket根据sessionid获取token，让websocket处理连接k8s认证用
    token = request.session.get('token')
    connect = {'namespace': namespace, 'pod_name': pod_name, 'containers': containers, 'auth_type': auth_type,
               'token': token}
    return render(request, 'workload/terminal.html', {'connect': connect})


from django.views.decorators.clickjacking import xframe_options_exempt


@xframe_options_exempt
@auth_check.self_login_required
def container_log(request):
    namespace = request.GET.get("namespace")
    pod_name = request.GET.get("pod_name")
    containers = request.GET.get("containers").split(',')  # 返回 nginx1,nginx2，转成一个列表方便前端处理
    auth_type = request.session.get(
        'auth_type')  # 认证类型和token，用于传递到websocket，websocket根据sessionid获取token，让websocket处理连接k8s认证用
    token = request.session.get('token')
    connect = {'namespace': namespace, 'pod_name': pod_name, 'containers': containers, 'auth_type': auth_type,
               'token': token}
    return render(request, 'workload/container_log.html', {'connect': connect})
