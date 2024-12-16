import dash_bootstrap_components as dbc
from dash import html, dcc

filters = dbc.Row(
    dbc.Col(
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        dbc.Tooltip(
                            "필터를 보기 위해 클릭하세요",
                            id="filter-tooltip",
                            placement="left",
                            target="filter-header-btn",
                        ),
                        dbc.Button(
                            [
                                html.P("Filters", className="m-0"),
                                html.Span(
                                    "keyboard_arrow_down",
                                    id="filter-header-icon",
                                    className="material-symbols-outlined",
                                ),
                            ],
                            id="filter-header-btn",
                            className="w-100 p-3 d-flex justify-content-between",
                            color="light",
                            n_clicks=0,
                        ),
                    ],
                    className="p-0 m-0",
                ),
                dbc.Collapse(
                    dbc.CardBody(
                        dbc.Stack(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Label(
                                                    "스토어 Type",
                                                    html_for="device",
                                                ),
                                                dcc.Checklist(
                                                    ["ios-all",'android-all'],
                                                     ["ios-all",'android-all'],
                                                    id="device",
                                                    className="d-flex justify-content-evenly",
                                                    inline=True,
                                                ),
                                            ],
                                            md=3,
                                            sm=12,
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Label(
                                                    "게임 명",
                                                    html_for="game",
                                                ),
                                                dcc.Dropdown(
                                                    id="game", multi=True, value=[]
                                                ),
                                            ],
                                            md=9,
                                            sm=12,
                                        ),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Label(
                                                    "Rating",
                                                    html_for="rating",
                                                ),
                                                dcc.RangeSlider(
                                                    1,
                                                    5,
                                                    1,
                                                    marks=None,
                                                    tooltip={
                                                        "placement": "bottom",
                                                        "always_visible": True,
                                                    },
                                                    value=[1,5],
                                                    id="rating",
                                                ),
                                            ],
                                            md=4,
                                            sm=12,
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Label(
                                                    "기간",
                                                    html_for="date",
                                                ),
                                                dcc.DatePickerRange(
                                                    start_date='2024-10-01',
                                                    end_date='2024-11-01',
                                                    display_format='YYYY-MM-DD',
                                                    id="date",
                                                ),
                                            ],
                                            md=8,
                                            sm=12,
                                        ),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Label(
                                                    "Language",
                                                    html_for="language",
                                                ),
                                                dcc.Dropdown(
                                                    id="language", multi=True, value=["ko"]
                                                ),
                                            ],
                                            md=6,  # md 크기 조정
                                            sm=12,
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Label(
                                                    "Country",
                                                    html_for="country",
                                                ),
                                                dcc.Dropdown(
                                                    id="country", multi=True, value=[]
                                                ),
                                            ],
                                            md=6,  # md 크기 조정
                                            sm=12,
                                        ),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                             dcc.Input(
                                                    id="keyword",
                                                    type="text",
                                                    placeholder="Enter a keyword",
                                                    style={"width": "100%"}
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    dbc.Col(
                                        dbc.Button(
                                            "필터 리셋",
                                            id="clear-filters-btn",
                                            color="link",
                                            n_clicks=0,
                                        ),
                                        className="d-flex justify-content-end",
                                    )
                                ),
                            ],
                            gap=3,
                        )
                    ),
                    id="filter-collapse",
                    is_open=False,
                ),
            ]
        )
    ),
    id="filters",
)