from flask import Flask, render_template, request
from models.nltk_model import NltkSentimentModel
from models.forms import FeedbackForm, LoginForm, RegisterForm
from models.models import Feedback, User #map_to_stars
from models import db, app
from flask import redirect, url_for, flash

sentiment_model = NltkSentimentModel()

#@app.route('/')
#def index(): 
#    return render_template('feedback.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            email=form.email.data,
            password=form.password1.data  # Assuming your User model has a 'password' attribute
        )
        db.session.add(user_to_create)
        db.session.commit()
        flash('Account created successfully! You can now log in.', category='success')
        return redirect(url_for('login'))

    # Fix: Change 'values' to 'values()' to correctly iterate over dictionary values
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(firstname=form.firstname.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            flash(f'Success! You are logged in as: {attempted_user.firstname} {attempted_user.lastname}', category='success')
            return redirect(url_for('result'))  # Redirect to the 'analyze' (or 'feedback') route
        else:
            flash('Username and Password do not match, try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/result', methods=['GET', 'POST'])
def result():
    form = FeedbackForm()
    stars = None  # Default value if form is not submitted
    names_with_stars = None  # Default value if form is not submitted

    if form.validate_on_submit():
        if request.method == 'POST':
            user_text = request.form['user_text']
            if user_text:
                nltk_result = sentiment_model.predict_sentiment(user_text)
                compound_score = nltk_result['compound_score']
                stars = map_to_stars(score=compound_score)
                feedback_to_create = Feedback(feedback=form.feedback.data,
                                              stars=stars,
                                              department=form.department.data,
                                              position=form.position.data)
                db.session.add(feedback_to_create)
                db.session.commit()

                min_stars = request.args.get('min_stars', 0) 

                names_with_stars = (
                    db.session.query(Feedback.stars, User.firstname, User.lastname)
                    .select_from(Feedback)
                    .join(User, Feedback.id == User.id)  
                    .filter(Feedback.stars >= min_stars)  
                    .all()
                )

    return render_template('result.html', stars=stars, names_with_stars=names_with_stars, zip=zip)
