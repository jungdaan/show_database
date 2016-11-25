# imports
from flask import Flask, request, redirect, url_for, session, render_template, flash, g
import sqlite3

#configuration
SECRET_KEY='development key'
ID='admin'
PASSWORD='11'
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
	cur = g.db.execute('select id, username, usermail, title, sender_name, sender_mail from maillist')
	maillist = [dict(id=row[0], username=row[1], usermail=row[2], title=row[3], sendername=row[4], sendermail=row[5]) for row in cur.fetchall()]
	return maillist

#get dns
def get_dns():
	cur = g.db.execute('select id, name, ttl, data from dns')
	dnslist = [dict(id=row[0], url=row[1], ttl=row[2], ip=row[3]) for row in cur.fetchall()]
	return dnslist

#get kakao
def get_kakao():
	cur = g.db.execute('select id, url from kakao')
	kakaolist = [dict(id=row[0], url=row[1]) for row in cur.fetchall()]
	return kakaolist

#homepage
@app.route('/')
def home():
	return render_template('homepage.html')

#show db
@app.route('/show')
def show_db():
	return render_template('show_db.html')

#maillist db
@app.route('/maillist')
def Maillist_db():
	maillist=[]
	maillist = get_mail()

	return render_template('Maillist_db.html', maillist=maillist)

#dns db
@app.route('/dns')
def DNS_db():
	dnslist=[]
	dnslist = get_dns()

	return render_template('DNS_db.html', dnslist=dnslist)

#kakao db
@app.route('/kakao')
def KAKAO_db():
	kakaolist=[]
	kakaolist = get_kakao()

	return render_template('KAKAO_db.html', kakaolist=kakaolist)

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['id'] != app.config['ID']:
			error='Invalid ID'
		elif request.form['password'] != app.config['PASSWORD']:
			error='Invalid Password'
		else:
			session['login']=True
			flash('You were logged in!')
			return redirect(url_for('home'))
	return render_template('login.html', error=error)

#logout
@app.route('/logout')
def logout():
	session.pop('login', None)
	flash('You were logged out!')
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run()