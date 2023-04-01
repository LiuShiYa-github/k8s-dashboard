from django.http import JsonResponse, QueryDict
from django.shortcuts import render
from dashboard import auth_check
from kubernetes import client


# Create your views here.


def daemonset(request):
    return render(request, 'workload/daemonset.html')


def deployment(request):
    return render(request, 'workload/deployment.html')


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
        containers_name = request.POST.get("containers_name", None)
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
                            name=containers_name,
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
            if current_replicas < replicas < max_replicas:
                # body = body.spec.template.spec.containers[0].image = "nginx:1.17"
                body.spec.replicas = replicas  # 更新对象内副本值
                apps_api.patch_namespaced_deployment(name=name, namespace=namespace, body=body)
                msg = "扩容成功！"
                code = 0
            elif current_replicas > replicas > min_replicas:
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
