# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonml']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jsonml',
    'version': '0.0.1',
    'description': '',
    'long_description': '# jsonml\n<!--\n[![Version](https://img.shields.io/pypi/v/asy)](https://pypi.org/project/asy)\n[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n-->\n\nThis library is a python implementation of jsonml.\n\nSee below for jsonml specifications.\n\n- http://www.jsonml.org/\n\n# Requirement\n\n- Python 3.8+\n\n\n# Getting Started\n\n``` python\nfrom jsonml import Parser\n\nparser = Parser()\n\nobj = ["tag1", ["tag2", ["tag3", "1"]]]\n\ntree_1 = parser.parse_from_obj(obj)\nxml_1 = parser.to_xml(tree_1)\njsonml = parser.to_jsonml(tree_1)\n\ntree_2 = parser.parse_from_xml_string(xml_1)\nassert parser.to_jsonml(tree_2) == jsonml\n```\n\n\n```\n<tag1><tag2><tag3>1</tag3></tag2></tag1>\n```\n\n```\n[\n  "tag1",\n  [\n    "tag2",\n    [\n      "tag3",\n      "1"\n    ]\n  ]\n]\n```\n\n\n# Contribute\n\n```\npoetry install\npre-commit install\nsource .venv/bin/activate\nmake\n```\n',
    'author': 'sasano8',
    'author_email': 'y-sasahara@ys-method.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sasano8/jsonml',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<=3.10',
}


setup(**setup_kwargs)
