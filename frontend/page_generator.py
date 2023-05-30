import os, signal
import time

import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Output, Input, State

from dash import dash_table as dt
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# === GET DEFAULT APP ===
def get_App(
        title: str = 'NoName',
        icons=dbc.icons.BOOTSTRAP,
        # pages: bool = True
):
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.SUPERHERO, icons],
        title=title,
        # use_pages=pages
        # assets_folder = 'frontend/css'
    )

    app.config.suppress_callback_exceptions = True
    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True

    return app


# === BUILD PAGE (MAIN CONTAINER) ===
def build_Page(
        fluid: bool = True,
        children=[]
):
    page = dbc.Container(
        children=[
                     dcc.Store(id='memory', storage_type='local'),
                 ] + children,
        fluid=fluid
    )

    return page


# === BUILD MAIN NAV BAR ===
def build_Navbar(
        title: str = "Без названия",
        menu: dict = {}
):
    menu_elems = menu.copy()
    menu = []

    for menu_elemKey in menu_elems.keys():
        if 'icon' in menu_elems[menu_elemKey].keys():
            menu.append(
                html.A(
                    [
                        html.Img(
                            src='assets/img/' + str(menu_elems[menu_elemKey]['icon']),
                            height='30',
                            width='30'
                        ),
                        menu_elemKey
                    ],
                    href=menu_elems[menu_elemKey]['link'],
                    className='navbar__menu__elem'
                )
            )
        else:
            menu.append(
                html.A(
                    menu_elemKey,
                    href=menu_elems[menu_elemKey]['link'],
                    className='navbar__menu__elem'
                )
            )

    navbar = html.Div(
        [
            html.A(
                html.H3(
                    [
                        title
                    ],
                    className='navbar__title',
                ),
                href='/'
            ),
            html.Div(
                menu,
                className='navbar__menu',
            ),
            dbc.Button(
                'X',
                id='ext',
                color='danger',
                className='navbar__closeBtn'
            )

        ],
        className='navbar'
    )

    return navbar


# === BUILD TABS WITH CONTENT ===
def build_Tabs(
        tabs_Info: dict = {}
):
    tabs_elems = []
    active_tab = tabs_Info[list(tabs_Info.keys())[0]]['tab_id']

    for tab_elemKey in tabs_Info.keys():
        tabs_elems.append(
            dbc.Tab(
                tabs_Info[tab_elemKey]['content'],
                label=tab_elemKey,
                tab_id=tabs_Info[tab_elemKey]['tab_id'],
                id=tabs_Info[tab_elemKey]['tab_id'],
                className="tab_panel__tab"
            )
        )

        if 'active' in list(tabs_Info[tab_elemKey].keys()) and tabs_Info[tab_elemKey]['active'] == True:
            active_tab = tabs_Info[tab_elemKey]['tab_id']

    tabs = dbc.Tabs(
        tabs_elems,
        id="tabid",
        active_tab=active_tab,
        className="tab_panel"
    )

    return tabs


# === BUILD SECTION OF BLOCKS ===
def build_Section(
        title: str = None,
        children: list = [],
        style: dict = {}
):
    if title is not None:
        children = [
                       dbc.Row(
                           html.H2(
                               title
                           )
                       )
                   ] + children

    section = html.Div(
        children,
        className="section",
        style=style,
    )

    return section


def build_Row(
        children: list = [],
        style: dict = {},
        classname: str = 'section__row'
):
    row = dbc.Row(
        children=children,
        className=classname,
        style=style
    )

    return row


def build_Col(
        width: str = None,
        children: list = [],
        classname: str = 'section__col',
        style: dict = {}
):
    if width is None:
        col = dbc.Col(
            children=children,
            className=classname,
            style=style
        )
    else:
        col = dbc.Col(
            children=children,
            className=classname,
            width=width,
            style=style
        )

    return col


# === BUILD BLOCK ===
def build_Block(
        id: str = '',
        title: str = None,
        children: list = [],
        style: dict = {}
):
    content = children

    if title is not None:
        content = [
                      html.H4(
                          title,
                          className='block__title'
                      )
                  ] + children

    block = html.Div(
        content,
        className="section__block",
        style=style,
        id=id
    )

    return block


# === BUILD CARD ===
def build_Card(
        header: list = [],
        content: list = [],
        idCard: str = '',
        colorCard: str = '',
        styleCard: dict = {},
        card_style: dict = {}
):
    if colorCard != '':
        styleCard['borderBottomColor'] = colorCard

    card = dbc.Card(
        [
            dbc.CardHeader(
                header,
                style=styleCard
            ),
            dbc.CardBody(
                content,
                id=idCard
            )
        ],
        style=card_style
    )

    return card


