from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, HistoryForm
from datetime import datetime
from models import User, HHistory
from werkzeug.utils import secure_filename
import os
import HH_Calculator as hCalc
 
@app.route('/')
@app.route('/index')
def index():
	user = g.user
	return render_template("index.html",
		title = 'Home',
		user = user)

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
	return render_template('login.html',
		title = 'Sign In',
		form = form,
		providers = app.config['OPENID_PROVIDERS'])


@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email == "":
		flash('Invalid login. Please try again')
		return redirect(url_for('login'))
	user = User.query.filter_by(email = resp.email).first()
	if user is None:
		nickname = resp.nickname
		if nickname is None or nickname == "":
			nickname = resp.email.split('@')[0]
		user = User(nickname=nickname, email = resp.email)
		db.session.add(user)
		db.session.commit()
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember = remember_me)
	return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
	user = User.query.filter_by(nickname = nickname).first()
	if user == None:
		flash('User' + nickname + ' not found.')
		return redirect(url_for('index'))
	return render_template('user.html',
		user = user)

@app.route('/user/<nickname>/files', methods = ['GET', 'POST'])
@login_required
def files(nickname):
	form = HistoryForm()
	if form.validate_on_submit():
		filename = secure_filename(form.fileName.data.filename)
		#insert query tests if file in database
		hHistory = HHistory(filelink = filename, user_id = g.user.id)
		file = form.fileName.data
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		db.session.add(hHistory)
		db.session.commit()
		flash('The file:' + filename + ' was uploaded')
	Hhist = HHistory.query.filter_by(user_id = g.user.id).all()
	return render_template('upload.html',
		form = form,
		files = Hhist)


@app.route('/user/<nickname>/progress/<file_id>')
@login_required
def progress(nickname, file_id):
	hist = HHistory.query.filter_by(id = file_id, user_id = g.user.id).first()
	Hhist = HHistory.query.filter_by(user_id = g.user.id).all()
	if hist:
		myHistory = hCalc.HandParse(os.path.join(app.config['UPLOAD_FOLDER'], hist.filelink))
		historyList = myHistory.profitList()
		return render_template('results.html',
			current_file = hist.filelink,
			files = Hhist,
			data = historyList)
	return render_template('results.html',
		files = Hhist,
		data = [])

@app.route('/user/<nickname>/file/<file_id>/delete')
@login_required
def delete_file(nickname, file_id):
	hist = HHistory.query.filter_by(id = file_id, user_id = g.user.id).first()
	if hist:
		if hist.filelink in os.listdir(app.config['UPLOAD_FOLDER']):
			os.remove(os.path.join(app.config['UPLOAD_FOLDER'], hist.filelink))
		db.session.delete(hist)
		db.session.commit()
		flash(hist.filelink + " successfully deleted.")
	return redirect(url_for('files', nickname = g.user.nickname))



def upload_file():
	if request.method =='POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FILE'], filename))
			return redirect(url_for('uploaded_file',
									filename = filename))

@app.before_request
def before_request():
	g.user = current_user