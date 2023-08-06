# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['authzed',
 'authzed.api.v0',
 'authzed.api.v1',
 'authzed.api.v1alpha1',
 'grpcutil',
 'validate']

package_data = \
{'': ['*']}

install_requires = \
['async_generator>=1.10,<2.0',
 'google-api-core>=2.4.0,<3.0.0',
 'google_api>=0.1.12,<0.2.0',
 'grpcio>=1.43.0,<2.0.0',
 'mock>=4.0.3,<5.0.0',
 'protobuf>=3.19.3,<4.0.0',
 'protoc-gen-validate>=0.4.1,<0.5.0',
 'typing-extensions>=3.7.4,<5']

setup_kwargs = {
    'name': 'authzed',
    'version': '0.5.1',
    'description': 'Client library for the Authzed service.',
    'long_description': '# Authzed Python Client\n\n[![PyPI](https://img.shields.io/pypi/v/authzed?color=%23006dad)](https://pypi.org/project/authzed)\n[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)\n[![Build Status](https://github.com/authzed/authzed-py/workflows/Test/badge.svg)](https://github.com/authzed/authzed-py/actions)\n[![Mailing List](https://img.shields.io/badge/email-google%20groups-4285F4)](https://groups.google.com/g/authzed-oss)\n[![Discord Server](https://img.shields.io/discord/844600078504951838?color=7289da&logo=discord "Discord Server")](https://discord.gg/jTysUaxXzM)\n[![Twitter](https://img.shields.io/twitter/follow/authzed?color=%23179CF0&logo=twitter&style=flat-square)](https://twitter.com/authzed)\n\nThis repository houses the Python client library for Authzed.\n\n[Authzed] is a database and service that stores, computes, and validates your application\'s permissions.\n\nDevelopers create a schema that models their permissions requirements and use a client library, such as this one, to apply the schema to the database, insert data into the database, and query the data to efficiently check permissions in their applications.\n\nSupported client API versions:\n- [v1](https://docs.authzed.com/reference/api#authzedapiv1)\n- [v1alpha1](https://docs.authzed.com/reference/api#authzedapiv1alpha1)\n\nYou can find more info on each API on the [Authzed API reference documentation].\nAdditionally, Protobuf API documentation can be found on the [Buf Registry Authzed API repository].\n\nSee [CONTRIBUTING.md] for instructions on how to contribute and perform common tasks like building the project and running tests.\n\n[Authzed]: https://authzed.com\n[Authzed API Reference documentation]: https://docs.authzed.com/reference/api\n[Buf Registry Authzed API repository]: https://buf.build/authzed/api/docs/main\n[CONTRIBUTING.md]: CONTRIBUTING.md\n\n## Getting Started\n\nWe highly recommend following the **[Protecting Your First App]** guide to learn the latest best practice to integrate an application with Authzed.\n\nIf you\'re interested in examples of a specific version of the API, they can be found in their respective folders in the [examples directory].\n\n[Protecting Your First App]: https://docs.authzed.com/guides/first-app\n[examples directory]: /examples\n\n## Basic Usage\n\n### Installation\n\nThis project is packaged as the wheel `authzed` on the [Python Package Index].\n\nIf you are using [pip], the command to install the library is:\n\n```sh\npip install authzed\n```\n\n[Python Package Index]: https://pypi.org/project/authzed\n[pip]: https://pip.pypa.io\n\n### Initializing a client\n\nWith the exception of [gRPC] utility functions found in `grpcutil`, everything required to connect and make API calls is located in a module respective to API version.\n\nIn order to successfully connect, you will have to provide a [Bearer Token] with your own API Token from the [Authzed dashboard] in place of `t_your_token_here_1234567deadbeef` in the following example:\n\n[grpc]: https://grpc.io\n[Bearer Token]: https://datatracker.ietf.org/doc/html/rfc6750#section-2.1\n[Authzed Dashboard]: https://app.authzed.com\n\n```py\nfrom authzed.api.v1 import Client\nfrom grpcutil import bearer_token_credentials\n\n\nclient = Client(\n    "grpc.authzed.com:443",\n    bearer_token_credentials("t_your_token_here_1234567deadbeef"),\n)\n```\n\n### Performing an API call\n\n```py\nfrom authzed.api.v1 import (\n    CheckPermissionRequest,\n    CheckPermissionResponse,\n    ObjectReference,\n    SubjectReference,\n)\n\n\npost_one = ObjectReference(object_type="blog/post", object_id="1")\nemilia = SubjectReference(object=ObjectReference(\n    object_type="blog/user",\n    object_id="emilia",\n))\n\n# Is Emilia in the set of users that can read post #1?\nresp = client.CheckPermission(CheckPermissionRequest(\n    resource=post_one,\n    permission="reader",\n    subject=emilia,\n))\nassert resp.permissionship == CheckPermissionResponse.PERMISSIONSHIP_HAS_PERMISSION\n```\n',
    'author': 'Authzed',
    'author_email': 'support@authzed.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
