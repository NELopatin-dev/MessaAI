import webbrowser
from threading import Timer

import frontend.page_generator as pg 
from frontend.pages import tabNews, tabWiki, tabTRassist

from NLPmodules import SequenceClassification as SC_model
from NLPmodules import newsParser

import callbacks

class App:
    def __init__(
        self,
        appTitle: str = 'AppName',
        appPort: int = 8053
    ):
        self.modules = {
            'sentiment': SC_model.model(),
            'newsParser': newsParser.parser(),
        }

        self.appTitle = appTitle
        self.appPort = appPort

        self.assistMess = []
        self.wikiMess = []

        self.appTabs = {
            'News': {
                'tab_id': 'tab_news',
                'content': tabNews.build(self)
            },
            'Wiki': {
                'tab_id': 'tab_wiki',
                'content': tabWiki.build(self)
            },
            'DB assist': {
                'tab_id': 'tab_TRassist',
                'content': tabTRassist.build(self)
            }
        }


    
    def open_browser(self):
        webbrowser.open_new("http://localhost:{}".format(self.appPort))


    def start(self):
        app = pg.get_App(self.appTitle)
        app.layout = pg.build_Page(
            fluid=True,
            children=[
                # pg.build_Navbar(self.appTitle),
                pg.build_Tabs(
                    tabs_Info=self.appTabs
                )
            ]
        )

        pg.callbacks_init(app)
        callbacks.init(app, self)
        
        Timer(1, self.open_browser()).start()
        app.run_server(port=self.appPort)
