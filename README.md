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
Create a configmap "example-configmap1" in default namespace, "example-configmap2" in default2 namespace, and "example-configmap3" in default3 namespace for testing
```
oc create namespace default2
oc create namespace default3
oc apply -f test.yaml
oc apply -f test2.yaml
oc apply -f test3.yaml
```
The main-rule.yaml has namespace: ["default","default2"]. So only the configmaps in default and default2 namewspace will get propogateed to all other active namespaces. Thus the example-configmap1 from test.yaml in default namespace and example-configmap2 from test2.yaml in default2 namespace propogate to other namespaces. The example-configmap3 from test3.yaml in default3 namespace does not propogate to other namespaces.


Update the configmap and see that it changes
```
oc edit cm example-configmap1 -n default # Modify it
oc get cm example-configmap1 -o yaml -n default
oc get cm example-configmap1 -o yaml -n default2 # See that this is also modified
```

We can cleanup the configmaps
```
oc get cm -A --no-headers | grep example-configmap1 | awk '{print $1}' | xargs -r -n 1 oc delete cm example-configmap1 -n
oc get cm -A --no-headers | grep example-configmap2 | awk '{print $1}' | xargs -r -n 1 oc delete cm example-configmap2 -n
oc get cm -A --no-headers | grep example-configmap3 | awk '{print $1}' | xargs -r -n 1 oc delete cm example-configmap3 -n
```

#### Debugging the Operator pod
```
oc exec -it deployment/copyrator -- sh
cat /usr/local/lib/python3.8/site-packages/kubernetes/config/incluster_config.py
```

#### Deleting the Operator
```
helm delete copyrator
```
