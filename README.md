k8s-python-operator-example
---------------------------
Original code at https://github.com/flant/examples/tree/master/2019/08-k8s-python-operator

Kubernetes operator written in Python.

* «[Writing a Kubernetes Operator in Python without frameworks and SDK](https://blog.flant.com/writing-a-kubernetes-operator-in-python-without-frameworks-and-sdk/)».
* Russian version: «[Kubernetes Operator на Python без фреймворков и SDK](https://habr.com/ru/company/flant/blog/459320/)».


#### Launching the operator
```bash
usage: copyrator [-h] [--namespace NAMESPACE] [--rule-name RULE_NAME]

Copyrator - copy operator.

optional arguments:
  -h, --help            show this help message and exit
  --namespace NAMESPACE
                        Operator Namespace (or ${NAMESPACE}), default: default
  --rule-name RULE_NAME
                        CRD Name (or ${RULE_NAME}), default: main-rule
``` 

#### Setting up with serviceaccount and token
Update the image: docker.io/karve/copyrator:latest in helm/templates/operator.yaml
```
podman build -t docker.io/karve/copyrator -f Dockerfile-token .
podman push docker.io/karve/copyrator:latest
```
The uses the KUBERNETES_PORT and KUBERNETES_SERVICE_PORT in the pod
```
KUBERNETES_PORT=tcp://10.43.0.1:443
KUBERNETES_SERVICE_PORT=443
```

#### Setting up with cacert, cert and key
Get the cacert, cert and key from $KUBECONFIG. Then build and push the image and update the image: docker.io/karve/copyrator2:latest in helm/templates/operator.yaml
```
cat $KUBECONFIG | grep certificate-authority-data: | sed "s/.*certificate-authority-data: //" | base64 -d > cacert
cat $KUBECONFIG | grep client-certificate-data: | sed "s/.*client-certificate-data: //" | base64 -d > cert
cat $KUBECONFIG | grep client-key-data: | sed "s/.*client-key-data: //" | base64 -d > key
podman build -t docker.io/karve/copyrator2 -f Dockerfile .
podman push docker.io/karve/copyrator2:latest
```

#### Running the Operator
```
helm install copyrator helm;oc apply -f main-rule.yaml
```

### Debugging the Operator
```
oc apply -f test.yaml
oc get cm -A --no-headers | grep example-configmap3 | awk '{print $1}' | xargs -r -n 1 oc delete cm example-configmap3 -n
```

#### Debugging the Operator pod
```
oc exec -it deployment/copyrator -- sh
```

#### Deleting the Operator
```
helm delete copyrator
```
