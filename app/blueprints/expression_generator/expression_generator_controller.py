from flask import render_template, request, redirect, url_for, current_app, abort
from werkzeug.utils import secure_filename
from app.tasks import add_together
from . import expression_blueprint

# PUT /expresion_generator/add
@expression_blueprint.route('/', methods=['GET'])
def get():
    current_app.logger.info("Put page loading")
    return render_template("expression_generator/index.html")

@expression_blueprint.route('/uploader', methods=['POST'])
def post():
    current_app.logger.info("Put page loading")
    f = request.files['file']
    f.save(secure_filename(f.filename))
    return redirect(url_for('expression_generator.get'))

@expression_blueprint.route('/add', methods=['GET'])
def add():
    results = add_together.apply_async(args=[34, 23])
    return results