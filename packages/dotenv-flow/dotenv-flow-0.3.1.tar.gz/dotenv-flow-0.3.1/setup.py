# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dotenv_flow']
install_requires = \
['python-dotenv>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'dotenv-flow',
    'version': '0.3.1',
    'description': 'Like the dotenv-flow NodeJS library, for Python',
    'long_description': "# dotenv_flow\n\nLoads different dotenv files based on the value of the `PY_ENV` variable.\n\nValues in more specific files override previous values.\n\nFiles have 2 flavors:\n\n- public (ex: .env.dev) that should be committed to version control\n- private (ex: .env.dev.local) that has preference over the previous one if present, and should **NOT**\n\nThis is the python version of Node's [dotenv-flow](https://www.npmjs.com/package/dotenv-flow)\n\ndotenv files are loaded with [python-dotenv](https://pypi.org/project/python-dotenv/)\n\nThis should be added to version control ignore file:\n```\n# local .env* files\n.env.local\n.env.*.local\n```\n",
    'author': 'Carlos Gonzalez',
    'author_email': 'gonsa.carlos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
