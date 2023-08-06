# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dsci_310_group_1_package', 'dsci_310_group_1_package..ipynb_checkpoints']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1', 'numpy>=1.22.3', 'pandas>=1.4.2']

setup_kwargs = {
    'name': 'dsci-310-group-1-package',
    'version': '0.1.0',
    'description': 'A package containing the necessary functions to smoothly run the analysis in DSCI-310-Group-1',
    'long_description': '# DSCI_310_group_1_package\n\nA package containing the necessary functions to smoothly run the analysis in DSCI-310-Group-1\n\n## Installation\n\n```bash\n$ pip install DSCI_310_group_1_package\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`DSCI_310_group_1_package` was created by Andres Perez, Daniel Hou, Zizhen Guo, Timothy Zhou. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`DSCI_310_group_1_package` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Andres Perez, Daniel Hou, Zizhen Guo, Timothy Zhou',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
