from flask import request, current_app, jsonify
from . import tokenizer_blueprint
from .models.code import Codes
from .helpers.tokenizer_helper import TokenizerHelper
from app import global_matcher

# [POST] /tokenizer

@tokenizer_blueprint.route('', methods=['POST'])
def post():
    content = request.get_json()
    if content is not None:
        current_app.logger.info(f"POST[tokenizer] content is: {content}")
        codes = Codes(**content)
        search_string_array = [code.display for code in codes.coding]
        c_codes = TokenizerHelper(global_matcher).find_nci_c_codes_from_array(search_string_array)
        return jsonify(c_codes)
    return None