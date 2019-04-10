from helloflask import app
from flask import Flask, render_template, url_for, jsonify, request, flash, session, redirect, Response, make_response
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
    session['next'] = request.url
    return render_template('main.htm', title="Main")


@app.route('/posting/detail/<postid>')
def detail(postid):
    p = Post.query.filter('postid = :postid').params(postid=postid).first()
    userid = p.user.userid
    return render_template('detailpost.htm', userid=userid)


@app.route('/posting/write')
def postwrite():
    return render_template('write.htm')


@app.route('/posting/lists/<userid>')
def lists(userid):
    if not session.get('loginUser'):
        return redirect('/login')
    else:
        userid = session['loginUser']['userid']
        posts = Post.query.options(subqueryload(Post.user)).filter('user_id = :userid').params(userid=userid).all()
        lsts = []
        for post in posts:
            l = post.json()
            l['username'] = post.user.username
            lsts.append(l)
        print(lsts)
        return jsonify(lsts)
# [s.json() for s in cmts]

@app.route('/posting')
def posting():
    session['next'] = request.url
    userid = session['loginUser']['userid']
    if not session.get('loginUser'):
        session['next'] = request.url
        return redirect('/login')
    print("userid>>>>>>>>>>", userid)
    return render_template('posting.htm', userid = userid)


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

@app.route('/logout')
def logout():
    if session.get('loginUser'):
        del session['loginUser']
    return redirect(session['next'])

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.htm')


@app.route('/login', methods=['POST'])
def loginpost():
    a = request.json
    print("aaaaaaaaaaaa>", a)
    u = User.query.filter('email = :email and passwd = sha2(:passwd, 256)').params(email = a['email'], passwd = a['passwd']).first()
    session['loginUser'] = {'userid':u.id, 'username':u.username}
    if u is not None:
        if (session.get('next')):
            statusjson = { 'status' : 'success', 'username' : session['loginUser']['username'], 'session' : 'OK', 'next': session.get('next')}
            return jsonify(statusjson)
        else:
            statusjson = { 'status' : 'success', 'username' : session['loginUser']['username'], 'session' : 'OK'}
        return jsonify(statusjson)
    else:
        errorjson = { 'status' : 'error'}
        return jsonify(errorjson)

@app.route('/compare')
def compare():
    session['next'] = request.url
    return render_template('compare.htm')


# def wc():
#     key = request.args.get('key')
#     value = request.args.get('val')
#     res = Response('Done',200)
#     res.set_cookie(key, value)
#     # session[key] = value
#     session['Token'] = '123X'
#     return make_response(res)


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

