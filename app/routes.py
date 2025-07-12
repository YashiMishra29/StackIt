from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db, login_manager
from app.models import User, Question, Answer, Tag, Vote
from app.forms import LoginForm, RegisterForm, QuestionForm, AnswerForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/')
def home():
    questions = Question.query.order_by(Question.date_posted.desc()).all()
    return render_template('home.html', questions=questions)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        flash('Login failed. Check email and password.', 'danger')
    return render_template('login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(title=form.title.data, description=form.description.data, author=current_user)
        db.session.add(question)

        tag_names = [t.strip().lower() for t in form.tags.data.split(',')]
        for name in tag_names:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
            question.tags.append(tag)

        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('ask.html', form=form)

@bp.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question_detail(question_id):
    question = Question.query.get_or_404(question_id)
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answer(content=form.content.data, author=current_user, question=question)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('main.question_detail', question_id=question.id))
    return render_template('question.html', question=question, form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You’ve been logged out.", "info")
    return redirect(url_for('main.home'))
