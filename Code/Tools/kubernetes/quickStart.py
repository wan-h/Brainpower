# coding: utf-8
# Author: wanhui0729@gmail.com

# apis
# https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md
# examples
# https://github.com/kubernetes-client/python/tree/master/examples

import os
import yaml
from kubernetes import client, config, watch

# 默认'~/.kube/config'
config.load_kube_config()

# list all pods
def list_all_pods():
    print("Listening pods with their IPs:")
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

# watch on namespace object
# watch会一直阻塞直到终止条件
def watch_on_namespace_object():
    count = 6
    w = watch.Watch()
    v1 = client.CoreV1Api()
    for event in w.stream(v1.list_namespace, _request_timeout=60):
        print("Event: %s %s" % (event['type'], event['object'].metadata.name))
        count -= 1
        if not count:
            w.stop()
    print("Ended.")

# `kubectl api-versions`
# 以"组/版本"的格式输出服务端支持的API版本
def api_discovery():
    print("Supported APIs (* is preferred version):")
    print("%-40s %s" % ("core", ",".join(client.CoreApi().get_api_versions().versions)))
    for api in client.ApisApi().get_api_versions().groups:
        versions = []
        for v in api.versions:
            name = ""
            if v.version == api.preferred_version.version and len(api.versions) > 1:
                name += "*"
            name += v.version
            versions.append(name)
        print("%-40s %s" % (api.name, ",".join(versions)))

# create deployment
def deployment_create():
    with open(os.path.join(os.path.dirname(__file__), "nginx-deployment.yaml")) as f:
        dep = yaml.safe_load(f)
        k8s_app_v1 = client.AppsV1Api()
        resp = k8s_app_v1.create_namespaced_deployment(
            body=dep,
            namespace='default'
        )
        # 记得去删除
        print("Deployment created. status='%s'" % resp.metadata.name)


if __name__ == '__main__':
    # list_all_pods()
    # watch_on_namespace_object()
    # api_discovery()
    deployment_create()