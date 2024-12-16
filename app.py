import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State, MATCH
from sqlalchemy import create_engine

from layout.navbar import navbar
from layout.filters import filters
from layout.dashboard import dashboard
from layout.about import about
import plotly.express as px
from utils.DataConnector import DataConnector
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64
from konlpy.tag import Okt
from collections import Counter


import openai
import os 

openai.api_key =  os.getenv('OPENAI_API_KEY')
data_connector = DataConnector()

initial_data = data_connector.get_default_data({
    "device": ["ios-all", "android-all"],
    "game": ["오딘: 발할라 라이징"],
    "rating": [1, 5],
    "start_date": '2024-10-01',
    "end_date": '2024-11-01',
    "language": ["ko"],
    "country": [],
})

initial_platforms = ["오딘: 발할라 라이징"]
plt.switch_backend('Agg')

print('INITIAL ', initial_data)
app = Dash(
    __name__,
    title="aibstract",
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200",
        "https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap",
    ]
    , suppress_callback_exceptions=True
)
server = app.server


app.layout = html.Div(
    [
        dcc.Store(
            id="filters-store",
            data={
                "device": ["ios-all", "android-all"],
                "game": ["오딘: 발할라 라이징"],
                "rating": [1, 5],
                "start_date": '2024-10-01',
                "end_date": '2024-11-01',
                "language": ["ko"],
                "country": [],
                "keyword" : ""
            },
        ),
        navbar,
        dbc.Container(
            dbc.Stack(
                [
                    dcc.Markdown(
                        "*이 앱의 데이터는 Data.ai API에서 가져옵니다.*",
                        link_target="_blank",
                        id="attribution",
                    ),
                    filters,
                    dashboard,
                    about
                ],
                gap=3,
            ),
            id="content",
            className="p-3",
        ),
    ],
    id="page",
)



# Layout callbacks
@app.callback(
    Output("filter-collapse", "is_open"),
    Input("filter-header-btn", "n_clicks"),
    State("filter-collapse", "is_open"),
)
def open_close_filter_collapse(n, current_state):
    if n == 0:
        raise dash.exceptions.PreventUpdate()
    return not current_state


@app.callback(
    Output("filter-header-icon", "children"), Input("filter-collapse", "is_open")
)
def switch_filter_header_icon(is_open):
    return "keyboard_arrow_up" if is_open else "keyboard_arrow_down"



@app.callback(
    Output({"type": "graph-modal", "index": MATCH}, "is_open"),
    Input({"type": "graph-info-btn", "index": MATCH}, "n_clicks"),
)
def show_graph_info_modals(n):
    if n == 0:
        raise dash.exceptions.PreventUpdate()
    return True



@app.callback(Output("about-modal", "is_open"), Input("page-info-btn", "n_clicks"))
def show_about_modal(n):
    if n == 0:
        raise dash.exceptions.PreventUpdate()
    return True



# Filter callbacks
@app.callback(Output("game", "options"), Input("game", "id"))
def populate_game_options(_):
    games = data_connector.get_available_games()
    return [{"label": i, "value": i} for i in sorted(games.game)]

@app.callback(Output("language", "options"), Input("language", "id"))
def populate_language_options(_):
    languages = data_connector.get_available_languages()
    return [{"label": i, "value": i} for i in sorted(languages.language)]

@app.callback(Output("country", "options"), Input("country", "id"))
def populate_country_options(_):
    countries = data_connector.get_available_countries()
    return [{"label": i, "value": i} for i in sorted(countries.country)]


@app.callback(
    Output("filters-store", "data"),
    Input("device", "value"),
    Input("game", "value"),
    Input("rating", "value"),
    Input("date", "start_date"),
    Input("date", "end_date"),
    Input("language", "value"),
    Input("country", "value"),
    Input("keyword", "value"),  # 키워드 입력 추가
    State("filters-store", "data"),
)
def update_filters_store(
    device, game, rating, start_date, end_date, language, country, keyword, data
):
    # 필터 값들을 업데이트
    data["device"] = device
    data["game"] = game
    data["rating"] = rating
    data["start_date"] = start_date
    data["end_date"] = end_date
    data["language"] = language
    data["country"] = country
    data["keyword"] = keyword  # 키워드 업데이트
    return data

