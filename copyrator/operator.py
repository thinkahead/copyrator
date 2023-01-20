from functools import partial
from operator import methodcaller

import kubernetes

from copyrator.const import ALLOWED_EVENT_TYPES, CREATE_TYPES_MAP, \
    LIST_TYPES_MAP, PATCH_TYPES_MAP, REPLACE_TYPES_MAP

__all__ = [
    'handle',
]

def handle_event(v1, specs, event):
    """
    The method for processing one Kubernetes event.
    """
    print('event type',event['type'])
    if event['type'] not in ALLOWED_EVENT_TYPES:
        return

    object_ = event['object']
    labels = object_['metadata'].get('labels', {})
    print("specs[selector]=",specs['selector'])
    print("handle_event=",event['type'],object_['metadata']['name'],labels)

    #if len(specs['selector'].items())==0: return
    # Look for the matches using selector
    for key, value in specs['selector'].items():
        print("   Checking",labels,key,value)
        if labels.get(key) != value:
            print("   Returning",key,value,"not found")
            return
    print("Found",key,value)
    # Get active namespaces
    namespaces = map(
        lambda x: x.metadata.name,
        filter(
            lambda x: x.status.phase == 'Active',
            v1.list_namespace().items
        )
    )
    print("Copying to","active namespaces")
    #print("Copying to",len(list(namespaces)),"active namespaces")
    for namespace in namespaces:
        print('target namespace',namespace,object_['metadata']['name'],object_['metadata'].get('labels',{}))
        # Clear the metadata, set the namespace
        object_['metadata'] = {
            'labels': object_['metadata'].get('labels',{}),
            'namespace': namespace,
            'name': object_['metadata']['name'],
        }
        # Call the method for creating/updating an object
        try:
            methodcaller(REPLACE_TYPES_MAP[specs['ruleType']], object_['metadata']['name'], namespace, object_)(v1)
            print("replaced")
            #methodcaller(PATCH_TYPES_MAP[specs['ruleType']], object_['metadata']['name'], namespace, object_)(v1)
            #print("patched")
        except kubernetes.client.rest.ApiException as e:
            print("ignoring error in patch",str(e))
            try:
                methodcaller(CREATE_TYPES_MAP[specs['ruleType']], namespace, object_)(v1)
                print("created")
            except kubernetes.client.rest.ApiException as e:
                print("ignoring error in create",str(e))


def handle(specs):
    """
    The main method to initiate events processing via operator.
    """
    kubernetes.config.load_incluster_config()
    v1 = kubernetes.client.CoreV1Api()

    # Get the method to watch the objects
    print('ruleType',specs['ruleType'],'selector',specs['selector'])
    method = getattr(v1, LIST_TYPES_MAP[specs['ruleType']])
    func = partial(method, specs['namespace'])

    w = kubernetes.watch.Watch()
    for event in w.stream(func): #, _request_timeout=60):
        handle_event(v1, specs, event)
