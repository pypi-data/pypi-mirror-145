# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['oaklib',
 'oaklib.conf',
 'oaklib.datamodels',
 'oaklib.implementations',
 'oaklib.implementations.amigo',
 'oaklib.implementations.bioportal',
 'oaklib.implementations.fhir',
 'oaklib.implementations.kgx',
 'oaklib.implementations.neo4j',
 'oaklib.implementations.ols',
 'oaklib.implementations.ontobee',
 'oaklib.implementations.owlery',
 'oaklib.implementations.owlontology',
 'oaklib.implementations.pronto',
 'oaklib.implementations.robot',
 'oaklib.implementations.scigraph',
 'oaklib.implementations.skos',
 'oaklib.implementations.solor',
 'oaklib.implementations.solr',
 'oaklib.implementations.sparql',
 'oaklib.implementations.sqldb',
 'oaklib.implementations.tccm',
 'oaklib.implementations.ubergraph',
 'oaklib.implementations.umls',
 'oaklib.implementations.uniprot',
 'oaklib.implementations.wikidata',
 'oaklib.interfaces',
 'oaklib.utilities',
 'oaklib.utilities.graph',
 'oaklib.utilities.lexical',
 'oaklib.utilities.semsim',
 'oaklib.utilities.subsets']

package_data = \
{'': ['*']}

install_requires = \
['SPARQLWrapper>=2.0.0,<3.0.0',
 'SQLAlchemy>=1.4.32,<2.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'linkml-runtime>=1.2.3,<2.0.0',
 'networkx>=2.7.1,<3.0.0',
 'nxontology>=0.4.0,<0.5.0',
 'pronto>=2.4.4,<3.0.0',
 'ratelimit>=2.2.1,<3.0.0',
 'sssom>=0.3.7,<0.4.0']

entry_points = \
{'console_scripts': ['runoak = oaklib.cli:cli']}

setup_kwargs = {
    'name': 'oaklib',
    'version': '0.0.0',
    'description': 'Ontology Access Kit: Python library for common ontology operations over a variety of backends',
    'long_description': None,
    'author': 'cmungall',
    'author_email': 'cjm@berkeleybop.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
