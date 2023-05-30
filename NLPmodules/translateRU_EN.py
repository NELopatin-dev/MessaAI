from transformers import MarianMTModel, MarianTokenizer

def translate(
        text: str = ''
    ):
    model_name = "Helsinki-NLP/opus-mt-ru-en"
    
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)

    inputs = tokenizer.encode(text, return_tensors="pt")

    translated = model.generate(inputs, max_length=128, num_beams=4, early_stopping=True)
    translation = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]

    return translation[0]