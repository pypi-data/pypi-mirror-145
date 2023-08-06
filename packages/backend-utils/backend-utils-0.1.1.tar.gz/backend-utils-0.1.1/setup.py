# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['backend_utils',
 'backend_utils.server',
 'backend_utils.server.app',
 'backend_utils.tools']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.75.0,<0.76.0']

setup_kwargs = {
    'name': 'backend-utils',
    'version': '0.1.1',
    'description': 'backend utils',
    'long_description': "# backend-utils\nutils for fastapi backend\n\n\n## Documentation\n\n### Tools\n\n* `Singleton` - metaclass to make singletons\n```python\nfrom backend_utils.tools import Singleton\n\nclass A(metaclass=Singleton):\n    pass\n\nprint(id(A()) == id(A())) # True\n```\n\n* `StrEnum` - subclasses that create variants using `auto()` will have values equal to their names\n```python\nfrom enum import auto\n\nfrom backend_utils.tools import StrEnum\n\nclass Bit(StrEnum):\n    one = auto()\n    two = auto()\n\nprint(Bit.one.value) # 'one'\nprint(Bit.two.value) # 'two'\n```\n\n### Server\n\n* `Router`, `compile_routers`, `register_routers` - build routers \nfor fastapi app\n\n```python\nfrom fastapi import FastAPI, APIRouter\n\nfrom backend_utils.server import (\n    Router, compile_routers, register_routers\n)\nrouter = APIRouter()\n\nrouters = [\n    Router(router=router, tags=['Users'], prefix='/users'),\n]\n\n\ncompiled_routers = compile_routers(\n    routers=routers,\n    root_prefix='/api/v1'\n)\n\napp = FastAPI()\nregister_routers(\n    app=app,\n    routers=[*compiled_routers]\n)\n```\nThis code will compile routers:\n`/api/v1/users/*`\n",
    'author': 'Mark Antipin',
    'author_email': 'antipinsuperstar@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Sistemka/backend-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
