
from kubernetes import client, config
import os
# print(os.getcwd())
# kubeconfig = os.path.join(os.getcwd(), "kubeconfig.yaml")
# config.load_kube_config(kubeconfig)
# apps_api = client.AppsV1Api() # 资源接口类实例化

configuration = client.Configuration()
configuration.host = "https://192.168.31.71:6443"  # APISERVER地址
ca_file = os.path.join(os.getcwd(),"ca.crt") # K8s集群CA证书（/etc/kubernetes/pki/ca.crt）
configuration.ssl_ca_cert= ca_file
configuration.verify_ssl = True   # 启用证书验证
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Im02NEUxRVNPaEY2VC1hYV9Jekc5dlVrQzJ5b0RIVC14UUE2Q2FweGMyeE0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tdG9rZW4tbXp3cXciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiNDI4MmQxYWQtNzM0ZC00NmM3LTk3ODgtNDJlZTM1ZGFiZWJhIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmRhc2hib2FyZC1hZG1pbiJ9.RXdmQsJH0zDLIoDsAqSu-Cm7hnndp8I3x_psemZbI0c9UULRpVCjIqSyyr3GD4rJeyR8EGEz4gE5zW0TUtJtL8numGSfOw8-am8YPIpPfKRNOwFkBFS4WaWkmXjtTXd2XNm9UKzypzU48XUu7_RJiH4zIqr7Y75OmHMOfKfiBcVyeCA2Lyl5A5kAIjcOQcvtGPFmbllYT0b3uENBOTywrEeopIqqHLjqqHSFGzOK48om9I0I7sxDTsuswXNvd0Wp6Nw3EWRM-uBxzxhgf6w6D1CDF9uM-0my1Huex2lfF5M11DXE9Ro6MaoSRbegOxVyFEWmWzXq-ZEuFwenBxhkjQ"  # 指定Token字符串，下面方式获取
configuration.api_key = {"authorization": "Bearer " + token}
client.Configuration.set_default(configuration)
apps_api = client.AppsV1Api()
core_api = client.CoreV1Api()

# for dp in apps_api.list_deployment_for_all_namespaces().items:
#     # print(dp) # 打印的deployment详细信息
#     print(dp.metadata.name)
#     print(dp.metadata.namespace)
#     print(dp.spec.replicas)

for i in core_api.list_node_with_http_info()[0].items:  # [{},{},{}]
    print(i.status.allocatable)
    print(i.metadata.name)
    break

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
# try:
#     apps_api.create_namespaced_deployment(namespace=namespace, body=body)
# except Exception as e:
#     status = getattr(e, "status")
#     if status == 409:
#         print("该Deployment资源已经创建")
#
# core_api = client.CoreV1Api()
# namespace = "default"
# name = "api-test"
# selector = {'a':'1', 'b':'2'}  # 不区分数据类型，都要加引号
# port = 80
# target_port = 80
# type = "NodePort"
# body = client.V1Service(
#     api_version="v1",
#     kind="Service",
#     metadata=client.V1ObjectMeta(
#         name=name
#     ),
#     spec=client.V1ServiceSpec(
#         selector=selector,
#         ports=[client.V1ServicePort(
#             port=port,
#             target_port=target_port
#         )],
#         type=type
#     )
# )
# try:
#     core_api.create_namespaced_service(namespace=namespace, body=body)
# except Exception as e:
#     status = getattr(e, "status")
#     if status == 409:
#         print("该Service资源已经创建")
#     elif status == 400:  # 400 格式错误，409 资源存在，403 没权限。
#         print("格式错误")
#     elif status == 403:
#         print("没权限")