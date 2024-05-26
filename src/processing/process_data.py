import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def get_processed_data(df_restaurants: pd.DataFrame):
    df_restaurants["info"] = (
        df_restaurants["description"].astype(str)
        + " "
        + df_restaurants["extra_features"].astype(str)
        + " "
        + df_restaurants["extra_content"].astype(str)
        + " "
        + df_restaurants["reviews"].astype(str)
        + " "
        + df_restaurants["street"].astype(str)
    )

    corpus = df_restaurants["info"].astype(str).tolist()
    processed_corpus = process_corpus(corpus)

    return pd.DataFrame(
        {
            "bar_name": df_restaurants["title"],
            "search_corpus": processed_corpus,
            "street": df_restaurants["street"],
            "extra": df_restaurants["extra_features"],
        }
    )


def process_corpus(corpus: list[str]):
    stop_words = get_stop_words()

    processed_corpus = []
    for document in corpus:
        words = [
            normalize_word(word)
            for word in word_tokenize(document, language="spanish")
            if word.isalpha()
            and word.lower() != "nan"
            and word.lower() not in stop_words
            and len(word) > 1
        ]

        unique_words = list(set(words))
        processed_corpus.append(" ".join(unique_words))

    return processed_corpus


def get_stop_words():
    list_of_topics = ["punkt", "stopwords"]
    for topic in list_of_topics:
        nltk.download(topic)

    return set(stopwords.words("spanish") + stopwords.words("english"))


def normalize_word(word: str) -> str:
    return word.lower()
