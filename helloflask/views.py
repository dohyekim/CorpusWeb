from helloflask import app
from flask import Flask, render_template, url_for, jsonify, request, flash, session, redirect, Response, make_response
from helloflask.init_db import init_database, db_session
from helloflask.models import Talk, User, Post, Checklist
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import subqueryload, joinedload
from sqlalchemy.sql import func
from helloflask.Search import ElasticSearch
from helloflask.forms import RegistrationForm, PostForm
import difflib
# import json

@app.route('/')
def main():
    session['next'] = request.url
    return render_template('main.htm', title="Main")

@app.route('/checklist/<userid>')
def checklist(userid):
    userid = session['loginUser']['userid']
    check = Checklist.query.options(subqueryload(Checklist.user)).filter('user_id = :userid').params(userid=userid).all()
    checklst = []
    for c in check:
        checklst.append(c.json())
    return jsonify(checklst)



@app.route('/posting/save/<userid>', methods=['POST'])
def save(userid):
    j={}
    savelst = request.json
    print("sssssssssssssssssssssssssssssssssssssssssss> ", savelst['checklist'], len(savelst['checklist']))
    c = Checklist(userid, savelst['name'], savelst['checklist'])
    try:
        db_session.add(c)
        db_session.commit()
        print("checklist data inserted")
        j['status'] = 'success'
    except:
        db_session.rollback()
        j['status'] = 'fail'
    return jsonify(j)

@app.route('/posting/detail/<userid>/postid=<postid>')
def detailajax(userid, postid):

    return render_template('detailpost.htm', userid=userid, postid=postid)

@app.route('/posting/<userid>/<postid>')
def detail(userid, postid):
    p = Post.query.options(subqueryload(Post.user)).filter('postid = :postid and user_id = :userid').params(postid=postid, userid=userid).first()
    a = p.json()
    a['username'] = p.user.username
    return jsonify(a)

@app.route('/posting/delete/<userid>/<postid>', methods=['DELETE'])
def delpost(userid, postid):
    dpost = Post.query.filter('postid=:postid and user_id = :userid').params(postid=postid, userid=userid).first()
    try:
        db_session.delete(dpost)
        db_session.commit()
        print("-------------------------------------------------Delete success")
        return ''
    except Exception as err:
        db_session.rollback()
        print("\n\n\n--------------------------Fail Delete", err, "\n\n\n\n")
        return ''


@app.route("/posting/write/checklist", methods=['GET'])
def postchecklist():
    userid = session['loginUser']['userid']
    select = request.args.get('namelist')

    print('dddddddddddddddddddddddddddddddddd', select)  
    print('dddddddddddddddddddddddddddddddddd', userid)
        
    return redirect('/posting/write')


@app.route('/posting/write', methods=['POST'])
def postwrite():

    loginUser = session.get('loginUser')
    userid = session['loginUser']['userid']
    title = request.form.get('title')
    content = request.form.get('content')
    select = request.form.get('namelist-' + str(userid))
        
    # if select:
        
    print("select>>>>>>", select)
    post = Post(title, content, loginUser.get('userid'))

    try:
        db_session.add(post)
        db_session.commit()
        print("Done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    except Exception as err:
        db_session.rollback()
        print("\n \n \n Error!!!!!!!!!!!!!!!!!!!!!!", err)

    return redirect('/posting')


@app.route('/posting/write', methods=['GET'])
def getwrite():
    if session.get('loginUser'):
        userid = session['loginUser']['userid']

        return render_template('write.htm', title="New Post", userid=userid)

    else:
        session['next'] = request.url
        return redirect('/login')


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

@app.route('/posting/compare', methods=['POST'])
def postingcompare():
    if not session.get('loginUser'):
        return redirect('/login')
    htmls = request.json
    print("htmls>>>>>> ", htmls)
    htm_1 = htmls['1'].splitlines()
    htm_2 = htmls['2'].splitlines()
    d2 = difflib.HtmlDiff()
    diffHtml = d2.make_file(htm_1, htm_2)
    # print(diffHtml)
    return jsonify({'HTML':diffHtml})
    

@app.route('/posting')
def posting():
    # request.args.get('list-title-')
    session['next'] = request.url
    if not session.get('loginUser'):
        session['next'] = request.url
        return redirect('/login')
    else:
        userid = session['loginUser']['userid']
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
    if u is not None:
        session['loginUser'] = {'userid':u.id, 'username':u.username}
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

