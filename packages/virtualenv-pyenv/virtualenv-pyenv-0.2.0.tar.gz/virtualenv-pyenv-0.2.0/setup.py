# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['_virtualenv_pyenv']

package_data = \
{'': ['*']}

install_requires = \
['pyenv-inspect>=0.2,<0.3', 'virtualenv']

entry_points = \
{'virtualenv.discovery': ['pyenv = _virtualenv_pyenv.discovery:Pyenv']}

setup_kwargs = {
    'name': 'virtualenv-pyenv',
    'version': '0.2.0',
    'description': 'A virtualenv Python discovery plugin using pyenv',
    'long_description': '# virtualenv-pyenv\n\nA [virtualenv][virtualenv] Python discovery plugin using [pyenv][pyenv]\n\n## Installation\n\n```shell\npip install virtualenv-pyenv\n```\n\n## Usage\n\nThe Python discovery mechanism can be specified by:\n\n* the CLI option `--discovery`:\n  ```shell\n  virtualenv --discovery pyenv -p 3.10 testenv\n  ```\n\n* the environment variable `VIRTUALENV_DISCOVERY`:\n  ```shell\n  export VIRTUALENV_DISCOVERY=pyenv\n  virtualenv -p 3.10 testenv\n  ```\n\n* the [config][virtualenv-docs-config-file] option `discovery`:\n  ```ini\n  [virtualenv]\n  discovery = pyenv\n  ```\n\n  ```shell\n  virtualenv pyenv -p 3.10 testenv\n  ```\n\nThe Python version can be expressed using either 2 or 3 version segments:\n\n* `-p 3.9`\n* `-p 3.9.3`\n\nIn the former case, the latest version found will be used.\n\n## Limitations\n\nOnly CPython is supported at the moment.\n\n\n[virtualenv]: https://virtualenv.pypa.io/\n[pyenv]: https://github.com/pyenv/pyenv\n[virtualenv-docs-config-file]: https://virtualenv.pypa.io/en/latest/cli_interface.html#configuration-file\n',
    'author': 'un.def',
    'author_email': 'me@undef.im',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/un-def/virtualenv-pyenv',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
