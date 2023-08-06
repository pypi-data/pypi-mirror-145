# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quickdump', 'quickdump.tests']

package_data = \
{'': ['*']}

install_requires = \
['dill>=0.3.4,<0.4.0',
 'loguru>=0.6.0,<0.7.0',
 'lz4>=4.0.0,<5.0.0',
 'multidict>=6.0.2,<7.0.0',
 'starlette[server]>=0.19.0,<0.20.0',
 'uvicorn[server]>=0.17.6,<0.18.0']

entry_points = \
{'console_scripts': ['quickdump_http = quickdump.server_http:main',
                     'quickdump_tcp = quickdump.server_tcp:main']}

setup_kwargs = {
    'name': 'quickdump',
    'version': '0.5.0',
    'description': 'Quickly store arbitrary Python objects in unique files.',
    'long_description': '# quickdump\n\nQuickly store arbitrary Python objects in local files.\n\n*Library status - this is an experimental work in progress that hasn\'t been\nbattle-tested at all. The API will change often between versions, and you may\nlose all your data due to silly bugs.*\n\n---\n\n### Features\n\n- Store arbitrary objects locally\n- No config or boilerplate required\n- Dump to TCP server\n- Dump to HTTP server\n\n### Notes\n\n(todo - rewrite this in a coherent manner)\n\n- Currently, compression is applied per call to `dump`. This isn\'t very\n  efficient (probably?)\n- Labels are slugified to prevent errors from invalid characters in the filename\n\n---\nQuickly dump (almost) any object you like:\n\n```python\nfrom quickdump import qd, QuickDumper\nfrom decimal import Decimal\n\nfor i in range(10):\n      result = Decimal(i) ** Decimal("0.5")\n      qd(result)\n```\n\nAnd use them whenever it\'s convenient later:\n\n```python\nfor obj in qd.iter_dumps():\n      print(obj)  # 0\n      # 1.000000000000000000000000000\n      # 1.414213562373095048801688724\n      # ...\n```\n\nDump objects assigning a label, or create a dumper with a pre-configured label:\n\n```python\nqd("Armação", "Campeche", "Solidão", label="beaches")\n\nbeach_dumper = QuickDumper("beaches")\nbeach_dumper("Morro das Pedras", "Açores", "Gravatá")\n```\n\nIterate over multiple labels (including the default):\n\n```python\nfor obj in qd.iter_dumps("beaches", "default_dump"):\n      print(obj)\n```\n\nIterate only over objects that match some filter:\n\n```python\ndef filter_initial_a(obj):\n      return not obj.startswith("A")\n\n\nfor obj in qd.iter_dumps("beaches", filter_fun=filter_initial_a):\n      print(obj)  # Campeche\n      # ...\n```\n\n## Someday™\n\n- [ ] Enable simple serialization of unpicklable types (e.g. save a `socket`\n  type property of some object as `socket`\'s string representation instead of\n  just ignoring the object)\n- [ ] Quickdump by piping from shell\n- [ ] Function decorator able to log function inputs and/or outputs\n- [ ] Real time visualization of dumped data and metadata\n',
    'author': 'Pedro Batista',
    'author_email': 'pedrovhb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pedrovhb/quickdump',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
