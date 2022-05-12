
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from typing import Union

class SentimentAnalysisHelper:

    def __init__(self) -> None:
        pass

    def get_setiment_analysis_for_criteria(self, criteria: str) -> Union[dict, None]:
        if criteria is not None:
            sid = SentimentIntensityAnalyzer()
            return sid.polarity_scores(criteria)
        return None