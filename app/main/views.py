from flask import render_template, session, redirect, url_for, current_app
from flask import request
from flask import abort

from datetime import datetime

from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    user_agent = request.headers.get('User-Agent')
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('homepage.html', user_agent=user_agent, 
                           current_time=datetime.utcnow(), form=form, 
                           name=session.get('name'), known = session.get('known', False))    

                           

                           
@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
    
@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
    
    
@main.route('/search')
def redirct():
    return redirect('http://www.google.com')    

@main.route('/userid/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1> 你好！%s </h1>' %id
	
