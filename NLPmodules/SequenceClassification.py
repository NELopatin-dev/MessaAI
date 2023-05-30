import torch
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizerFast


class model:
    def __init__(self):
        self.tokenizer = BertTokenizerFast.from_pretrained('blanchefort/rubert-base-cased-sentiment-rusentiment')
        self.model = AutoModelForSequenceClassification.from_pretrained('blanchefort/rubert-base-cased-sentiment-rusentiment', return_dict=True)

    @torch.no_grad()
    def predict(self, text):
        inputs = self.tokenizer(text, max_length=512, padding=True, truncation=True, return_tensors='pt')
        outputs = self.model(**inputs)

        """
        0: NEUTRAL
        1: POSITIVE
        2: NEGATIVE
        """

        # Ignore neutral res
        predicted = torch.nn.functional.softmax(outputs.logits, dim=1).numpy()[0][1:]

        """
        0: POSITIVE
        1: NEGATIVE
        """
        return list(predicted)