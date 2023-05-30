from frontend import page_generator as pg 
from dash import html, dcc
import dash_bootstrap_components as dbc
from NLPmodules import loadDB

def build(app):
    df = loadDB.loader().getData().round(2)

    return pg.build_Section(
        style={
            'maxHeight': 'calc(100vh - 130px)',
            'height': 'calc(100vh - 130px)',
            'position': 'relative',
        },
        children=[
            pg.build_Row(
                style={
                    'height': '100%'
                },
                children=[
                    pg.build_Col(
                        width='5',
                        children=[
                            pg.build_Block(
                                title='Чат',
                                children=[
                                    html.Div(
                                        className='block',
                                        style={
                                            'height': '100%',
                                        },
                                        children=[
                                            dcc.Loading(
                                                type='circle',
                                                children=[
                                                    html.Div(
                                                        id='chat_mess_wrapper',
                                                        className='chat_mess_wrapper',
                                                        style={
                                                            'height': '73vh',
                                                            'overflow': 'auto',
                                                        },
                                                        children=app.assistMess
                                                    )
                                                ],
                                            ),
                                            html.Div(
                                                className='chat_input_wrapper',
                                                children=[
                                                    dbc.Input(
                                                        id='assist__send_mess__input'
                                                    ),
                                                    dbc.Button(
                                                        'Отправить',
                                                        id='assist__send_mess__btn',
                                                        style={
                                                            'borderRadius': 'var(--border-radius)',
                                                            'padding': 'var(--padding-min) var(--padding-mid)',
                                                        }
                                                    ),
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),

                    pg.build_Col(
                        width='7',
                        children=[
                            pg.build_Block(
                                title='База данных',
                                children=[
                                    html.Div(
                                        className='block',
                                        children=[
                                            pg.build_Tabel(
                                                cols=[
                                                    {
                                                        "name": i, 
                                                        "id": i
                                                    } for i in df.columns
                                                ],
                                                rows=df.to_dict('records'),
                                                height='75vh',
                                                page_size=20
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                ]
            )
        ]
    )