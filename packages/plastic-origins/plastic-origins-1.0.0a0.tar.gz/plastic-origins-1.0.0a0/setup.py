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
['Flask==2.0.3',
 'Werkzeug==2.0.3',
 'debugpy==1.5.1',
 'gunicorn==19.10.0',
 'imgaug==0.4.0',
 'opencv-python==4.5.5.62',
 'psycopg2-binary==2.8.5',
 'pycocotools==2.0.4',
 'pykalman>=0.9.5,<0.10.0',
 'scikit-video>=1.1.11,<2.0.0',
 'scipy==1.7.3',
 'torch==1.10.1',
 'torchvision==0.11.2',
 'tqdm==4.62.3']

setup_kwargs = {
    'name': 'plastic-origins',
    'version': '1.0.0a0',
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
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
