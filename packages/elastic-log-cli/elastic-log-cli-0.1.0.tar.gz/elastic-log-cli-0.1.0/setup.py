# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elastic_log_cli', 'elastic_log_cli.kql', 'elastic_log_cli.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0',
 'elasticsearch>=7,<8',
 'lark>=1.1.1,<2.0.0',
 'pydantic>=1.9.0,<2.0.0']

entry_points = \
{'console_scripts': ['elastic-logs = elastic_log_cli.__main__:run_cli']}

setup_kwargs = {
    'name': 'elastic-log-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': "# Elastic Log CLI\n\nCLI for streaming logs from Elasticsearch to a terminal.\n\n## Installation\n\nThis project is not currently packaged and so must be installed manually.\n\nClone the project with the following command:\n```\ngit clone https://github.com/jacksmith15/elastic-log-cli.git\n```\n\n## Configuration\n\nThe following environment variables are used to configure the tool. For secure, easy selection of target clusters, a tool like [envchain](https://github.com/sorah/envchain) is recommended.\n\n<!-- generated env. vars. start -->\n### `ELASTICSEARCH_URL`\n\n**Required**\n\nURL of the Elasticsearch cluster containing logs. You can also provide an Elastic Cloud ID by prefixing with it `cloud:`.\n\n### `ELASTICSEARCH_USERNAME`\n\n*Optional*\n\nUsername for the Elasticsearch cluster containing logs.\n\n### `ELASTICSEARCH_PASSWORD`\n\n*Optional*\n\nPassword for the Elasticsearch cluster containing logs.\n\n### `ELASTICSEARCH_AUTH_MODE`\n\n*Optional*, default value: `basicauth`\n\nWhether to authenticate using Basic Auth or an API Key. If using `apikey`, provide as follows:\n\n```\nELASTICSEARCH_USERNAME=${APIKEY_NAME}\nELASTICSEARCH_PASSWORD=${APIKEY_KEY}\n```\n\n#### Possible values\n\n`basicauth`, `apikey`\n\n### `ELASTICSEARCH_TIMEOUT`\n\n*Optional*, default value: `40`\n\nHow long to wait on Elasticsearch requests.\n<!-- generated env. vars. end -->\n\n## Usage\n\n<!-- generated usage start -->\n```\nUsage: elastic-logs [OPTIONS] QUERY\n\n  Stream logs from Elasticsearch.\n\n  Accepts a KQL query as its only positional argument.\n\nOptions:\n  -p, --page-size INTEGER RANGE  The number of logs to fetch per page  [x>=0]\n  -i, --index TEXT               The index to target. Globs are supported.\n  -s, --start TEXT               When to begin streaming logs from.\n  -e, --end TEXT                 When to stop streaming logs. Omit to\n                                 continuously stream logs until interrupted.\n  --source CSV                   Source fields to retrieve, comma-separated.\n                                 Default behaviour is to fetch full document.\n  -t, --timestamp-field TEXT     The field which denotes the timestamp in the\n                                 indexed logs.\n  --version                      Show version and exit.\n  --help                         Show this message and exit.\n\n```\n<!-- generated usage end -->\n\n\n### Example\n\n```shell\nelastic-logs \\\n    --start 2022-03-05T12:00:00 \\\n    --end 2022-03-05T13:00:00 \\\n    --source time,level,message,error \\\n    --index filebeat-7.16.2 \\\n    --timestamp-field time \\\n    'level:ERROR and error.code:500'\n```\n\n### KQL support\n\nThe following KQL features are not yet supported:\n\n- Wildcard fields, e.g. `*:value` or `machine.os*:windows 10`\n- Prefix matching, e.g. `machine.os:win*`\n\n\n## Development\n\nInstall dependencies:\n\n```shell\npyenv shell 3.10.x\npre-commit install  # Configure commit hooks\npoetry install  # Install Python dependencies\n```\n\nRun tests:\n\n```shell\npoetry run inv verify\n```\n\n# License\nThis project is distributed under the MIT license.\n",
    'author': 'Jack Smith',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jacksmith15/elastic-log-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
