import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

class MarkdownCard(dbc.Card):
    def __init__(self, title, id, content=None, description=None):
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
                            id={"type": "markdown-info-btn", "index": id},
                            n_clicks=0,
                            color="light",
                        ),
                    ],
                    className="d-flex justify-content-between align-center p-3",
                    style={"backgroundColor": "#f8f9fa"},  # 밝은 회색 배경
                ),
                dbc.Spinner(
                    dcc.Markdown(
                        children=description,  # description을 children으로 설정
                        id={"type": "markdown", "index": id},
                        style={"padding": "15px", "margin": "15px"},  # 패딩 추가
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
                    id={"type": "markdown-modal", "index": id},
                    is_open=False,
                    size="md",
                ),
            ],
            className="mb-3 markdown-card",
            style={"border": "1px solid #dee2e6", "borderRadius": "0.5rem"},  # 카드 테두리와 둥근 모서리
        )