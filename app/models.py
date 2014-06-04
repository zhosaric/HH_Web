from app import db
from hashlib import md5

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	histories = db.relationship('HHistory', backref = 'player', lazy = 'dynamic')
	last_seen = db.Column(db.DateTime)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

	def __repr__(self):
		return '<User {}>'.format(self.nickname)	

class HHistory(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	filelink = db.Column(db.String)
	filedate = db.Column(db.DateTime)

	def __repr__(self):
		return '<File {}, {}>'.format(self.filelink, self.filedate)