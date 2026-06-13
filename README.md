# 🚀 Term Project: Scalable & Resilient Microservices with MicroK8s

## 📌 Overview
This is a simple project showing how a basic microservices setup can run locally using MicroK8s.

It includes:
- A small stateless FastAPI app
- A local container registry
- Auto scaling (HPA)
- Self-healing pods
- Ingress load balancing

Everything is kept lightweight so it can run on lower-end hardware without issues.

---

## ⚡ Quick Start

```bash
git clone https://github.com/itsYali/microk8s-cloud-project
cd microk8s-cloud-project

docker build -t localhost:32000/stateless-app:v1 .
docker push localhost:32000/stateless-app:v1

kubectl apply -f k8s/
```

Check if everything is running:

```bash
kubectl get deployments,pods,services,ingress,hpa
```

---

## ⚙️ Requirements
- MicroK8s
- Docker (or Podman)
- Linux system

---

## 🛠 Setup

### Install MicroK8s
```bash
sudo snap install microk8s --classic
sudo usermod -a -G microk8s $USER
mkdir -p ~/.kube
chmod 0700 ~/.kube
```

Log out and back in after running this.


### Enable add-ons
```bash
microk8s enable dns registry ingress metrics-server
```


### Optional alias
```bash
alias kubectl='microk8s kubectl'
```


## 📁 Project Structure
```
k8s/
  deployment.yaml
  ingress.yaml
  hpa.yaml

app.py
Dockerfile
README.md
```


## 🧠 Resource Limits
Set in `k8s/deployment.yaml`:

| Resource | Request | Limit |
|--------|--------|-------|
| CPU | 100m | 250m |
| Memory | 64Mi | 128Mi |

This helps prevent crashes if the machine is limited.


## 🚀 Deployment

### Build image
```bash
docker build -t localhost:32000/stateless-app:v1 .
```

### Push image
```bash
docker push localhost:32000/stateless-app:v1
```


### Apply configs
```bash
kubectl apply -f k8s/
```


### Check status
```bash
kubectl get deployments,pods,services,ingress,hpa
```


## ✅ Testing

### Registry check
```bash
curl http://localhost:32000/v2/_catalog
kubectl get deployment stateless-app-deployment -o yaml | grep image
```


### Load balancing test
```bash
while true; do
  curl -s http://localhost/ | grep -E "pod_name|pod_ip"
  sleep 0.5
done
```

You should see different pods responding over time.


### Self-healing test
```bash
kubectl get pods
kubectl delete pod <POD_NAME>
kubectl get pods -w
```

The deleted pod should get recreated automatically.


### Auto scaling test

Manual:
```bash
kubectl scale deployment stateless-app-deployment --replicas=5
```

Load-based:
```bash
kubectl run -i --tty load-generator --rm   --image=busybox:latest --restart=Never   -- /bin/sh -c "while true; do wget -q -O- http://stateless-app-service; done"
```

Monitor:
```bash
kubectl get hpa -w
```

Pods should scale up when load increases.

## 🏁 Conclusion
This project is just a small demo, but it shows how scaling, load balancing, and self-healing work together in Kubernetes.
