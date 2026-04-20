# Практикум по промышленной разработке ПО, дз2

flask приложение в кубере с логированием + istio service mesh

## что тут лежит

app/ - само приложение на питоне + докерфайл
k8s/ - манифесты для кубера
k8s/istio/ - gateway, virtualservice, destinationrule
deploy.sh - запускает все включая istio

## запуск

нужен docker, kubectl, minikube

```
minikube start --driver=docker
./deploy.sh
```

## как проверить

узнаем ip ingress gateway:
```
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
export INGRESS_HOST=$(minikube ip)
export GATEWAY_URL=$INGRESS_HOST:$INGRESS_PORT
```

проверяем эндпоинты:
```
curl http://$GATEWAY_URL/
curl http://$GATEWAY_URL/status
curl -X POST http://$GATEWAY_URL/log -H "Content-Type: application/json" -d '{"message":"test"}'
curl http://$GATEWAY_URL/logs
```

404 на неизвестный маршрут:
```
curl http://$GATEWAY_URL/wrong
```

таймаут на POST /log (задержка 2с > таймаут 1с):
```
curl -v -X POST http://$GATEWAY_URL/log -H "Content-Type: application/json" -d '{"message":"timeout test"}'
```

istio ресурсы:
```
kubectl get gateway,virtualservice,destinationrule
```

все ресурсы:
```
kubectl get all
```