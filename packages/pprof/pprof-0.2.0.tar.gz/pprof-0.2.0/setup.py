# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pprof']

package_data = \
{'': ['*']}

install_requires = \
['line-profiler>=3.5.1,<4.0.0']

setup_kwargs = {
    'name': 'pprof',
    'version': '0.2.0',
    'description': 'Python profiling tool',
    'long_description': '<p align="center">\n  <a href="https://github.com/mirecl/pprof"><img src="https://github.com/mirecl/pprof/blob/master/examples/report.png?raw=true" alt="pprof"></a>\n</p>\n\n[![PyPI](https://img.shields.io/pypi/v/pprof)](https://pypi.org/project/pprof/)\n[![Downloads](https://pepy.tech/badge/pprof)](https://pepy.tech/project/pprof)\n[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyPI - License](https://img.shields.io/pypi/l/pprof)](https://github.com/mirecl/pprof/blob/master/LICENSE)\n[![Tests](https://github.com/mirecl/pprof/actions/workflows/test.yaml/badge.svg)](https://github.com/mirecl/pprof/actions/workflows/test.yaml)\n[![codecov](https://codecov.io/gh/mirecl/pprof/branch/master/graph/badge.svg?token=UFDA1JG40A)](https://codecov.io/gh/mirecl/pprof)\n[![python version](https://img.shields.io/pypi/pyversions/pprof.svg)](https://pypi.org/project/pprof/)\n\n## Installing\n\n```sh\npip install pprof\n```\n\nor\n\n```sh\npoetry add pprof\n```\n\n## A Simple Example\n\n```python\nfrom time import sleep\nfrom typing import List\nfrom pprof import cpu\n\ncpu.auto_report()\n\ndef foo():\n    sleep(1.01)\n    return 3\n\n@cpu\ndef run(arr: List) -> float:\n    tmp = []\n    cnt = foo()\n\n    # comment action #1\n    for row in arr:\n        # comment action #2 row 1\n        # comment action #2 row 2\n        if row % cnt == 0:\n            tmp.append(row)\n    result = (sum(tmp * 200) + len(arr)) / len(tmp)  # comment action #3\n    return result\n\nrun(list(range(250000)))\n```\n\n```sh\n(venv) python run.py\n```\n\n## Links\n\n+ **line_profiler** (<https://github.com/pyutils/line_profiler>)\n',
    'author': 'mirecl',
    'author_email': 'grazhdankov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
