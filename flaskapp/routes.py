
from flask import request, redirect, render_template, url_for, flash, jsonify
from flaskapp.models import User, Flight
from flaskapp import db, bcrypt, app, mail
from flaskapp.forms import LoginForm, RegistrationForm, AccountForm, RequestResetForm, ResetPasswordForm
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp.imagegen import generate_url
from ast import literal_eval
from flask_mail import Message

@app.route("/")
@app.route("/home")
def home ():
    return render_template("home.html", title="Welcome to Gooday Airlines!", subtitle="Flights that make you dream", animation=True)

@app.route("/frequent")
def frequent ():
    return render_template("frequent.html", title="Frequent Flyer Program")


@app.route("/book")
@login_required
def book ():
    flights = Flight.query.all()
    return render_template("book.html", title="Book A Flight", flights=flights)

@app.route("/credits")
def credits ():
    return render_template("credits.html", title="Credits")

@app.route("/job")
def job ():
    return render_template("job.html", title="Jobs Available")

#the one below is only for testing purposes
@app.route("/layout")
def layout ():
    return render_template("layout.html")


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account ():
    form = AccountForm()
    user = current_user
    if form.validate_on_submit():
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if (form.username.data != ""):
                user.username = form.username.data
            if (form.email.data != ""):
                user.email = form.email.data

            db.session.commit()
            flash("Change Successful", 'success')
            return redirect(url_for('home'))
        else:
            flash("Change Unccessful. Please check password", 'danger')
    return render_template("account.html", title="Your Account", form=form, user=user, forms=True)


@app.route("/logout")
@login_required
def logout ():
    logout_user()
    return redirect(url_for('home'))

@app.route("/register", methods=["GET", 'POST'])
def register ():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        print("this is atleast working")
        hashed_password = bcrypt.generate_password_hash(
            form.password.data.encode('utf-8'))
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Your account has been created, and now you can login 👍", 'success')
        return redirect(url_for('login'))
        
    return render_template("register.html", form=form, head=False, forms=True, title="Register", image="../static/img/plane.jpg")

    

@app.route("/login", methods=["GET", "POST"])
def login ():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash("Login Successful. Welcome 😄", 'success')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Unccessful. Please check username and password", 'danger')
    return render_template("login.html", name="login", head=False, form=form, forms=True, title="Login", image="../static/img/plane.jpg")

@login_required
@app.route("/final", methods=['GET', 'POST'])
def final ():
    if (request.method == 'GET'):
        return render_template("final.html")


#need to work on this one
@app.route("/forgot", methods=['GET', 'POST'])
def forgot ():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('home.html')


'''
@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        output_word = request.form['search_word']
        return redirect(url_for('search', word=output_word))
    else:
        try:
            input_word = request.args.get('word')
            word_meaning = extract(input_word).compile_json()
            if current_user.is_authenticated:
                looking_word = Word.query.filter_by(
                    user_id=current_user.id, word=input_word).first()
                if (looking_word != None):

                    looking_word.time = datetime.utcnow()
                    looking_word.level = 1 if looking_word.level == 1 or looking_word.level == 0 else looking_word.level//2

                    looking_word.due_date = new_time(
                        datetime.utcnow(), looking_word.level)
                    db.session.add(looking_word)
                    db.session.commit()
                else:
                    word = Word(word=input_word, user_id=current_user.id,
                                due_date=new_time(datetime.utcnow(), 0), level=0) #change this boy!!!!!
                    db.session.add(word)
                    db.session.commit()
            else:
                flash(
                    "Your words will not be saved. Login or Sign Up to save words", 'info')
            return render_template('search.html', word=word_meaning, name="search", background_url=generate_url())

        except:
            return redirect(url_for("error"))


@app.route("/error", methods=["GET", "POST"])
def error():
    if request.method == 'POST':
        output_word = request.form['search_word']
        return redirect(url_for('search', word=output_word))
    else:
        return render_template("error.html", name="error", background_url=generate_url())


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash("Login Successful. Welcome 😄", 'success')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Unccessful. Please check username and password", 'danger')
    return render_template("login.html", name="login", form=form, background_url=blue_gradient())


@app.route("/")
@app.route("/home", methods=['GET', "POST"])
def home():
    if request.method == 'POST':
        output_word = request.form['search_word']
        return redirect(url_for('search', word=output_word))
    else:
        return render_template('home.html', name="home", background_url=white_screen())


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data.encode('utf-8'))
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Your account has been created, and now you can login 👍", 'success')
        return redirect(url_for('login'))
    return render_template("register.html", name="register", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', "POST"])
@login_required
def account():
    form = AccountForm()
    user = current_user
    if form.validate_on_submit():
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if (form.username.data != ""):
                user.username = form.username.data
            if (form.email.data != ""):
                user.email = form.email.data

            db.session.commit()
            flash("Change Successful", 'success')
            return redirect(url_for('home'))
        else:
            flash("Change Unccessful. Please check password", 'danger')
    return render_template("account.html", name="login", form=form, background_url="rgb(255, 255, 255)", user=user)


@app.route("/view", methods=['GET', 'POST'])
@login_required
def view():
    if request.method == 'POST':
        output_word = request.form['search_word']
        return redirect(url_for('search', word=output_word))
    else:
        return render_template('view.html', name='view', words=current_user.words, background_url=generate_url())


@app.route("/practice")
@login_required
def practice():
    if request.method == 'POST':
        output_word = request.form['search_word']
        return redirect(url_for('search', word=output_word))
    else:
        user_words = User.query.get(current_user.id).words
        due_today = []
        for word in user_words:
            if (word.due_date.date() <= datetime.today().date()):
                due_today.append(word)
        return render_template('practice.html', name='practice', background_color="rgb(52,58,64)", words_due_today=due_today, js_file="practice.js")


@app.route("/review", methods=['GET', 'POST'])
@login_required
def review():
    if (request.method == 'POST'):
        jsdata = request.get_json()
        return redirect(url_for('review', data=jsdata))
    else:
        inpjsdata = literal_eval(request.args.get('data'))
        words_to_review = {}
        for key, value in inpjsdata.items():
            current_word = Word.query.filter_by(
                user_id=current_user.id, word=key).first()
            current_word.time = datetime.utcnow()
            if (value == 1):
                current_word.level = current_word.level + 1
            else:
                words_to_review[key] = extract(key).compile_json()

            current_word.due_date = new_time(
                current_word.time, current_word.level)
            db.session.add(current_word)
            db.session.commit()

        return render_template("review.html", data=words_to_review, name="review", background_url=generate_url())

def send_reset_email(user):
    token = user.get_reset_token()
    print(token) #omg change this later
    print(user.email)
    msg = Message('Password Reset Request', recipients=[user.email])
    msg.body = f''' '''To reset your password, click on this link: 
    {url_for('reset_token', token=token, _external=True)}

    If you did not make this request, don't worry you are safe 😁'''
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to you ✔")
        return redirect(url_for('login'))
    return render_template("reset_request.html", name="Reset Password", form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token. Are you a hacker? Or just clicked on wrong link 🤔", "warning")
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data.encode('utf-8'))
        user.password = hashed_password
        db.session.commit()

        flash("Your password has been updated 👍", 'success')
        return redirect(url_for('login'))
    return render_template("reset_token.html", name="Reset Password", form=form)
'''