#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "building docker image..."
sudo docker build -t custom-app:latest "$SCRIPT_DIR/app"
minikube image load custom-app:latest

echo "applying manifests..."
kubectl apply -f "$SCRIPT_DIR/k8s/01-configmap.yaml"

kubectl apply -f "$SCRIPT_DIR/k8s/02-pod.yaml"
kubectl wait --for=condition=Ready pod/custom-app-pod --timeout=120s
echo "test pod ok, removing..."
kubectl delete pod custom-app-pod --wait=false

kubectl apply -f "$SCRIPT_DIR/k8s/03-deployment.yaml"
kubectl rollout status deployment/custom-app --timeout=180s

kubectl apply -f "$SCRIPT_DIR/k8s/04-service.yaml"
kubectl apply -f "$SCRIPT_DIR/k8s/05-daemonset.yaml"
kubectl apply -f "$SCRIPT_DIR/k8s/07-statefulset.yaml"
kubectl apply -f "$SCRIPT_DIR/k8s/06-cronjob.yaml"

echo ""
echo "done, checking:"
kubectl get all
