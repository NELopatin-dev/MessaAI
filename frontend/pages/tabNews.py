from frontend import page_generator as pg 
from dash import html
import pandas as pd
import datetime
import dash_bootstrap_components as dbc

def build(app):

    news_list = app.modules['newsParser'].getNews()
    
    other_news_positive = []
    other_news_negative = []

    news_df = pd.DataFrame(news_list)
    news_df['sentiment'] = None

    for i, news in enumerate(news_list):       
        res = app.modules['sentiment'].predict(
            news['full_content']
        )

        sentiment = 'Позитивная новость' if res.index(max(res)) == 0 else 'Негативная новость'
        news_df.loc[news_df['link'] == news['link'], 'sentiment'] = res.index(max(res))

        if sentiment == 'Позитивная новость':
            other_news_positive.append(
                html.Div(
                    className='news__other_news_card',
                    children=[
                        html.Img(
                            className='news__main_news__img',
                            src=news['img_link']
                        ),
                        html.H5(
                            className='news__other_news__title',
                            children=[news['title']]
                        ),
                        html.Div(
                            className='news__other_news__bottom',
                            children=[
                                html.P(
                                    className='news__other_news__sentiment',
                                    children=[sentiment],
                                ),
                                html.A(
                                    className='news__other_news__link',
                                    children=['Подробнее'],
                                    href=news['link'],
                                    target='_blank'
                                )
                            ]
                        )
                    ]
                )
            )
        elif sentiment == 'Негативная новость':
            other_news_negative.append(
                html.Div(
                    className='news__other_news_card',
                    children=[
                        html.Img(
                            className='news__main_news__img',
                            src=news['img_link']
                        ),
                        html.H5(
                            className='news__other_news__title',
                            children=[news['title']]
                        ),
                        html.Div(
                            className='news__other_news__bottom',
                            children=[
                                html.P(
                                    className='news__other_news__sentiment',
                                    children=[sentiment],
                                ),
                                html.A(
                                    className='news__other_news__link',
                                    children=['Подробнее'],
                                    href=news['link'],
                                    target='_blank'
                                )
                            ]
                        )
                    ]
                )
            )

    news_df = news_df[['date', 'sentiment']]
    news_df['date'] = pd.to_datetime(news_df['date']).dt.date

    news_graph_df = pd.DataFrame()
    news_graph_df['date'] = news_df['date'].unique()
    news_graph_df['positive'] = 0
    news_graph_df['negative'] = 0

    for date in list(news_graph_df['date']):
        news_graph_df.loc[news_graph_df['date'] == date , 'positive'] = news_df[
            (
                news_df['date'] == date
            ) & (
                news_df['sentiment'] == 0
            )
        ].shape[0]
        news_graph_df.loc[news_graph_df['date'] == date , 'negative'] = news_df[
            (
                news_df['date'] == date
            ) & (
                news_df['sentiment'] == 1
            )
        ].shape[0]

    news_graph = {
        'data': [
            {
                'x': news_graph_df.date,
                'y': news_graph_df.positive,
                'type': 'bar',
                'name': 'Позитивные новости'
            },
            {
                'x': news_graph_df.date,
                'y': news_graph_df.negative,
                'type': 'bar',
                'name': 'Негативные новости'
            },
            {
                'x': news_graph_df.date,
                'y': news_graph_df.positive + news_graph_df.negative,
                'name': 'Всего новостей'
            },
        ],
        'layout': {
            'legend': {
                'orientation': 'h'
            },
            'hovermode': 'x unified'
        }
    }


    return pg.build_Section(
        style={
            'maxHeight': 'calc(100vh - 80px)',
            'height': 'calc(100vh - 80px)',
            'position': 'relative',
        },
        children=[
            pg.build_Row(
                style={
                    'height': '100%'
                },
                children=[
                    pg.build_Col(
                        width='6',
                        children=[
                            pg.build_Block(
                                title='Динамика последних 100 новостей',
                                children=[
                                    pg.build_Graph(
                                        data=news_graph['data'],
                                        layout=news_graph['layout'],
                                    )
                                ]
                            )
                        ]
                    ),
                    pg.build_Col(
                        style={
                            'height': '100%',
                            'overflow': 'auto',
                        },
                        children=[
                            pg.build_Block(
                                title='Позитивные новости',
                                children=other_news_positive
                            )
                        ]
                    ),
                    pg.build_Col(
                        style={
                            'height': '100%',
                            'overflow': 'auto',
                        },
                        children=[
                            pg.build_Block(
                                title='Негативные новости',
                                children=other_news_negative
                            )
                        ]
                    ),
                ]
            )
        ]
    )