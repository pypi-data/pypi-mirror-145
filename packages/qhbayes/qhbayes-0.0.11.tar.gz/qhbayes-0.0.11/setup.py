# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qhbayes',
 'qhbayes.app',
 'qhbayes.data',
 'qhbayes.gp',
 'qhbayes.notebooks',
 'qhbayes.scripts',
 'qhbayes.stats',
 'qhbayes.utilities']

package_data = \
{'': ['*'],
 'qhbayes': ['QHBayes.egg-info/*', 'qhbayes.egg-info/*'],
 'qhbayes.app': ['assets/*'],
 'qhbayes.notebooks': ['.ipynb_checkpoints/*']}

install_requires = \
['Pint>=0.18,<0.19',
 'argparse>=1.4.0,<2.0.0',
 'arviz>=0.11.4,<0.12.0',
 'click>=4.0,<8',
 'dash-bootstrap-components>=1.0.3,<2.0.0',
 'dash-extensions>=0.0.71,<0.0.72',
 'dash>=2.3.0,<3.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.15.0,<1.22.2',
 'odfpy>=1.4.1,<2.0.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.4.1,<2.0.0',
 'plotly>=5.6.0,<6.0.0',
 'pymc3>=3.11.5,<4.0.0',
 'scipy>=1.7.3,<1.8.0',
 'seaborn>=0.11.2,<0.12.0',
 'setuptools>=60.10.0,<61.0.0']

entry_points = \
{'console_scripts': ['QHBayes = qhbayes.scripts.run_qhbayes:run_qhbayes',
                     'QHBayes_App = qhbayes.scripts.run_app:run_app',
                     'QHBayes_Example = qhbayes.scripts.example:run_example']}

setup_kwargs = {
    'name': 'qhbayes',
    'version': '0.0.11',
    'description': 'Bayesian methods for inferring mass eruption rate for column height (or vice versa) for volcanic eruptions',
    'long_description': '# QHBayes #\n\nBayesian methods for inferring mass eruption rate from column height (or vice versa) for volcanic eruptions\n\n### What is it? ###\n\n*QHBayes* uses Bayesian methods to explore the relationship between the mass eruption rate (Q) of a volcanic eruption and the height reached by the volcanic eruption column (H) that is produced.\n\nThe mass eruption rate is a quantity that is very important in volcanology and in the dispersion of volcanic ash in the atmosphere, but it is very difficult to measure directly.\n\nOften the mass eruption rate is inferred from observations of the height of the volcanic eruption column, since the eruption column is often much easier to measure.  The eruption column height is linked to the mass eruption rate through the fluid dynamics of turbulent buoyant plumes, but there are often external volcanological and atmospheric effects that contribute and complicate the relationship.\n\nDatasets of the mass eruption rate and eruption column height have been compiled and used to determine an empirical relationship these quantities, using linear regression.  This has then been used to infer the mass eruption rate from the plume height.\n\n*QHBayes* goes further, by using Bayesian methods to perform the regression.  Bayesian methods:\n* allow us to incorporate a range of *uncertainties* quantitatively into our model;\n* provide a meaningful quantitative comparison of different models;\n\n### Main Features ###\n\n\n### How do I get set up? ###\n\n* Summary of set up\n\n\n* Configuration\n* Dependencies\n* Database configuration\n* How to run tests\n* Deployment instructions\n\n### Contribution guidelines ###\n\n* Writing tests\n* Code review\n* Other guidelines\n\n### Who do I talk to? ###\n\n* Repo owner or admin\n* Other community or team contact\n',
    'author': 'markwoodhouse',
    'author_email': 'mark.woodhouse@bristol.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
