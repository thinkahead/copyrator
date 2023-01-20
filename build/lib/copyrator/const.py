# CRD Settings
CRD_GROUP = 'flant.com'
CRD_VERSION = 'v1'
CRD_PLURAL = 'copyrators'

# Type methods maps
LIST_TYPES_MAP = {
    'configmap': 'list_namespaced_config_map',
    'secret': 'list_namespaced_secret',
}

REPLACE_TYPES_MAP = {
    'configmap': 'replace_namespaced_config_map',
    'secret': 'replace_namespaced_secret',
}

PATCH_TYPES_MAP = {
    'configmap': 'patch_namespaced_config_map',
    'secret': 'patch_namespaced_secret',
}

CREATE_TYPES_MAP = {
    'configmap': 'create_namespaced_config_map',
    'secret': 'create_namespaced_secret',
}

# Allowed events
ALLOWED_EVENT_TYPES = {'ADDED', 'MODIFIED'}
