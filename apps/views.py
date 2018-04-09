# -*- coding: utf-8 -*-

import os
from functools import wraps
from flask import render_template, request, redirect, url_for, flash, session, make_response

from blogdb import query_user_by_name, insert_user_to_db, update_user_by_name, delete_user_by_name
from model import User
from forms import RegistForm, LoginForm, ChangePWDForm, ChangeInfoForm, DeleteForm
from utils import change_filename_to_uuid, check_files_ext, ALLOWED_IMAGE_EXT

from apps import app, UPLOAD_FOLDER


def user_login_req(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		if "user_name" not in session:
			return redirect(url_for("user_login", next=request.url))
		return func(*args, **kwargs)

	return decorated_function


@app.route('/')
def index():
	resp = make_response(render_template('index.html'))
	return resp


@app.route('/login/', methods=['GET', 'POST'])
def user_login():
	loginForm = LoginForm()
	if loginForm.validate_on_submit():
		username = request.form['user_name']
		pwd = request.form['user_pwd']
		user_x = query_user_by_name(username)
		if not user_x:
			flash(u"用户不存在，登录失败", category='error')
			return render_template('user_login.html', form=loginForm)
		else:
			if str(pwd) != str(user_x.pwd):
				flash(u"密码错误！", category="error")
				return render_template('user_login.html', form=loginForm)
			else:
				session["user_name"] = user_x.name
				return redirect(url_for("index"))
	return render_template('user_login.html', form=loginForm)


@app.route('/regist/', methods=['GET', 'POST'])
def user_regist():
	regForm = RegistForm()
	if regForm.validate_on_submit():
		if not check_files_ext([regForm.user_face.data.filename], ALLOWED_IMAGE_EXT):
			flash(message=u'上传的图片格式不支持！', category='error')
			return render_template('user_regist.html', form=regForm)
		user = User()
		user.name = request.form['user_name']
		user.pwd = request.form['user_pwd']
		user.email = request.form['user_email']
		user.age = request.form['user_age']
		user.birthday = request.form['user_birthday']
		f = request.files['user_face']
		user.face = change_filename_to_uuid(f.filename)
		user_x = query_user_by_name(user.name)
		if user_x:
			flash(u"用户名已经存在！", category='error')
			return render_template('user_regist.html', form=regForm)
		insert_user_to_db(user)
		userfolder = os.path.join(app.config["UPLOAD_FOLDER"], user.name)
		if not os.path.exists(userfolder):
			os.mkdir(userfolder, os.O_RDWR)
		f.save(os.path.join(userfolder, user.face))
		flash(u"注册成功", category='ok')
		return redirect(url_for("user_login", username=user.name))
	return render_template('user_regist.html', form=regForm)


@app.route('/center/')
@user_login_req
def user_center():
	return render_template("user_center.html")


@app.route('/detail/')
@user_login_req
def user_detail():
	user = query_user_by_name(session.get('user_name', ''))
	return render_template("user_detail.html", user=user, uploadfolder=UPLOAD_FOLDER)


@app.route('/pwd/', methods=['GET', 'POST'])
@user_login_req
def user_pwd():
	changeForm = ChangePWDForm()
	if changeForm.validate_on_submit():
		old_pwd = request.form['old_pwd']
		new_pwd = request.form['new_pwd']
		user = query_user_by_name(session.get("user_name"))
		if str(user.pwd) == str(old_pwd):
			user.pwd = str(new_pwd)
			update_user_by_name(user.name, {"pwd": user.pwd})
			session.pop("user_name", None)
			flash(message=u"密码修改成功", category="ok")
			return redirect(url_for('user_login', username=user.name))
		else:
			flash(message=u"密码输入错误", category="error")
			return render_template("user_pwd.html", form=changeForm)
	return render_template("user_pwd.html", form=changeForm)


@app.route('/info/', methods=['GET', 'POST'])
@user_login_req
def user_info():
	infoForm = ChangeInfoForm()
	user_old = query_user_by_name(session.get('user_name'))
	if infoForm.validate_on_submit():
		user = User()
		user.name = request.form.get('user_name') if request.form['user_name'] else user_old.name
		user.email = request.form.get('user_email') if request.form['user_email'] else user_old.email
		user.age = request.form.get('user_age') if request.form['user_age'] else user_old.age
		user.birthday = request.form.get('user_birthday') if request.form['user_birthday'] else user_old.birthday
		user.face = request.form.get('user_face') if request.form['user_face'] else user_old.face
		update_user_by_name(user_old.name,
							{
								"name": user.name,
								"email": user.email,
								"age": user.age,
								"birthday": user.birthday,
								"face": user.face
							}
							)
		session['user_name'] = user.name
		return redirect(url_for("user_detail"))
	return render_template("user_info.html", user=user_old, form=infoForm)


@app.route('/delete/', methods=['GET', 'POST'])
@user_login_req
def user_delete():
	delForm = DeleteForm()
	if delForm.validate_on_submit():
		delete_user_by_name(session.get('user_name'))
		return redirect(url_for('logout'))
	return render_template("user_delete.html", form=delForm)


@app.route('/logout')
def logout():
	session.pop('user_name', None)
	return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
	resp = make_response(render_template("page_not_found.html"), 404)
	return resp
