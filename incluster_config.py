#!/usr/bin/env python

# Copyright 2016 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from kubernetes.client import Configuration

from .config_exception import ConfigException

class InClusterConfigLoader(object):

    def __init__(self, ca_file_name, cert_file_name, key_file_name, environ=os.environ):
        self._ca_file_name = ca_file_name
        self._cert_file_name = cert_file_name
        self._key_file_name = key_file_name
        self._environ = environ

    def load_and_set(self):
        self._load_config()
        self._set_config()

    def _load_config(self):
        self.host = "https://10.0.2.15:6443"
        if not os.path.isfile(self._ca_file_name): raise ConfigException("ca_file_name file does not exist.")
        if not os.path.isfile(self._cert_file_name): raise ConfigException("cert_file_name file does not exist.")
        if not os.path.isfile(self._key_file_name): raise ConfigException("key_file_name file does not exist.")

    def _set_config(self):
        configuration = Configuration()
        configuration.host = self.host
        configuration.ssl_ca_cert = self._ca_file_name
        configuration.cert_file = self._cert_file_name
        configuration.key_file = self._key_file_name
        Configuration.set_default(configuration)


def load_incluster_config():
    """Use the service account kubernetes gives to pods to connect to kubernetes
    cluster. It's intended for clients that expect to be running inside a pod
    running on kubernetes. It will raise an exception if called from a process
    not running in a kubernetes environment."""
    InClusterConfigLoader(ca_file_name="/cacert", cert_file_name="/cert", key_file_name="/key").load_and_set()