@app.callback(
    Output("device", "value"),
    Output("game", "value"),
    Output("rating", "value"),
    Output("date", "start_date"),
    Output("date", "end_date"),
    Output("language", "value"),
    Output("country", "value"),
    Output("keyword", "value"),
    Input("clear-filters-btn", "n_clicks"),
)

def clear_all_filters(n):
    if n == 0:
        return [["ios-all", "android-all"], initial_platforms, [0, 5], '2024-10-01', '2024-11-01', ["ko"], [], ""]
    return [["ios", "android-all"], [], [0, 5], '2024-10-01', '2024-11-01', ["ko"], [], ""]



@app.callback(Output("filter-tooltip", "children"), Input("filter-collapse", "is_open"))
def change_tooltip_message(is_open):
    return "필터를 보지 않기 위해 hide 버튼을 클릭하세요" if is_open else "필터를 보기 위해 show 버튼을 클릭하세요"





# Metric card callbacks
@app.callback(
    Output({"type": "metric-value", "index": "reviews-count"}, "children"),
    Input("filters-store", "data"),
)
def display_review_count(filters):
    print(filters)
    review_count = data_connector.get_review_count(filters)
    return f"{review_count:,}"




@app.callback(
    Output({"type": "metric-value", "index": "avg-rating"}, "children"),
    Input("filters-store", "data"),
)
def display_avg_rating(filters):
    avg_rating = data_connector.get_avg_rating(filters)
    # avg_rating을 숫자로 변환
    try:
        avg_rating = float(avg_rating)
        return f"{avg_rating:,.2f}"  # 소수점 두 자리까지 표시
    except ValueError:
        return "N/A"





@app.callback(
    Output({"type": "line-graph", "index": "daily-posts"}, "figure"),
    Input("filters-store", "data"),
)
def update_daily_posts_graph(filters):
    # 일별 게시글 수 데이터 가져오기
    daily_counts = data_connector.get_daily_post_counts(filters)
    
    # 라인 그래프 생성
    fig = px.line(
        daily_counts,
        x='date',
        y='post_count',
        color='game',  # 게임별로 다른 색상 지정
        labels={'post_count': '게시글 수', 'date': '날짜', 'game': '게임'},
        template='plotly'
    )
    fig.update_layout(
        plot_bgcolor='white',  # 그래프 배경색을 하얀색으로 설정
        paper_bgcolor='white',
        xaxis_title='날짜',
        yaxis_title='게시글 수',
        hovermode='x unified',  # x축에 따라 호버 정보 통합
        margin=dict(l=20, r=20, t=30, b=20),  # 여백 설정
    )
    fig.update_traces(mode='lines+markers')
    
    return fig



@app.callback(
    Output({"type": "bar-graph", "index": "rating-counts"}, "figure"),
    Input("filters-store", "data"),
)
def update_rating_counts_graph(filters):
    # 평점별 리뷰 수 데이터 가져오기
    rating_counts = data_connector.get_rating_counts(filters)
    
    # 데이터가 비어 있는지 확인
    if rating_counts.empty:
        return go.Figure()  # 빈 Figure 반환
    
    # 바 그래프 생성
    fig = px.bar(
        rating_counts,
        x='rating',
        y='count',
        color='game',  # 게임별로 다른 색상 지정
        barmode='group',  # 바를 그룹으로 표시
        labels={'count': 'Review Count', 'rating': 'Rating', 'game': 'Game'},
        template='plotly'
    )
    
    # 그래프 레이아웃 설정
    fig.update_layout(
        xaxis_title='Rating',
        yaxis_title='Review Count',
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=30, b=20),
    )
    
    return fig



