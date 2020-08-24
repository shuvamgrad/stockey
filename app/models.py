from app import db

class Stock(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), index=True)
	price = db.Column(db.Integer)

	def __repr__(self):
		return '<Stock {}>'.format(self.name)

	
