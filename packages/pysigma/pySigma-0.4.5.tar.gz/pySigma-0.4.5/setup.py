# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sigma',
 'sigma.backends.test',
 'sigma.conversion',
 'sigma.pipelines',
 'sigma.processing']

package_data = \
{'': ['*']}

install_requires = \
['pyparsing>=3.0.7,<4.0.0', 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'pysigma',
    'version': '0.4.5',
    'description': 'Sigma rule processing and conversion tools',
    'long_description': "# pySigma\n\n![Tests](https://github.com/SigmaHQ/pySigma/actions/workflows/test.yml/badge.svg)\n![Coverage Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/thomaspatzke/11b31b4f709b6dc54a30d5203e8fe0ee/raw/SigmaHQ-pySigma-coverage.json)\n![Status](https://img.shields.io/badge/Status-pre--release-orange)\n\n`pySigma` is a python library that parses and converts Sigma rules into queries. It is a replacement\nfor the legacy Sigma toolchain (sigmac) with a much cleaner design and is almost fully tested.\nBackends for support of conversion into query languages and processing pipelines for transforming\nrule for log data models are separated into dedicated projects to keep pySigma itself slim and\nvendor-agnostic. See the *Related Projects* section below to get an overview.\n\n## Getting Started\n\nTo start using `pySigma`, install it using your python package manager of choice. Examples:\n\n```\npip install pysigma\npipenv install pysigma\npoetry add pysigma\n```\n\nDocumentation with some usage examples can be found [here](https://sigmahq-pysigma.readthedocs.io/).\n\n## Features\n\n`pySigma` brings a number of additional features compared to `sigmac`, as well as some changes.\n\n### Modifier comparison between pySigma and sigmac\n\n|Modifier|Use|sigmac legacy|\n|--------|---|:-------------:|\n|contains|the value is matched anywhere in the field (strings and regular expressions)|X|\n|startswith|The value is expected at the beginning of the field's content (strings and regular expressions)|X|\n|endswith|The value is expected at the end of the field's content (strings and regular expressions)|X|\n|base64|The value is encoded with Base64|X|\n|base64offset|If a value might appear somewhere in a base64-encoded value the representation might change depending on the position in the overall value|X|\n|wide|transforms value to UTF16-LE encoding|X|\n|re|value is handled as regular expression by backends|X|\n|cidr|value is handled as a IP CIDR by backends||\n|all|This modifier changes OR logic to AND|X|\n|lt|Field is less than the value||\n|lte|Field is less or egal than the value||\n|gt|Field is Greater than the value||\n|gte|Field is Greater or egal than the value||\n|expand|Modifier for expansion of placeholders in values. It replaces placeholder strings (%something%)||\n\n## Overview\n\nConversion Overview\n\n![Conversion Graph](/docs/images/conversion.png)\n\nPipelines\n\n![Conversion Graph](/docs/images/pipelines.png)\n\nMore details are described in [the documentation](https://sigmahq-pysigma.readthedocs.io/).\n\n## Testing\n\npySigma uses pytest as testing framework. Simply run `pytest` to run all tests. Run `pytest\n--cov=sigma` to get a coverage report.\n\n## Building\n\nTo build your own package run `poetry build`.\n\n## Contributing\n\nPull requests are welcome. Please feel free to lodge any issues/PRs as discussion points.\n\n## Maintainers\n\nThe project is currently maintained by:\n\n- Thomas Patzke <thomas@patzke.org>\n- [frack113](https://github.com/frack113)\n\n## Related Projects\n\npySigma isn't a monolithic library attempting to support everything but the core. Support for target\nquery languages and log data models is provided by additional packages that extend pySigma:\n\n* [sigma-cli](https://github.com/SigmaHQ/sigma-cli): a command line interface for conversion of\n  Sigma rules based on pySigma. (work in progress, not yet on PyPI)\n* [pySigma-backend-splunk](https://github.com/SigmaHQ/pySigma-backend-splunk):\n* [pySigma-pipeline-sysmon](https://github.com/SigmaHQ/pySigma-pipeline-sysmon)\n* [pySigma-pipeline-crowdstrike](https://github.com/SigmaHQ/pySigma-pipeline-crowdstrike)\n\nAll packages can also be installed from PyPI if not mentioned otherwise by the Python package\nmanager of your choice.\n\n## License\n\nGNU Lesser General Public License v2.1. For details, please see the full license file [located here](https://github.com/SigmaHQ/pySigma/blob/main/LICENSE).\n",
    'author': 'Thomas Patzke',
    'author_email': 'thomas@patzke.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SigmaHQ/pySigma',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
