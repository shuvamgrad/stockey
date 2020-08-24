from app import app, db, celery
from flask import render_template, redirect, url_for
from app.forms import StockNameForm
from app.models import Stock
import FundamentalAnalysis as fa
import json


@app.route('/', methods=['GET','POST'])
def getStockName():
	form = StockNameForm()
	if form.validate_on_submit():
		print(form.stock_name.data.split(','))
		for name in form.stock_name.data.split(','):
			stock = Stock(name=name)
			db.session.add(stock)
			db.session.commit()
		return redirect(url_for('stock'))
	return render_template('index.html', title='Stockey', form=form)


@app.route('/stock')
def stock():
	stocks = Stock.query.all()
	json_data = json.dumps(stocks)
	print(json_data)
	task = get_background_price.apply_async(args=[json_data])
	return render_template('stock.html', title='Stock Details', stocks=stocks)


@celery.task
def get_background_price(json_data):
	#print(fa.available_companies(app.config['FUNDAMENTAL_ANALYSIS_API_KEY']))
	for stock in json_data:
		if stock.name in fa.available_companies(app.config['FUNDAMENTAL_ANALYSIS_API_KEY']):
			profile = fa.profile(stock.name, app.config['FUNDAMENTAL_ANALYSIS_API_KEY'])
			print('profile :', profile)
	return {"profile": True}