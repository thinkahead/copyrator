k8s-python-operator-example
---------------------------
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

#### Debugging
Get the cacert, cert and key from $KUBECONFIG. Then build and push the image and update the image in helm/templates/operator.py
```
echo certificate-authority-data | base64 -d > cacert
echo client-certificate-data | base64 -d > cert
echo client-key-data | base64 -d > key

podman build -t docker.io/karve/copyrator2 -f Dockerfile .
podman push docker.io/karve/copyrator2:latest

helm install copyrator helm;oc apply -f main-rule.yaml
oc apply -f test.yaml
oc get cm -A --no-headers | grep example-configmap3 | awk '{print $1}' | xargs -n 1 oc delete cm example-configmap3 -n
helm delete copyrator
```
