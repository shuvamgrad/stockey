from app import app, db, celery, logger
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
	task = get_background_price.apply_async()
	return render_template('stock.html', title='Stock Details', stocks=stocks)


@celery.task(bind=True)
def get_background_price(self):
	stocks = Stock.query.all()
	for stock in stocks:
		logger.info(stock)
		#avail = fa.available_companies(app.config['FUNDAMENTAL_ANALYSIS_API_KEY'])
		profile = fa.profile(str(stock.name), str(app.config['FUNDAMENTAL_ANALYSIS_API_KEY']))
		#logger.info(avail.to_dict())
		logger.info(stock.name)
		stock.price = profile.to_dict()[0]['price']
		logger.info(stock.price)
		db.session.add(stock)
		self.update_state(state='PROGRESS',
							meta={'id': stock.id, 'name': stock.name, 'price': stock.price})
		logger.info(self.update_state)
	db.session.commit()
	return {'state':'COMPLETE'}