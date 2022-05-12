from flask import render_template, request, redirect, url_for, current_app, jsonify
from werkzeug.utils import secure_filename
from app.blueprints.expression_generator.helpers.sentiment_analysis_helper import SentimentAnalysisHelper
from app.blueprints.expression_generator.helpers.scispacy_tokenizer import SciSpacyTokenizer
from app.blueprints.expression_generator.models.criteria import Criteria
from app.blueprints.expression_generator.models.expression import Expression
from app.blueprints.tokenizer.helpers.tokenizer_helper import TokenizerHelper
from . import expression_blueprint
from app import global_matcher, global_spispacy
import numpy as np

# Example of file upload with a htlm view already built.  Leaving for reference, but is not active currently

# PUT /expresion_generator/add
@expression_blueprint.route('/', methods=['GET'])
def get():
    current_app.logger.info("Put page loading")
    return render_template("expression_generator/index.html")

@expression_blueprint.route('', methods=['POST'])
def create():
    content = request.get_json()
    if content is not None:
        current_app.logger.info(f"POST[expression_generator] content is: {content}")
        criteria = Criteria(**content)
        expressions = []
        for inclusion in criteria.inclusions:
            docs = SciSpacyTokenizer(global_spispacy).tokenize(inclusion)
            docs = [doc.lower() for doc in docs]
            doc_string = ', '.join(docs)
            expression = Expression(
                criteria=inclusion,
                sentiment_analysis=SentimentAnalysisHelper().get_setiment_analysis_for_criteria(inclusion),
                codes=TokenizerHelper(global_matcher).find_nci_c_codes_from_array([doc_string]),
                expression=""
            )
            expression_list = []
            for code in expression.codes:
                for k in code:
                    for value in code[k]:
                        expression_list.append(f"check_if_any('{value})=='YES'")
            expression.expression = ' || '.join(expression_list)
            expressions.append(expression)
        for exclusion in criteria.exclusions:
            expression = Expression(
                criteria=exclusion,
                sentiment_analysis=SentimentAnalysisHelper().get_setiment_analysis_for_criteria(exclusion),
                codes=TokenizerHelper(global_matcher).find_nci_c_codes_from_array([exclusion]),
                expression=""
            )
            expressions.append(expression)
        return jsonify(expressions)
    return None
                

# POST /expression_generator/uploader
@expression_blueprint.route('/uploader', methods=['POST'])
def post():
    current_app.logger.info("Put page loading")
    f = request.files['file']
    f.save(secure_filename(f.filename))
    return redirect(url_for('expression_generator.get'))