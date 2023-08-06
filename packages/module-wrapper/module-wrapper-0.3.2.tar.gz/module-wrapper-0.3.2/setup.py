# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['module_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['stdlib_list>=0.8.0,<0.9.0']

setup_kwargs = {
    'name': 'module-wrapper',
    'version': '0.3.2',
    'description': 'Module wrapper Python library',
    'long_description': '# module-wrapper - module wrapper Python library (maintenance mode)\n[![License](https://img.shields.io/pypi/l/module-wrapper.svg)](https://www.apache.org/licenses/LICENSE-2.0)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/module-wrapper.svg)\n[![PyPI](https://img.shields.io/pypi/v/module-wrapper.svg)](https://pypi.org/project/module-wrapper/)\n[![Documentation Status](https://img.shields.io/readthedocs/module-wrapper.svg)](http://module-wrapper.readthedocs.io/en/latest/)\n \n# Warning\nAuthors of aioify and module-wrapper decided to discontinue support of\nthese libraries since the idea: "let\'s convert sync libraries to async\nones" works only for some cases. Existing releases of libraries won\'t\nbe removed, but don\'t expect any changes since today. Feel free to\nfork these libraries, however, we don\'t recommend using the automatic\nsync-to-async library conversion approach, as unreliable. Instead,\nit\'s better to run synchronous functions asynchronously using\nhttps://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor\nor https://anyio.readthedocs.io/en/stable/api.html#running-code-in-worker-threads.\n\n# Old documentation\n`module-wrapper` contains `wrap` function, which is used to wrap module, class, function or another variable \nrecursively.\n\n## Installation\nTo install from [PyPI](https://pypi.org/project/module-wrapper/) run:\n```shell\n$ pip install module-wrapper\n```\n\n## Usage\nExample from [aioify](https://github.com/yifeikong/aioify):\n```pyhton\nfrom functools import wraps, partial\nimport asyncio\n\nimport module_wrapper\n\n\n__all__ = [\'aioify\']\n\n\ndef wrap(func):\n    @wraps(func)\n    async def run(*args, loop=None, executor=None, **kwargs):\n        if loop is None:\n            loop = asyncio.get_event_loop()\n        pfunc = partial(func, *args, **kwargs)\n        return await loop.run_in_executor(executor, pfunc)\n    return run\n\n\ndef aioify(obj, name=None):\n    def create(cls):\n        return \'create\', wrap(cls)\n\n    return module_wrapper.wrap(obj=obj, wrapper=wrap, methods_to_add={create}, name=name)\n```\n',
    'author': 'Roman Inflianskas',
    'author_email': 'infroma@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rominf/module-wrapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
