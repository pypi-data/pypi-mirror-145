from pyzotero import zotero
import pandas as pd
import moment
import datetime
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class ZoteroDocumentData:
    created_at: datetime.datetime
    accessed_at: datetime.datetime
    url: str
    title: str
    added_by: str
    creator_summary: str
    creators: List[str]
    publication_title: str
    abstract: str
    journal: str

def process_zotero_item(data, meta) -> ZoteroDocumentData:
    title = data["title"]
    accessed_at = moment.date(data["accessDate"]).datetime
    created_at = moment.date(data["accessDate"]).datetime
    added_by = meta["createdByUser"]["username"]
    if "creatorSummary" in meta:
        creator_summary = meta["creatorSummary"]
    else:
        creator_summary = ""
    if "creators" in data:
        creators = [f"{creator['firstName']} {creator['lastName']}" for creator in data["creators"]]
    else:
        creators = []
    publication_title = data["publicationTitle"] if "publicationTitle" in data else ""
    journal = data["journalAbbreviation"] if "journalAbbreviation" in data else ""
    abstract = data["abstractNote"] if "abstractNote" in data else ""
    url = data["url"]
    if "filename" in data:
        filename = data["filename"].replace(".pdf", "")
        title = f"{title} ({filename})"
    
    return ZoteroDocumentData(
        title=title,
        accessed_at=accessed_at,
        created_at=created_at,
        url=url,
        added_by=added_by,
        creator_summary=creator_summary,
        creators=creators,
        publication_title=publication_title,
        abstract=abstract,
        journal=journal,
    )

def merge_items(a, b):
    a_data = a["data"]
    b_data = b["data"]
    if "contentType" not in a_data and "contentType" not in b_data:
        pass
    elif "contentType" not in a_data and "contentType" in b_data:
        pass
    elif "contentType" in a_data and "contentType" not in b_data:
        a, b = b, a
    else:
        content_type_a = a["data"]["contentType"]
        content_type_b = b["data"]["contentType"]
        if content_type_a == "application/pdf" and content_type_b != "application/pdf":
            a, b = b, a
        
    # a is weak
    a_data = a["data"]
    a_meta = a["meta"]
    for key in b:
        a[key] = b
    a["meta"] = {**a_meta, **b["meta"]}
    a["data"] = {**a_data, **b["data"]}
    return a


async def get_zotero_publications_df(
    token: str,
    library_id: int,
    library_type: str = "group",
) -> pd.DataFrame:
    lib = zotero.Zotero(library_id, library_type, token)    
    items = list(lib.items())
        
    new_items = []
    items_map = dict()
    for item in items:
        if "up" in item["links"]:
            up_link = item["links"]["up"]["href"]
            if up_link in items_map:
                items_map[up_link] = merge_items(items_map[up_link], item)
            else:
                items_map[up_link] = item 
        else:
            new_items.append(item)
    for item_key in items_map.keys():
        new_items.append(items_map[item_key])
    items = new_items
    
    rows: List[ZoteroDocumentData] = []
    for item in items:
        if "title" not in item["data"]:
            continue
        rows.append(process_zotero_item(item["data"], item["meta"]))
    return pd.DataFrame(rows)

    
