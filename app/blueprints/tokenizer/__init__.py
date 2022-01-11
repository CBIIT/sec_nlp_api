from flask import Blueprint

tokenizer_blueprint = Blueprint('tokenizer', __name__, template_folder='templates')

from . import tokenizer_controller, tokenizer_event

