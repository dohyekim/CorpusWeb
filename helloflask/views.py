from helloflask import app
from flask import Flask, render_template, url_for, jsonify, request, flash, session, redirect, Response, make_response
from helloflask.init_db import init_database, db_session
from helloflask.models import Talk, User, Post, Checklist, Memo
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import subqueryload, joinedload
from sqlalchemy.sql import func
from helloflask.Search import ElasticSearch
from helloflask.forms import RegistrationForm, PostForm
import difflib
from helloflask.email import send_email
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

# import json

@app.route("/notes")
def notes():
    if session.get('loginUser'):
        userid = session['loginUser']['userid']
        return render_template('notes.htm', title="Notes", userid=userid)

    else:
        session['next'] = request.url
        return redirect('/login')

@app.route('/corpus')
def corpus():
    session['next'] = request.url
    return render_template('corpus.htm', title="Corpus")


@app.route('/', methods=['GET', 'POST'])
def note():
    session['next'] = request.url
    return render_template('main.htm', title="Main")

@app.route('/checklist/edit/<userid>/<id>', methods=['GET', 'POST'])
def editchecklist(userid, id):
    req = request.json
    userid = session['loginUser']['userid']
    name = req['name']
    content = ",".join(req['content'])
    print("name>>", name, "content>>", content)
    check = Checklist(userid, name, content)
    print("check>>>>>",check)
    check.id = id
    try:
        db_session.merge(check)
        db_session.commit()
        print("Update Success!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return jsonify({'status':'success'})

    except Exception as err:
        db_session.rollback()
        print("\n \n \n Error!!!!!!!!!!!!!!!!!!!!!!", err)
        return jsonify({'status':'fail'})

@app.route('/memo/edit/<userid>/<id>', methods=['GET', 'POST'])
def editmemolist(userid, id):
    req = request.json
    userid = session['loginUser']['userid']
    name = req['name']
    content = req['content']
    print("name>>", name, "content>>", content)
    memo = Memo(userid, name, content)
    memo.id = id
    try:
        db_session.merge(memo)
        db_session.commit()
        print("Update Success!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return jsonify({'status':'success'})

    except Exception as err:
        db_session.rollback()
        print("\n \n \n Error!!!!!!!!!!!!!!!!!!!!!!", err)
        return jsonify({'status':'fail'})

@app.route('/write/revision/<userid>/<id>', methods=['GET'])
def editajax(userid, id):
    p = Post.query.options(subqueryload(Post.user)).filter('user_id=:userid and postid=:id').params(userid=userid, id=id).first()
    posts = p.json()
    return jsonify(posts)


@app.route('/write/edit/<userid>/<id>', methods=['GET', 'POST'])
def edit(userid, id):

    userid=session['loginUser']['userid']
    title = request.form.get('title')
    print("title>>", title)
    content = request.form.get('content')
    print("content>>", content)
    post = Post(title, content, userid)
    print(post)
    post.postid = id

    try:
        db_session.merge(post)
        db_session.commit()
        print("Update Success!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return redirect('/posting')

    except Exception as err:
        db_session.rollback()
        print("\n \n \n Error!!!!!!!!!!!!!!!!!!!!!!", err)

    return render_template('writelayout.htm', title="Revise", userid=userid, postid=id, action="/write/edit/{}/{}".format(userid, id), mode="revision")


@app.route('/memo/<userid>')
def memo(userid):
    userid = session['loginUser']['userid']
    memo = Memo.query.options(subqueryload(Memo.user)).filter('user_id = :userid').params(userid=userid).all()
    memolst = []
    for m in memo:
        mJson = m.json()
        memolst.append(mJson)
    print("memolist>>>>>>>", memolst)
    return jsonify(memolst)


@app.route('/test')
def test():
    return render_template('test2.htm')

@app.route('/checklist/<userid>')
def checklist(userid):
    userid = session['loginUser']['userid']
    check = Checklist.query.options(subqueryload(Checklist.user)).filter('user_id = :userid').params(userid=userid).all()
    # checklst = check.json()
    # print(checklst, "ccccc")
    checklst = []
    for c in check:
        a = c.json()
        a['content'] = a['content'].split(",")
        checklst.append(a)
    return jsonify(checklst)


@app.route('/posting/save/<userid>', methods=['POST'])
def save(userid):
    j={}
    savelst = request.json
    print("sssssssssssssssssssssssssssssssssssssssssss> ", savelst['checklist'], len(savelst['checklist']))
    savelst['checklist'] = ",".join(savelst['checklist'])
    c = Checklist(userid, savelst['name'], savelst['checklist'])
    try:
        db_session.add(c)
        db_session.commit()
        print("checklist data inserted")
        j['status'] = 'success'
    except Exception as err:
        db_session.rollback()
        print("Error?>>>>>>>", err)
        j['status'] = 'fail'
    return jsonify(j)


@app.route('/posting/detail/<userid>/postid=<postid>')
def detailajax(userid, postid):

    return render_template('detailpost.htm', title="Your Post",userid=userid, postid=postid)


@app.route('/posting/<userid>/<postid>')
def detail(userid, postid):
    ps = Post.query.options(subqueryload(Post.user)).filter('postid = :postid and user_id = :userid').params(postid=postid, userid=userid).first()
    print(ps)
    a = ps.json()
    a['username'] = ps.user.username
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

@app.route('/checklist/delete/<userid>/<ids>', methods=['DELETE'])
def delchecklist(userid, ids):
    print("delete view")
    dchecklist = Checklist.query.filter('user_id=:userid and id=:id').params(userid=userid,id=ids).first()
    print("checklist to delete >>>>>>>>> ", dchecklist)
    try:
        db_session.delete(dchecklist)
        db_session.commit()
        print("-------------------------------------------------Delete success")
        return jsonify({'status':'success'})
    except Exception as err:
        db_session.rollback()
        print("\n\n\n--------------------------Fail Delete", err, "\n\n\n\n")
        return ''


@app.route('/memolist/delete/<userid>/<id>', methods=['DELETE'])
def delmemo(userid, id):
    dmemo = Memo.query.filter('user_id =:userid and id=:id').params(userid=userid, id=id).first()
    try:
        db_session.delete(dmemo)
        db_session.commit()
        print("-----------SUCCESSFULLY DELETED MEMO---------------")
        return ''
    except Exception as err:
        db_session.rollback()
        print("Failed to delete the memo", err)
        return ''


@app.route('/posting/memo', methods=['POST'])
def postmemo():
    mJson = {}
    memoJson = request.json
    print("\n\n\n\n\n\n", memoJson)
    userid = session['loginUser']['userid']
    title = memoJson['name']
    memo = memoJson['content']
    m = Memo(userid, title, memo)
    try:
        db_session.add(m)
        db_session.commit()
        mJson['status'] = 'success'
        print("Done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    except Exception as err:
        db_session.rollback()
        mJson['status'] = 'fail'
        print("\n \n \n Error!!!!!!!!!!!!!!!!!!!!!!", err)
    return jsonify(mJson)


@app.route("/posting/write/checklist", methods=['POST'])
def postchecklist():
    loadJson = request.json
    # print("lllllllllllllllllllll", loadJson)
    userid = session['loginUser']['userid']
    name = loadJson['name']
    # print("name>>", name)
    check = Checklist.query.options(subqueryload(Checklist.user)).filter('user_id = :userid and name = :name').params(userid=userid, name=name).first()
    # print("ccccccccccccccccccC>", type(check))
    checkJson = check.json()
    checkJson['lists'] = checkJson['content'].split(",")
    return jsonify(checkJson)


@app.route('/posting/write/memolist', methods=['POST'])
def postmemolist():
    loadJson = request.json
    userid = session['loginUser']['userid']
    name = loadJson['name']
    memo = Memo.query.options(subqueryload(Memo.user)).filter('user_id = :userid and name = :name').params(userid=userid, name=name).first()
    memoJson = memo.json()
    memoJson['lists'] = memoJson['content'].split(",")
    return jsonify(memoJson)


@app.route('/posting/write', methods=['POST'])
def postwrite():

    loginUser = session.get('loginUser')
    userid = session['loginUser']['userid']
    title = request.form.get('title')
    content = request.form.get('content')
        
    # if select:
    print("ccc>> ", content)
    print("title>> ", title)
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

        return render_template('writelayout.htm', title="New Post", userid=userid)

    else:
        session['next'] = request.url
        return redirect('/login')


@app.route('/posting/lists/<userid>')
def lists(userid):
    if not session.get('loginUser'):
        return redirect('/login')
    else:
        userid = session['loginUser']['userid']
        posts = Post.query.order_by(Post.postid.desc()).options(subqueryload(Post.user)).filter('user_id = :userid').params(userid=userid).all()
        lsts = []
        for post in posts:
            l = post.json()
            l['username'] = post.user.username
            lsts.append(l)
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
    return render_template('posting.htm', title="Posts", userid = userid)

@app.route('/register/doublecheck', methods=['POST'])
def doublecheck():
    signdata = request.json
    username = signdata['username']
    email = signdata['email']
    us = User.query.filter('username = :username').params(username=username).first()
    ue = User.query.filter('email = :email').params(email = email).first()
    if us != None:
        return jsonify({'status':'username duplicate', 'isChecked': 'False'})
    if ue != None:
        return jsonify({'status':'email duplicate', 'isChecked': 'False'})
    else:
        return jsonify({'status': 'success', 'isChecked': 'False'})
    

@app.route('/register', methods=['GET','POST'])
def register_post():
    register = RegistrationForm()
    if register.validate_on_submit():
        flash('Account created for {}'.format(register.username.data), 'success')
        u = User(register.password.data, register.email.data,  register.username.data)
        try:
            subject = "회원가입 메일"
            mail = "회원가입을 축하합니다"
            # s = URLSafeTimedSerializer('The_Key') # QQQ secret key 바꾸기
            # token = s.dumps(register.email.data, salt = 'email_confirm')
            # confirm_email(token)
            # link = url_for('confirm_email', token = token, _external = True)
            send_email(subject, mail ,register.email.data)
            db_session.add(u)
            db_session.commit()
            print("data inserted")
        except Exception as err:
            db_session.rollback()
            print("ROLL BACK FOR REGISTER", err)

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
    return render_template('login.htm', title="Login")


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
    return render_template('compare.htm', title="Compare")


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

