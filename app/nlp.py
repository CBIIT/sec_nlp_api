from nis import match
import click
from spacy import blank
from spacy.matcher import PhraseMatcher
from flask import (current_app, g)
from flask.cli import with_appcontext
from app.db import get_db
from pickle import (dumps, loads)
from bz2 import (compress, decompress)

def get_nlp():
    if "nlp" not in g:
        g.nlp = blank("en")
    return g.nlp

def get_matcher():
    if "nlp_matcher" not in g:
        db = get_db()
        pickled = db.get(current_app.config['NLP_PICKLE_SQL'])[0][0]
        uncompressed_pickle = decompress(pickled)
        g.nlp_matcher = loads(uncompressed_pickle)
    return g.nlp_matcher

def clear_nlp(e=None):
    nlp = g.pop("nlp", None)
    if nlp is not None:
        nlp = None

def clear_matcher(e=None):
    matcher = g.pop("nlp_matcher", None)
    if matcher is not None:
        matcher = None

def init_nlp():
    nlp = get_nlp()
    with current_app.app_context():
        db = get_db()
        sql = '''select code, synonyms from ncit
        where (concept_status is null or (concept_status not like '%Obsolete%' and concept_status not like '%Retired%') ) 
        /* and (lower(synonyms) like '%chemotherapy%' or lower(s`       `nonyms) like '%ecog%' or lower(synonyms) like '%white blood cell%') */
        '''
        records = db.get(sql)
        ncit_syns_sql = '''select code, l_syn_name from ncit_syns'''
        records.extend(db.get(ncit_syns_sql))
        code_synonym_set = set() # []
        for record in records:
            code = record[0]
            synonyms = record[1].split('|')
            new_tuple = (zip([code] * len(synonyms), synonyms)) # list(zip([code] * len(synonyms), synonyms)) 
            code_synonym_set.add(new_tuple)
        patterns = []
        for code_synonym in code_synonym_set: # patterns = [nlp.make_doc(v[1]) for v in code_synonym_set]
            v = next(code_synonym)
            patterns.append(nlp.make_doc(v[1]))
        matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
        matcher.add("TerminologyList", patterns)
        compressed_pickled_string = compress(dumps(matcher))
        db.save("insert into test_ncit_version (ncit_tokenizer) values (%s)", (compressed_pickled_string,))

@click.command("init-nlp")
@with_appcontext
def init_nlp_command():
    """Clear existing data and create new file."""
    click.echo("Initializing nlp....Please wait.")
    init_nlp()
    click.echo("Initialized the nlp.")

def init_app(app):
    """Register nlp functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(clear_nlp)
    app.teardown_appcontext(clear_matcher)
    app.cli.add_command(init_nlp_command)