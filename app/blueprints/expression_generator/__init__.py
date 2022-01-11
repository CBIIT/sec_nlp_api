from flask import Blueprint

expression_blueprint = Blueprint('expression_generator', __name__, template_folder='templates')

from . import expression_generator_controller