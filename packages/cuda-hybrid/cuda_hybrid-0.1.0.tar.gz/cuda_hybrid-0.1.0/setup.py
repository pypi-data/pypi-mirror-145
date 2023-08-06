# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cuda_hybrid']

package_data = \
{'': ['*']}

install_requires = \
['networkx', 'numba', 'numpy']

setup_kwargs = {
    'name': 'cuda-hybrid',
    'version': '0.1.0',
    'description': 'Runs ABM/FCM hybrid models on CUDA cores to drastically reduce runtime.',
    'long_description': '# CUDA_HYBRID\n\nThis repository contains the first ever ABM/FCM Hybrid Model on CUDA cores that can help run the simulation in parallel, \nreducing the runtime\n\n## Requirements:\nThe project requires Python 3.7 or higher, depending on the version of the packages in `requirements.txt`.\n\n## Installation\n\n```bash\n$ pip install cuda-hybrid\n```\n\n## Quick Start\n',
    'author': 'Kareem Ghumrawi',
    'author_email': 'kghumrawi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.csi.miamioh.edu/620_final/cse620c_finalproject/-/tree/add-docs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
