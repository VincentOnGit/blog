import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g
from model import User

app = Flask(__name__)
app.config["DATABASE"] = 'database.db'


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
	sql_insert = "INSERT INTO users (name, pwd, email, age, birthday, face) VALUES (?, ?, ?, ?, ?, ?)"
	args = [user.name, user.pwd, user.email, user.age, user.birthday, user.face]
	g.db.execute(sql_insert, args)
	g.db.commit()


def query_users_from_db():
	users = []
	sql_query = "SELECT * FROM users ORDER BY id ASC"
	args = []
	cur = g.db.execute(sql_query, args)
	for item in cur.fetchall():
		users.append(item)
	return users


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def user_login():
	users = query_users_from_db()
	print users
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
		insert_user_to_db(user)
		return redirect(url_for("user_login", username=user.name))
	return render_template('user_regist.html')


if __name__ == '__main__':
	app.run(debug=True)
