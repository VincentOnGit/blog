# -*- coding: utf-8 -*-

import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g, flash, session, make_response
from model import User

app = Flask(__name__)
app.config["DATABASE"] = 'database.db'
app.config["SECRET_KEY"] = '\xa2\xda\x01\xdb\xa7\x03\xeb\x9c-\xaec\xca\xea\xd1\xa7\x14\xe1\xd34\xd9\xa8\xcf\x99'


def connect_db():
	"""Connects to the specific database."""
	db = sqlite3.connect(app.config['DATABASE'])
	return db


@app.before_request
def before_request():
	g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
	if hasattr(g, 'db'):
		g.db.close()


def init_db():
	with app.app_context():
		db = connect_db()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()


def insert_user_to_db(user):
	attrsRepr, placeHolders = user.getAttrsRepr()
	sql_insert = "INSERT INTO users " + attrsRepr + " VALUES " + placeHolders
	args = user.toList()
	g.db.execute(sql_insert, args)
	g.db.commit()


def query_users_from_db():
	users = []
	sql_query = "SELECT * FROM users ORDER BY id ASC"
	args = []
	cur = g.db.execute(sql_query, args)
	for item in cur.fetchall():
		user = User()
		user.fromList(item[1:])
		users.append(user)
	return users


def query_user_by_name(user_name):
	sql_select = "select * from users where name=?"
	args = [user_name]
	cur = g.db.execute(sql_select, args)
	item = cur.fetchone()
	if item:
		user = User()
		user.fromList(item[1:])
		return user
	return None


def delete_user_by_name(user_name):
	sql_delete = "delete from users where name=?"
	args = [user_name]
	g.db.execute(sql_delete, args)
	g.db.commit()


def update_user_by_name(user_name, attrs):
	if 'name' in attrs:
		raise Exception(u'不能修改用户名')
	setter = ''
	cnt = len(attrs.keys())
	i = 0
	for key, value in attrs.iteritems():
		setter += (key + '=?')
		if i < cnt - 1:
			setter += ', '
		i += 1
	sql_update = "update users set " + setter + " where name=?"
	args = []
	for key, value in attrs.iteritems():
		args.append(value)
	args.append(user_name)
	g.db.execute(sql_update, args)
	g.db.commit()


def show_all_rows():
	users = query_users_from_db()
	for user in users:
		print user.toList()


@app.route('/')
def index():
	print session
	resp = make_response(render_template('index.html'))
	resp.set_cookie('aaa', 'bbb')
	return resp


@app.route('/login/', methods=['GET', 'POST'])
def user_login():
	if request.method == 'POST':
		username = request.form['user_name']
		pwd = request.form['user_pwd']
		user_x = query_user_by_name(username)
		if not user_x:
			flash(u"用户不存在，登录失败", category='error')
			return render_template('user_login.html')
		else:
			if str(pwd) != str(user_x.pwd):
				flash(u"密码错误！", category="error")
				return render_template('user_login.html')
			else:
				session["user_name"] = user_x.name
				return render_template('index.html')
	return render_template('user_login.html')


@app.route('/regist/', methods=['GET', 'POST'])
def user_regist():
	if request.method == 'POST':
		user = User()
		user.name = request.form['user_name']
		user.pwd = request.form['user_pwd']
		user.email = request.form['user_email']
		user.age = request.form['user_age']
		user.birthday = request.form['user_birthday']
		user.face = request.form['user_face']
		user_x = query_user_by_name(user.name)
		if user_x:
			flash(u"用户名已经存在！", category='error')
			return render_template('user_regist.html')
		insert_user_to_db(user)
		flash(u"注册成功", category='ok')
		return redirect(url_for("user_login", username=user.name))
	return render_template('user_regist.html')


@app.route('/logout')
def logout():
	session.pop('user_name', None)
	return redirect(url_for('index'))


if __name__ == '__main__':
	app.run(debug=True)
