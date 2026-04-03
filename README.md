# Практикум по промышленной разработке ПО, дз1

разворачиваем flask приложение в кубере с логированием

## что тут лежит

app/ - само приложение на питоне + докерфайл
k8s/ - ямлики для кубера
deploy.sh - запускает все

## запуск

нужен docker, kubectl, minikube

```
minikube start --driver=docker
./deploy.sh
```

## как проверить

```
kubectl port-forward svc/custom-app-service 8080:80 &
curl http://localhost:8080/
curl http://localhost:8080/status
curl -X POST http://localhost:8080/log -H "Content-Type: application/json" -d '{"message":"test"}'
curl http://localhost:8080/logs
```

проверяем что запросы идут на разные поды:
```
for i in 1 2 3 4 5; do curl -s http://localhost:8080/status; echo; done
kubectl get pods -l app=custom-app
```

логи агента:
```
kubectl logs -l app=log-agent --tail=10
```

проверяем cronjob:
```
kubectl get cronjob
kubectl get jobs
```

проверяем statefulset:
```
kubectl get statefulset
kubectl logs log-storage-0 --tail=5
```

все поды разом:
```
kubectl get all
```