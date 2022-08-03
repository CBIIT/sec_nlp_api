
from dataclasses import dataclass

from app.blueprints.expression_generator.models.comparison import Comparison


@dataclass
class Expression:
    codes: [dict]
    words: [str]
    # sentiment_analysis: dict
    criteria: str
    expression: str
    comparision: Comparison

    def __post_init__(self):
        if bool(self.codes):
            expression_list = []
            for code in self.codes:
                for _, values in code.items():
                    for value in values:
                        expression_list.append(f"check_if_any('{value})=='YES'")
            self.expression = ' || '.join(expression_list)