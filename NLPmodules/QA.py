from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

def answer_question(question, context, model_name, language="en"):
    # Load the pre-trained model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)

    # Tokenize the input question and context
    inputs = tokenizer.encode_plus(question, context, return_tensors="pt", padding=True, truncation=True)

    # Obtain the model's predictions
    outputs = model(**inputs)
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    # Find the start and end positions with the highest scores
    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores)

    # Decode the predicted answer from the tokenized input
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][start_index:end_index+1]))

    return answer

# Example usage
question = "Who wrote Harry Potter?"
context = "Harry Potter is a series of fantasy novels written by British author J. K. Rowling."

english_model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
english_answer = answer_question(question, context, english_model_name, language="en")

russian_model_name = "sberbank-ai/rugpt3large_based_on_gpt2"
russian_context = "Гарри Поттер — серия фантастических романов, написанных британской писательницей Джоан Роулинг."
russian_answer = answer_question(question, russian_context, russian_model_name, language="ru")

print(f"Question: {question}")
print(f"English Answer: {english_answer}")
print(f"Russian Answer: {russian_answer}")
