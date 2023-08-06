# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kubecrd']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0', 'apischema>=0.15.0', 'kubernetes>=23.3.0,<24.0.0']

setup_kwargs = {
    'name': 'kubecrd',
    'version': '0.4.0',
    'description': 'Create Kubernetes CRD using Python dataclasses',
    'long_description': '========\nKube CRD\n========\n\nThe primary purpose of this project is to simplify working with Kubernetes\nCustom Resources. To achieve that it provides a base class,\n``kubecrd.OpenAPISchemaBase`` that can create Python\ndataclassses into Kubernetes Custom Resources and also generate and install\nCustom Resource Definitions for those resource into the K8s cluster directly.\n\n  >>> from dataclasses import dataclass, field\n  >>> from uuid import UUID\n  >>> from kubecrd import OpenAPISchemaBase\n  >>> from apischema import schema\n\n  >>> @dataclass\n  ... class Resource(OpenAPISchemaBase):\n  ...     __group__ = \'example.com\'\n  ...     __version__ = \'v1alpha1\'\n  ...\n  ...     name: str\n  ...     tags: list[str] = field(\n  ...         default_factory=list,\n  ...         metadata=schema(\n  ...            description=\'regroup multiple resources\',\n  ...            unique=False,\n  ...         ),\n  ...     )\n\n  >>> print(Resource.crd_schema())\n  apiVersion: apiextensions.k8s.io/v1\n  kind: CustomResourceDefinition\n  metadata:\n    name: resources.example.com\n  spec:\n    group: example.com\n    names:\n      kind: Resource\n      plural: resources\n      singular: resource\n    scope: Namespaced\n    versions:\n    - name: v1alpha1\n      schema:\n        openAPIV3Schema:\n          properties:\n            spec:\n              properties:\n                name:\n                  type: string\n                tags:\n                  default: []\n                  description: regroup multiple resources\n                  items:\n                    type: string\n                  type: array\n                  uniqueItems: false\n              required:\n              - name\n              type: object\n          type: object\n      served: true\n      storage: true\n  <BLANKLINE>\n\n\nCreate CRD in K8s Cluster\n=========================\n\nIt is also possible to install the CRD in a cluster using a Kubernetes Client\nobject::\n\n  from from kubernetes import client, config\n  config.load_kube_config()\n  k8s_client = client.ApiClient()\n  Resource.install(k8s_client)\n\nYou can then find the resource in the cluster::\n\n  » kubectl get crds/resources.example.com\n  NAME                    CREATED AT\n  resources.example.com   2022-03-20T03:58:25Z\n\n  $ kubectl api-resources | grep example.com\n  resources     example.com/v1alpha1                  true         Resource\n\nInstallation of resource is idempotent, so re-installing an already installed\nresource doesn\'t raise any exceptions if ``exist_ok=True`` is passed in::\n\n  Resource.install(k8s_client, exist_ok=True)\n\n\nSerialization\n=============\n\nYou can serialize a Resource such that it is suitable to POST to K8s::\n\n  >>> example = Resource(name=\'myResource\', tags=[\'tag1\', \'tag2\'])\n  >>> import json\n  >>> print(json.dumps(example.serialize(), sort_keys=True, indent=4))\n  {\n      "apiVersion": "example.com/v1alpha1",\n      "kind": "Resource",\n      "metadata": {\n          "name": "..."\n      },\n      "spec": {\n          "name": "myResource",\n          "tags": [\n              "tag1",\n              "tag2"\n          ]\n      }\n  }\n\n\nObjects can also be serialized and saved directly in K8s::\n\n  example.save(k8s_client)\n\nWhere ``client`` in the above is a Kubernetes client object. You can also use\nasyncio with kubernetes_asyncio client and instead do::\n\n  await example.async_save(k8s_async_client)\n\n\nDeserialization\n===============\n\nYou can deserialize the JSON from Kubernetes API into Python CR objects.\n::\n\n   $ cat -p testdata/cr.json\n   {\n    "apiVersion": "example.com/v1alpha1",\n    "kind": "Resource",\n    "metadata": {\n        "generation": 1,\n        "name": "myresource1",\n        "namespace": "default",\n        "resourceVersion": "105572812",\n        "uid": "02102eb3-968b-418a-8023-75df383daa3c"\n    },\n    "spec": {\n        "name": "bestID",\n        "tags": [\n            "tag1",\n            "tag2"\n        ]\n    }\n    }\n\nby using ``from_json`` classmethod on the resource::\n\n   >>> import json\n   >>> with open(\'testdata/cr.json\') as fd:\n   ...     json_schema = json.load(fd)\n   >>> res = Resource.from_json(json_schema)\n   >>> print(res.name)\n   bestID\n   >>> print(res.tags)\n   [\'tag1\', \'tag2\']\n\n\nThis also loads the Kubernetes\'s ``V1ObjectMeta`` and sets it as the\n``.metadata`` property of CR::\n\n  >>> print(res.metadata.namespace)\n  default\n  >>> print(res.metadata.name)\n  myresource1\n  >>> print(res.metadata.resource_version)\n  105572812\n\nWatch\n=====\n\nIt is possible to Watch for changes in Custom Resources using the standard\nWatch API in Kubernetes. For example, to watch for all changes in Resources::\n\n\n  async for happened, resource in Resource.async_watch(k8s_async_client):\n      print(f\'Resource {resource.metadata.name} was {happened}\')\n\n\nOr you can use the block sync API for the watch::\n\n\n  for happened, resource in Resource.watch(k8s_client):\n      print(f\'Resource {resource.metadata.name} was {happened}\')\n  \n\nInstalling\n==========\n\nKube CRD can be install from PyPI using pip or your favorite tool::\n\n  $ pip install kubecrd\n',
    'author': 'Abhilash Raj',
    'author_email': 'raj.abhilash1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maxking/kubecrd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
