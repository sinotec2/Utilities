---
layout: default
title: zero to JupyterHub
nav_order: 99
parent: 地端JupyterHub伺服器
grand_parent: Web Jokers
last_modified_date: 2024-09-16 14:30:21
tags: operation_systems
---

# zero to JupyterHub

## Table of contents

{: .no_toc .text-delta }

1. TOC
{:toc}

---

- [Zero to JupyterHub with Kubernetes](https://z2jh.jupyter.org/en/stable/kubernetes/minikube/step-zero-minikube.html)

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
sudo dpkg -i minikube_latest_amd64.deb
minikube start
# kubectl installation
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
kubectl get po -A
NAMESPACE     NAME                               READY   STATUS    RESTARTS        AGE
kube-system   coredns-6f6b679f8f-kl7zc           1/1     Running   0               7m52s
kube-system   etcd-minikube                      1/1     Running   0               7m57s
kube-system   kube-apiserver-minikube            1/1     Running   0               7m57s
kube-system   kube-controller-manager-minikube   1/1     Running   0               7m58s
kube-system   kube-proxy-rwxlw                   1/1     Running   0               7m52s
kube-system   kube-scheduler-minikube            1/1     Running   0               7m57s
kube-system   storage-provisioner                1/1     Running   1 (7m21s ago)   7m56s
```

### minikube start

```bash
minikube start --kubernetes-version stable --nodes 2 --cpus 2 --memory 2000 --cni calico
```

kubectl get node
kubectl get nodes -o wide

### Post-installation checklist

helm upgrade --cleanup-on-fail   --install "release-1" jupyterhub/jupyterhub   --namespace "minikube"   --create-namespace   --version=3.3.8   --values ~/MyPrograms/helm/config.yaml

  - Verify that created Pods enter a Running state:

    ```bash
      kubectl --namespace=minikube-m02 get pod
    ```

    If a pod is stuck with a Pending or ContainerCreating status, diagnose with:

      kubectl --namespace=minikube-m02 describe pod <name of pod>

    If a pod keeps restarting, diagnose with:

      kubectl --namespace=minikube-m02 logs --previous <name of pod>

  - Verify an external IP is provided for the k8s Service proxy-public.

      kubectl --namespace=minikube-m02 get service proxy-public

    If the external ip remains <pending>, diagnose with:

      kubectl --namespace=minikube-m02 describe service proxy-public

  - Verify web based access:

    You have not configured a k8s Ingress resource so you need to access the k8s
    Service proxy-public directly.

    If your computer is outside the k8s cluster, you can port-forward traffic to
    the k8s Service proxy-public with kubectl to access it from your
    computer.

      kubectl --namespace=minikube-m02 port-forward service/proxy-public 8080:http

    Try insecure HTTP access: http://localhost:8080
(base)

```bash
kubectl --namespace=minikube port-forward service/proxy-public 8080:http --address=172.20.31.1
```

```bash
helm upgrade --cleanup-on-fail "release-1"  \
   jupyterhub/jupyterhub \
  --namespace "minikube-m02"  \
  --version=3.3.8\
  --values config.yaml
```

```bash
#轉換工作目錄
cd ../binder

#開啟新的命名空間
kubectl create namespace sesbind

#開啟新的helm圖像
helm install sesbind jupyterhub/binderhub --version=1.0.0-0.dev.git.3506.hba24eb2a --namespace=sesbind -f secret.yaml -f config.yaml

#暴露IP及端口
export NODE_PORT=$(kubectl get --namespace sesbind -o jsonpath="{.spec.ports[0].nodePort}" services binder)
export NODE_IP=$(kubectl get nodes --namespace sesbind -o jsonpath="{.items[0].status.addresses[0].address}")

kubectl --namespace=sesbind port-forward service/proxy-public 8081:http --address=172.20.31.1




 1823  curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
 1824  sudo dpkg -i minikube_latest_amd64.deb
 1843  kubectl logs hub-f5df4d48d-vgb7z --namespace=minikube-m02
 1847  kubectl logs hub-f5df4d48d-vgb7z --namespace=minikube-m02 |tail
 1864  kubectl logs hub-85c8888b5f-gbtff --namespace=minikube-m02|T
 1865  kubectl logs hub-85c8888b5f-gbtff --namespace=minikube-m02|more
 1870  kubectl --namespace minikube-m02 get service proxy-public
 1871  kubectl --namespace minikube get service proxy-public
 1873  helm upgrade --cleanup-on-fail "release-1"     jupyterhub/jupyterhub   --namespace "minikube-m02"    --version=3.3.8  --values config.yaml
 1876  NAMESPACE=minikube-m02
 1888  helm upgrade --cleanup-on-fail "release-1"     jupyterhub/jupyterhub   --namespace "minikube-m02"    --version=3.3.8  --values config.yaml
 1889  kubectl --namespace=minikube-m02 get pod
 1907  helm upgrade --cleanup-on-fail "release-1"     jupyterhub/jupyterhub   --namespace "minikube-m02"    --version=3.3.8  --values config.yaml
 1908  kubectl --namespace=minikube-m02 get pod
 1918  helm upgrade --cleanup-on-fail "release-1"     jupyterhub/jupyterhub   --namespace "minikube-m02"    --version=3.3.8  --values config.yaml
 1919  kubectl --namespace=minikube-m02 get pod
 1923  kubectl logs hub-f5df4d48d-vgb7z --namespace=minikube-m02
 1925  kubectl logs $i --namespace=minikube-m02
 1928  helm upgrade --cleanup-on-fail "release-1"     jupyterhub/jupyterhub   --namespace "minikube-m02"    --version=3.3.8  --values config.yaml
 1929  kubectl --namespace=minikube-m02 get pod
 1931  kubectl logs $i --namespace=minikube-m02
 1933  helm upgrade --cleanup-on-fail "release-1"     jupyterhub/jupyterhub   --namespace "minikube-m02"    --version=3.3.8  --values config.yaml
 1934  kubectl --namespace=minikube-m02 get pod
 1936  kubectl logs $i --namespace=minikube-m02
 1943  helm upgrade --cleanup-on-fail "release-1"     jupyterhub/jupyterhub   --namespace "minikube-m02"    --version=3.3.8  --values config.yaml
 1944  kubectl --namespace=minikube-m02 get pod
 1946  kubectl logs $i --namespace=minikube-m02
 2154  minikube service binder
 2155  minikube service list
 2164  minikube service list
 2211  kubectl --namespace minikube get service proxy-public
 2217  kubectl get svc --namespace minikube
 2219  minikube stop
 2234  minikube start
 2245  minikube start
 2250  minikube stop
 2251  minikube status
 2350  helm upgrade --cleanup-on-fail   --install "release-1" jupyterhub/jupyterhub   --namespace "minikube"   --create-namespace   --version=3.3.8   --values config.yaml
 2351  helm upgrade --cleanup-on-fail   --install "release-1" jupyterhub/jupyterhub   --namespace "minikube"   --version=3.3.8   --values config.yaml
 2352  kubectl --namespace=minikube port-forward service/proxy-public 8080:http
 2353  kubectl --namespace=minikube get service hub-798bdf7f49-btpxb
 2355  kubectl --namespace=minikube describe pod hub-798bdf7f49-btpxb
 2356  kubectl --namespace=minikube port-forward service/proxy-public 8080:http --address=172.20.31.1
 2357  kubectl --namespace=minikube-m02 describe service proxy-public
 2358  kubectl --namespace=minikube describe service proxy-public
 2359  kubectl --namespace=minikube describe
 2360  kubectl --namespace=minikube
--More--
