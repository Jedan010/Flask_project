from flask import render_template
from flask import redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm
from ..email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('账户或者密码错误！')
    return render_template('auth/login.html', form=form)
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录！')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        token = user.generate_confirmation_token()
        send_email(user.email, '验证您的账户', 'auth/email/confirm', user=user, token=token)
        flash('验证邮件已经发送到您的账号')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('您已经成功验证您的邮箱了！感谢！')
    else:
        flash('验证链接无效或者已经过期了！')
    return redirect(url_for('main.index'))


@auth.before_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed \
        and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous() or current_user.confirmed:
        return redirect(url_for('mail.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '验证您的账户', 'auth/email/confirm', user=current_user, token=token)
    flash('一封新的验证邮件已经发送到您的邮箱。')
    return redirect(url_for('mail.index'))

