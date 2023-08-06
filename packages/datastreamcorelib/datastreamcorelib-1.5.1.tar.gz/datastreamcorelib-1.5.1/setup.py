# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datastreamcorelib']

package_data = \
{'': ['*']}

install_requires = \
['libadvian>=0.3,<=2.0', 'msgpack>=1.0,<2.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

setup_kwargs = {
    'name': 'datastreamcorelib',
    'version': '1.5.1',
    'description': 'Helpers and utilities for https://gitlab.com/advian-oss/python-datastreamservicelib that are not eventloop specific.',
    'long_description': '=================\ndatastreamcorelib\n=================\n\nCore helpers and Abstract Base Classes for making use of ZMQ nice, easy and DRY.\n\nYou should probably look at https://gitlab.com/advian-oss/python-datastreamservicelib and\nhttps://gitlab.com/advian-oss/python-datastreamserviceapp_template unless you\'re working\non an adapter for yet unsupported eventloop.\n\nDocker\n------\n\nFor more controlled deployments and to get rid of "works on my computer" -syndrome, we always\nmake sure our software works under docker.\n\nIt\'s also a quick way to get started with a standard development environment.\n\nSSH agent forwarding\n^^^^^^^^^^^^^^^^^^^^\n\nWe need buildkit_::\n\n    export DOCKER_BUILDKIT=1\n\n.. _buildkit: https://docs.docker.com/develop/develop-images/build_enhancements/\n\nAnd also the exact way for forwarding agent to running instance is different on OSX::\n\n    export DOCKER_SSHAGENT="-v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock -e SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock"\n\nand Linux::\n\n    export DOCKER_SSHAGENT="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK"\n\nCreating a development container\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\nBuild image, create container and start it::\n\n    docker build --ssh default --target devel_shell -t datastreamcorelib:devel_shell .\n    docker create --name datastreamcorelib_devel -v `pwd`":/app" -it -v /tmp:/tmp `echo $DOCKER_SSHAGENT` datastreamcorelib:devel_shell\n    docker start -i datastreamcorelib_devel\n\npre-commit considerations\n^^^^^^^^^^^^^^^^^^^^^^^^^\n\nIf working in Docker instead of native env you need to run the pre-commit checks in docker too::\n\n    docker exec -i datastreamcorelib_devel /bin/bash -c "pre-commit install"\n    docker exec -i datastreamcorelib_devel /bin/bash -c "pre-commit run --all-files"\n\nYou need to have the container running, see above. Or alternatively use the docker run syntax but using\nthe running container is faster::\n\n    docker run -it --rm -v `pwd`":/app" datastreamcorelib:devel_shell -c "pre-commit run --all-files"\n\nTest suite\n^^^^^^^^^^\n\nYou can use the devel shell to run py.test when doing development, for CI use\nthe "tox" target in the Dockerfile::\n\n    docker build --ssh default --target tox -t datastreamcorelib:tox .\n    docker run -it --rm -v `pwd`":/app" `echo $DOCKER_SSHAGENT` datastreamcorelib:tox\n\nProduction docker\n^^^^^^^^^^^^^^^^^\n\nThere\'s a "production" target since it\'s our standard pattern, however this library does not yet\nexpose any CLI tools so the production target is kinda useless.\n\nLocal Development\n-----------------\n\nTLDR:\n\n- Create and activate a Python 3.6 virtualenv (assuming virtualenvwrapper)::\n\n    mkvirtualenv -p `which python3.6` my_virtualenv\n\n- change to a branch::\n\n    git checkout -b my_branch\n\n- install Poetry: https://python-poetry.org/docs/#installation\n- Install project deps and pre-commit hooks::\n\n    poetry install\n    pre-commit install\n    pre-commit run --all-files\n\n- Ready to go.\n\nUse Python 3.6 for development since it\'s the lowest supported version so you don\'t accidentally\nuse features only available in higher versions and then have to re-do everything when CI tests fail\non 3.6.\n\nRemember to activate your virtualenv whenever working on the repo, this is needed\nbecause pylint and mypy pre-commit hooks use the "system" python for now (because reasons).\n\nRunning "pre-commit run --all-files" and "py.test -v" regularly during development and\nespecially before committing will save you some headache.\n',
    'author': 'Eero af Heurlin',
    'author_email': 'eero.afheurlin@iki.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/advian-oss/python-datastreamcorelib/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
