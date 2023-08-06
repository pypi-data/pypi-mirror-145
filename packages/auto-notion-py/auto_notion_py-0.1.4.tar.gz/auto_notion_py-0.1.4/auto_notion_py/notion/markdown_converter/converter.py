from io import StringIO
from notion_client import AsyncClient
from auto_notion_py.notion.page_client.client import NotionClient
from auto_notion_py.notion.page_client.block import PageBlock
from .uploader import upload


async def push_notion_page(
    client: AsyncClient,
    auth: str,
    page_id: str,
    content: str,
    overwrite_content: bool = False,
):
    page_url = (await client.pages.retrieve(page_id=page_id))["url"]

    # Follow the instructions at https://github.com/jamalex/notion-py#quickstart to setup Notion.py
    sub_client = NotionClient(token_v2=auth)
    page = sub_client.get_block(page_url)

    input_file = StringIO(content)
    upload(
        input_markdown_file=input_file,
        input_file_name="input.md",
        output_notion_block=page,
        overwrite_content=overwrite_content,
    )

