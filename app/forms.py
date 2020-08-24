from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class StockNameForm(FlaskForm):
	stock_name = StringField('Stock Names', validators=[DataRequired()])
	submit = SubmitField('Search')