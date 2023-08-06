# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minos', 'minos.plugins.kong']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0',
 'minos-microservice-common>=0.6.0,<0.7.0',
 'minos-microservice-networks>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'minos-discovery-kong',
    'version': '0.1.0a1',
    'description': 'The minos-kong plugin offer an interface that permit integrate Minos Microservice with Kong API Gateway',
    'long_description': '<p align="center">\n  <a href="https://minos.run" target="_blank"><img src="https://raw.githubusercontent.com/minos-framework/.github/main/images/logo.png" alt="Minos logo"></a>\n</p>\n\n## minos-kong\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/minos-kong.svg)](https://pypi.org/project/minos-kong/)\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/minos-framework/minos-python/pages%20build%20and%20deployment?label=docs)](https://minos-framework.github.io/minos-python)\n[![License](https://img.shields.io/github/license/minos-framework/minos-python.svg)](https://github.com/minos-framework/minos-python/blob/main/LICENSE)\n[![Coverage](https://codecov.io/github/minos-framework/minos-python/coverage.svg?branch=main)](https://codecov.io/gh/minos-framework/minos-python)\n[![Stack Overflow](https://img.shields.io/badge/Stack%20Overflow-Ask%20a%20question-green)](https://stackoverflow.com/questions/tagged/minos)\n\n## Summary\nPre-Alpha release, use at your own risk\nMinos Kong is a plugin that integrate minos micorservices with Kong API Gateway\n\n## Installation\n\nInstall the dependency:\n\n```shell\npip install minos-kong\n```\n\nModify `config.yml` file:\n\n```yaml\n...\ndiscovery:\n  connector: minos.networks.DiscoveryConnector\n  client: minos.plugins.minos_kong.MinosKongClient\n  host: localhost\n  port: 5567\n...\n```\n\n## Documentation\n\nThe official API Reference is publicly available at the [GitHub Pages](https://minos-framework.github.io/minos-python).\n\n## Source Code\n\nThe source code of this project is hosted at the [GitHub Repository](https://github.com/minos-framework/minos-python).\n\n## Getting Help\n\nFor usage questions, the best place to go to is [StackOverflow](https://stackoverflow.com/questions/tagged/minos).\n\n## Discussion and Development\n\nMost development discussions take place over the [GitHub Issues](https://github.com/minos-framework/minos-python/issues). In addition, a [Gitter channel](https://gitter.im/minos-framework/community) is available for development-related questions.\n\n## License\n\nThis project is distributed under the [MIT](https://raw.githubusercontent.com/minos-framework/minos-python/main/LICENSE) license.\n',
    'author': 'Minos Framework Devs',
    'author_email': 'hey@minos.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.minos.run/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
