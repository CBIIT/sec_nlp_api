from flask import render_template, request, redirect, url_for, current_app, jsonify
from werkzeug.utils import secure_filename
from app.blueprints.expression_generator.helpers.sentiment_analysis_helper import SentimentAnalysisHelper
from app.blueprints.expression_generator.helpers.scispacy_tokenizer import SciSpacyTokenizer
from app.blueprints.expression_generator.helpers.bert_tokenizer import BertTokenizer
from app.blueprints.expression_generator.models.comparison import Comparison
from app.blueprints.expression_generator.models.criteria import Criteria
from app.blueprints.expression_generator.models.expression import Expression
from app.blueprints.tokenizer.helpers.tokenizer_helper import TokenizerHelper
from . import expression_blueprint
from app import global_matcher, global_spispacy, global_bert

# Example of file upload with a htlm view already built.  Leaving for reference, but is not active currently


def create_sci_docs(sentence: str) -> list:
    sci = SciSpacyTokenizer(global_spispacy, sentence)
    return sci.get_words_and_labels()

#pass back bert and call the correct function for the time
def create_bert_docs(sentence: str) -> list:
    bert = BertTokenizer(global_bert, sentence)
    return bert.get_words_and_label()

def create_doc_string(word_list: list) -> str:
    docs = [doc.lower() for doc in word_list]
    doc_string = ', '.join(docs)
    return doc_string

# GET /expression_generator
@expression_blueprint.route('/', methods=['GET'])
def get():
    content = request.get_json()
    if content is not None:
        current_app.logger.info(f"GET[expression_generator] content is: {content}")
        criteria = Criteria(**content)
        expressions = []
        for inclusion in criteria.inclusions:
            sci_docs = create_sci_docs(inclusion)
            bert_docs = create_bert_docs(inclusion)
            expression = Expression(
                criteria=inclusion,
                words=list(set(list(sci_docs.keys()) + list(bert_docs.keys()))),
                # sentiment_analysis=SentimentAnalysisHelper().get_setiment_analysis_for_criteria(inclusion),
                codes=TokenizerHelper(global_matcher).find_nci_c_codes_from_array([create_doc_string(list(bert_docs.keys()) + list(sci_docs.keys()))]),
                expression="",
                comparision=Comparison(bert_docs, sci_docs)
            )
            expressions.append(expression)
        for exclusion in criteria.exclusions:
            sci_docs = create_sci_docs(exclusion)
            bert_docs = create_bert_docs(exclusion)
            expression = Expression(
                criteria=exclusion,
                words=list(set(list(bert_docs.keys()) + list(sci_docs.keys()))),
                # sentiment_analysis=SentimentAnalysisHelper().get_setiment_analysis_for_criteria(exclusion),
                codes=TokenizerHelper(global_matcher).find_nci_c_codes_from_array([create_doc_string(list(bert_docs.keys()) + list(sci_docs.keys()))]),
                expression="",
                comparision=Comparison(bert_docs, sci_docs)
            )
            expressions.append(expression)
        return jsonify(expressions)
    return None