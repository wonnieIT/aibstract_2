import json
import dash_bootstrap_components as dbc
from dash import html, dcc

from .components.MetricCard import MetricCard
from .components.FigureCard import FigureCard
from .components.LineGraphCard import LineGraphCard
from .components.WordCloudCard import WordCloudCard
from .components.BarGraphCard import BarGraphCard
from .components.MarkdownCard import MarkdownCard 


with open("assets/figure_descriptions.json", "r") as f:
    figure_descriptions = json.load(f)

dashboard = dbc.Row(
    dbc.Col(
        [
            dbc.Row(
                [
                    dbc.Col(MetricCard("해당 기간 리뷰 수", id="reviews-count"), width=4),
                    dbc.Col(MetricCard("평점", id="avg-rating"), width=4)
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        LineGraphCard(
                            title = "일별 리뷰 수",
                            id="daily-posts",
                            description=figure_descriptions.get("daily-posts"),
                        ),
                        sm=12,
                        md=7,
                    ),
                    dbc.Col(
                        BarGraphCard(
                            title ="Rating Distribution",
                            id="rating-counts"
                        ),
                        sm=12,
                        md=5,
                    ),
                ],
                className="dashboard-row",
            ),
            dbc.Row(
                dbc.Col(
                    WordCloudCard(
                        "Word Cloud",
                        id="wordcloud-graph",
                        description=figure_descriptions.get("wordcloud-graph")
                    ),
                    width=12,
                ),
                className="dashboard-row",
            ),
            dbc.Row(
                dbc.Col(
                    MarkdownCard(
                        title="동향 요약",  # 카드의 제목
                        id="summary-output",  # 카드의 ID
                        content="",  # 초기 내용은 비워둡니다.
                        description="이 섹션은 요약된 내용을 보여줍니다.",  # 설명
                    ),
                    width=12
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        MarkdownCard(
                            title="긍정 요약",  # 카드의 제목
                            id="summary-positive-output",  # 카드의 ID
                            content="",  # 초기 내용은 비워둡니다.
                            description="이 섹션은 요약된 내용을 보여줍니다."
                        ),
                        sm=12,
                        md=6
                    ),
                    dbc.Col(
                        MarkdownCard(
                            title="부정 요약",  # 카드의 제목
                            id="summary-negative-output",  # 카드의 ID
                            content="",  # 초기 내용은 비워둡니다.
                            description="이 섹션은 요약된 내용을 보여줍니다."
                        ),
                        sm=12,
                        md=6
                    )
                ]
            ),
            
        ],
    ),
    id="dashboard"
)
