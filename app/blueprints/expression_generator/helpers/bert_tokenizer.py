

class BertTokenizer:


    def __init__(self, nlp, sentence: str) -> None:
        self.nlp = nlp
        self.table = {
            'LABEL_0': 'O',  # We don't care about O labels
            'LABEL_1': 'B-Chemical',
            'LABEL_2': 'B-Disease',
            'LABEL_3': 'I-Disease',
            'LABEL_4': 'I-Chemical',
        }
        self.tokens = nlp(sentence)

    def get_words_and_label(self) -> dict:
        doc_list = {}
        for index, result in enumerate(self.tokens):
            if all(result['entity'] != label for label in ['LABEL_0', 'LABEL_3', 'LABEL_4']) and (not result['word'].startswith('##')):
                word, label = self._create_word(self.tokens[index:])
                doc_list[word] = label
                # doc_list.append({f"{word}": label})
        return doc_list
        
    def get_word_list(self) -> list:
        doc_list = []
        for index, result in enumerate(self.tokens):
            if all(result['entity'] != label for label in ['LABEL_0', 'LABEL_3', 'LABEL_4']) and (not result['word'].startswith('##')):
                word, _ = self._create_word(self.tokens[index:])
                doc_list.append(word)
        return doc_list

    def _create_word(self, tokens: list) -> tuple:
        first_token = tokens.pop(0)
        word = first_token['word']
        label = self.table[first_token['entity']]
        for token in tokens:
            if token.get('word').startswith('##'):
                word = word + token['word'][2:]
            elif self.table[token.get('entity')].startswith('I-') and self.table[token.get('entity')][2:] == label[2:]:
                word = word + ' ' + token['word']
            elif not token.get('word').startswith('##'):
                return word, label
        return word, label

    def _combine_words(self):
        pass