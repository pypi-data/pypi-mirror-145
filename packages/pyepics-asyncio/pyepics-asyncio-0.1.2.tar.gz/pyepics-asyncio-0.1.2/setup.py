# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyepics_asyncio']

package_data = \
{'': ['*']}

install_requires = \
['pyepics>=3.5.1,<4.0.0']

setup_kwargs = {
    'name': 'pyepics-asyncio',
    'version': '0.1.2',
    'description': 'Async/await wrapper for PyEpics',
    'long_description': '# pyepics-asyncio\n\nSimple `async`/`await` wrapper for [PyEpics](https://github.com/pyepics/pyepics).\n\nCurrently there is a wrapper only for `PV` class.\n\n## Usage\n\n### Import\n\n```python\nfrom pyepics_asyncio import Pv\n```\n\n### Connect to PV\n\n```python\npv = await Pv.connect("pvname")\n```\n\n### Read PV value\n\n```python\nprint(await pv.get())\n```\n\n### Write value to PV\n\n```python\nawait pv.put(3.1415)\n```\n\n### Monitor PV\n\n```python\nasync with pv.monitor() as mon:\n    async for value in mon:\n        print(value)\n```\n\n*NOTE: By default values are yielded only on PV update.*\n*If you need monitor to also provide current value on start use `pv.monitor(current=True)`.*\n',
    'author': 'Alexey Gerasev',
    'author_email': 'alexey.gerasev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/agerasev/pyepics-asyncio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
