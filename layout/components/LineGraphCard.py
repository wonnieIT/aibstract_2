import dash
import dash_bootstrap_components as dbc
from dash import html, dcc


class LineGraphCard(dbc.Card):
    def __init__(self, title, id, description=None):
        super().__init__(
            children=[
                html.Div(
                    [
                        html.H5(title, className="m-0 align-center"),
                        dbc.Button(
                            html.Span(
                                "help",
                                className="material-symbols-outlined d-flex",
                            ),
                            id={"type": "graph-info-btn", "index": id},
                            n_clicks=0,
                            color="light",
                        ),
                    ],
                    className="d-flex justify-content-between align-center p-3",
                    style={"backgroundColor": "#f8f9fa"},  # 밝은 회색 배경
                ),
                dbc.Spinner(
                    dcc.Graph(
                        id={"type": "line-graph", "index": id},
                        responsive=True,
                        style={"height": "100%", "backgroundColor": "white"},  # 하얀 배경
                    ),
                    size="lg",
                    color="dark",
                    delay_show=750,
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(html.H4(title)),
                        dbc.ModalBody(dcc.Markdown(description, link_target="_blank")),
                    ],
                    id={"type": "graph-modal", "index": id},
                    is_open=False,
                    size="md",
                ),
            ],
            className="mb-3 line-graph-card",
            style={"border": "1px solid #dee2e6", "borderRadius": "0.5rem"},  # 카드 테두리와 둥근 모서리
        )