# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auto_notion_py',
 'auto_notion_py.github',
 'auto_notion_py.notion',
 'auto_notion_py.notion.markdown_converter',
 'auto_notion_py.notion.page_client',
 'auto_notion_py.zotero']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.55,<2.0',
 'aiomultiprocess>=0.9.0,<0.10.0',
 'bs4>=0.0.1,<0.0.2',
 'cached-property>=1.5.2,<2.0.0',
 'chart-studio>=1.1.0,<2.0.0',
 'commonmark>=0.9.1,<0.10.0',
 'dictdiffer>=0.9.0,<0.10.0',
 'githubpy>=1.1.0,<2.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'mistletoe>=0.8.2,<0.9.0',
 'moment>=0.12.1,<0.13.0',
 'notion-client>=0.8.0,<0.9.0',
 'pandas>=1.3.5,<2.0.0',
 'plotly>=5.6.0,<6.0.0',
 'python-slugify>=6.1.1,<7.0.0',
 'pyzotero>=1.5.1,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'tzlocal>=4.2,<5.0']

entry_points = \
{'console_scripts': ['publish = publish:publish']}

setup_kwargs = {
    'name': 'auto-notion-py',
    'version': '0.1.3',
    'description': 'Notion automation package',
    'long_description': '# Notion automation utilities\n\n**Note: Package in heavy development**\n\nInstallation:\n\n```bash\n    $ poetry add "auto_notion_py==0.1.3"\n```\n\nQuick exmple:\n\n```python\n\nfrom auto_notion_py.github.api import get_pull_requests_df, GHFetch, GHFetchOrg, GHFetchRepo\nfrom auto_notion_py.notion.api import notion_db_push\nfrom auto_notion_py.zotero.api import get_zotero_publications_df\nimport asyncio\n\n# Query all Zotero publications and update the Notion database\nzotero_df = await get_zotero_publications_df(\n    zotero_api_key,\n    zotero_db_id,\n)\nawait notion_db_push(notion_token, notion_db_id_zotero_publications, zotero_df)\n\n# Query all PRs and update the Notion database\nall_prs_df = await get_pull_requests_df([\n    GHFetch(\n        token=github_token,\n        creators=None,\n        organizations=[\n            GHFetchOrg(\n                name="covid-genomics",\n                creators=None,\n                repositories=None,\n            ),\n        ],\n    ),\n\n])\nawait notion_db_push(notion_token, notion_db_id_pull_requests, all_prs_df)\n```\n',
    'author': 'Piotr Styczyński',
    'author_email': 'pstyczynski@sumologic.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
