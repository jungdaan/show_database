# imports
from flask import Flask, request, redirect, url_for, session, render_template, flash, g
import sqlite3

#configuration
SECRET_KEY='development key'
ID='hellopjhs'
PASSWORD='admin'
DEBUG=True
DATABASE='result.db'

#application
app = Flask(__name__)
app.config.from_object(__name__)

#connect db
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

#before_request
@app.before_request
def before_request():
	g.db = connect_db()

#teardown_request
@app.teardown_request
def teardown_request(exception):
	g.db.close()

#get maillist
def get_mail():
	cur = g.db.execute('select username, usermail, title, sender_name, sender_mail from maillist')
	maillist = [dict(username=row[0], usermail=row[1], title=row[2], sendername=row[3], sendermail=row[4]) for row in cur.fetchall()]
	return maillist

#get dns
def get_dns():
	cur = g.db.execute('select name, ttl, data from dns')
	dnslist = [dict(url=row[0], ttl=row[1], ip=row[2]) for row in cur.fetchall()]
	return dnslist

#get kakao
def get_kakao():
	cur = g.db.execute('select url from kakao')
	kakaolist = [dict(url=row[0]) for row in cur.fetchall()]
	return kakaolist

#homepage
@app.route('/')
def home():
	return render_template('homepage.html')

#show db
@app.route('/show')
def show_db():
	maillist=[]
	dnslist=[]
	kakaolist=[]
	maillist = get_mail()
	dnslist = get_dns()
	kakaolist = get_kakao()

	return render_template('show_db.html', maillist=maillist, dnslist=dnslist, kakaolist=kakaolist)

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['id'] != app.config['ID']:
			error='Invalid ID'
		elif request.form['password'] != app.config['PASSWORD']:
			error='Invalid Password'
			flash('You were logged in!')
			return redirect(url_for('show_db'))
	return render_template('login.html', error=error)

#logout
@app.route('/logout')
def logout():
	session.pop('login', None)
	flash('You were logged out!')
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run()


