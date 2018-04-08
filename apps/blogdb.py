# -*- coding: utf-8 -*-
import sqlite3

from flask import g
from apps import app
from model import User


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
