from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from app.forum import forum_db
from app.forum.login import bp
from app.forum.login.forms import LoginForm, RegistrationForm
from app.forum.models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_forum.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main_forum.index')
        return redirect(next_page)
    return render_template('login/login_forum.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_forum.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_forum.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, name=form.name.data, surname=form.name.data)
        user.set_password(form.password.data)
        forum_db.session.add(user)
        forum_db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login.login'))
    return render_template('login/register_forum.html', title='Register', form=form)
