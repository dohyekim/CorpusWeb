from helloflask import app
from flask import Flask, render_template, url_for, jsonify, request, flash, session, redirect
from helloflask.init_db import init_database, db_session
from helloflask.models import Talk, User, Post
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import subqueryload, joinedload
from sqlalchemy.sql import func
from helloflask.Search import ElasticSearch
from helloflask.forms import RegistrationForm
# import json

@app.route('/')
def main():

    return render_template('main.htm', title="Main")

@app.route('/register', methods=['GET','POST'])
def register_post():
    register = RegistrationForm()
    if register.validate_on_submit():
        flash('Account created for {}'.format(register.username.data), 'success')
        u = User(register.password.data, register.email.data,  register.username.data)
        try:
            db_session.add(u)
            db_session.commit()
            print("data inserted")
        except:
            db_session.rollback()

        return redirect('/login')

    return render_template('register.htm', title='Register Page', register = register)

# @app.route('/tags')
# def tags():
#     # tags = Talk.query.filter(Talk.id == talkid)
#     tags = Talk.query.first()
#     print(tags)
#     tag = {"tags":tags}
#     print(type(tags))
#     print(tags.tags)
#     return jsonify(tags.json())

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.htm')

@app.route('/posting/lists/<userid>')
def lists(userid):
    userid = session['loginUser']['userid']
    posts = Post.query.options(subqueryload(Post.user)).filter('user_id = :userid').params(userid=userid).all()

    lsts = []
    for post in posts:
        l = post.json()
        lsts.append(l)
    return jsonify(lsts)

@app.route('/posting')
def posting():
    return render_template('posting.htm')

@app.route('/login', methods=['POST'])
def loginpost():
    a = request.json
    u = User.query.filter('email = :email and passwd = sha2(:passwd, 256)').params(email = a['email'], passwd = a['passwd']).first()
    if u is not None:
        session['loginUser'] = {'userid':u.id, 'username':u.username}
        statusjson = { 'status' : 'success', 'username' : session['loginUser']['username']}
        if (session.get('next')):
            nextpg = {'next': session.get('next')}
            return jsonify(nextpg)
        return jsonify(statusjson)
    else:
        errorjson = { 'status' : 'error'}
        return jsonify(errorjson)

@app.route('/compare')
def compare():
    return render_template('compare.htm')

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

