import re
from pathlib import Path
from urllib.parse import unquote, urlparse, ParseResult
import mistletoe
from auto_notion_py.notion.page_client.block import EmbedOrUploadBlock, CollectionViewBlock, PageBlock
from auto_notion_py.notion.page_client.client import NotionClient
from .renderer import NotionPyRenderer


def get_relative_path_for_md_url(url, markdown_file_path):
    """
    Markdown images commonly referenence local files the URL portion but the URLs
    might not be valid file paths.
    Figure out the first valid file path by trying different permutations of the
    url parts
    @param {str} The url to parse
    @param {str} markdown_file_path The path to the file we're parsing, for relative paths
    @returns {None|Path} None of the url is not a valid local file path or is
    an external URL (http/https). Path path if it's valid
    """

    if '://' in url:
        # Try stripping file:// and decoding
        url_scheme = url[url.index('://')+3:]
        paths = [ Path(markdown_file_path).parent / Path(unquote(url_scheme)) ]
    else:
        # Try both the normal file, then the url decoded file
        paths = [
            Path(markdown_file_path).parent / Path(url),
            Path(markdown_file_path).parent / Path(unquote(url))
        ]

    for path in paths:
        # Test for validity (the try/except) and existance
        try:
            if path.exists():
                return path
            else:
                print(f"File not found '{path}'")
        except OSError as e:
            pass
    return None

def upload_md_block(block_descriptor, block_parent, markdown_file_path, image_path_provider_fn=None):
    """
    Uploads a single block_descriptor for NotionPyRenderer as the child of another block
    and does any post processing for Markdown importing
    @param {dict} block_descriptor A block descriptor, output from NotionPyRenderer
    @param {NotionBlock} block_parent The parent to add it as a child of
    @param {string} markdown_file_path The path to the markdown file to find images with
    @param {callable|None) [image_path_provider_fn=None] See upload()
    @todo Make markdown_file_path optional and don't do searching if not provided
    """
    block_class = block_descriptor["type"]
    del block_descriptor["type"]
    if "schema" in block_descriptor:
        collection_schema = block_descriptor["schema"]
        collection_rows = block_descriptor["rows"]
        del block_descriptor["schema"]
        del block_descriptor["rows"]
    block_children = None
    if "children" in block_descriptor:
        block_children = block_descriptor["children"]
        del block_descriptor["children"]
    new_block = block_parent.children.add_new(block_class, **block_descriptor)
    # Upload images to Notion.so that have local file paths
    # most of the time, this will be a standard ImageBlock; however some markdown
    # generators use the image syntax for general purpose "embedded" files; hence we
    # check for any subclass of EmbedOrUploadBlock (which provides upload_file)
    if issubclass(block_class, EmbedOrUploadBlock):
        image_relative_src = block_descriptor["source"]
        if re.search(r"(?<!file)://", image_relative_src, re.I):
            return #Don't upload images that are external urls

        if image_path_provider_fn: #Transform by image_path_provider_fn insteadif provided
            image_src = image_path_provider_fn(image_relative_src, markdown_file_path)
        else:
            image_src = get_relative_path_for_md_url(image_relative_src, markdown_file_path)
            if not image_src:
                print(f"ERROR: Local image '{image_relative_src}' not found to upload. Skipping...")
                return

        print(f"Uploading file '{image_src}'")
        new_block.upload_file(str(image_src))
    elif isinstance(new_block, CollectionViewBlock):
        #We should have generated a schema and rows for this one
        notion_client_instance = block_parent._client #Hacky internals stuff...
        new_block.collection = notion_client_instance.get_collection(
            #Low-level use of the API
            #TODO: Update when notion-py provides a better interface for this
            notion_client_instance.create_record("collection", parent=new_block, schema=collection_schema)
        )
        view = new_block.views.add_new(view_type="table")
        for row in collection_rows:
            new_row = new_block.collection.add_row()
            for idx, property_name in enumerate(prop["name"] for prop in collection_schema.values()):
                # TODO: If rows aren't uploading, check to see if there's special
                # characters that don't map to property_name in notion-py
                property_name = property_name.lower() #The actual prop name in notion-py is lowercase
                property_value = row[idx]
                setattr(new_row, property_name, property_value)
    if block_children:
        for child_block in block_children:
            upload_md_block(child_block, new_block, markdown_file_path, image_path_provider_fn)


def convert(input_markdown_file, notion_renderer=NotionPyRenderer):
    """
    Converts a input_markdown_file into an array of NotionBlock descriptors
    @param {file|string} input_markdown_file The file handle to a markdown file, or a markdown string
    @param {NotionPyRenderer} notion_renderer Class inheritting from the renderer
    incase you want to render the Markdown => Notion.so differently
    """
    return mistletoe.markdown(input_markdown_file, notion_renderer)

def upload(
    input_markdown_file,
    input_file_name,
    output_notion_block,
    image_path_provider_fn=None,
    notion_renderer=NotionPyRenderer,
    overwrite_content=False,
):
    """
    Uploads a single markdown file at markdown_file_path to Notion.so as a child of
    output_notion_block.
    @param {file} input_markdown_file The file handle to a markdown file
    @param {NotionBlock} output_notion_block The Notion.so block to add the markdown to
    @param {callable|None) [image_path_provider_fn=None] Function taking image source and markdown_file_path
    to transform the relative image paths by if necessary (useful if your images are stored in weird
    locations relative to your md file. Should return a pathlib.Path
    @param {NotionPyRenderer} notion_renderer Class inheritting from the renderer
    incase you want to render the Markdown => Notion.so differently
    """
    # Convert the Markdown file
    rendered = convert(input_markdown_file, notion_renderer)

    if overwrite_content:
        for child in output_notion_block.children:
            child.remove()

    # Upload all the blocks
    for idx, block_descriptor in enumerate(rendered):
        pct = (idx+1)/len(rendered) * 100
        print(f"\rUploading {block_descriptor['type'].__name__}, {idx+1}/{len(rendered)} ({pct:.1f}%)", end='')
        upload_md_block(block_descriptor, output_notion_block, input_file_name, image_path_provider_fn)




