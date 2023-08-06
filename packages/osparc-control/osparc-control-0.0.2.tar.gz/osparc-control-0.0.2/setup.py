# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['osparc_control', 'osparc_control.transport']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'pydantic>=1.8.2',
 'pyzmq>=14.0.0',
 'tenacity>=8.0.1',
 'u-msgpack-python>=2.7.1']

setup_kwargs = {
    'name': 'osparc-control',
    'version': '0.0.2',
    'description': 'Osparc Control',
    'long_description': '# Osparc Control\n\n[![PyPI](https://img.shields.io/pypi/v/osparc-control.svg)](https://pypi.org/project/osparc-control/) [![Status](https://img.shields.io/pypi/status/osparc-control.svg)](https://pypi.org/project/osparc-control/) [![Python Version](https://img.shields.io/pypi/pyversions/osparc-control)](https://pypi.org/project/osparc-control) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n[![Tests](https://github.com/ITISFoundation/osparc-control/workflows/Tests/badge.svg)](https://github.com/ITISFoundation/osparc-control/actions?workflow=Tests) [![codecov](https://codecov.io/gh/ITISFoundation/osparc-control/branch/master/graph/badge.svg?token=3P04fQlaEb)](https://codecov.io/gh/ITISFoundation/osparc-control) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n---\n\n## Installation\n\nYou can install _Osparc Control_ via [pip] from [PyPI]:\n\n```bash\npip install osparc-control\n```\n\n## Documentation\n\nRead docs at https://itisfoundation.github.io/osparc-control\n\n## Examples\n\nTo run below examples either clone the repo or copy code from the snippets\nbelow the commands\n\n### Simple example\n\nA first example where `requester.py` asks for a random number and\n`replier.py` defines an interface to provide it.\n\n- In a first terminal run:\n\n```bash\npython examples/1_simple/requester.py\n```\n\n#### examples/1_simple/requester.py\n\n[filename](examples/1_simple/requester.py ":include :type=code")\n\n- In a second terminal run:\n\n```bash\npython examples/1_simple/replier.py\n```\n\n#### examples/1_simple/replier.py\n\n[filename](examples/1_simple/replier.py ":include :type=code")\n\n### Advanced example\n\nA showcase of all the types of supported requests.\n\n- In a first terminal run:\n\n```bash\npython examples/2_base_time_add/controller.py\n```\n\n#### examples/2_base_time_add/controller.py\n\n[filename](examples/2_base_time_add/controller.py ":include :type=code")\n\n- In a second terminal run:\n\n```bash\npython examples/2_base_time_add/solver.py\n```\n\n#### examples/2_base_time_add/solver.py\n\n[filename](examples/2_base_time_add/solver.py ":include :type=code")\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\nOur [Code of Conduct] pledge.\n\n## License\n\nDistributed under the terms of the [MIT license],\n_Osparc Control_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]\'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[cookiecutter]: https://github.com/audreyr/cookiecutter\n[mit license]: LICENSE.md\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/ITISFoundation/osparc-control/issues\n[pip]: https://pip.pypa.io/\n[contributor guide]: CONTRIBUTING.md\n[code of conduct]: CODE_OF_CONDUCT.md\n',
    'author': 'Andrei Neagu',
    'author_email': 'neagu@itis.swiss',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ITISFoundation/osparc-control',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
