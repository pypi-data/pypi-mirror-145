# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nwon_baseline',
 'nwon_baseline.directory_helper',
 'nwon_baseline.file_helper',
 'nwon_baseline.image_helper',
 'nwon_baseline.import_helper',
 'nwon_baseline.poetry',
 'nwon_baseline.print_helper',
 'nwon_baseline.shell_helper',
 'nwon_baseline.type_helper',
 'nwon_baseline.typings']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2', 'pyhumps>=3.0.2,<4.0.0']

entry_points = \
{'console_scripts': ['clean-dist-folder = '
                     'scripts.clean_dist_folder:clean_dist_folder',
                     'create-type-stubs = '
                     'scripts.create_type_stubs:create_type_stubs',
                     'prepare = scripts.prepare:prepare']}

setup_kwargs = {
    'name': 'nwon-baseline',
    'version': '0.1.17',
    'description': 'Python Code that is used in several projects',
    'long_description': '# NVON Python baseline package\n\nThis package provides some basic python functions that can be used across several projects.\n\nThe dependencies of the project are kept to a minimum in order to prevent version conflicts with other projects.\n\nPackage is meant for internal use at [NVON](https://nvon.com) as breaking changes may occur on version changes. This may change at some point but not for now 😇. \n\n## Development Setup\n\nWe recommend developing using poetry. \n\nThis are the steps to setup the project with a local virtual environment:\n\n1. Tell poetry to create dependencies in a `.venv` folder withing the project: `poetry config virtualenvs.in-project true`\n1. Create a virtual environment using the local python version: `poetry env use $(cat .python-version)`\n1. Install dependencies: `poetry install`\n\n## Publish package\n\nFirst you need the package via `poetry build`.\n\nTest package publication\n\n1. Add test PyPi repository: `poetry config repositories.testpypi https://test.pypi.org/legacy/`\n1. Publish the package to the test repository: `poetry publish -r testpypi`\n1. Test package: `pip install --index-url https://test.pypi.org/simple/ nvon_baseline`\n\nIf everything works fine publish the package via `poetry publish`.',
    'author': 'Reik Stiebeling',
    'author_email': 'reik.stiebeling@nvon.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://nvon.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