@app.callback(
    Output({"type": "wordcloud", "index": "wordcloud-graph"}, "figure"),
    Input("filters-store", "data"),
)
def update_wordcloud(filters):
    # 데이터에서 텍스트 부분 추출
    text_data = data_connector.get_word_cloudtext(filters)
    okt = Okt()
    nouns = okt.nouns(text_data)
    word_counts = Counter(nouns)
    
    # 워드클라우드 이미지 생성
    wordcloud = WordCloud(
        font_path='/Library/Fonts/KakaoRegular.ttf',
        background_color='white',
        width=4000,  # 너비 증가
        height=1600   # 높이 증가
    ).generate_from_frequencies(word_counts)

    # 이미지 버퍼에 저장
    buffer = io.BytesIO()
    plt.figure(figsize=(10, 3))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    # 이미지 데이터를 base64로 인코딩
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Plotly Figure로 변환
    fig = {
        "data": [{
            "type": "image",
            "source": f"data:image/png;base64,{img_base64}",
            "xref": "x",
            "yref": "y",
            "x": 0,
            "y": 0,
            "sizex": 1,
            "sizey": 1,
            "sizing": "stretch",
            "layer": "below"
        }],
        "layout": {
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
            "margin": {"l": 0, "r": 0, "t": 0, "b": 0}
        }
    }
    return fig




@app.callback(
    Output({"type": "markdown", "index": "summary-output"}, "children"),
    Input("filters-store", "data"),
)
def generate_summary(filters):
    # Define the prompt for review analysis
    prompt = (
        "You are a helpful review analyzer. You read app reviews formatted as `Game Name: Review`, "
        "with each game's reviews separated by a slash. Analyze the reviews to identify overall trends "
        "and provide insights in Korean in markdown format.\n\n"
        "If there is only one game, structure the analysis as follows:\n"
        "1. Summarize the **overall trends**.\n"
        "2. Provide **5 key takeaways (시사하는 점)** based on the analysis.\n"
        "3. Identify **5 frequently mentioned keywords** and summarize the reviews related to each keyword in detail.\n\n"
        "If there are multiple games, structure the analysis as follows:\n"
        "1. Analyze the **overall trends** for each game.\n"
        "2. Highlight **commonalities and differences** in reactions between games for each section (trends, takeaways, keywords).\n"
        "3. Use headers to distinguish the analysis for each game while noting shared themes and unique points.\n\n"
        "Use only `###` and `####` headers for structuring the content. Provide a detailed and thorough analysis in all cases, "
        "ensuring clarity and depth in your insights."
    )
    # Fetch the long text for analysis
    long_text = data_connector.get_game_long_text(filters)
    print("Fetched long_text for analysis.")

    # Call the OpenAI API to generate a summary
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"{long_text}"}
        ]
    )

    # Extract and return the summary content
    summary = response['choices'][0]['message']['content'].strip()
    print("Generated Summary:\n", summary)
    return summary




@app.callback(
    Output({"type": "markdown", "index": "summary-positive-output"}, "children"),
    Input("filters-store", "data"),
)
def generate_positive_summary(filters):
    long_text = data_connector.get_game_long_text(filters)
    print('long_text')
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful review analyzer. You read app reviews formatted as Game Name: Review separated by slash. Analyze the reviews for each game individually and extract positive insights only. Respond in Korean and in markdown format. Summarize why the feedback was positive in detail for each game with 5 key points. For a single key point (bold), include 3 bullet points as supporting details. only use h3 for game name and do not use other headers. Ensure the analysis is organized under each game name."},
            {"role": "user", "content": f"All reviews: {long_text}"}
        ]
    )
    summary = response.choices[0].message['content'].strip()
    print(summary)
    return summary



@app.callback(
    Output({"type": "markdown", "index": "summary-negative-output"}, "children"),
    Input("filters-store", "data"),
)
def generate_negative_summary(filters):
    long_text = data_connector.get_game_long_text(filters)
    print('long_text')
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful review analyzer. You read app reviews formatted as Game Name: Review separated by slash. Analyze the reviews for each game individually and extract negative insights only. Respond in Korean and in markdown format. Summarize why the feedback was negative in detail for each game with 5 key points. For a single key point (bold), include 3 bullet points as supporting details. only use h3 for game name and do not use other headers. Ensure the analysis is organized under each game name."},
            {"role": "user", "content": f"All reviews: {long_text}"}
        ]
    )
    summary = response.choices[0].message['content'].strip()
    print(summary)
    return summary


# 서버 실행
if __name__ == '__main__':
    app.run_server(debug=True)