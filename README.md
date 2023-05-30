# MessaAI
Student NLP project in the oil and gas sector based on Hugging face models.

## Tabs
1. News
2. Wiki
3. DB assist

## News
This tab contains 100 latest news from the site [rt.com](https://russian.rt.com/tag/neft) on the topic of oil with a sentiment mark and a dynamic news sentiment graph. Using this tab, you can analyze the trend of oil news in recent times and read the latest news, which is divided into two categories: positive news and negative news.

For news parsing, the requests and BeautifulSoup libraries were used.
The Higging face model ["blanchefort/rubert-base-cased-sentiment-rusentiment"](https://huggingface.co/blanchefort/rubert-base-cased-sentiment-rusentiment) was used to assess sentiment.

## Wiki
Wiki - chatbot for searching for definitions of terms. An excellent tool for beginners who get confused and lost in a huge number of terms and abbreviations that are used in the oil and gas industry.

For the search of terms in the table, the Hugging Face model ["google/tapas-large-finetuned-wtq"](https://huggingface.co/google/tapas-large-finetuned-wtq) is used, for translation from Russian into English ["Helsinki-NLP/opus-mt-ru-en"](https://huggingface.co/Helsinki-NLP/opus-mt-ru-en), for translation from English into Russian ["Helsinki-NLP/opus-mt-en-ru"](https://huggingface.co/Helsinki-NLP/opus-mt-en-ru),

## DB assist
DB assistant - a chat bot for answering questions about well parameters from the database (for example, from the data of the technical mode of operation). It will help to find out the current flow rate of liquid or oil in the well, the current values of bottomhole and buffer pressure, water cut and much more. If necessary, you can replace the database with your own in the project directory.

The DB Assist uses the Hugging Face model for translating from Russian into English ["Helsinki-NLP/opus-mt-ru-en"](https://huggingface.co/Helsinki-NLP/opus-mt-ru-en) and the model for finding answers in a table ["google/tapas-large-finetuned-wtq"](https://huggingface.co/google/tapas-large-finetuned-wtq).
