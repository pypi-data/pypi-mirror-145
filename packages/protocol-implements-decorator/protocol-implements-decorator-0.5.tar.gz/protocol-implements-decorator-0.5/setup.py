# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['protocol_implements_decorator']

package_data = \
{'': ['*'],
 'protocol_implements_decorator': []}

setup_kwargs = {
    'name': 'protocol-implements-decorator',
    'version': '0.5',
    'description': "Adds '@implements' decorator to aid in explicit use of protocols.",
    'long_description': '# protocol_implements_decorator\n\nAdds the "implements" decorator to make using protocols easier and more explicit\n\n\n## Description\n\nAdds the @implements decorator.\nThis will cause a runtime NotImplementedError if the class does not implement all parts of the protocol.\nAlso adds the get_protocols_implemented method to the class providing a list of all protocols the decorated class adhears to.',
    'author': 'rbroderi',
    'author_email': 'richard@sanguinesoftware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
