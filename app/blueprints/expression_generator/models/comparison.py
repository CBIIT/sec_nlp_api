

from dataclasses import dataclass


@dataclass
class Comparison:
    bert_words: [dict]
    sci_words: [dict]
    bert_percentage: float = None
    sci_percentage: float = None



    def __post_init__(self):
        total = len(self.bert_words) + len(self.sci_words)
        if total == 0: return
        self.bert_percentage = len(self.bert_words) / total
        self.sci_percentage = len(self.sci_words) / total

    
    