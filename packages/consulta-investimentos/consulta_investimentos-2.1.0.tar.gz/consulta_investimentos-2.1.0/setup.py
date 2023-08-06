# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['consulta_investimentos',
 'consulta_investimentos.ativos_cotacoes',
 'consulta_investimentos.ativos_dividendos',
 'consulta_investimentos.ativos_eventos',
 'consulta_investimentos.ativos_posicao',
 'consulta_investimentos.moeda_cotacao',
 'consulta_investimentos.utils']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas-datareader>=0.10.0,<0.11.0',
 'pandas>=1.4.1,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'selenium>=4.1.2,<5.0.0']

setup_kwargs = {
    'name': 'consulta-investimentos',
    'version': '2.1.0',
    'description': 'Baixa infos diversas de ativos financeiros.',
    'long_description': None,
    'author': 'Vinicius Maciel',
    'author_email': 'vinimaciel01@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
