from helloflask import app
from flask import Flask, render_template, url_for, jsonify, request
from helloflask.init_db import init_database, db_session
from helloflask.models import Talk
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import subqueryload, joinedload
from sqlalchemy.sql import func
from helloflask.Search import ElasticSearch
# import json

@app.route('/')
def main():

    return render_template('main.htm', title="Main")

@app.route('/tags')
def tags():
    # tags = Talk.query.filter(Talk.id == talkid)
    tags = Talk.query.first()
    # print(tags)
    # tag = {"tags":tags}
    # print(type(tags))
    # print(tags.tags)
    return jsonify(tags.json())

@app.route('/korsearch/<searchwords>')
def ksearchjson(searchwords):
    s = ElasticSearch()
    searchres = s.kortoEngequiv(searchwords)
    return jsonify(searchres)


@app.route('/engsearch/<searchwords>')
def esearchjson(searchwords):
    s = ElasticSearch()
    searchres = s.engtoKorequiv(searchwords)
    return jsonify(searchres)

