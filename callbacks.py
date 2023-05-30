import pandas as pd
from dash import html
import dash_bootstrap_components as dbs
from dash import callback, Input, Output, State

from NLPmodules import tableQA, loadDB, translateRU_EN, translateEN_RU, wikiParser

def init(appDash, app):
    @appDash.callback(
        [
            Output('chat_mess_wrapper', 'children'),
            Output('assist__send_mess__input', 'value'),
        ],
        Input('assist__send_mess__btn', 'n_clicks'),
        State('assist__send_mess__input', 'value'),
        prevent_initial_call=True
    )
    def sendMessAssist(btn, textUser):
        mess = app.assistMess

        if textUser != '':
            mess.append(
                html.Div(
                    className='chat_mess user',
                    children=[
                        html.P(textUser)
                    ]
                ),
            )

            table_df = loadDB.loader().getData()
            quastion = translateRU_EN.translate(textUser)

            textAI = tableQA.getAnswer(
                table = table_df,
                question = quastion,
            )

            mess.append(
                html.Div(
                    className='chat_mess ai',
                    children=[
                        html.P(textAI)
                    ]
                ),
            )

            app.assistMess = mess

        return [
            mess,
            ''
        ]
    

    @appDash.callback(
        [
            Output('wiki__chat_mess_wrapper', 'children'),
            Output('wiki__send_mess__input', 'value'),
        ],
        Input('wiki__send_mess__btn', 'n_clicks'),
        State('wiki__send_mess__input', 'value'),
        prevent_initial_call=True
    )
    def sendMessWiki(btn, textUser):
        mess = app.assistMess

        if textUser != '':
            mess.append(
                html.Div(
                    className='chat_mess user',
                    children=[
                        html.P(textUser)
                    ]
                ),
            )

            # Use for generate dataframe from web
            table_df = pd.DataFrame(
                wikiParser.parser().getWiki()
            )
            quastion = textUser

            table_df.to_excel(
                r'/home/nel/Общедоступные/Jupyter/ML_UTMN/NLP/BDassisit/MessaAI/DataBases/wiki.xslx'
            )
            
            textAI = tableQA.getAnswer(
                table = table_df,
                question = quastion,
                # question = translateRU_EN.translate(quastion),
            )

            textAI = translateEN_RU.translate(textAI)

            mess.append(
                html.Div(
                    className='chat_mess ai',
                    children=[
                        html.P(textAI)
                    ]
                ),
            )

            app.assistMess = mess

        return [
            mess,
            ''
        ]
