# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DateField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange


class RegistForm(FlaskForm):
	user_name = StringField(
		label="用户名",
		validators=[
			DataRequired(message=u"用户名不能为空！"),
			Length(min=3, max=15, message=u"用户名长度在[%(min)d, %(max)d]之间")
		],
		render_kw={"id": "user_name", "class": "form-control", "placeholder": u"请输入用户名"}
	)
	user_pwd = PasswordField(
		label="密码",
		validators=[
			DataRequired(message=u"密码不能为空"),
			Length(min=3, max=16, message=u"密码长度在[%(min)d, %(max)d]之间")
		],
		render_kw={"id": "user_pwd", "class": "form-control", "placeholder": u"请输入密码"}
	)
	user_email = StringField(
		label="邮箱",
		validators=[
			DataRequired(message=u"邮箱不能为空"),
			Email(message=u"邮箱格式错误")
		],
		render_kw={"id": "user_email", "class": "form-control", "placeholder": u"请输入邮箱"}
	)
	user_age = IntegerField(
		label="年龄",
		validators=[
			DataRequired(message=u"年龄不能为空"),
			NumberRange(min=1, max=200, message=u"年龄在1到200之间")
		],
		render_kw={"id": "user_age", "class": "form-control", "placeholder": u"请输入年龄"}
	)
	user_birthday = DateField(
		label="生日",
		validators=[
			DataRequired(message=u"生日不能为空")
		],
		render_kw={"id": "user_birthday", "class": "form-control", "placeholder": u"请输入生日"}
	)
	user_face = FileField(
		label="头像",
		validators=[],
		render_kw={"id": "user_face", "class": "form-control"}
	)
	submit = SubmitField(
		label="注册",
		render_kw={
			"class": "btn btn-success",
			"values": "注册",
		}
	)
