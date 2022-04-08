from re import S, match, search
from flask import (current_app, session)
from app.db import  get_db
from app.nlp import get_matcher, get_nlp
from spacy.util import filter_spans
from spacy.tokens.doc import Doc
from typing import List, Set, Union
from sqlite3 import OperationalError

class TokenizerHelper:


    def __init__(self, matcher) -> None:
        self.matcher = matcher

    def find_nci_c_codes_from_array(self, search_string_array: List) -> List:
        if isinstance(search_string_array, list):
            search_string = ", ".join(search_string_array)
            return self.find_nci_c_codes_from_string(search_string)
        return None

    def find_nci_c_codes_from_string(self, search_string: str) -> List:
        documents = self.get_document(search_string)
        matches = self.find_word_matches(documents)
        spans = self.build_spans(matches, documents)
        return self.get_associated_codes(spans)

    def get_associated_codes(self, filtered_spans: Set) -> List:
        c_codes = []
        try:
            if filtered_spans:
                db_cursor = get_db().cursor()
                for span in filtered_spans:
                    db_cursor.execute(get_db().safe_sql(self.get_best_ncit_code_sql_for_span()), [span.text])
                    db_codes = db_cursor.fetchall()
                    if len(db_codes) > 0:
                        code_dict = {}
                        code_dict[span.text] = []
                        for db_code in db_codes:
                            code_dict[span.text] += db_code
                        # code_dict[span.text] = [ dict(db_code)['code'] for db_code in db_codes ]
                        c_codes.append(code_dict)
                    else:
                        db_cursor.execute(get_db().safe_sql(self.get_ncit_code_sql_for_span()), [span.text])
                        rcodes = db_cursor.fetchall()
                        if rcodes:
                            code_dict = {}
                            code_dict[span.text] = []
                            for db_code in rcodes:
                                code_dict[span.text] += db_code
                            # code_dict[span.text] = [ dict(db_code)['code'] for db_code in rcodes ]
                            c_codes.append(code_dict)
        except OperationalError as error:
            current_app.logger.error(f"get associated codes in TokenizerHelper failed with error #{error}")
        return c_codes

    def build_spans(self, matches: List, search_document: Doc) -> Union[List, None]:
        if matches:
            spans = set()
            for _, start, end in matches:
                spans.add(search_document[start:end])
            filtered_spans_list = filter_spans(spans) #Returns list and doesnt remove dups like expected
            return filtered_spans_list
        return None

    def find_word_matches(self, search_document: Doc) -> Union[List, None]:
        if search_document and self.matcher:
            return self.matcher(search_document)
        return None

    def get_document(self, search_string: str) -> Union[Doc, None]:
        if isinstance(search_string, str):
            nlp = get_nlp()
            return nlp(search_string)
        return None

    def get_best_ncit_code_sql_for_span(self) -> str:
        return """
            select code from ncit where code not in (select descendant from ncit_tc where parent in ('C25709')) 
            and lower(pref_name) = ? 
            and lower(pref_name) not in ('i', 'ii', 'iii', 'iv', 'v', 'set', 'all', 'at', 'is', 'and', 'or', 'to', 'a', 'be', 'for', 'an', 'as', 'in', 'of', 'x', 'are', 'no', 'any', 'on', 'who', 'have', 't', 'who', 'at')
        """

    def get_ncit_code_sql_for_span(self) -> str:
        return """
            select distinct code from ncit_syns where code not in (select descendant from ncit_tc where parent in ('C25709'))
            and l_syn_name = ? 
            and l_syn_name not in ('i', 'ii', 'iii', 'iv', 'v', 'set', 'all', 'at', 'is', 'and', 'or', 'to', 'a', 'be', 'for', 'an', 'as', 'in', 'of', 'x', 'are', 'no', 'any', 'on', 'who', 'have', 't', 'who', 'at')
        """