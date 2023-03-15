from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from app.extensions import limiter, db
from app.models.user import User
from app.forms import LoginForm, RegisterForm, AdminUserForm, UpdateEmailForm
from app.auth import auth_bp


@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("100 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.homepage'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('login'))

    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("100 per minute")
def register():
    is_admin = False
    if current_user.is_authenticated and current_user.is_admin:
        is_admin = True

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('An account already exists with that email')
            return redirect(url_for('auth.register'))
        else:
            user = User(email=email, is_admin=is_admin)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('main.homepage'))

    return render_template('auth/register.html', is_admin=is_admin, form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))


@auth_bp.route('/admin', methods=['GET', 'POST'])
@login_required
@limiter.limit("100 per minute")
def admin():
    if not current_user.is_admin:
        abort(403)

    form = AdminUserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('An account already exists with that email')
        else:
            is_admin = form.is_admin.data
            user = User(email=email, is_admin=is_admin)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('User added successfully')
        return redirect(url_for('auth.admin'))

    users = User.query.all()
    return render_template('auth/admin.html', users=users, form=form)

@auth_bp.route('/update_email', methods=['GET', 'POST'])
@login_required
def update_email():
    form = UpdateEmailForm()
    if form.validate_on_submit():
        email = form.email.data
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email provided already exists.', 'danger')
            return redirect(url_for('auth.update_email'))
        else:
            if current_user.check_password(form.password.data):
                current_user.email = form.email.data
                db.session.commit()
                flash('Your email has been updated.', 'success')
                return redirect(url_for('main.homepage'))
            else:
                flash('Invalid password.', 'danger')
                return redirect(url_for('auth.update_email'))
    return render_template('auth/update_email.html', form=form)
