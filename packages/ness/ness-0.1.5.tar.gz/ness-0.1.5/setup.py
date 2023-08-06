# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ness']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.0', 'pandas>=0.18.1']

entry_points = \
{'console_scripts': ['ness = ness.cli:main']}

setup_kwargs = {
    'name': 'ness',
    'version': '0.1.5',
    'description': 'A Python datalake client.',
    'long_description': '# Ness\n\n<p align="center">\n    <em>A Python datalake client.</em>\n</p>\n<p align="center">\n    <a href="https://github.com/postpayio/ness/actions">\n        <img src="https://github.com/postpayio/ness/actions/workflows/test-suite.yml/badge.svg" alt="Test">\n    </a>\n    <a href="https://codecov.io/gh/postpayio/ness">\n        <img src="https://img.shields.io/codecov/c/github/postpayio/ness?color=%2334D058" alt="Coverage">\n    </a>\n    <a href="https://pypi.org/project/ness">\n        <img src="https://img.shields.io/pypi/v/ness" alt="Package version">\n    </a>\n</p>\n\n## Requirements\n\n- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)\n\n## Installation\n\n```sh\npip install pyarrow ness\n```\n\n## Quickstart\n\n```py\nimport ness\n\ndl = ness.dl(bucket="mybucket", key="mydatalake")\ndf = dl.read("mytable")\n```\n\n## Sync\n\n```py\n# Sync all tables\ndl.sync()\n\n# Sync a single table\ndl.sync("mytable")\n\n# Sync and read a single table\ndf = dl.read("mytable", sync=True)\n```\n\n## Format\n\nSpecify the input data source format, the default format is `parquet`:\n\n```py\nimport ness\n\ndl = ness.dl(bucket="mybucket", key="mydatalake", format="csv")\n```\n\n## AWS Profile\n\nFiles are synced using `default` AWS profile, you can configure another one:\n\n```py\nimport ness\n\ndl = ness.dl(bucket="mybucket", key="mydatalake", profile="myprofile")\n```\n\n## Command Line\n\n```\nUsage: ness sync [OPTIONS] S3_URI\n\nOptions:\n  --format TEXT   Data lake source format.\n  --profile TEXT  AWS profile.\n  --table TEXT    Table name to sync.\n  --help          Show this message and exit.\n```\n\n```sh\nness sync bucket/key --table mytable\n```\n',
    'author': 'Dani',
    'author_email': 'dani@postpay.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/postpayio/ness',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
