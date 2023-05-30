import pandas as pd
import pathlib

class loader:
    def __init__(self):
        self.path = rf'{pathlib.Path(__file__).resolve().parent.parent}/DataBases/data.xlsx'

    def getData(self):
        return pd.read_excel(self.path)
