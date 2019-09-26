from google.cloud import language_v1
from google.cloud.language_v1 import enums
from google.auth import compute_engine
import numpy as np


def analyze_sentiment(text):
    """
    Analyze sentiment in a text
    Args:
        text -> The content to be analyzed
    """
    try:
        client = language_v1.LanguageServiceClient().from_service_account_json(
            "./service_account_key.json"
        )
    except FileNotFoundError:
        credentials = compute_engine.Credentials()
        client = language_v1.LanguageServiceClient(credentials=credentials)

    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    encoding_type = enums.EncodingType.UTF8
    document = {"content": text, "type": type_, "language": language}

    response = client.analyze_sentiment(document, encoding_type=encoding_type)

    # Get overall sentiment
    document_sentiment = response.document_sentiment
    score = document_sentiment.score

    sentiment = assign_sentiment(score)

    return sentiment


def assign_sentiment(score):
    positive_max = 1.0
    positive_min = 0.25

    neutral_max = 0.24
    neutral_min = -0.24

    negative_max = -0.25
    negative_min = -1.0

    if positive_min <= score <= positive_max:
        return "positive"
    if neutral_min <= score <= neutral_max:
        return "neutral"
    if negative_min <= score <= negative_max:
        return "negative"
    return np.NaN

