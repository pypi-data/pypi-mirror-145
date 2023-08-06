# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hotaru',
 'hotaru.console',
 'hotaru.console.run',
 'hotaru.eval',
 'hotaru.footprint',
 'hotaru.image',
 'hotaru.image.filter',
 'hotaru.optimizer',
 'hotaru.sim',
 'hotaru.train',
 'hotaru.util']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0,<9.0',
 'ffmpeg-python>=0.2,<0.3',
 'matplotlib>=3.5,<4.0',
 'pandas>=1.4,<2.0',
 'scipy>=1.8,<2.0',
 'seaborn>=0.11.2,<0.12.0',
 'tensorflow>=2.8,<3.0',
 'tifffile>=2022.3,<2023.0']

entry_points = \
{'console_scripts': ['hotaru = hotaru.console.app:app']}

setup_kwargs = {
    'name': 'hotaru',
    'version': '4.0.0',
    'description': 'High performance Optimizer to extract spike Timing And cell location from calcium imaging data via lineaR impUlse',
    'long_description': '# HOTARU\n\nHigh performance Optimizer to extract spike Timing And cell location from calcium imaging data via lineaR impUlse\n\n### Author\nTAKEKAWA Takashi <takekawa@tk2lab.org>\n\n### Reference\n- Takekawa., T, et. al.,\n  HOTARU: Automatic sorting system for large scale calcium imaging data,\n  bioRxiv, preparing (2022).\n- Takekawa., T, et. al.,\n  Automatic sorting system for large scale calcium imaging data,\n  bioRxiv, https://doi.org/10.1101/215145 (2017).\n\n\n## Install\n\n### Require\n- python >= 3.8\n- tensorflow >= 2.8\n\n### Install Procedure (using venv)\n- Create venv environment for hotaru\n  - `python3.x -m venv hotaru`\n- Activate hotaru environment\n  - `source hotaru/bin/activate`\n- Install hotaru\n  - `pip install hotaru`\n\n\n## Usage\n\n### Config and Prepare\n- Move to your workspace\n  `cd work`\n- Edit config file `hotaru.ini`\n``` hotaru.ini\n[DEFAULT]\nimgs_path = imgs.tif\nmask_type = 0.pad\nhz = 20.0\ntau_rise = 0.08\ntau_fall = 0.16\n\n[main]\ntag = r20\n\n[r20]\nradius_max = 20.0\n```\n\n### Check Cell Radius Stats\n- Trial\n```hotaru trial```\n- Check peaks stats\n  [see hotaru/figure/r20_trial.pdf]\n- Change `radius_max` if need\n``` hotaru.ini\n[DEFAULT]\nimgs_path = imgs.tif\nmask_type = 0.pad\nhz = 20.0\ntau_rise = 0.08\ntau_fall = 0.16\n\n[main]\ntag = r10\n\n[r10]\nradius_max = 10.0\n\n[r20]\nradius_max = 20.0\n```\n\n### Apply\n- Run\n```hotaru auto```\n  \n### Check Resutls\n- see `hotaru/figure/r10_curr.pdf` and `hotaru/output` directory\n',
    'author': 'TAKEKAWA Takashi',
    'author_email': 'takekawa@tk2lab.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tk2lab/HOTARU',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
