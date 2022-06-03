

class SciSpacyTokenizer:

    def __init__(self, nlp) -> None:
        self.nlp = nlp

    def tokenize(self, sentence: str) -> list:
        doc = self.nlp(sentence)
        doc_list = []
        for ent in doc.ents:
            print(f"{ent.text}: {ent.label_}")
            if ent.label_ == 'DISEASE':
                doc_list.append(ent.text)
        return doc_list