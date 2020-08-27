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
			name = name.strip()
			if not Stock.query.filter_by(name=name).first():
				stock = Stock(name=name)
				db.session.add(stock)
				# stocks.append(name)
		db.session.commit()
		stocks = Stock.query.all()
		task = get_background_price.apply_async()
		location_url = url_for('taskstatus', task_id=task.id)
		form.stock_name.data = ""
		return render_template('index.html', title='Stockey', stocks=stocks, form=form, location_url=location_url)
	return render_template('index.html', title='Stockey', form=form)


@celery.task(bind=True)
def get_background_price(self):
	stock_dict = []
	stocks = Stock.query.all()
	for stock in stocks:
		profile = fa.profile(str(stock.name), str(app.config['FUNDAMENTAL_ANALYSIS_API_KEY']))
		# price = profile.to_dict()[0]['price']
		stock.price = profile.to_dict()[0]['price']
		stock_list = {'id':stock.id,'name':stock.name, 'price':stock.price}
		stock_dict.append(stock_list)
		self.update_state(state='PROGRESS', meta={'stock_dict':stock_dict})
	db.session.commit()
	return {'status':'COMPLETE', 'stock_dict': stock_dict}

@app.route('/status/<task_id>')
def taskstatus(task_id):
	task = get_background_price.AsyncResult(task_id)
	if task.state != 'FAILURE':
		return json.dumps(task.info.get('stock_dict'))


