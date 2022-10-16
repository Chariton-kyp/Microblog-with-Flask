
from app.forum.main_forum import main_forum
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import current_user
from app.forum.models import User, Question, Answer
from app.forum import forum_db
from app import current_app


@main_forum.route('/', methods=['GET', 'POST'])
@main_forum.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['Category']
        if not title:
            flash("Title is required!")
        elif not content:
            flash('Content is required!')
        elif not category:
            flash('Category is required!')
        else:
            if current_user.is_anonymous:
                post = Question(body=content, author=None, title=title, category=category)
                forum_db.session.add(post)
                forum_db.session.commit()
                flash('Your post is now live!')
                return redirect(url_for('main_forum.index'))
            else: 
                post = Question(body=content, author=current_user, title=title, category=category)
                forum_db.session.add(post)
                forum_db.session.commit()
                flash('Your post is now live!')
                return redirect(url_for('main_forum.index'))      
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        return render_template('main_forum/index_forum.html', title="Home", form="form" , user=user)
    return render_template('main_forum/index_forum.html', title="Home", form="form")
    

@main_forum.route('/general/filter/<category>' ,methods=['GET', 'POST'] )
def general_filter(category):
    page = request.args.get('page', 1, type=int)
    questions = Question.query.filter(Question.category==category).order_by(Question.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main_forum.general_filter',category= category, page=questions.next_num) \
        if questions.has_next else None
    prev_url = url_for('main_forum.general_filter',  category= category, page=questions.prev_num) \
        if questions.has_prev else None
    if request.method == 'POST':
        category = request.form['Category']
        return redirect(url_for('main_forum.general_filter',category=category))
    return render_template('main_forum/index_forum.html', title='filtered', questions=questions.items,
                        next_url=next_url, prev_url=prev_url, category=category) 


@main_forum.route('/explore/<category>' ,methods=['GET', 'POST'])
def explore(category):
    if request.method == 'POST':
        category = request.form['Category']
        return redirect(url_for('main_forum.general_filter',category=category))
    else:
        page = request.args.get('page', 1, type=int)
        questions = Question.query.order_by(Question.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('main_forum.explore',category= category, page=questions.next_num) \
            if questions.has_next else None
        prev_url = url_for('main_forum.explore',  category= category, page=questions.prev_num) \
            if questions.has_prev else None
        return render_template('main_forum/index_forum.html', title='Explore', questions=questions.items,
                            next_url=next_url, prev_url=prev_url, category=category)


@main_forum.route('/explore/question/<question_id>/answer' ,methods=['GET', 'POST'])
def answer(question_id):
    page = request.args.get('page', 1, type=int)
    question = Question.query.filter_by(id=question_id).first()
    answers = Answer.query.filter_by(question_id=question_id).order_by(Answer.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main_forum.answer', question_id=question_id , page=answers.next_num) \
        if answers.has_next else None
    prev_url = url_for('main_forum.answer',  question_id=question_id , page=answers.prev_num) \
        if answers.has_prev else None 
    if request.method == 'POST':
        answer = request.form['answer']
        if not answer:
            flash('Answser is required to submit!')
            return redirect(url_for('main_forum.answer'))
        else:
            if current_user.is_anonymous:
                flash('Sorry you have to register in order to answer a question')
                return redirect(url_for('main_forum.answer'))
            else: 
                post = Answer(body=answer, author=current_user, question_id=question_id)
                forum_db.session.add(post)
                forum_db.session.commit()
                flash('Your answer is now live!')
                return redirect(url_for('main_forum.answer',question_id=question_id))
    return render_template('main_forum/answer.html',question_id=question_id, question=question, answers=answers, next_url=next_url, prev_url=prev_url )


@main_forum.route('/general')
def general():
    category = Question.category
    return redirect(url_for('main_forum.explore',category=category))

