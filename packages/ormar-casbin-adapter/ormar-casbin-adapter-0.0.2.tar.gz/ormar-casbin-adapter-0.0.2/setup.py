# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ormar_casbin_adapter']

package_data = \
{'': ['*']}

install_requires = \
['asynccasbin>=1.1.8,<2.0.0', 'ormar>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'ormar-casbin-adapter',
    'version': '0.0.2',
    'description': 'ormar casbin adapter',
    'long_description': 'ormar Adapter for PyCasbin\n====\n\n## Repo\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/shepilov-vladislav/ormar-casbin-adapter/Pytest?logo=github&style=for-the-badge)](https://github.com/shepilov-vladislav/ormar-casbin-adapter)\n[![Codecov](https://img.shields.io/codecov/c/github/shepilov-vladislav/ormar-casbin-adapter?logo=codecov&style=for-the-badge)](https://github.com/shepilov-vladislav/ormar-casbin-adapter)\n[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/shepilov-vladislav/ormar-casbin-adapter?logo=code%20climate&style=for-the-badge)](https://github.com/shepilov-vladislav/ormar-casbin-adapter)\n[![Dependabot](https://img.shields.io/badge/dependabot-Active-brightgreen?logo=dependabot&style=for-the-badge)](https://github.com/shepilov-vladislav/ormar-casbin-adapter)\n\n\n## GitHub\n\n[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/shepilov-vladislav/ormar-casbin-adapter?label=latest%20stable&sort=semver&style=for-the-badge)](https://github.com/shepilov-vladislav/ormar-casbin-adapter/releases)\n[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/shepilov-vladislav/ormar-casbin-adapter?label=latest%20unstable&style=for-the-badge)](https://github.com/shepilov-vladislav/ormar-casbin-adapter/releases)\n[![GitHub last commit](https://img.shields.io/github/last-commit/shepilov-vladislav/ormar-casbin-adapter?style=for-the-badge)](https://github.com/shepilov-vladislav/ormar-casbin-adapter/commits/master)\n\n## PyPI\n\n[![PyPI - Version](https://img.shields.io/pypi/v/ormar-casbin-adapter?style=for-the-badge)](https://pypi.org/project/ormar-casbin-adapter)\n[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/ormar-casbin-adapter?style=for-the-badge)](https://pypi.org/project/ormar-casbin-adapter)\n[![PyPI - Python Wheel](https://img.shields.io/pypi/wheel/ormar-casbin-adapter?style=for-the-badge)](https://pypi.org/project/ormar-casbin-adapter)\n[![PyPI - Format](https://img.shields.io/pypi/format/ormar-casbin-adapter?style=for-the-badge)](https://pypi.org/project/ormar-casbin-adapter)\n[![PyPI - Status](https://img.shields.io/pypi/status/ormar-casbin-adapter?style=for-the-badge)](https://pypi.org/project/ormar-casbin-adapter)\n[![PyPI - Downloads](https://img.shields.io/pypi/dd/ormar-casbin-adapter?style=for-the-badge)](https://pypi.org/project/ormar-casbin-adapter)\n[![PyPI - License](https://img.shields.io/pypi/l/ormar-casbin-adapter?style=for-the-badge)](https://pypi.org/project/ormar-casbin-adapter)\n\normar Adapter is the [ormar](https://collerek.github.io/ormar/) adapter for [PyCasbin](https://github.com/casbin/pycasbin). With this library, Casbin can load policy from ormar supported database or save policy to it.\n\nBased on [Officially Supported Databases](https://collerek.github.io/ormar/), The current supported databases are:\n\n- PostgreSQL\n- MySQL\n- SQLite\n\n## Installation\n\n```\npip install ormar_casbin_adapter\n```\n\nor\n\n```\npoetry add ormar-casbin-adapter\n```\n\n## Simple Example\n\n```python\nimport casbin\nimport databases\nimport ormar\nfrom ormar_casbin_adapter import DatabasesAdapter\nimport sqlalchemy\n\ndatabase = Database("sqlite://", force_rollback=True)\nmetadata = sqlalchemy.MetaData()\n\n\nclass CasbinRule(ormar.Model):\n    class Meta:\n        database = database\n        metadata = metadata\n        tablename = "casbin_rules"\n\n    id: int = ormar.Integer(primary_key=True)\n    ptype: str = ormar.String(max_length=255)\n    v0: str = ormar.String(max_length=255)\n    v1: str = ormar.String(max_length=255)\n    v2: str = ormar.String(max_length=255, nullable=True)\n    v3: str = ormar.String(max_length=255, nullable=True)\n    v4: str = ormar.String(max_length=255, nullable=True)\n    v5: str = ormar.String(max_length=255, nullable=True)\n\n\nadapter = DatabasesAdapter(model=CasbinRule)\n\ne = casbin.Enforcer("path/to/model.conf", adapter, True)\n\nsub = "alice"  # the user that wants to access a resource.\nobj = "data1"  # the resource that is going to be accessed.\nact = "read"  # the operation that the user performs on the resource.\n\nif e.enforce(sub, obj, act):\n    # permit alice to read data1ormar_casbin_adapter\n    pass\nelse:\n    # deny the request, show an error\n    pass\n```\n\n\n### Getting Help\n\n- [PyCasbin](https://github.com/casbin/pycasbin)\n\n### License\n\nThis project is licensed under the [Apache 2.0 license](LICENSE).\n',
    'author': 'Vladislav Shepilov',
    'author_email': 'shepilov.v@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shepilov-vladislav/ormar-casbin-adapter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
