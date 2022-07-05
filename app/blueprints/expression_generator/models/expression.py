
from dataclasses import dataclass


@dataclass
class Expression:
    codes: [str]
    sentiment_analysis: dict
    criteria: str
    expression: str

    def __post_init__(self):
        if bool(self.codes):
            expression_list = []
            for code in self.codes:
                for _, values in code.items():
                    for value in values:
                        expression_list.append(f"check_if_any('{value})=='YES'")
            self.expression = ' || '.join(expression_list)