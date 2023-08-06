# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qwikstart',
 'qwikstart.cli',
 'qwikstart.operations',
 'qwikstart.repository',
 'qwikstart.utils']

package_data = \
{'': ['*'], 'qwikstart.cli': ['templates/*']}

install_requires = \
['binaryornot>=0.4.4,<0.5.0',
 'click>=8.1.2,<9.0.0',
 'colorlog>=6.6.0,<7.0.0',
 'gitpython>=3.1.0,<4.0.0',
 'jinja2-time>=0.2.0,<0.3.0',
 'jinja2>=3.1.1,<4.0.0',
 'prompt-toolkit>=3.0.3,<4.0.0',
 'pygments>=2.5.2,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'rope>=0.23.0,<0.24.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'termcolor>=1.1.0,<2.0.0',
 'typing-extensions>=4.1.1,<5.0.0',
 'yamllint>=1.23.0,<2.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8'],
 'docs': ['sphinx>=4.5.0,<5.0.0',
          'sphinx-autobuild',
          'sphinxcontrib-apidoc>=0.3.0,<0.4.0',
          'sphinxcontrib-napoleon']}

entry_points = \
{'console_scripts': ['qwikstart = qwikstart.cli.main:main']}

setup_kwargs = {
    'name': 'qwikstart',
    'version': '0.8.0',
    'description': 'Code generator for automating configuration, setup, and yak shaving.',
    'long_description': 'qwikstart: Code generator for fun and profit\n============================================\n\n.. default-role:: literal\n\n.. image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg\n   :target: https://github.com/tonysyu/qwikstart/blob/master/LICENSE\n\n.. image:: https://travis-ci.com/tonysyu/qwikstart.svg?branch=master\n   :target: https://travis-ci.com/tonysyu/qwikstart\n\n.. image:: https://codecov.io/gh/tonysyu/qwikstart/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/tonysyu/qwikstart\n\n.. image:: https://readthedocs.org/projects/qwikstart/badge/\n   :target: https://qwikstart.readthedocs.io\n\n\n- **Documentation:** https://qwikstart.readthedocs.io\n- **Source:** https://github.com/tonysyu/qwikstart\n\n`qwikstart` is a code generator for integrating code into existing projects. It\'s\nsimilar to code generators like cookiecutter_, yeoman_, and hygen_ but with a focus on\nadding code to existing projects.\n\nA simple `hello-world.yml` script in qwikstart would look something like:\n\n.. code-block:: yaml\n\n    steps:\n        "Ask for name":\n            name: prompt\n            inputs:\n                - name: "name"\n                  default: "World"\n        "Display message":\n            name: echo\n            message: |\n\n                Hello, {{ qwikstart.name }}!\n\nThe first step uses the `prompt` operation with a single input `"name"`, with a default\nvalue of `"World"` (which is editable when running the script). The next step just uses\nthe `echo` operation to display a message. This script can be using `qwikstart run`:\n\n.. code-block:: bash\n\n    $ qwikstart run hello-world.yml\n\n    Please enter the following information:\n    name: World\n\n    Hello, World!\n\nInstall\n=======\n\nThe recommended way of installing `qwikstart` is to use pipx_:\n\n.. code-block:: bash\n\n    pipx install qwikstart\n\nIf you happen to be setting up pipx_ for the first time, the\n`pipx installation instructions`_ suggest running `pipx ensurepath` to update\nthe user path. Note, if you use `~/.profile` instead of `~/.bash_profile`,\nthis will add `~/.bash_profile`, which will take precendence over `~/.profile`.\nEither move the code from `~/.bash_profile` to `~/.profile` or\n`link your profiles <https://superuser.com/a/789465>`_.\n\n.. _pipx: https://pypi.org/project/pipx/\n.. _pipx installation instructions:\n    https://pipxproject.github.io/pipx/installation/\n\n\nBasic Usage\n===========\n\nAfter installing `qwikstart`, you can run a simple hello-world example using the\nfollowing:\n\n.. code-block:: bash\n\n    $ qwikstart run --repo https://github.com/tonysyu/qwikstart examples/hello_world.yml\n\n\nBy default, there are abbreviations for common git repos, so the above can also be\nwritten:\n\n.. code-block:: bash\n\n    qwikstart run --repo gh:tonysyu/qwikstart examples/hello_world.yml\n\n\nSee Also\n========\n\nThere are a lot code generators and scaffolding tools out there, and the following is\njust a selection of some of the most popular ones:\n\n- cookiecutter_: A command-line utility that creates projects from cookiecutters\n  (project templates)\n- hygen_: The scalable code generator that saves you time.\n- yeoman_: The web\'s scaffolding tool for modern webapps\n\n.. _hygen: https://www.hygen.io/\n.. _cookiecutter: https://cookiecutter.readthedocs.io/\n.. _yeoman: https://yeoman.io/\n\n',
    'author': 'Tony S. Yu',
    'author_email': 'tsyu80@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tonysyu/qwikstart',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
