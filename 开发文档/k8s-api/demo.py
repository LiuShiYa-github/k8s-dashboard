#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@FileName: demo.py.py
@Time    : 2023/2/3 10:17
@Author  : 热气球
@Software: PyCharm
@Version : 1.0
@Contact : 2573514647@qq.com
@Des     : 
"""
from kubernetes import client, config
import os

kubeconfig = os.path.join(os.getcwd(), "kubeconfig.yaml")  # 获取当前目录并拼接文件
config.load_kube_config(kubeconfig)  # 指定kubeconfig配置文件（/root/.kube/config）
apps_api = client.AppsV1Api()  # 资源接口类实例化

for dp in apps_api.list_deployment_for_all_namespaces().items:
    print(dp)  # 打印Deployment对象详细信息
