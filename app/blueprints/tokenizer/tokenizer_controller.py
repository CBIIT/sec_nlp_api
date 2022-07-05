from flask import request, current_app, jsonify
from . import tokenizer_blueprint
from .models.code import Codes
from .helpers.tokenizer_helper import TokenizerHelper
from app import global_matcher
from app.db import  get_db

# [POST] /tokenizer

@tokenizer_blueprint.route('', methods=['POST'])
def post():
    content = request.get_json()
    if content is not None:
        current_app.logger.info(f"POST[tokenizer] content is: {content}")
        codes = Codes(**content)
        db_cursor = get_db().cursor()
        new_coding = []
        db_codes = {}
        for code in codes.coding:
            if code.code and (code.system in ['ICD-9-CM', 'ICD-10-CM']):
                db_cursor.execute(get_c_code_from_curated_single(), (code.code,))
                db_code = db_cursor.fetchone()
                if db_code:
                    if db_code[1] and db_code[2]:
                        db_codes[db_code[2].lower()] = [db_code[1]]
                    else:
                        new_coding.append(code)
            else:
                new_coding.append(code)
        codes.coding = new_coding
        search_string_array = [code.display for code in codes.coding]
        c_codes = TokenizerHelper(global_matcher).find_nci_c_codes_from_array(search_string_array)
        c_codes.append(db_codes)
        return jsonify(c_codes)
    return None

def get_c_code_from_curated_single() -> str:
    return """ SELECT disease_code, evs_c_code, evs_preferred_name FROM
        curated_crosswalk WHERE
        disease_code = %s LIMIT 1;
    """


def get_c_code_from_curated_crosswalk() -> str:
        return """SELECT disease_code, evs_c_code, evs_preferred_name FROM 
        curated_crosswalk WHERE 
        disease_code in %s """
        