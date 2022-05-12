
from dataclasses import dataclass


@dataclass
class Expression:
    codes: [str]
    sentiment_analysis: dict
    expression: str
    criteria: str