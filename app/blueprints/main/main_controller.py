from . import main_blueprint
from flask import render_template, request, redirect, url_for, current_app, abort

@main_blueprint.route('/')
def index():
    current_app.logger.info("Index page loading")
    return render_template('main/index.html')