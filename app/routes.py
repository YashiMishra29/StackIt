from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db, login_manager
from app.models import User, Question, Answer, Tag, Vote
from app.forms import LoginForm, RegisterForm, QuestionForm, AnswerForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

bp = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ✅ Home with filters and pagination
@bp.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    filter_by = request.args.get('filter', 'newest')

    if filter_by == 'unanswered':
        questions = Question.query.filter(~Question.answers.any()).order_by(Question.date_posted.desc())
    elif filter_by == 'votes':
        questions = Question.query.outerjoin(Answer).group_by(Question.id).order_by(func.count(Answer.id).desc())
    else:
        questions = Question.query.order_by(Question.date_posted.desc())

    questions = questions.paginate(page=page, per_page=5)
    return render_template('home.html', questions=questions)


# ✅ Login
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


# ✅ Register
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


# ✅ Ask a Question
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


# ✅ View Question + Answer
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


# ✅ Logout
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You’ve been logged out.", "info")
    return redirect(url_for('main.home'))


# ✅ Vote on an answer (up/down)
@bp.route('/vote/<int:answer_id>/<vote_type>', methods=['POST'], endpoint='vote_answer')
@login_required
def vote_answer(answer_id, vote_type):
    answer = Answer.query.get_or_404(answer_id)

    if vote_type not in ['up', 'down']:
        flash("Invalid vote type.", "danger")
        return redirect(url_for('main.question_detail', question_id=answer.question.id))

    existing_vote = Vote.query.filter_by(user_id=current_user.id, answer_id=answer.id).first()

    if existing_vote:
        flash("You have already voted on this answer.", "warning")
    else:
        vote = Vote(user_id=current_user.id, answer_id=answer.id, vote_type=vote_type)
        db.session.add(vote)
        db.session.commit()
        flash(f"{vote_type.capitalize()}voted!", "success")

    return redirect(url_for('main.question_detail', question_id=answer.question.id))


# ✅ Delete your own answer
@bp.route('/delete_answer/<int:answer_id>', methods=['POST'])
@login_required
def delete_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)

    if answer.author != current_user:
        flash("You can only delete your own answers.", "danger")
        return redirect(url_for('main.question_detail', question_id=answer.question.id))

    question_id = answer.question.id
    db.session.delete(answer)
    db.session.commit()
    flash("Answer deleted.", "info")
    return redirect(url_for('main.question_detail', question_id=question_id))

@bp.route('/accept_answer/<int:answer_id>', methods=['POST'])
@login_required
def accept_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question = answer.question

    if question.author != current_user:
        flash("Only the question owner can accept an answer.", "danger")
        return redirect(url_for('main.question_detail', question_id=question.id))

    # Un-accept all previous answers
    for ans in question.answers:
        ans.is_accepted = False

    # Accept this one
    answer.is_accepted = True
    db.session.commit()
    flash("Answer marked as accepted.", "success")
    return redirect(url_for('main.question_detail', question_id=question.id))
