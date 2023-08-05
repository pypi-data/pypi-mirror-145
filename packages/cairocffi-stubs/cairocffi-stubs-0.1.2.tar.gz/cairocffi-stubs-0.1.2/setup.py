# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cairocffi-stubs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cairocffi-stubs',
    'version': '0.1.2',
    'description': 'Stubs for cairocffi. ',
    'long_description': "# cairocffi-stubs\n\nThis package contains type stubs to provide more precise static types and type inference for cairocffi.\n\n## Installation\n\n```\npip install cairocffi-stubs\n```\n\n## Usage\n\n```python\nfrom io import BytesIO\nimport cairocffi as cairo\nimport matplotlib.pyplot as plt\n\nsurface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 300, 200)\ncontext = cairo.Context(surface)\ncontext.show_text('Hello World!')\nimg = BytesIO(surface.write_to_png())  # overloaded\nplt.imshow(plt.imread(img))\nplt.show()\n```\n\nStatic type checker can correctly recognize the return type of `surface.write_to_png()` as `bytes` when passing no arguments. No type errors will be raised.\n\n## Style Guidelines\n\nFollow the same style guidelines as [typeshed](https://github.com/python/typeshed/blob/master/CONTRIBUTING.md).\n",
    'author': '忘忧北萱草',
    'author_email': 'wybxc@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Wybxc/cairocffi-stubs',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
