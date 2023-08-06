# Notion automation utilities

**Note: Package in heavy development**

Installation:

```bash
    $ poetry add "auto_notion_py==0.1.3"
```

Quick exmple:

```python

from auto_notion_py.github.api import get_pull_requests_df, GHFetch, GHFetchOrg, GHFetchRepo
from auto_notion_py.notion.api import notion_db_push
from auto_notion_py.zotero.api import get_zotero_publications_df
import asyncio

# Query all Zotero publications and update the Notion database
zotero_df = await get_zotero_publications_df(
    zotero_api_key,
    zotero_db_id,
)
await notion_db_push(notion_token, notion_db_id_zotero_publications, zotero_df)

# Query all PRs and update the Notion database
all_prs_df = await get_pull_requests_df([
    GHFetch(
        token=github_token,
        creators=None,
        organizations=[
            GHFetchOrg(
                name="covid-genomics",
                creators=None,
                repositories=None,
            ),
        ],
    ),

])
await notion_db_push(notion_token, notion_db_id_pull_requests, all_prs_df)
```
