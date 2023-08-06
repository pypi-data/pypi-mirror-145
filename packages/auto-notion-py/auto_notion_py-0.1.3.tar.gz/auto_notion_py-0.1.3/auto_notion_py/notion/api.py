from notion_client import AsyncClient
import pandas as pd
from typing import Optional, Dict, List
from dataclasses import dataclass
from enum import Enum
import moment
import re
import asyncio

from .markdown_converter import push_notion_page, embed_notion_plotly

class ColumnType(Enum):
    COL_TITLE = 1
    COL_DATE = 2
    COL_URL = 3
    COL_MULTI_SELECT = 4
    COL_TEXT = 5
    COL_NUMBER = 6
    COL_SELECT = 7

@dataclass
class NotionColumn:
    notion_name: str
    data_name: str
    type: ColumnType

def normalize_df_column_name(name: str) -> str:
    new_name = name.replace(" ", "_").replace("-", "_").lower()
    return re.sub("[^0-9a-zA-Z]+", "", new_name)

def find_matching_df_column(df: pd.DataFrame, name: str) -> Optional[str]:
    norm_name = normalize_df_column_name(name)
    for col in df.columns:
        if norm_name == normalize_df_column_name(col):
            return col
    return None

async def infer_notion_columns(
    auth: str,
    db_id: str,
    data: pd.DataFrame,
    db = None,
) -> List[NotionColumn]:
    if db is None:
        notion = AsyncClient(auth=auth)
        db = await notion.databases.query(db_id)
    cols: List[NotionColumn] = []
    props = db["results"][0]["properties"]
    for prop_name in props.keys():
        prop = props[prop_name]

        col_type: Optional[ColumnType] = None
        notion_name = prop_name
        data_name = find_matching_df_column(data, notion_name)
        
        col_type_name = prop["type"]
        if col_type_name == "title":
            col_type=ColumnType.COL_TITLE
        elif col_type_name == "rich_text":
            col_type=ColumnType.COL_TEXT
        elif col_type_name == "url":
            col_type=ColumnType.COL_URL
        elif col_type_name == "multi_select":
            col_type=ColumnType.COL_MULTI_SELECT
        elif col_type_name == "select":
            col_type=ColumnType.COL_SELECT
        elif col_type_name == "number":
            col_type=ColumnType.COL_NUMBER
        elif col_type_name == "date":
            col_type=ColumnType.COL_DATE
        if col_type and data_name:
            cols.append(NotionColumn(notion_name=notion_name, data_name=data_name, type=col_type))
    return cols


async def notion_page_push(
    auth: str,
    user_token: str,
    page_id: str,
    markdown_text: str,
    overwrite_content: bool = False,
):
    client = AsyncClient(auth=auth)
    await push_notion_page(
        client=client,
        auth=user_token,
        page_id=page_id,
        content=markdown_text,
        overwrite_content=overwrite_content,
    )


async def notion_db_push(
    auth: str,
    db_id: str,
    data: pd.DataFrame,
    columns: Optional[List[NotionColumn]] = None,
):
    notion = AsyncClient(auth=auth)
    db = await notion.databases.query(db_id)

    if columns is None:
        columns = await infer_notion_columns(
            auth=auth,
            db_id=db_id,
            data=data,
            db=db,
        )
    print(columns)

    rows = []
    for index in range(len(data)):
        new_row = dict()
        for col in columns:
            val = data[col.data_name].values[index]
            prop = None
            val = str(val)
            if len(val) == 0:
                continue
            if col.type == ColumnType.COL_TITLE:
                prop = {'type': 'title', 'title': [{'type': 'text', 'text': {'content': val, 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': val, 'href': None}]}
            elif col.type == ColumnType.COL_NUMBER:
                if isinstance(val, str):
                    val = int(val)
                prop = {'type': 'number', 'number': val}
            elif col.type == ColumnType.COL_TEXT:
                prop = {'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': val, 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': val, 'href': None}]}
            elif col.type in [ColumnType.COL_MULTI_SELECT, ColumnType.COL_SELECT]:
                try:
                    new_val = pd.eval(val)
                    val = new_val
                except Exception:
                    pass
                if isinstance(val, str):
                    val = [str(val)]
                elif isinstance(val, list):
                    pass
                else:
                    try:
                        val = [str(item) for item in val]
                    except Exception:
                        val = [str(val)]
                # Map all values now
                val_objs = []
                for item in val:
                    val_objs.append({'name': item})
                if col.type == ColumnType.COL_MULTI_SELECT:
                    prop = {'type': 'multi_select', 'multi_select': val_objs}
                elif col.type == ColumnType.COL_SELECT:
                    if len(val_objs) > 0:
                        prop = {'type': 'select', 'select': val_objs[0]}
                    else:
                        prop = {'type': 'select', 'select': None}
                else:
                    raise Exception("Invalid condition")
            elif col.type == ColumnType.COL_DATE:
                if hasattr(val, "to_pydatetime"):
                    val = val.to_pydatetime()
                val = moment.date(val).format('YYYY-MM-DD')
                prop = {'type': 'date', 'date': {'start': val, 'end': None, 'time_zone': None}}
                #prop = {'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': val, 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': val, 'href': None}]}
            elif col.type == ColumnType.COL_URL:
                prop = {'type': 'url', 'url': val}
            else:
                raise Exception(f'Invalid column type was specified: {col.data_name} of type {col.type}')
            new_row[col.notion_name] = prop
        rows.append(new_row)
    existing_rows = db["results"]
    
    promises = []
    for (index, new_row) in enumerate(rows):
        if index >= len(existing_rows):
            break
        row = rows[index]
        for (p, val) in row.items():
            existing_p = existing_rows[index]["properties"]
            pid = existing_p[p]["id"]
            existing_p[p] = val
            existing_p[p]["id"] = pid
        promises.append(notion.pages.update(existing_rows[index]["id"], properties=existing_p))

    for index in range(len(existing_rows), len(rows)):
        promises.append(notion.pages.create(parent=dict(database_id=db_id), properties=rows[index]))

    for index in range(len(rows), len(existing_rows)):
        promises.append(notion.pages.update(existing_rows[index]["id"], archived=True))
        
    await asyncio.gather(*promises)
