from flask import render_template, render_template_string, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, ItemForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Fridge, Reference
from datetime import datetime, timedelta
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from binascii import a2b_base64
import json

cfapp = ClarifaiApp(api_key='4f436d3877f148a7bf8ec1c680a44233')
model = cfapp.models.get('food-items-v1.0')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/view')
@login_required
def view():
	return render_template('view.html', title='View Items', fridges=Fridge.query.filter_by(user_id=current_user.get_id()).order_by(Fridge.expiration))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	form = ItemForm()
	if form.validate_on_submit():
		# Calls to Reference table deactivated until it is populated
		# ref_item = Reference.query.filter_by(item=form.item.data).first()
		item = Fridge(user_id=current_user.get_id(),
					  item=form.item.data,
					  quantity=form.quant.data,
					  expiration=datetime.now()+timedelta(days=5)#ref_item.roomtemp)
				     )
		db.session.add(item)
		db.session.commit()
		flash("Item successfully added.")
		return redirect(url_for('add'))
	return render_template('add.html', title='Add Items', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash("Invalid username or password.")
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash("You have been registered. You may log in.")
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/addbyimg')
@login_required
def webcam():
	return render_template('webcam.html')

@app.route('/ai', methods=['POST'])
def ai():
	#if request.form['img'] is None:
	#	return redirect(url_for('webcam'))
	idata = request.form['img'][22:]
	bdata = a2b_base64(idata)
	with open('temp.png','wb') as fo:
   		fo.write(bdata)

	image = ClImage(file_obj=open('temp.png', 'rb'))
	response = model.predict([image])
	concept = response['outputs'][0]['data']['concepts'][0]['name']
	return render_template_string("{{ data }}", data=concept)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
	itemID = request.form['id']
	Fridge.query.filter_by(id=itemID).delete()
	db.session.commit()
	return render_template_string("success")
	


