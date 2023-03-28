
<!-- TOC -->
  * [0、前置知识](#0)
    * [1、 产品背景](#1-)
    * [2、MVP（最简化可实行产品）](#2mvp)
    * [3、迭代思维](#3)
    * [4、得培养创新和快速构建项目模型的能力](#4)
    * [5、为什么开发K8s管理平台？](#5k8s)
    * [6、了解下整体设计（开发功能和平台页面）](#6)
  * [1、Kubernetes API使用](#1kubernetes-api)
    * [1.1 API是什么？](#11-api)
    * [1.2 K8s认证方式](#12-k8s)
    * [1.3 示例](#13-)
      * [客户端库](#)
      * [HTTP API](#http-api)
  * [2、 网站布局](#2-)
    * [2.1 准备登录页面](#21-)
    * [2.2 登录认证（集成RBAC）](#22-rbac)
    * [2.3 管理平台页面布局](#23-)
    * [2.4 命名空间选择](#24-)
  * [3、数据表格展示K8s常见资源](#3k8s)
    * [3.1 Namespace](#31-namespace)
    * [3.2 Node](#32-node)
    * [3.3 PV](#33-pv)
    * [3.4 Deployment](#34-deployment)
    * [3.5 DaemonSet](#35-daemonset)
    * [3.6 StatefulSet](#36-statefulset)
    * [3.7 Pod](#37-pod)
    * [3.8 Service](#38-service)
    * [3.9 Ingress](#39-ingress)
    * [3.10 PVC](#310-pvc)
    * [3.11 ConfigMap](#311-configmap)
    * [3.12 Secret](#312-secret)
    * [优化](#)
  * [4、创建资源](#4)
  * [5、查看和编辑YAML](#5yaml)
  * [6、Node与Deployment详情页](#6nodedeployment)
  * [7、容器终端与容器日志](#7)
    * [**容器终端**](#)
      * [1、前端（模板）](#1)
      * [2、服务端（视图）](#2)
      * [3、前端（终端页面）](#3)
      * [4、服务端（Django Channels）](#4django-channels)
      * [小结](#)
    * [**容器实时日志**](#)
      * [1、路由](#1)
      * [2、服务端（视图）](#2)
      * [3、前端（模板）](#3)
      * [4、点击日志按钮，与终端一样](#4)
      * [5、添加Websocket路由](#5websocket)
      * [6、处理Websocket消费者](#6websocket)
  * [8、仪表盘](#8)
<!-- TOC -->
## 0、前置知识

### 1、 产品背景

### 2、MVP（最简化可实行产品）

### 3、迭代思维

### 4、得培养创新和快速构建项目模型的能力

### 5、为什么开发K8s管理平台？

### 6、了解下整体设计（开发功能和平台页面）

K8s管理平台功能清单：

| 模块       | 功能                                    | 描述                                                         |
| ---------- | --------------------------------------- | ------------------------------------------------------------ |
| 公共部分   | 权限管理（登录）                        | 集成K8s自身RBAC授权                                          |
| 公共部分   | 命名空间选择                            | 展示不同命名空间资源                                         |
| 仪表盘     | 命名空间、计算资源、存储资源、节点状态  | 展示主要指标状况                                             |
| K8s集群    | node、namespace、pv                     | 创建、删除、修改（YAML）与查看（数据表格）                   |
| 工作负载   | deployment，daemonset，statefulset，pod | 创建、删除、修改（YAML）与查看（数据表格）  容器实时日志，容器终端 |
| 负载均衡   | service，ingress                        | 创建、删除、修改（YAML）与查看（数据表格）                   |
| 存储与配置 | configmap，secret                       | 创建、删除、修改（YAML）与查看（数据表格）                   |

## 1、Kubernetes API使用

### 1.1 API是什么？

API（Application Programming Interface，应用程序接口）： 是一些预先定义的接口（如函数、HTTP接口），或指软件系统不同组成部分衔接的约定。 用来提供应用程序与开发人员基于某软件或硬件得以访问的一组例程，而又无需访问源码，或理解内部工作机制的细节。 

![](https://k8s-1252881505.cos.ap-beijing.myqcloud.com/web-dev/web-k8s-etcd.png)

K8s也提供API接口，提供这个接口的是管理节点的apiserver组件，apiserver服务负责提供HTTP API，以便用户、其他组件相互通信。  

有两种方式可以操作K8s中的资源：

- HTTP API：https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/  
- 客户端库： https://kubernetes.io/zh/docs/reference/using-api/client-libraries/  

### 1.2 K8s认证方式

K8s支持三种客户端身份认证：

- HTTPS 证书认证：基于CA证书签名的数字证书认证（kubeconfig文件，默认路径~/.kube/config）

- HTTP Token认证：通过一个Token来识别用户（ServiceAccount）

- HTTP Base认证：用户名+密码的方式认证（1.19+已经弃用）

安装Kubernetes客户端库：

```
pip install kubernetes -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**HTTPS证书认证（kubeconfig）：**

```
from kubernetes import client, config
import os
kubeconfig = os.path.join(os.getcwd(),"kubeconfig") # 获取当前目录并拼接文件
config.load_kube_config(kubeconfig)  # 指定kubeconfig配置文件（/root/.kube/config）
apps_api = client.AppsV1Api()  # 资源接口类实例化

for dp in apps_api.list_deployment_for_all_namespaces().items:
    print(dp)  # 打印Deployment对象详细信息
```

**HTTP Token认证（ServiceAccount）：**

```
from kubernetes import client
import os
configuration = client.Configuration()
configuration.host = "https://192.168.31.61:6443"  # APISERVER地址
ca_file = os.path.join(os.getcwd(),"ca.crt") # K8s集群CA证书（/etc/kubernetes/pki/ca.crt）
configuration.ssl_ca_cert= ca_file
configuration.verify_ssl = True   # 启用证书验证
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImdlQlFUM3..."  # 指定Token字符串，下面方式获取
configuration.api_key = {"authorization": "Bearer " + token}  
client.Configuration.set_default(configuration)
apps_api = client.AppsV1Api() 

for dp in apps_api.list_deployment_for_all_namespaces().items:
    print(dp)
```

获取Token字符串：创建service account并绑定默认cluster-admin管理员集群角色：

```
# 创建用户
kubectl create serviceaccount dashboard-admin -n kube-system
# 用户授权
kubectl create clusterrolebinding dashboard-admin --clusterrole=cluster-admin --serviceaccount=kube-system:dashboard-admin
# 获取用户Token
kubectl describe secrets -n kube-system $(kubectl -n kube-system get secret | awk '/dashboard-admin/{print $1}')
```

其他常用资源接口类实例化：

```
core_api = client.CoreV1Api()  # namespace,pod,service,pv,pvc
apps_api = client.AppsV1Api()  # deployment,statefulset,daemonset
networking_api = client.NetworkingV1beta1Api()  # ingress
storage_api = client.StorageV1Api()  # storage_class
```

### 1.3 示例

#### 客户端库

Deployment操作：

```
# 查询
for dp in apps_api.list_deployment_for_all_namespaces().items:
    print(dp.metadata.name)

# 创建
namespace = "default"
name = "api-test"
replicas = 3
labels = {'a':'1', 'b':'2'}  # 不区分数据类型，都要加引号
image = "nginx"
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
                            name="web",
                            image=image
                        )]
                    )
                ),
            )
        )
try:
    apps_api.create_namespaced_deployment(namespace=namespace, body=body)
except Exception as e:
    status = getattr(e, "status")
    if status == 400:  # 400 格式错误，409 资源存在，403 没权限。
        print(e)
        print("格式错误")
    elif status == 409:
    	print(“资源存在”)
    elif status == 403:
        print("没权限")
# 删除
namespace = "default"
name = "api-test"
apps_api.delete_namespaced_deployment(namespace=namespace, name=name)
```

 Service操作：

```
# 查询
for svc in core_api.list_namespaced_service(namespace="default").items:
    print(svc.metadata.name)

# 创建
core_api = client.CoreV1Api()
namespace = "default"
name = "api-test"
selector = {'a':'1', 'b':'2'}  # 不区分数据类型，都要加引号
port = 80
target_port = 80
type = "NodePort"
body = client.V1Service(
    api_version="v1",
    kind="Service",
    metadata=client.V1ObjectMeta(
        name=name
    ),
    spec=client.V1ServiceSpec(
        selector=selector,
        ports=[client.V1ServicePort(
            port=port,
            target_port=target_port
        )],
        type=type
    )
)
core_api.create_namespaced_service(namespace=namespace, body=body)

# 删除
core_api.delete_namespaced_service(namespace=namespace, name=name)
```

#### HTTP API

直接通过HTTP客户端访问K8s HTTP API接口：

```
token="eyJhbGciOiJSUzI1NiIsI..."
curl --cacert /etc/kubernetes/pki/ca.crt -H "Authorization: Bearer $token"  https://192.168.31.71:6443/api/v1/namespaces/default/pods
```

```
curl https://192.168.31.71:6443/api/v1/nodes \
--cacert /etc/kubernetes/pki/ca.crt \
--cert /etc/kubernetes/pki/apiserver-kubelet-client.crt \
--key /etc/kubernetes/pki/apiserver-kubelet-client.key   
```

## 2、 网站布局

### 2.1 准备登录页面

创建应用，用于存放首页、登录、退出、命名空间等公共资源。

```
python manage.py startapp dashboard
```

### 2.2 登录认证（集成RBAC）

![](https://k8s-1252881505.cos.ap-beijing.myqcloud.com/web-dev/k8s-auth.jpg)

使用session就必须启用数据库，用于保存session状态：

```
python manage.py makemigrations
python manage.py migrate
```

![](https://k8s-1252881505.cos.ap-beijing.myqcloud.com/web-dev/k8s-login-auth.png)

登录认证流程：AJAX提交登录认证数据->验证提交数据格式合法性（编写一个登录认证检查函数）->确认没问题向session里写入认证信息->返回AJAX，AJAX跳转到首页。

登录认证检查：

```
import os
from kubernetes import client, config
import yaml
from dashboard.models import User

# 验证认证信息是否有效
def auth_check(auth_type, token):
    if auth_type == "token":
        configuration = client.Configuration()
        configuration.host = "https://192.168.31.71:6443"
        # configuration.ssl_ca_cert = os.path.join('kubeconfig', 'ca.crt')
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + token}
        client.Configuration.set_default(configuration)
        try:
            core_api = client.CoreApi()
            core_api.get_api_versions()  # 随便查询个资源测试
            return True
        except Exception as e:
            print(e)
            return False
    elif auth_type == "kubeconfig":
        try:
            user= User.objects.filter(token=token)
            content = user[0].content
            content = yaml.load(content, Loader=yaml.FullLoader)
            config.load_kube_config_from_dict(content)
            core_api = client.CoreApi()
            core_api.get_api_versions()
            return True
        except Exception as e:
            print(e)
            return False
```

登录认证装饰器：

```
def self_login_required(func):
    def inner(request, *args, **kwargs):
        is_login = request.session.get('is_login', False)
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return redirect("/login")
    return inner
```

视图：

```
from django.shortcuts import render
from django.http import JsonResponse
from kubernetes import client, config
import os,hashlib,random
from devops import k8s
# Create your views here.

@k8s.self_login_required
def index(request):
    return  render(request, 'index.html')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        print(request.POST)
        token = request.POST.get("token")
        # 处理token登录
        if token:
            # 验证你的token是不是有效，对于k8s来说这个token能不能用，如果能用跳转到首页
            if k8s.auth_check('token', token):
                request.session['is_login'] = True
                request.session['auth_type'] = "token"
                request.session['token'] = token # 还需要标识用户，之前我们写的是用户名
                code = 0
                msg = "登录成功"
            else:
                code = 1
                msg = "Token无效！"
        else:
        # 处理kubeconfig文件登录
            file_obj = request.FILES.get("file")
            # 生成一个随时字符串（token）保存到session中作为kubeconfig登录标识用户
            token_random = hashlib.md5(str(random.random()).encode()).hexdigest()
            try:
                content = file_obj.read().decode()  # bytes to str
                User.objects.create(
                    auth_type="kubeconfig",
                    token=token_random,
                    content=content
                )
            except Exception:
                code = 1
                msg = "文件类型错误！"
            if k8s.auth_check('kubeconfig', token_random):
                request.session['is_login'] = True
                request.session['auth_type'] = "kubeconfig"
                request.session['token'] = token_random  # 标识kubeconfig登录用户
                code = 0
                msg = "登录成功"
            else:
                code = 1
                msg = "kubeconfig文件无效！"

        result = {'code': code, 'msg': msg}
        return  JsonResponse(result)
```

### 2.3 管理平台页面布局

根据布局创建对象的django 应用。

```
python manage.py startapp <应用名称>
```

应用名称：

- dashboard：存放公共
- k8s

  - Node：K8s集群计算节点

  - Namespaces：命名空间，用于隔离资源

  - PersistentVolumes（PV）：持久卷，存储数据
- workload

  - Deployments：无状态应用部署控制器
  - DaemonSets：守护进程控制器，在每个节点启动一个Pod
  - StatefulSets：有状态应用部署控制器
  - Pods：K8s最小部署单元
- loadbalancer

  - Services：为Pod提供服务发现和负载均衡
  - Ingresses：集群中应用统一入口，对外暴露应用
- storage

  - PersistentVolumeClaims（PVC）：持久卷申请，与PV绑定
  - ConfigMaps：存储配置内容，例如应用程序配置文件
  - Secrets：存储应用敏感数据，例如用户名密码

导航栏显示：

```
layui-nav-itemed  # 展开的样式类
layui-this  # 子菜单选中背景样式类

<li class="layui-nav-item {% block nav-item-1 %}{% endblock %}">
    <a href="javascript:;">Kubernetes</a>
    <dl class="layui-nav-child">
    <dd><a href="{% url 'node' %}" class="{% block nav-this-1-1 %}{% endblock %}">Nodes</a></dd>
    <dd><a href="{% url 'namespace' %}" class="{% block nav-this-1-2 %}{% endblock %}">Namespaces</a></dd>
    <dd><a href="javascript:;" class="{% block nav-this-1-3 %}{% endblock %}">PersistentVolumes</a></dd>
    </dl>
</li>
```

### 2.4 命名空间选择

工作流程：登录成功跳转到首页->ajax GET请求namespace接口获取所有命名空间并追究到select列表项，再设置default为默认命名空间->再将当前命名空间存储到本地session，实现其他页面能共享获取，每次根据当前命名空间请求资源接口。

命名空间作用：

- 基于命名空间查询资源
- 特点：与其他页面共享当前选择命名空间，共享：
  - 每个页面JS动态获取select值
  - 存到数据库里
  - 使用sessionStorage浏览器中存储，关闭浏览器自动删除（对应还有一个功能  localStorage，持久存储 ）

## 3、数据表格展示K8s常见资源

![](https://k8s-1252881505.cos.ap-beijing.myqcloud.com/web-dev/k8s-api-flow.png)

大致思路：

1. 使用Layui从接口获取JSON数据，动态渲染表格

2. Django准备接口，以JSON格式返回

   资源增删改查采用不同HTTP方法：

   | HTTP方法 | **数据处理** | **说明**     |
   | -------- | ------------ | ------------ |
   | POST     | 新增         | 新增一个资源 |
   | GET      | 获取         | 取得一个资源 |
   | PUT      | 更新         | 更新一个资源 |
   | DELETE   | 删除         | 删除一个资源 |

3. 接口类实例化，遍历获取接口数据，取对应字段值，组成一个字典

### 3.1 Namespace

查询：

```
for ns in core_api.list_namespace().items: # items返回一个对象，类LIST（[{命名空间属性},{命名空间属性}] ），每个元素是一个类字典（命名空间属性），操作类字典
    name = ns.metadata.name
    labels = ns.metadata.labels
    create_time = ns.metadata.creation_timestamp
    namespace = {"name": name, "labels": labels, "create_time": create_time}
```

> 字段：名称、标签、创建时间

删除：

```
core_api.delete_namespace(name=name)
```

创建：

```
body = client.V1Namespace(
    api_version="v1",
    kind="Namespace",
    metadata=client.V1ObjectMeta(
    name=ns_name
    )
)
core_api.create_namespace(body=body)
```

数据表格：

```
      table.render({
        elem: '#test'
        ,url:'{% url 'namespace_api' %}'
        ,toolbar: '#toolbarDemo' //开启头部工具栏，并为其绑定左侧模板
        ,defaultToolbar: ['filter', 'exports', 'print', { //自定义头部工具栏右侧图标。如无需自定义，去除该参数即可
          title: '提示'
          ,layEvent: 'LAYTABLE_TIPS'
          ,icon: 'layui-icon-tips'
        }]
        ,cols: [[
          {field: 'name', title: '名称', sort: true}
          ,{field: 'labels', title: '标签',templet: labelsFormat}
          ,{field: 'create_time', title: '创建时间'}
          ,{fixed: 'right', title:'操作', toolbar: '#barDemo', width:150}
        ]]
        ,page: true
      });
      // 标签格式化，是一个对象
      function labelsFormat(d){
          result = "";
          if (d.labels == null){
              return "None"
          } else {
              for (let key in d.labels) {
                  result += '<span style="border: 1px solid #d6e5ec;border-radius: 8px">' +
                      key + ':' + d.labels[key] +
                      '</span><br>'
              }
              return result
          }
      }
```

> 其他资源功能开发与命名空间一样，拷贝后需要的修改位置：
>
> - 服务端：新添加一个url，函数视图
> - 服务端：函数视图GET方法里修改for遍历的K8s API接口、对应字段，DELETE方法里修改删除的K8s API接口
> - 前端：面包屑
> - 前端：table.renader修改连接的API接口，对应表头，删除接口及提示文字
> - 另外，除了Namespace、Node、PV，其他适配加命名空间

### 3.2 Node

查询：

```
for node in core_api.list_node_with_http_info()[0].items:
    name = node.metadata.name
    labels = node.metadata.labels
    status = node.status.conditions[-1].status
    scheduler = ("是" if node.spec.unschedulable is None else "否")
    cpu = node.status.capacity['cpu']
    memory = node.status.capacity['memory']
    kebelet_version = node.status.node_info.kubelet_version
    cri_version = node.status.node_info.container_runtime_version
    create_time = node.metadata.creation_timestamp
    node = {"name": name, "labels": labels, "status":status,
                 "scheduler":scheduler , "cpu":cpu, "memory":memory,
                 "kebelet_version":kebelet_version, "cri_version":cri_version,
                "create_time": create_time}
```

> 字段：名称、标签、准备就绪、可调度、CPU、内存、kubelet版本、CRI版本、创建时间

数据表格：

```
  table.render({
    elem: '#test'
    ,url:'{% url 'node_api' %}'
    ,toolbar: '#toolbarDemo' //开启头部工具栏，并为其绑定左侧模板
    ,defaultToolbar: ['filter', 'exports', 'print', { //自定义头部工具栏右侧图标。如无需自定义，去除该参数即可
      title: '提示'
      ,layEvent: 'LAYTABLE_TIPS'
      ,icon: 'layui-icon-tips'
    }]
    ,cols: [[
      {field: 'name', title: '名称', sort: true}
      ,{field: 'labels', title: '标签',templet: labelsFormat}
      ,{field: 'status', title: '准备就绪'}
      ,{field: 'scheduler', title: '可调度'}
      ,{field: 'cpu', title: 'CPU'}
      ,{field: 'memory', title: '内存'}
      ,{field: 'kebelet_version', title: 'kubelet版本'}
      ,{field: 'cri_version', title: 'CRI版本'}
      ,{field: 'create_time', title: '创建时间'}
      ,{fixed: 'right', title:'操作', toolbar: '#barDemo', width:150}
    ]]
    ,page: true
  });
  // 标签格式化，是一个对象
      function labelsFormat(d){
          result = "";
          if (d.labels == null){
              return "None"
          } else {
              for (let key in d.labels) {
                  result += '<span style="border: 1px solid #d6e5ec;border-radius: 8px">' +
                      key + ':' + d.labels[key] +
                      '</span><br>'
              }
              return result
          }
   }
```

### 3.3 PV

Pod->PVC->PV->外部存储，例如NFS、Ceph

查询：

```
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
                pv = {"name": name, "capacity": capacity, "access_modes":access_modes,
                             "reclaim_policy":reclaim_policy , "status":status, "pvc":pvc,
                            "storage_class":storage_class,"create_time": create_time}
```

> 字段：名称、容量、访问模式、回收策略、状态、卷申请（PVC）/命名空间、存储类、创建时间

创建：

```
        name = request.POST.get("name", None)
        capacity = request.POST.get("capacity", None)
        access_mode = request.POST.get("access_mode", None)
        storage_type = request.POST.get("storage_type", None)
        server_ip = request.POST.get("server_ip", None)
        mount_path = request.POST.get("mount_path", None)

		body = client.V1PersistentVolume(
            api_version="v1",
            kind="PersistentVolume",
            metadata=client.V1ObjectMeta(name=name),
            spec=client.V1PersistentVolumeSpec(
                capacity={'storage':capacity},
                access_modes=[access_mode],
                nfs=client.V1NFSVolumeSource(
                    server=server_ip,
                    path="/ifs/kubernetes/%s" %mount_path
                )
            )
        )
        core_api.create_persistent_volume(body=body)
```

删除：

```
core_api.delete_persistent_volume(name=name)
```

数据表格：

```
table.render({
  elem: '#test'
  ,url:'{% url 'pv_api' %}'
  ,toolbar: '#toolbarDemo' //开启头部工具栏，并为其绑定左侧模板
  ,defaultToolbar: ['filter', 'exports', 'print', { //自定义头部工具栏右侧图标。如无需自定义，去除该参数即可
    title: '提示'
    ,layEvent: 'LAYTABLE_TIPS'
    ,icon: 'layui-icon-tips'
  }]
  ,cols: [[
    {field: 'name', title: '名称', sort: true}
    ,{field: 'capacity', title: '容量'}
    ,{field: 'access_modes', title: '访问模式'}
    ,{field: 'reclaim_policy', title: '回收策略'}
    ,{field: 'status', title: '状态'}
    ,{field: 'pvc', title: 'PVC(命名空间/名称)'}
    ,{field: 'storage_class', title: '存储类'}
    ,{field: 'create_time', title: '创建时间'}
    ,{fixed: 'right', title:'操作', toolbar: '#barDemo', width:150}
  ]]
  ,page: true
  ,id: 'pvtb'
});
```

### 3.4 Deployment

查询：

```
for dp in apps_api.list_namespaced_deployment(namespace).items:
    name = dp.metadata.name
    namespace = dp.metadata.namespace
    replicas = dp.spec.replicas
    available_replicas = ( 0 if dp.status.available_replicas is None else dp.status.available_replicas)
    labels = dp.metadata.labels
    selector = dp.spec.selector.match_labels
    containers = {}
    for c in dp.spec.template.spec.containers:
        containers[c.name] = c.image
    create_time = dp.metadata.creation_timestamp
    dp = {"name": name, "namespace": namespace, "replicas":replicas,
                 "available_replicas":available_replicas , "labels":labels, "selector":selector,
                 "containers":containers, "create_time": create_time}
```

> 字段：名称、命名空间、预期副本数、可用副本数、Pod标签选择器、镜像/状态、创建时间

创建：

```
        name = request.POST.get("name",None)
        namespace = request.POST.get("namespace",None)
        image = request.POST.get("image",None)
        replicas = int(request.POST.get("replicas",None))
        # 处理标签
        labels = {}
        try:
            for l in request.POST.get("labels",None).split(","):
                k = l.split("=")[0]
                v = l.split("=")[1]
                labels[k] = v
        except Exception as e:
            res = {"code": 1, "msg": "标签格式错误！"}
            return JsonResponse(res)
        resources = request.POST.get("resources",None)
        health_liveness = request.POST.get("health[liveness]",None)  # {'health[liveness]': ['on'], 'health[readiness]': ['on']}
        health_readiness = request.POST.get("health[readiness]",None)

        if resources == "1c2g":
            resources = client.V1ResourceRequirements(limits={"cpu":"1","memory":"1Gi"},
                                                      requests={"cpu":"0.9","memory":"0.9Gi"})
        elif resources == "2c4g":
            resources = client.V1ResourceRequirements(limits={"cpu": "2", "memory": "4Gi"},
                                                      requests={"cpu": "1.9", "memory": "3.9Gi"})
        elif resources == "4c8g":
            resources = client.V1ResourceRequirements(limits={"cpu": "4", "memory": "8Gi"},
                                                      requests={"cpu": "3.9", "memory": "7.9Gi"})
        else:
            resources = client.V1ResourceRequirements(limits={"cpu":"500m","memory":"1Gi"},
                                                      requests={"cpu":"450m","memory":"900Mi"})
        liveness_probe = ""
        if health_liveness == "on":
            liveness_probe = client.V1Probe(http_get="/",timeout_seconds=30,initial_delay_seconds=30)
        readiness_probe = ""
        if health_readiness == "on":
            readiness_probe = client.V1Probe(http_get="/",timeout_seconds=30,initial_delay_seconds=30)

        for dp in apps_api.list_namespaced_deployment(namespace=namespace).items:
            if name == dp.metadata.name:
                res = {"code": 1, "msg": "Deployment已经存在！"}
                return JsonResponse(res)

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
                        containers=[client.V1Container(   # https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Container.md
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

   apps_api.create_namespaced_deployment(namespace=namespace, body=body)
```

删除：

```
apps_api.delete_namespaced_deployment(namespace=namespace, name=name)
```

数据表格：

```
      table.render({
        elem: '#test'
        ,url:'{% url 'deployment_api' %}?namespace=' + namespace
        ,toolbar: '#toolbarDemo' //开启头部工具栏，并为其绑定左侧模板
        ,defaultToolbar: ['filter', 'exports', 'print', { //自定义头部工具栏右侧图标。如无需自定义，去除该参数即可
          title: '提示'
          ,layEvent: 'LAYTABLE_TIPS'
          ,icon: 'layui-icon-tips'
        }]
        ,cols: [[
          {field: 'name', title: '名称', sort: true}
          ,{field: 'namespace', title: '命名空间'}
          ,{field: 'replicas', title: '预期副本数'}
          ,{field: 'available_replicas', title: '可用副本数'}
          ,{field: 'labels', title: '标签',templet: labelsFormat}
          ,{field: 'selector', title: 'Pod标签选择器',templet: selectorFormat}
          ,{field: 'containers', title: '容器', templet: containersFormat}
          ,{field: 'create_time', title: '创建时间'}
          ,{fixed: 'right', title:'操作', toolbar: '#barDemo', width:150}
        ]]
        ,page: true
          ,id: 'dptb'
      });
      // 标签格式化，是一个对象
      function labelsFormat(d){
          result = "";
          if(d.labels == null){
              return "None"
          } else {
              for (let key in d.labels) {
                  result += '<span style="border: 1px solid #d6e5ec;border-radius: 8px">' +
                      key + ':' + d.labels[key] +
                      '</span><br>'
              }
              return result
          }
      }
      function selectorFormat(d){
          result = "";
          for(let key in d.selector) {
             result += '<span style="border: 1px solid #d6e5ec;border-radius: 8px">' +
                  key + ':' + d.selector[key] +
                     '</span><br>'
          }
          return result
      }
      function containersFormat(d) {
          result = "";
          for(let key in d.containers) {
              result += key + '=' + d.containers[key] + '<br>'
          }
          return result
      }
```



### 3.5 DaemonSet

查询：

```
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
```

> 字段：名称、命名空间、预期节点数、可用节点数、Pod标签选择器、镜像、创建时间

创建：

        name = request.POST.get("name",None)
        namespace = request.POST.get("namespace",None)
        image = request.POST.get("image",None)
        # 处理标签
        labels = {}
        try:
            for l in request.POST.get("labels",None).split(","):
                k = l.split("=")[0]
                v = l.split("=")[1]
                labels[k] = v
        except Exception as e:
            res = {"code": 1, "msg": "标签格式错误！"}
            return JsonResponse(res)
        resources = request.POST.get("resources",None)
        health_liveness = request.POST.get("health[liveness]",None)  # {'health[liveness]': ['on'], 'health[readiness]': ['on']}
        health_readiness = request.POST.get("health[readiness]",None)
    
        if resources == "1c2g":
            resources = client.V1ResourceRequirements(limits={"cpu":"1","memory":"1Gi"},
                                                      requests={"cpu":"0.9","memory":"0.9Gi"})
        elif resources == "2c4g":
            resources = client.V1ResourceRequirements(limits={"cpu": "2", "memory": "4Gi"},
                                                      requests={"cpu": "1.9", "memory": "3.9Gi"})
        elif resources == "4c8g":
            resources = client.V1ResourceRequirements(limits={"cpu": "4", "memory": "8Gi"},
                                                      requests={"cpu": "3.9", "memory": "7.9Gi"})
        else:
            resources = client.V1ResourceRequirements(limits={"cpu":"500m","memory":"1Gi"},
                                                      requests={"cpu":"450m","memory":"900Mi"})
        liveness_probe = ""
        if health_liveness == "on":
            liveness_probe = client.V1Probe(http_get="/",timeout_seconds=30,initial_delay_seconds=30)
        readiness_probe = ""
        if health_readiness == "on":
            readiness_probe = client.V1Probe(http_get="/",timeout_seconds=30,initial_delay_seconds=30)
    
        for dp in apps_api.list_namespaced_daemon_set(namespace=namespace).items:
            if name == dp.metadata.name:
                res = {"code": 1, "msg": "DaemonSet已经存在！"}
                return JsonResponse(res)
    
        body = client.V1DaemonSet(
            api_version="apps/v1",
            kind="DaemonSet",
            metadata=client.V1ObjectMeta(name=name),
            spec=client.V1DeploymentSpec(
                selector={'matchLabels': labels},
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(labels=labels),
                    spec=client.V1PodSpec(
                        containers=[client.V1Container(   # https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Container.md
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
删除：

```
apps_api.delete_namespaced_daemon_set(namespace=namespace, name=name)
```

数据表格：

```
      table.render({
        elem: '#test'
        ,url:'{% url 'daemonset_api' %}?namespace=' + namespace
        ,toolbar: '#toolbarDemo' //开启头部工具栏，并为其绑定左侧模板
        ,defaultToolbar: ['filter', 'exports', 'print', { //自定义头部工具栏右侧图标。如无需自定义，去除该参数即可
          title: '提示'
          ,layEvent: 'LAYTABLE_TIPS'
          ,icon: 'layui-icon-tips'
        }]
        ,cols: [[
          {field: 'name', title: '名称', sort: true}
          ,{field: 'namespace', title: '命名空间',sort: true}
          ,{field: 'desired_number', title: '预期节点数',width: 100}
          ,{field: 'available_number', title: '可用节点数',width: 100}
          ,{field: 'labels', title: '标签',templet: labelsFormat}
          ,{field: 'selector', title: 'Pod 标签选择器',templet: selecotrFormat}
          ,{field: 'containers', title: '容器', templet: containersFormat}
          ,{field: 'create_time', title: '创建时间',width: 200}
          ,{fixed: 'right', title:'操作', toolbar: '#barDemo',width: 150}
        ]]
        ,page: true
          ,id: 'dstb'
      });
      // 标签格式化，是一个对象
      function labelsFormat(d){
          result = "";
          if(d.labels == null){
              return "None"
          } else {
              for (let key in d.labels) {
                  result += '<span style="border: 1px solid #d6e5ec;border-radius: 8px">' +
                      key + ':' + d.labels[key] +
                      '</span><br>'
              }
              return result
          }
      }
      function selecotrFormat(d){
          result = "";
          for(let key in d.selector) {
             result += '<span style="border: 1px solid #d6e5ec;border-radius: 8px">' +
                  key + ':' + d.selector[key] +
                     '</span><br>'
          }
          return result
      }
      function containersFormat(d) {
          result = "";
          for(let key in d.containers) {
              result += key + '=' + d.containers[key] + '<br>'
          }
          return result
      }
```

### 3.6 StatefulSet

查询：

```
for sts in apps_api.list_namespaced_stateful_set(namespace).items:
    name = sts.metadata.name
    namespace = sts.metadata.namespace
    labels = sts.metadata.labels
    selector = sts.spec.selector.match_labels
    replicas = sts.spec.replicas
    ready_replicas = ("0" if sts.status.ready_replicas is None else sts.status.ready_replicas)
    #current_replicas = sts.status.current_replicas
    service_name = sts.spec.service_name
	containers = {}
	for c in sts.spec.template.spec.containers:
		containers[c.name] = c.image    
    create_time = sts.metadata.creation_timestamp
 
    ds = {"name": name, "namespace": namespace, "labels": labels, "replicas": replicas,
            "ready_replicas": ready_replicas, "service_name": service_name,
            "selector": selector, "containers": containers, "create_time": create_time}
```

> 字段：名称、命名空间、Service名称、预期副本数、可用副本数、Pod标签选择器、镜像、创建时间

删除：

```
apps_api.delete_namespaced_stateful_set(namespace=namespace, name=name)
```

数据表格：

```
      table.render({
        elem: '#test'
        ,url:'{% url 'statefulset_api' %}?namespace=' + namespace
        ,toolbar: '#toolbarDemo' //开启头部工具栏，并为其绑定左侧模板
        ,defaultToolbar: ['filter', 'exports', 'print', { //自定义头部工具栏右侧图标。如无需自定义，去除该参数即可
          title: '提示'
          ,layEvent: 'LAYTABLE_TIPS'
          ,icon: 'layui-icon-tips'
        }]
        ,cols: [[
          {field: 'name', title: '名称', sort: true}
          ,{field: 'namespace', title: '命名空间',sort: true}
          ,{field: 'service_name', title: 'Service名称'}
          ,{field: 'replicas', title: '预期副本数',width: 100}
          ,{field: 'ready_replicas', title: '可用副本数',width: 100}
          ,{field: 'labels', title: '标签',templet: labelsFormat}
          ,{field: 'selector', title: 'Pod 标签选择器',templet: selecotrFormat}
          ,{field: 'containers', title: '容器', templet: containersFormat}
          ,{field: 'create_time', title: '创建时间',width: 200}
          ,{fixed: 'right', title:'操作', toolbar: '#barDemo',width: 150}
        ]]
        ,page: true
          ,id: 'ststb'
      });
      // 标签格式化，是一个对象
      function labelsFormat(d){
          result = "";
          if(d.labels == null){
              return "None"
          } else {
              for (let key in d.labels) {
                  result += '<span style="border: 1px solid #d6e5ec;border-radius: 8px">' +
                      key + ':' + d.labels[key] +
                      '</span><br>'
              }
              return result
          }
      }
      function selecotrFormat(d){
          result = "";
          for(let key in d.selector) {
             result += '<span style="border: 1px solid #d6e5ec;border-radius: 8px">' +
                  key + ':' + d.selector[key] +
                     '</span><br>'
          }
          return result
      }
      function containersFormat(d) {
          result = "";
          for(let key in d.containers) {
              result += key + '=' + d.containers[key] + '<br>'
          }
          return result
      }
```



### 3.7 Pod

查询：

```
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

            c = {'c_name': c_name,'c_image':c_image ,'restart_count': restart_count, 'c_status': c_status}
            containers.append(c)

    create_time = po.metadata.creation_timestamp

    po = {"name": name, "namespace": namespace, "pod_ip": pod_ip,
            "labels": labels, "containers": containers, "status": status,
            "create_time": create_time}
```

> 字段：名称、命名空间、IP地址、标签、容器组、状态、创建时间

删除：

```
core_api.delete_namespaced_pod(namespace=namespace, name=name)
```

数据表格：

```
table.render({
  elem: '#test'
  ,url:'{% url 'pod_api' %}?namespace=' + namespace
  ,toolbar: '#toolbarDemo' //开启头部工具栏，并为其绑定左侧模板
  ,defaultToolbar: ['filter', 'exports', 'print', { //自定义头部工具栏右侧图标。如无需自定义，去除该参数即可
    title: '提示'
    ,layEvent: 'LAYTABLE_TIPS'
    ,icon: 'layui-icon-tips'
  }]
  ,cols: [[
    {field: 'name', title: '名称', sort: true}
    ,{field: 'namespace', title: '命名空间',sort: true}
    ,{field: 'pod_ip', title: 'IP地址'}
    ,{field: 'labels', title: '标签', templet: labelsFormat}
    ,{field: 'containers', title: '容器组', templet: containersFormat}
    ,{field: 'status', title: '状态',sort: true, templet: statusFormat}
    ,{field: 'create_time', title: '创建时间'}
    ,{fixed: 'right', title:'操作', toolbar: '#barDemo',width: 250}
  ]]
  ,page: true
  ,id: 'potb'
});
// 标签格式化，是一个对象
function labelsFormat(d){
    result = "";
    if(d.labels == null){
        return "None"
    } else {
        for (let key in d.labels) {
            result += '<span style="border: 1px solid #d6e5ec;border-radius: 8px">' +
                key + ':' + d.labels[key] +
                '</span><br>'
        }
        return result
    }
}
function containersFormat(d) {
	result = "";
    if (d.containers) {
        for(let key in d.containers) {
            data = d.containers[key];
            result += key + ':' + data.c_name  + '=' + data.c_image + '<br>' +
                      '重启次数:' + data.restart_count  + '<br>' +
                      '状态:' + data.c_status + '<br>'
        }
        return result
    } else {
        return "None"
    }
}
// 如果status为None，使用容器状态显示
function statusFormat(d){
	result = "";
    if(d.status == "None"){
        for(let key in d.containers) {
            result += d.containers[key].c_status + '<br>'
        }
        return result
    } else {
        return d.status
    }
}
```

### 3.8 Service

查询：

```
for svc in core_api.list_namespaced_service(namespace=namespace).items:
    name = svc.metadata.name
    namespace = svc.metadata.namespace
    labels = svc.metadata.labels
    type = svc.spec.type
    cluster_ip = svc.spec.cluster_ip
    ports = []
    for p in svc.spec.ports:  # 不是序列，不能直接返回
        port_name = p.name
        port = p.port
        target_port = p.target_port
        protocol = p.protocol
        node_port = ""
        if type == "NodePort":
            node_port = " <br> NodePort: %s" % p.node_port

        port = {'port_name': port_name, 'port': port, 'protocol': protocol, 'target_port':target_port, 'node_port': node_port}
        ports.append(port)

    selector = svc.spec.selector
    create_time = svc.metadata.creation_timestamp

    # 确认是否关联Pod
    endpoint = ""
    for ep in core_api.list_namespaced_endpoints(namespace=namespace).items:
        if ep.metadata.name == name and ep.subsets is None:
            endpoint = "未关联"
        else:
            endpoint = "已关联"

    svc = {"name": name, "namespace": namespace, "type": type,
            "cluster_ip": cluster_ip, "ports": ports, "labels": labels,
            "selector": selector, "endpoint": endpoint, "create_time": create_time}
```

> 字段：名称、命名空间、类型、集群IP、端口信息、Pod标签选择器、后端Pod、创建时间

创建：

```
        name = request.POST.get("name",None)
        namespace = request.POST.get("namespace",None)
        port = int(request.POST.get("port",None))
        target_port = int(request.POST.get("target-port",None))
        labels = {}
        try:
            for l in request.POST.get("labels",None).split(","):
                k = l.split("=")[0]
                v = l.split("=")[1]
                labels[k] = v
        except Exception as e:
            res = {"code": 1, "msg": "标签格式错误！"}
            return JsonResponse(res)
        type = request.POST.get("type","")

        body = client.V1Service(
            api_version="v1",
            kind="Service",
            metadata=client.V1ObjectMeta(
                name=name
            ),
            spec=client.V1ServiceSpec(
                selector=labels,
                ports=[client.V1ServicePort(
                    port=port,
                    target_port=target_port,

                )],
                type=type
            )
        )
       core_api.create_namespaced_service(namespace=namespace, body=body)
```

删除：

```
core_api.delete_namespaced_service(namespace=namespace, name=name)
```

数据表格：

```
table.render({
  elem: '#test'
  ,url:'{% url 'service_api' %}?namespace=' + namespace
  ,toolbar: '#toolbarDemo' //开启头部工具栏，并为其绑定左侧模板
  ,defaultToolbar: ['filter', 'exports', 'print', { //自定义头部工具栏右侧图标。如无需自定义，去除该参数即可
    title: '提示'
    ,layEvent: 'LAYTABLE_TIPS'
    ,icon: 'layui-icon-tips'
  }]
  ,cols: [[
      {field: 'name', title: '名称', sort: true, width: 150}
      ,{field: 'namespace', title: '命名空间',width: 150, sort: true}
      ,{field: 'type', title: '类型',width: 120, sort: true}
      ,{field: 'cluster_ip', title: '集群IP',width: 100}
      ,{field: 'ports', title: '端口信息',templet: portsFormat}
      ,{field: 'labels', title: '标签', templet: labelsFormat}
      ,{field: 'selector', title: 'Pod 标签选择器', templet: selecotrFormat}
      ,{field: 'endpoint', title: '后端 Pod'}
      ,{field: 'create_time', title: '创建时间'}
    ,{fixed: 'right', title:'操作', toolbar: '#barDemo',width: 150}
  ]]
  ,page: true
    ,id: 'svctb'
});
// 标签格式化，是一个对象
function labelsFormat(d){
    result = "";
    if(d.labels == null){
        return "None"
    } else {
        for (let key in d.labels) {
            result += '<span style="border: 1px solid #d6e5ec;border-radius: 8px">' +
                key + ':' + d.labels[key] +
                '</span><br>'
        }
        return result
    }
}
function selecotrFormat(d){
    result = "";
    for(let key in d.selector) {
       result += '<span style="border: 1px solid #d6e5ec;border-radius: 8px">' +
            key + ':' + d.selector[key] +
               '</span><br>'
    }
    return result
}
function portsFormat(d) {
    result = "";
    for(let key in d.ports) {
        data = d.ports[key];
        result += '名称: ' + data.port_name + '<br>' +
                '端口: ' + data.port + '<br>' +
                '协议: ' + data.protocol + '<br>' +
                '容器端口: ' + data.target_port + '<br>'
    }
    return result
}
```

### 3.9 Ingress

查询：

```
for ing in networking_api.list_namespaced_ingress(namespace=namespace).items:
    name = ing.metadata.name
    namespace = ing.metadata.namespace
    labels = ing.metadata.labels
    service = "None"
    http_hosts = "None"
    for h in ing.spec.rules:
        host = h.host
        path = ("/" if h.http.paths[0].path is None else h.http.paths[0].path)
        service_name = h.http.paths[0].backend.service_name
        service_port = h.http.paths[0].backend.service_port
        http_hosts = {'host': host, 'path': path, 'service_name': service_name, 'service_port': service_port}

    https_hosts = "None"
    if ing.spec.tls is None:
        https_hosts = ing.spec.tls
    else:
        for tls in ing.spec.tls:
            host = tls.hosts[0]
            secret_name = tls.secret_name
            https_hosts = {'host': host, 'secret_name': secret_name}

    create_time = ing.metadata.creation_timestamp

    ing = {"name": name, "namespace": namespace,"labels": labels ,"http_hosts": http_hosts,
            "https_hosts": https_hosts, "service": service, "create_time": create_time

```

> 字段：名称、命名空间、HTTP、HTTPS、关联Service、创建时间

创建：

```
        name = request.POST.get("name",None)
        namespace = request.POST.get("namespace",None)
        host = request.POST.get("host",None)
        path = request.POST.get("path","/")
        svc_name = request.POST.get("svc_name",None)
        svc_port = int(request.POST.get("svc_port",None))

        body = client.NetworkingV1beta1Ingress(
            api_version="networking.k8s.io/v1beta1",
            kind="Ingress",
            metadata=client.V1ObjectMeta(name=name, annotations={
                "nginx.ingress.kubernetes.io/rewrite-target": "/"
            }),
            spec=client.NetworkingV1beta1IngressSpec(
                rules=[client.NetworkingV1beta1IngressRule(
                    host=host,
                    http=client.NetworkingV1beta1HTTPIngressRuleValue(
                        paths=[client.NetworkingV1beta1HTTPIngressPath(
                            path=path,
                            backend=client.NetworkingV1beta1IngressBackend(
                                service_port=svc_port,
                                service_name=svc_name)

                        )]
                    )
                )
                ]
            )
        )
    networking_api.create_namespaced_ingress(namespace=namespace, body=body)
```

删除：

```
networking_api.delete_namespaced_ingress(namespace=namespace, name=name)
```

数据表格：

```
table.render({
  elem: '#test'
  ,url:'{% url 'ingress_api' %}?namespace=' + namespace
  ,toolbar: '#toolbarDemo' //开启头部工具栏，并为其绑定左侧模板
  ,defaultToolbar: ['filter', 'exports', 'print', { //自定义头部工具栏右侧图标。如无需自定义，去除该参数即可
    title: '提示'
    ,layEvent: 'LAYTABLE_TIPS'
    ,icon: 'layui-icon-tips'
  }]
  ,cols: [[
    {field: 'name', title: '名称', sort: true, width: 300}
    ,{field: 'namespace', title: '命名空间',width: 200, sort: true}
    ,{field: 'http_hosts', title: 'HTTP',templet: httpFormat}
    ,{field: 'https_hosts', title: 'HTTPS',templet: httpsFormat}
    ,{field: 'service', title: '关联 Service', templet: serviceFormat}
    ,{field: 'create_time', title: '创建时间',width: 200}
    ,{fixed: 'right', title:'操作', toolbar: '#barDemo',width: 150}
  ]]
  ,page: true
    ,id: 'ingtb'
});
// 标签格式化，是一个对象
function httpFormat(d){
    return "域名: " + d.http_hosts.host + '<br>' + "路径: " + d.http_hosts.path + '<br>'
}
function httpsFormat(d){
    if(d.https_hosts != null){
        return "域名: " + d.https_hosts.host + '<br>' + "证书Secret名称: " + d.https_hosts.secret_name + '<br>';
    } else {
        return "None"
    }
}
function serviceFormat(d) {
    return "名称: " + d.http_hosts.service_name + '<br>' + "端口: " + d.http_hosts.service_port + '<br>';
}
```

### 3.10 PVC

查询：

```
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
```

> 字段：名称、命名空间、状态、卷名称、容量、访问模式、存储类、创建时间

创建：

```
        name = request.POST.get("name", None)
        namespace = request.POST.get("namespace", None)
        storage_class = request.POST.get("storage_class", None)
        access_mode = request.POST.get("access_mode", None)
        capacity = request.POST.get("capacity", None)
        body = client.V1PersistentVolumeClaim(
                api_version="v1",
                kind="PersistentVolumeClaim",
                metadata=client.V1ObjectMeta(name=name,namespace=namespace),
                spec=client.V1PersistentVolumeClaimSpec(
                    storage_class_name=storage_class,   # 使用存储类创建PV，如果不用可去掉
                    access_modes=[access_mode],
                    resources=client.V1ResourceRequirements(
                      requests={"storage" : capacity}
                    )
                )
            )
         core_api.create_namespaced_persistent_volume_claim(namespace=namespace, body=body)
```

删除：

```
core_api.delete_namespaced_persistent_volume_claim(namespace=namespace, name=name)
```

数据表格：

```
layui.use('table', function(){
  var table = layui.table;
  var $ = layui.jquery;

  table.render({
    elem: '#test'
    ,url:'{% url 'pvc_api' %}?namespace=' + namespace
    ,toolbar: '#toolbarDemo' //开启头部工具栏，并为其绑定左侧模板
    ,defaultToolbar: ['filter', 'exports', 'print', { //自定义头部工具栏右侧图标。如无需自定义，去除该参数即可
      title: '提示'
      ,layEvent: 'LAYTABLE_TIPS'
      ,icon: 'layui-icon-tips'
    }]
    ,cols: [[
      {field: 'name', title: '名称', sort: true}
      ,{field: 'namespace', title: '命名空间',sort: true}
      ,{field: 'labels', title: '标签',templet: labelsFormat}
      ,{field: 'status', title: '状态',width: 130}
      ,{field: 'volume_name', title: '卷名称'}
      ,{field: 'capacity', title: '容量',width: 130}
      ,{field: 'access_modes', title: '访问模式'}
      ,{field: 'storage_class_name', title: '存储类'}
      ,{field: 'create_time', title: '创建时间',width: 200}
      ,{fixed: 'right', title:'操作', toolbar: '#barDemo',width: 150}
    ]]
    ,page: true
      ,id: 'pvctb'
  });
  // 标签格式化，是一个对象
  function labelsFormat(d){
      result = "";
      if(d.labels == null){
          return "None"
      } else {
          for (let key in d.labels) {
              result += '<span style="border: 1px solid #d6e5ec;border-radius: 8px">' +
                  key + ':' + d.labels[key] +
                  '</span><br>'
          }
          return result
      }
  }
```

### 3.11 ConfigMap

查询：

```
for cm in core_api.list_namespaced_config_map(namespace=namespace).items:
    name = cm.metadata.name
    namespace = cm.metadata.namespace
    data_length = ("0" if cm.data is None else len(cm.data))
    create_time = cm.metadata.creation_timestamp

    cm = {"name": name, "namespace": namespace, "data_length": data_length, "create_time": create_time}
```

> 字段：名称、命名空间、数据数量、创建时间

删除：

```
core_api.delete_namespaced_config_map(name=name,namespace=namespace)
```

数据表格：

```
table.render({
  elem: '#test'
  ,url:'{% url 'configmap_api' %}?namespace=' + namespace
  ,toolbar: '#toolbarDemo' //开启头部工具栏，并为其绑定左侧模板
  ,defaultToolbar: ['filter', 'exports', 'print', { //自定义头部工具栏右侧图标。如无需自定义，去除该参数即可
    title: '提示'
    ,layEvent: 'LAYTABLE_TIPS'
    ,icon: 'layui-icon-tips'
  }]
  ,cols: [[
    {field: 'name', title: '名称', sort: true}
    ,{field: 'namespace', title: '命名空间',sort: true}
    ,{field: 'data_length', title: '数据数量'}
    ,{field: 'create_time', title: '创建时间'}
    ,{fixed: 'right', title:'操作', toolbar: '#barDemo',width: 150}
  ]]
  ,page: true
    ,id: 'cmtb'
});
// 标签格式化，是一个对象
function labelsFormat(d){
    result = "";
    if(d.labels == null){
        return "None"
    } else {
        for (let key in d.labels) {
            result += '<span style="border: 1px solid #d6e5ec;border-radius: 8px">' +
                key + ':' + d.labels[key] +
                '</span><br>'
        }
        return result
    }
}
```

### 3.12 Secret

查询：

```
for secret in core_api.list_namespaced_secret(namespace=namespace).items:
    name = secret.metadata.name
    namespace = secret.metadata.namespace
    data_length = ("空" if secret.data is None else len(secret.data))
    create_time = secret.metadata.creation_timestamp

    se = {"name": name, "namespace": namespace, "data_length": data_length, "create_time": create_time}
```

> 字段：名称、命名空间、数据数量、创建时间

删除：

```
core_api.delete_namespaced_secret(namespace=namespace, name=name)
```

数据表格：

```
table.render({
  elem: '#test'
  ,url:'{% url 'secret_api' %}?namespace=' + namespace
  ,toolbar: '#toolbarDemo' //开启头部工具栏，并为其绑定左侧模板
  ,defaultToolbar: ['filter', 'exports', 'print', { //自定义头部工具栏右侧图标。如无需自定义，去除该参数即可
    title: '提示'
    ,layEvent: 'LAYTABLE_TIPS'
    ,icon: 'layui-icon-tips'
  }]
  ,cols: [[
    {field: 'name', title: '名称', sort: true}
    ,{field: 'namespace', title: '命名空间'}
    ,{field: 'data_length', title: '数据数量'}
    ,{field: 'create_time', title: '创建时间'}
    ,{fixed: 'right', title:'操作', toolbar: '#barDemo',width: 150}
  ]]
  ,page: true
    ,id: 'secrettb'
});
// 标签格式化，是一个对象
function labelsFormat(d){
    result = "";
    if(d.labels == null){
        return "None"
    } else {
        for (let key in d.labels) {
            result += '<span style="border: 1px solid #d6e5ec;border-radius: 8px">' +
                key + ':' + d.labels[key] +
                '</span><br>'
        }
        return result
    }
}
```

### 优化

- 每个k8s资源都有一个时间，默认是UTC，进行格式化中国时区

```
def dt_format(dt):
    current_datetime = dt + timedelta(hours=8)
    dt = date.strftime(current_datetime, '%Y-%m-%d %H:%M:%S')
    return dt
```

## 4、创建资源

## 5、查看和编辑YAML

ACE 是一个开源的、独立的、基于浏览器的代码编辑器，可以嵌入到任何web页面或JavaScript应用程序中。  

https://github.com/ajaxorg/ace

```
yum install epel-release -y
yum install npm git -y
git clone https://github.com/ajaxorg/ace.git
cd ace
npm install
node ./Makefile.dryice.js
```

使用步骤：

1、将ace包放到static目录下

2、准备导出yaml接口

3、准备ace editor编辑器页面（弹出层）

4、ajax调用导出的yaml接口并将yaml内容填充到当前打开的编辑器

小结：

点击YAML按钮 -> layer.open(/ace_editor/?namespace=default&resource=deployment&name=web1) -> 后端（视图） 接收到URL参数并渲染到模板（在线编辑器）中 -> ajax 从导出yaml接口（/export_resource_api/?namespace=default&resource=deployment&name=web1 带资源属性）获取对应资源yaml，动态填充到在线编辑器里面。 

## 6、Node与Deployment详情页

## 7、容器终端与容器日志

### **容器终端**

现在我们就是做这个功能，用于连接容器，但容器不像虚拟机那样经常登录进去维护，容器是一个封装好的应用环境，即开即用，一个容器启动后基本不再对里面的环境做相关操作，即使修改也是重新构建镜像，我们做这个功能主要还是方便故障排查，进入容器里做一些调试工作。

要想实现类似SSH终端功能并非易事，主要难点在于页面与连接的目标是实时交互的。说起实时交互，相信大家都有接触过，例如qq、微信、在线客服这些都是，像一些网页版的在线聊天系统常用的实现方案就是用websocket。

**WebSocket**协议与HTTP的主要区别：HTTP是无状态协议，由客户端发起请求，客户端与服务器“一问一答”，因此服务器端无法主动向客户端发送信息。而WebSocket是基于TCP长连接的协议，客户端与服务器建立连接后，服务器端随时能向客户端发送信息。

WebSocket协议的主要价值在于其与HTTP的差异（服务器端与客户端能够保持实时的双向通信），使其在某些应用情景下比HTTP更能满足技术需求。

Django Web框架实现WebSocket主要有两种方式：channels和dwebsocket。

Channels是针对Django项目的一个增强框架，使得Django不仅支持HTTP协议，还能支持WebSocket协议。

为了更好的模拟shell终端，还需要一个前端库xterm.js ，这是一个比较成熟的shell终端模拟库，目前大部分公司实现的webssh都是用的这个。

官网：https://xtermjs.org/

大概思路就是这样的：
  1、写一个前端页面，里面用xterm.js模拟shell终端，再打开一个websocket，监听用户输入通过 websocket 将用户输入的内容上传到 django
  2、django 接受到用户输入的内容, 将内容通过k8s stream与容器建立通道在容器里执行，将返回的处理结果返回给django。 
  3、django 将 k8s stream返回的结果通过 websocket 返回到终端页面

![](https://k8s-1252881505.cos.ap-beijing.myqcloud.com/web-dev/k8s-stream-websocket.png)

#### 1、前端（模板）

```
<script type="text/html" id="barDemo">
  <a class="layui-btn layui-btn-primary layui-btn-xs" lay-event="yaml">YAML</a>
  <a class="layui-btn layui-btn-xs" lay-event="log">查看日志</a>
  <a class="layui-btn layui-btn-normal layui-btn-xs" lay-event="terminal" style="color: #FFF;background-color: #385985">终端</a>
  <a class="layui-btn layui-btn-danger layui-btn-xs" lay-event="del">重建</a>
</script>
```

```
} else if(obj.event === 'terminal'){
        // 逗号拼接容器名, 例如containers=c1,c2
        cs = data['containers'];
        containers = "";
        for(let c in cs) {
            if (c < cs.length-1) {
                containers += cs[c]['c_name'] + ","
            } else {
                containers += cs[c]['c_name']
            }
        }
        layer.open({
            title: "容器终端",
            type: 2,  // 加载层，从另一个网址引用
            area : [ '50%', '60%' ],
            content: '{% url "terminal" %}?namespace=' + data["namespace"] + "&pod_name=" + data["name"] + "&containers=" + containers,
        });
}
```

#### 2、服务端（视图）

```
re_path('^terminal/$', views.terminal, name="terminal"),
```

```
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
@k8s.self_login_required
def terminal(request):
    namespace = request.GET.get("namespace")
    pod_name = request.GET.get("pod_name")
    containers = request.GET.get("containers").split(',')  # 返回 nginx1,nginx2，转成一个列表方便前端处理
    auth_type = request.session.get('auth_type') # 认证类型和token，用于传递到websocket，websocket根据sessionid获取token，让websocket处理连接k8s认证用
    token = request.session.get('token')
    connect = {'namespace': namespace, 'pod_name': pod_name, 'containers': containers, 'auth_type': auth_type, 'token': token}
    return render(request, 'workload/terminal.html', {'connect': connect})
```

#### 3、前端（终端页面）

容器终端页面：workload/terminal.html

```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>容器终端</title>
    <link href="/static/xterm/xterm.css" rel="stylesheet" type="text/css"/>
    <style>
        body {
            background-color: black
        }
        .terminal-window {
            background-color: #2f4050;
            width: 99%;
            color: white;
            line-height: 25px;
            margin-bottom: 10px;
            font-size: 18px;
            padding: 10px 0 10px 10px
        }
        .containers select,.containers option {
            width: 100px;
            height: 25px;
            font-size: 18px;
            color: #2F4056;
            text-overflow: ellipsis;
            outline: none;
        }
    </style>
</head>

<body>
  <div class="terminal-window">
      <div class="containers">
          Pod名称：{{ connect.pod_name }}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          容器：
          <select name="container_name" id="containerSelect">
          {% for c in connect.containers %}
            <option value="{{ c }}">{{ c }}</option>
          {% endfor %}
          </select>
      </div>
  </div>
  <div id="terminal" style="width: 100px;"></div>
</body>

<script src="/static/xterm/xterm.js"></script>

<script>

    var term = new Terminal({cursorBlink: true,rows:70});
    term.open(document.getElementById('terminal'));

    var auth_type = '{{ connect.auth_type }}';
    var token = '{{ connect.token }}';
    var namespace = '{{ connect.namespace }}';
    var pod_name = '{{ connect.pod_name }}';
    var container = document.getElementById('containerSelect').value;

     // 打开一个 websocket，django也会把sessionid传过去
    var ws = new WebSocket('ws://' + window.location.host + '/workload/terminal/' + namespace + '/' + pod_name + '/' + container + '/?auth_type=' + auth_type + '&token=' + token);

    //打开websocket连接，并打开终端
    ws.onopen = function () {
        // 实时监控输入的字符串发送到后端
        term.on('data', function (data) {
            ws.send(data);
        });

        ws.onerror = function (event) {
          console.log('error:' + e);
        };
        //读取服务器发送的数据并写入web终端
        ws.onmessage = function (event) {
          term.write(event.data);
        };
        // 关闭websocket
        ws.onclose = function (event) {
          term.write('\n\r\x1B[1;3;31m连接关闭！\x1B[0m');
        };
    };

</script>

</html>
```

#### 4、服务端（Django Channels）

```
pip install channels
pip install channels_redis
```

- channels ：是Django的扩展模块，用于处理WebSocket。

- channels_redis ：使用redis作为存储，维护不同消息传递。

**4.1 在settings.py文件中注册channels**

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels'
]
ASGI_APPLICATION = 'devops.routing.application'
```

**4.2 配置路由**

devops/routing.py # 路由文件

```
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import re_path
from devops.consumers import StreamConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            re_path(r'^workload/terminal/(?P<namespace>.*)/(?P<pod_name>.*)/(?P<container>.*)/', StreamConsumer),
        ])
    ),
})
```

正则匹配所有以workload/terminal开头的websocket连接，都交由名为StreamConsumer的处理。

**4.3 WebSocket服务端消费**

devops/consumers.py # 建立K8s Stream容器通道和处理前端与Django Websocket通道

```
from channels.generic.websocket import WebsocketConsumer
from kubernetes.stream import stream
from threading import Thread
from kubernetes import client
from devops import k8s

# 多线程
class K8sStreamThread(Thread):
    def __init__(self, websocket, container_stream):
        Thread.__init__(self)
        self.websocket = websocket
        self.stream = container_stream

    def run(self):
        while self.stream.is_open():
            # 读取标准输出
            if self.stream.peek_stdout():
                stdout = self.stream.read_stdout()
                self.websocket.send(stdout)
            # 读取错误输出
            if self.stream.peek_stderr():
                stderr = self.stream.read_stderr()
                self.websocket.send(stderr)
        else:
            self.websocket.close()

# 继承WebsocketConsumer 类，并修改下面几个方法，主要连接到容器
class StreamConsumer(WebsocketConsumer):

    def connect(self):
        # self.scope 请求头信息
        self.namespace = self.scope["url_route"]["kwargs"]["namespace"]
        self.pod_name = self.scope["url_route"]["kwargs"]["pod_name"]
        self.container = self.scope["url_route"]["kwargs"]["container"]

        k8s_auth = self.scope["query_string"].decode()  # b'auth_type=kubeconfig&token=7402e616e80cc5d9debe66f31b7a8ed6'
        auth_type = k8s_auth.split('&')[0].split('=')[1]
        token = k8s_auth.split('&')[1].split('=')[1]

        k8s.load_auth_config(auth_type, token)
        core_api = client.CoreV1Api()

        exec_command = [
            "/bin/sh",
            "-c",
            'TERM=xterm-256color; export TERM; [ -x /bin/bash ] '
            '&& ([ -x /usr/bin/script ] '
            '&& /usr/bin/script -q -c "/bin/bash" /dev/null || exec /bin/bash) '
            '|| exec /bin/sh']
        try:
            self.conn_stream = stream(core_api.connect_get_namespaced_pod_exec,
                                 name=self.pod_name,
                                 namespace=self.namespace,
                                 command=exec_command,
                                 container=self.container,
                                 stderr=True, stdin=True,
                                 stdout=True, tty=True,
                                 _preload_content=False)
            kube_stream = K8sStreamThread(self, self.conn_stream)
            kube_stream.start()
        except Exception as e:
            print(e)
            status = getattr(e, "status")
            if status == 403:
                msg = "你没有进入容器终端权限！"
            else:
                msg = "连接容器错误，可能是传递的参数有问题！"
            print(msg)

        self.accept()

    def disconnect(self, close_code):
        self.conn_stream.write_stdin('exit\r')

    def receive(self, text_data):
        self.conn_stream.write_stdin(text_data)
```

**4.4 配置Channels存储**

```
docker run --name redis -d -p 6379:6379 redis:3
```

 在settings.py配置文件添加redis配置，内容如下：

```
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('192.168.31.61', 6379)],
        },
    },
}
 
# 也可以不用redis放到内存中，适用于少量终端连接
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}
```

#### 小结

终端->弹出框（从另一个加载/workload/terminal/?namespace=default&pod_name=web-7989784f96-wxbnm&containers=nginx）->执行页面里websocket建立连接（/workload/terminal/default/web-7989784f96-wxbnm/nginx/）->routing.py路由到StreamConsumer处理（K8s Stream与容器建立通道）

### **容器实时日志**

#### 1、路由

```
# workload/urls.py 
re_path('^pod_log/$', views.pod_log, name="pod_log"),
```

#### 2、服务端（视图）

```
# workload/views.py
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
@k8s.self_login_required
def pod_log(request):
    namespace = request.GET.get("namespace")
    pod_name = request.GET.get("pod_name")
    containers = request.GET.get("containers").split(',')   # 返回 nginx1,nginx2，转成一个列表方便前端处理
    auth_type = request.session.get('auth_type') # 认证类型和token，用于传递到websocket，websocket根据sessionid获取token，让websocket处理连接k8s认证用
    token = request.session.get('token')
    connect = {'namespace': namespace, 'pod_name': pod_name, 'containers': containers, 'auth_type': auth_type, 'token': token}
    return render(request, 'workload/pod_log.html', {'connect': connect})
```

#### 3、前端（模板）

```
# templates/workload/pod_log.html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>容器日志</title>
    <script src="/static/layui/layui.js"></script>
    <style>
        body {
            background-color: black
        }
        .terminal-window {
            background-color: #2f4050;
            width: 99%;
            color: white;
            line-height: 25px;
            margin-bottom: 10px;
            font-size: 18px;
            padding: 10px 0 10px 10px;
        }
        .containers select,.containers option {
            width: 100px;
            height: 25px;
            font-size: 18px;
            color: #2F4056;
            text-overflow: ellipsis;
            outline: none;
        }
        #logs pre {
            color: #eeeeee;
        }
    </style>
</head>

<body>
  <div class="terminal-window" id="lll">
      <div class="containers">
          Pod名称：{{ connect.pod_name }}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          容器：
          <select name="container_name" id="containerSelect">
          {% for c in connect.containers %}
            <option value="{{ c }}">{{ c }}</option>
          {% endfor %}
          </select>
      </div>
  </div>
  <div id="logs">
     <pre></pre>
  </div>
</body>


<script>
layui.use('layer', function(){
  var $ = layui.jquery;

    var auth_type = '{{ connect.auth_type }}';
    var token = '{{ connect.token }}';
    var namespace = '{{ connect.namespace }}';
    var pod_name = '{{ connect.pod_name }}';
    var container = document.getElementById('containerSelect').value;

     // 打开一个 websocket，django也会把sessionid传过去
    var ws = new WebSocket('ws://' + window.location.host + '/workload/pod_log/' + namespace + '/' + pod_name + '/' + container + '/?auth_type=' + auth_type + '&token=' + token);

    //打开websocket连接，并打开终端
    ws.onopen = function () {
        // 建立WS异常
        ws.onerror = function (event) {
          console.log('error:' + e);
        };
        //读取服务器发送的数据并写入web终端
        ws.onmessage = function (event) {
            $("#logs pre").append(event.data);
        };
    };
});
</script>

</html>
```

#### 4、点击日志按钮，与终端一样

```
} else if(obj.event === 'log'){
    // 逗号拼接容器名, 例如containers=c1,c2
    cs = data['containers'];
    containers = "";
    for(let c in cs) {
        if (c < cs.length-1) {
            containers += cs[c]['c_name'] + ","
        } else {
            containers += cs[c]['c_name']
        }
    }
    layer.open({
        title: "容器日志",
        type: 2,
        area : [ '60%', '70%' ],
        content: '{% url 'pod_log' %}?namespace=' + data.namespace + '&pod_name=' + data.name + '&containers=' + containers
    });
```

#### 5、添加Websocket路由

```
# devops/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import re_path
from devops.consumers import StreamConsumer
from devops.logs_consumers import StreamLogConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            re_path(r'^workload/terminal/(?P<namespace>.*)/(?P<pod_name>.*)/(?P<container>.*)/', StreamConsumer),
            re_path(r'^workload/pod_log/(?P<namespace>.*)/(?P<pod_name>.*)/(?P<container>.*)/', StreamLogConsumer),
        ])
    ),
})
```

 #### 6、处理Websocket消费者

新建文件，与之前consumers.py同级。

```
# devops/logs_consumers.py
from channels.generic.websocket import WebsocketConsumer
from threading import Thread
from kubernetes import client
from devops import k8s

# 多线程
class K8sStreamThread(Thread):
    def __init__(self, websocket, conn_stream):
        Thread.__init__(self)
        self.websocket = websocket
        self.stream = conn_stream

    def run(self):
        for line in self.stream:
            # 读取流的输出，发送到websocket（前端）
            self.websocket.send(line.decode())
        else:
            self.websocket.close()

# 继承WebsocketConsumer 类，并修改下面几个方法，主要连接到容器
class StreamLogConsumer(WebsocketConsumer):
    def connect(self):
        # self.scope 请求头信息
        self.namespace = self.scope["url_route"]["kwargs"]["namespace"]
        self.pod_name = self.scope["url_route"]["kwargs"]["pod_name"]
        self.container = self.scope["url_route"]["kwargs"]["container"]

        k8s_auth = self.scope["query_string"].decode()  # b'auth_type=kubeconfig&token=7402e616e80cc5d9debe66f31b7a8ed6'
        auth_type = k8s_auth.split('&')[0].split('=')[1]
        token = k8s_auth.split('&')[1].split('=')[1]

        k8s.load_auth_config(auth_type, token)
        core_api = client.CoreV1Api()

        try:
            self.conn_stream = core_api.read_namespaced_pod_log(name=self.pod_name,
                                                                namespace=self.namespace,
                                                                follow = True,
                                                                _preload_content=False
                                                                ).stream()
            kube_stream = K8sStreamThread(self, self.conn_stream)
            kube_stream.start()
        except Exception as e:
            status = getattr(e, "status")
            if status == 403:
                msg = "没有访问容器日志权限！"
            else:
                msg = "访问容器异常！"
        self.accept()
```

至此完成。整体与容器终端思路一样。

## 8、仪表盘

