from transformers import pipeline
import pandas as pd

import re 

def has_en(text):
    res = bool(re.search('[a-zA-Z]', text))
    print('Has en:', res)
    return res

def getAnswer(
        table = pd.DataFrame, 
        question: str = ''
    ):
    table = table.round(2).astype(str).dropna()

    tqa = pipeline(
        task="table-question-answering", 
        model="google/tapas-large-finetuned-wtq" #if has_en(question) else "tvsupertask/tvsupertask-tqa-base"
    )

    return(
        tqa(
            table=table, 
            query=question
        )['cells'][0]
    )
