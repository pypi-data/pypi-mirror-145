import chart_studio
import os

if "PLOTLY_API_KEY" in os.environ and "PLOTLY_USERNAME" in os.environ:
    chart_studio.tools.set_credentials_file(
        username=os.environ["PLOTLY_USERNAME"],
        api_key=os.environ["PLOTLY_API_KEY"],
    )
    chart_studio.tools.set_config_file(
        sharing='secret',
        world_readable=False,
    )

import chart_studio.plotly as py
import plotly.graph_objects as go

def embed_notion_plotly(fig, name: str):
    url = py.plot(fig, filename=name, sharing='public', auto_open=False)
    return f"![plotly:{name}]({url})"
