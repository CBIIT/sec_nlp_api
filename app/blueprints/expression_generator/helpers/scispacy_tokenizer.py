

class SciSpacyTokenizer:

    def __init__(self, nlp) -> None:
        self.nlp = nlp

    def tokenize(self, sentence: str) -> list:
        doc = self.nlp(sentence)
        doc_list = []
        for ent in doc.ents:
            doc_list.append(ent.text)
        return doc_list