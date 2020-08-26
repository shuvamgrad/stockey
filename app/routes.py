from app import app, db, celery, logger
from flask import render_template, redirect, url_for, jsonify
from app.forms import StockNameForm
from app.models import Stock
import FundamentalAnalysis as fa
import json


@app.route('/', methods=['GET','POST'])
def getStockName():
	form = StockNameForm()
	if form.validate_on_submit():
		for name in form.stock_name.data.split(','):
			stock = Stock(name=name)
			db.session.add(stock)
			db.session.commit()
		return redirect(url_for('stock'))
	return render_template('index.html', title='Stockey', form=form)


@app.route('/stock')
def stock():
	stocks = Stock.query.all()
	task = get_background_price.apply_async()
	return render_template('stock.html', title='Stock Details', stocks=stocks)


@celery.task()
def get_background_price():
	stocks = Stock.query.all()
	for stock in stocks:
		profile = fa.profile(str(stock.name), str(app.config['FUNDAMENTAL_ANALYSIS_API_KEY']))
		stock.price = profile.to_dict()[0]['price']
		db.session.add(stock)
		# self.update_state(state='PROGRESS',
		# 					meta={'id': stock.id, 'name': stock.name, 'price': stock.price})
	db.session.commit()
	return {'state':'COMPLETE'}


@app.route('/status')
def status():
	stock_list = []
	stocks = Stock.query.all()
	for stock in stocks:
		if stock.price != None:
			response = {
				'id': stock.id,
				'price': stock.price
			}
			stock_list.append(response)
	return json.dumps(stock_list)