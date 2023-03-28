from kubernetes import client, config
import os

kubeconfig = os.path.join(os.getcwd(), "kubeconfig.yaml")  # 获取当前目录并拼接文件
config.load_kube_config(kubeconfig)  # 指定kubeconfig配置文件（/root/.kube/config）
apps_api = client.AppsV1Api()  # 资源接口类实例化

for dp in apps_api.list_deployment_for_all_namespaces().items:
    # print(dp.metadata.name)  # 打印Deployment对象详细信息
    # print(dp.metadata.namespace)  # 打印Deployment对象详细信息
    print(dp.spec.replicas)  # 打印Deployment对象详细信息

# namespace = "default"
# name = "api-test"
# replicas = 3
# labels = {'a':'1', 'b':'2'}  # 不区分数据类型，都要加引号
# image = "nginx"
# body = client.V1Deployment(
#             api_version="apps/v1",
#             kind="Deployment",
#             metadata=client.V1ObjectMeta(name=name),
#             spec=client.V1DeploymentSpec(
#                 replicas=replicas,
#                 selector={'matchLabels': labels},
#                 template=client.V1PodTemplateSpec(
#                     metadata=client.V1ObjectMeta(labels=labels),
#                     spec=client.V1PodSpec(
#                         containers=[client.V1Container(
#                             name="web",
#                             image=image
#                         )]
#                     )
#                 ),
#             )
#         )
#
# apps_api.create_namespaced_deployment(namespace=namespace, body=body)


core_api = client.CoreV1Api()
namespace = "default"
name = "api-test"
selector = {'a': '1', 'b': '2'}  # 不区分数据类型，都要加引号
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