# === BUILD TABEL ===
def build_Tabel(
        data=pd.DataFrame(),
        rows: dict = None,
        cols: list = None,
        tooltip_data=[],
        fixHead: bool = True,
        fixCols: int = 0,
        page_size: int = None,
        filter_action: str = 'native',
        sort_action: str = 'native',
        sort_mode: str = 'multi',
        height: str = "100vh",
        style_data_conditional: list = [],
        tabelId: str = "",
        css: list = [],
        row_selct_rule: str = '',
        selected_rows: list = [],
        width: str = '100%',
        maxWidth: str = '100%',
        row_deletable: bool = False,
        editable: bool = False
):
    classTabel = ''
    overflow = 'auto'
    if tooltip_data != []:
        overflow = 'visible'

    if data.shape[0] == 0 and data.shape[1] == 0 and rows == None:
        tabel = html.Div(
            [
                html.H4(
                    "Нет данных",
                    style={
                        "color": "var(--bs-gray-600)",
                        "fontWeight": "500",
                        "textAlign": "center"
                    }
                ),
            ],
            style={
                "padding": "var(--padding-max)",
                "width": "100%",
            }
        )
    elif rows is None or cols is None:
        if fixHead:
            classTabel = 'table-fixed'

        tabel = dbc.Table(
            dark=True,
            bordered=True,
        ).from_dataframe(
            data,
            className=classTabel,
            id=tabelId
        )
    else:
        if page_size is None:
            page_size = len(rows)

        tabel = dt.DataTable(
            rows,
            cols,
            filter_action=filter_action,
            sort_action=sort_action,
            sort_mode=sort_mode,
            page_size=page_size,
            row_selectable=row_selct_rule,
            selected_rows=selected_rows,
            row_deletable=row_deletable,
            editable=editable,
            css=css,
            fixed_rows={'headers': fixHead},
            fixed_columns={'headers': True, 'data': fixCols},
            style_header={
                "backgroundColor": "var(--bs-gray-900)"
            },
            style_filter={
                'whiteSpace': 'normal',
                "backgroundColor": "var(--bs-gray-900)",
                "color": 'var(--bs-body-color)'
            },
            style_data={
                "backgroundColor": "var(--bs-body-dg)"
            },
            style_data_conditional=[
                                       {
                                           'if': {'row_index': 'even'},
                                           'backgroundColor': 'var(--bs-gray-dark)',
                                       },
                                       {
                                           'if': {'row_index': 'odd'},
                                           'backgroundColor': 'var(--bs-body-bg)',
                                       }
                                   ] + style_data_conditional,
            style_table={
                'width': width,
                'maxWidth': maxWidth,
                'height': height,
                'maxHeight': height,
            },
            tooltip_data=tooltip_data,
            tooltip_delay=0,
            tooltip_duration=None,
            style_cell={
                # all three widths are needed
                'minWidth': '150px',
                # 'width': '180px',
                'maxWidth': '250px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'borderSizing': "border-box",
                'padding': '5px'
            },
            id=tabelId
        )

    return html.Div(
        [
            tabel
        ],
        id=tabelId + '__wrapper',
        style={
            "overflow": overflow,
            "width": "100%",
            "postion": 'relative',
            "maxHeight": str(float(height.replace('vh', '').replace('%', '')) + 5) + 'vh',
        }
    )


# === BUILD GRAPH ===
def build_Graph(
        graphId: str = '',
        data: list = [],
        marker: dict = {},
        layout: dict = {},
        height: str = '100%'
):
    layout['template'] = 'plotly_dark'
    # layout['hovermode'] = "x"

    if data != []:
        resElem = html.Div(
            [
                dcc.Graph(
                    id=graphId + '__graph',
                    figure=go.Figure(
                        data=data,
                        # marker=marker, #TODO add colors for graphs
                        layout=layout
                    ),
                    style={
                        'width': '100%',
                        'height': '100%'
                    }
                )
            ],
            id=graphId,
            style={
                'position': 'relative',
                'height': height
            }
        )
    else:
        resElem = html.Div(
            [
                html.H4(
                    "Нет данных",
                    style={
                        "color": "var(--bs-gray-600)",
                        "fontWeight": "500",
                        "textAlign": "center"
                    }
                ),
            ],
            id=graphId,
            style={
                'position': 'relative',
                'height': height
            }
        )

    return resElem


# === CALLBACKS ===
def callbacks_init(app):
    @app.callback(Output('ext', 'size'), Input('ext', 'n_clicks'), prevent_initial_call=True)
    def close_app(clc):
        os.kill(os.getpid(), signal.SIGTERM)
        return "sm"
