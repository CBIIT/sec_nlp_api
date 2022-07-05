from flask import render_template, request, redirect, url_for, current_app, jsonify
from werkzeug.utils import secure_filename
from app.blueprints.expression_generator.helpers.sentiment_analysis_helper import SentimentAnalysisHelper
from app.blueprints.expression_generator.helpers.scispacy_tokenizer import SciSpacyTokenizer
from app.blueprints.expression_generator.models.criteria import Criteria
from app.blueprints.expression_generator.models.expression import Expression
from app.blueprints.tokenizer.helpers.tokenizer_helper import TokenizerHelper
from . import expression_blueprint
from app import global_matcher, global_spispacy

# Example of file upload with a htlm view already built.  Leaving for reference, but is not active currently


def create_doc_string(sentence: str) -> list:
    docs = SciSpacyTokenizer(global_spispacy).tokenize(sentence)
    docs = [doc.lower() for doc in docs]
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
            doc_string = create_doc_string(inclusion)
            expression = Expression(
                criteria=inclusion,
                sentiment_analysis=SentimentAnalysisHelper().get_setiment_analysis_for_criteria(inclusion),
                codes=TokenizerHelper(global_matcher).find_nci_c_codes_from_array([doc_string]),
                expression=""
            )
            expressions.append(expression)
        for exclusion in criteria.exclusions:
            doc_string = create_doc_string(exclusion)
            expression = Expression(
                criteria=exclusion,
                sentiment_analysis=SentimentAnalysisHelper().get_setiment_analysis_for_criteria(exclusion),
                codes=TokenizerHelper(global_matcher).find_nci_c_codes_from_array([doc_string]),
                expression=""
            )
            expressions.append(expression)
        return jsonify(expressions)
    return None

# POST /expression_generator
# @expression_blueprint.route('', methods=['POST'])
# def create():
#     return None
                
# POST /expression_generator/uploader
# @expression_blueprint.route('/uploader', methods=['POST'])
# def post():
#     current_app.logger.info("Put page loading")
#     f = request.files['file']
#     f.save(secure_filename(f.filename))
#     return redirect(url_for('expression_generator.get'))