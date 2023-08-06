# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aniclustermap']

package_data = \
{'': ['*'], 'aniclustermap': ['bin/Linux/*']}

install_requires = \
['pandas>=1.4.1,<2.0.0', 'seaborn>=0.11.2,<0.12.0']

entry_points = \
{'console_scripts': ['ANIclustermap = aniclustermap.aniclustermap:main']}

setup_kwargs = {
    'name': 'aniclustermap',
    'version': '0.1.0',
    'description': 'A tool for drawing ANI clustermap between all-vs-all microbial genomes',
    'long_description': "# ANIclustermap: Draw Clustermap of All-vs-All ANI\n\n![Python3](https://img.shields.io/badge/Language-Python3-steelblue)\n![OS](https://img.shields.io/badge/OS-Mac_|_Linux-steelblue)\n![License](https://img.shields.io/badge/License-MIT-steelblue)\n[![Latest PyPI version](https://img.shields.io/pypi/v/aniclustermap.svg)](https://pypi.python.org/pypi/aniclustermap)\n\n## Overview\n\nANIclustermap is easy-to-use tool for drawing ANI clustermap between all-vs-all microbial genomes.\n\n![ANIclustermap.png](https://raw.githubusercontent.com/moshi4/ANIclustermap/main/images/minimal_dataset/ANIclustermap_annotation.png)  \n\n## Installation\n\nANIclustermap is implemented in Python3. [fastANI](https://github.com/ParBLiSS/FastANI) is required to calculate ANI.\n\nInstall PyPI stable version with pip:\n\n    pip install aniclustermap\n\nInstall latest development version with pip:\n\n    pip install git+https://github.com/moshi4/ANIclustermap.git\n\n## Workflow\n\nDescription of ANIclustermap's automated workflow.\n\n1. Calculate ANI between all-vs-all microbial genomes by fastANI.  \n   If similarity between genomes is low, fastANI output NA. In that case, NA is replaced by 0.0.\n2. Clustering ANI matrix by scipy's UPGMA method.  \n3. Using clustered matrix, drawing clustermap by seaborn.  \n\n## Usage\n\n### Basic Command\n\n    ANIclustermap -i [Genome fasta directory] -o [output directory]\n\n### Options\n\n    -h, --help           show this help message and exit\n    -i I, --indir I      Input genome fasta directory (*.fa|*.fna[.gz]|*.fasta)\n    -o O, --outdir O     Output directory\n    -t , --thread_num    fastANI thread number parameter (Default: 11)\n    --fig_width          Figure width (Default: 10)\n    --fig_height         Figure height (Default: 10)\n    --dendrogram_ratio   Dendrogram ratio to figsize (Default: 0.15)\n    --cmap_colors        cmap interpolation colors parameter (Default: 'lime,yellow,red')\n    --cmap_gamma         cmap gamma parameter (Default: 1.0)\n    --annotation         Show ANI value annotation (Default: OFF)\n    -v, --version        Print version information\n\n### Example Command\n\n    ANIclustermap -i ./example/minimal_dataset/ -o ./aniclustermap_result\n\n## Output Contents\n\nANIclustermap outputs 3 types of files.\n\n- **`ANIclustermap.[png|svg]`**  \n  ANI clustermap result figure.\n\n- **`ANIclustermap_matrix.tsv`**  \n  Clustered all-vs-all ANI matrix.\n\n- **`ANIclustermap_dendrogram.nwk`**  \n  Newick format clustering dendrogram.\n",
    'author': 'moshi',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/moshi4/ANIclustermap/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
