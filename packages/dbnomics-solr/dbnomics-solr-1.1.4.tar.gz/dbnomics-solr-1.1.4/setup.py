# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbnomics_solr', 'dbnomics_solr.services']

package_data = \
{'': ['*']}

install_requires = \
['daiquiri>=3.0.1,<4.0.0',
 'dbnomics-data-model>=0.13.24,<0.14.0',
 'dirhash>=0.2.1,<0.3.0',
 'environs>=9.5.0,<10.0.0',
 'orjson>=3.6.7,<4.0.0',
 'pysolr>=3.9.0,<4.0.0',
 'python-slugify>=6.1.1,<7.0.0',
 'requests>=2.27.1,<3.0.0',
 'solrq>=1.1.1,<2.0.0',
 'tenacity>=8.0.1,<9.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['dbnomics-solr = dbnomics_solr.cli:app']}

setup_kwargs = {
    'name': 'dbnomics-solr',
    'version': '1.1.4',
    'description': 'Index DBnomics data with Apache Solr for full-text and faceted search',
    'long_description': '# DBnomics Solr\n\nIndex DBnomics data into Apache Solr for full-text and faceted search.\n\nRequirements:\n\n- a running instance of [Apache Solr](http://lucene.apache.org/solr/); at the time this documentation is written, we use the version 7.3.\n\nSee [dbnomics-docker](https://git.nomics.world/dbnomics/dbnomics-docker) to run a local DBnomics instance with Docker that includes a service for Apache Solr.\n\n## Configuration\n\nEnvironment variables:\n\n- `DEBUG_PYSOLR`: display pysolr DEBUG logging messages (cf <https://github.com/django-haystack/pysolr>)\n\n## Index a provider\n\nReplace `wto` by the real provider slug in the following command:\n\n```bash\ndbnomics-solr index-provider /path/to/wto-json-data\n```\n\n### Full mode vs incremental mode\n\nWhen data is stored in a regular directory, the script always indexes all datasets and series of a provider. This is called _full mode_.\n\nWhen data is stored in a Git repository, the script runs by default in _incremental mode_: it indexes only the datasets modified since the last indexation.\n\nIt is possible to force the _full mode_ with the `--full` option.\n\n### Bare repositories\n\nThe script has an option `--bare-repo-fallback` which tries to add `.git` at the end of the storage dir name, if not found.\n\n## Remove all data from a provider\n\nTo remove all the documents related to a provider (`type:provider`, `type:dataset` and `type:series`):\n\n```bash\ndbnomics-solr --debug delete-provider --code <provider_code>\ndbnomics-solr --debug delete-provider --slug <provider_slug>\n\n# Examples:\ndbnomics-solr --debug delete-provider --code WTO\ndbnomics-solr --debug delete-provider --slug wto\n```\n',
    'author': 'Christophe Benz',
    'author_email': 'christophe.benz@nomics.world',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.nomics.world/dbnomics/dbnomics-solr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
