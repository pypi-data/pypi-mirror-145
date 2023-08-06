# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bigearthnet_common']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4,<2.0',
 'fastcore>=1.3,<2.0',
 'natsort>=8,<9',
 'pydantic>=1.8,<2.0',
 'python-dateutil>=2,<3',
 'rich>=10,<13',
 'typer>=0.4,<0.5']

entry_points = \
{'console_scripts': ['ben_build_csv_sets = '
                     'bigearthnet_common.sets:build_csv_sets_cli',
                     'ben_constant_prompt = bigearthnet_common.constants:cli',
                     'ben_validate_s1_root_dir = '
                     'bigearthnet_common.base:validate_ben_s1_root_directory_cli',
                     'ben_validate_s2_root_dir = '
                     'bigearthnet_common.base:validate_ben_s2_root_directory_cli']}

setup_kwargs = {
    'name': 'bigearthnet-common',
    'version': '2.4.1',
    'description': 'A collection of common tools to interact with the BigEarthNet dataset.',
    'long_description': '# BigEarthNet Common\n> A personal collection of common tools to interact with the BigEarthNet dataset.\n\n[See the official documentation for more information.](https://docs.kai-tub.tech/bigearthnet_common/)\n\n\n## Contributing\n\nContributions are always welcome!\n\nMore information is available in the [contributing guidelines](https://github.com/kai-tub/bigearthnet_common/blob/main/.github/CONTRIBUTING.md) document.\n',
    'author': 'Kai Norman Clasen',
    'author_email': 'k.clasen@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kai-tub/bigearthnet_common',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
