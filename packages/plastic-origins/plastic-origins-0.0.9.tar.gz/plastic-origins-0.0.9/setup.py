# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['plasticorigins',
 'plasticorigins.detection',
 'plasticorigins.detection.centernet',
 'plasticorigins.detection.centernet.networks',
 'plasticorigins.tools',
 'plasticorigins.tracking']

package_data = \
{'': ['*']}

install_requires = \
['Flask==1.1.1',
 'Werkzeug==2.0.3',
 'debugpy==1.5.1',
 'gunicorn==19.10.0',
 'imgaug==0.4.0',
 'opencv-python==4.5.5.62',
 'psycopg2-binary==2.8.5',
 'pycocotools==2.0.4',
 'scipy==1.7.3',
 'torch==1.10.1',
 'torchvision==0.11.2',
 'tqdm==4.62.3']

setup_kwargs = {
    'name': 'plastic-origins',
    'version': '0.0.9',
    'description': 'A package containing methods commonly used to make inferences',
    'long_description': None,
    'author': 'Chayma Mesbahi',
    'author_email': 'chayma.mesbahi@neoxia.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
