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
    tags = Talk.query.first()
    # print(tags)
    # tag = {"tags":tags}
    # print(type(tags))
    # print(tags.tags)
    return jsonify(tags.json())

@app.route('/korsearch/<searchwords>')
def ksearchjson(searchwords):
    # searchwords = request.args.get("ksearchwords")
    s = ElasticSearch()
    s.kortoEng(searchwords)
    searchres = s.kortoEngequiv()
    return jsonify(searchres)


@app.route('/engsearch/<searchwords>')
def esearchjson(searchwords):
    # searchwords = request.args.get("ksearchwords")
    s = ElasticSearch()
    s.engtoKor(searchwords)
    searchres = s.engtoKorequiv()
    return jsonify(searchres)

