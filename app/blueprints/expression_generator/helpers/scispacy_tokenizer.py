

class SciSpacyTokenizer:

    def __init__(self, nlp, sentence: str) -> None:
        self.nlp = nlp
        self.tokens = nlp(sentence)

    def get_words_and_labels(self) -> list:
        doc_list = {}
        if self.tokens:
            for ent in self.tokens.ents:
                if ent.label_ in ['DISEASE', 'CHEMICAL']:
                    doc_list[ent.text] = ent.label_
                    # doc_list.append({f"{ent.text}": ent.label_})
        return doc_list

    def get_word_list(self) -> list:
        doc_list = []
        if self.tokens:
            for ent in self.tokens.ents:
                if ent.label_ in ['DISEASE', 'CHEMICAL']:
                    doc_list.append(ent.text)
        return doc_list