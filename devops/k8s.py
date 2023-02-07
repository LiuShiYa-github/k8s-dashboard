from kubernetes import client, config
from django.shortcuts import redirect
from dashboard.models import User
import yaml

apiserver = "https://192.168.31.71:6443"

# 连接k8s验证输入的token或者kubeconfig是否有效
def auth_check(auth_type, token=None):
    if auth_type == "token":
        configuration = client.Configuration()
        configuration.host = apiserver  # APISERVER地址
        # ca_file = os.path.join(os.getcwd(), "ca.crt")  # K8s集群CA证书（/etc/kubernetes/pki/ca.crt）
        # configuration.ssl_ca_cert = ca_file
        configuration.verify_ssl = False  # 关闭证书验证
        configuration.api_key = {"authorization": "Bearer " + token}
        client.Configuration.set_default(configuration)
        try:
            core_api = client.CoreApi()
            core_api.get_api_versions() # 查看k8s版本，由此验证是否有效的
            return True
        except Exception as e:
            print(e)
            return False
    elif auth_type == "kubeconfig":
        user = User.objects.get(token=token)
        content = user.content
        yaml_content = yaml.load(content, Loader=yaml.FullLoader) # 将yaml文件转为json
        try:
            config.load_kube_config_from_dict(yaml_content)
            core_api = client.CoreApi()
            core_api.get_api_versions()  # 查看k8s版本，由此验证是否有效的
            return True
        except Exception as e:
            print(e)
            return False

# 视图登录认证装饰器
def self_login_required(func):
    def inner(request):
        is_login = request.session.get('is_login', False)
        if is_login:
            return func(request)
        else:
            return redirect('/login')
    return inner

# 加载连接k8s api的认证配置
def load_auth_config(auth_type, token):
    if auth_type == "token":
        configuration = client.Configuration()
        configuration.host = apiserver  # APISERVER地址
        # ca_file = os.path.join(os.getcwd(), "ca.crt")  # K8s集群CA证书（/etc/kubernetes/pki/ca.crt）
        # configuration.ssl_ca_cert = ca_file
        configuration.verify_ssl = False  # 关闭证书验证
        configuration.api_key = {"authorization": "Bearer " + token}
        client.Configuration.set_default(configuration)
    elif auth_type == "kubeconfig":
        user = User.objects.get(token=token)
        content = user.content
        yaml_content = yaml.load(content, Loader=yaml.FullLoader) # 将yaml文件转为json
        config.load_kube_config_from_dict(yaml_content)

# 资源创建时间格式化
from datetime import date, timedelta
def timestamp_format(timestamp):
    c = timestamp + timedelta(hours=8)
    t = date.strftime(c, '%Y-%m-%d %H:%M:%S')
    return t