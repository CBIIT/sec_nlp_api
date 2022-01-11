import uuid
from flask import (current_app, session)
from flask_socketio import emit
from app import socketio
from .models.code import Codes
from .helpers.tokenizer_helper import TokenizerHelper
from app.nlp import get_matcher


@socketio.on('connect')
def join(message):
    session['matcher'] = get_matcher()
    session['sid'] = uuid.uuid4()
    current_app.logger.info(f"SocketIO[tokenizer] SID: #{session['sid']} connection was made")
    emit('status_matcher', 'Matcher set in session')

@socketio.on('disconnect')
def leave():
    current_app.logger.info(f"SocketIO[tokenizer] SID: #{session['sid']} disconnected")
    session['matcher'] = None
    session['sid'] = None

@socketio.on('OutsideCodes')
def test(message):
    current_app.logger.info(f"SocketIO[tokenizer] SID: #{session['sid']} OutsideCodes recieved message {message}")
    codes = Codes(**message)
    search_string_array = [code.display for code in codes.coding]
    c_codes = TokenizerHelper(session.get('matcher')).find_nci_c_codes_from_array(search_string_array)
    emit('nci_codes', c_codes)