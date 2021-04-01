from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from forms import AddCafeForm, EditCafeForm, RegisterForm, LoginForm
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_gravatar import Gravatar
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps
import psycopg2
# import details

app = Flask(__name__)
# app.config['SECRET_KEY'] = details.secret_key
app.config['SECRET_KEY'] = os.environ.get("MELBOURNE_CAFES_KEY")
Bootstrap(app)

# CONNECT TO DB
# app.config['SQLALCHEMY_DATABASE_URI'] = details.database
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///cafes.db")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///cafes1.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    flash("You must login or register to be able to add new cafes to the list")
    return redirect(url_for('login'))


gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Configure tables in the database
class Cafe(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.String(250), nullable=False)
    has_wifi = db.Column(db.String(10), nullable=False)
    quiet_noisy = db.Column(db.String(10), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)
    # TODO: think about adding working hours
    # open = db.Column(db.String(250), unique=True, nullable=False)
    # close = db.Column(db.String(250), unique=True, nullable=False)
    # coffee_rating = db.Column(db.String(250), unique=True, nullable=False)
    # wifi = db.Column(db.String(250), unique=True, nullable=False)
    # power = db.Column(db.String(250), unique=True, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))


db.create_all()


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if current_user.id == 1:
                return f(*args, **kwargs)
            else:
                flash("You must be admin to be able to delete cafe from the list")
                return redirect(url_for('login'))
        except:
            flash("Please log-in as admin to delete cafe")
            return redirect(url_for('login'))
    return decorated_function


@app.route("/")
def home():
    cafes = Cafe.query.all()
    return render_template("cafes.html", all_cafes=cafes)


@app.route("/add-cafe", methods=["GET", "POST"])
@login_required
def add_cafe():
    form = AddCafeForm()
    if form.btn_cancel.data:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            coffee_price=form.coffee_price.data,
            seats=form.seats.data,
            has_wifi=form.has_wifi.data,
            has_sockets=form.has_sockets.data,
            quiet_noisy=form.quiet_noisy.data,
            location=form.location.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add-cafe.html", form=form)


@app.route('/edit-cafe/<int:cafe_id>', methods=["GET", "POST"])
@login_required
def edit_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    edit_form = EditCafeForm(
        name=cafe.name,
        coffee_price=cafe.coffee_price,
        seats=cafe.seats,
        has_wifi=cafe.has_wifi,
        has_sockets=cafe.has_sockets,
        quiet_noisy=cafe.quiet_noisy,
        location=cafe.location,
        map_url=cafe.map_url,
        img_url=cafe.img_url,
    )
    if edit_form.btn_cancel.data:
        return redirect(url_for('home'))
    if edit_form.validate_on_submit():
        cafe.name = edit_form.name.data
        cafe.coffee_price = edit_form.coffee_price.data
        cafe.seats = edit_form.seats.data
        cafe.has_wifi = edit_form.has_wifi.data
        cafe.has_sockets = edit_form.has_sockets.data
        cafe.quiet_noisy = edit_form.quiet_noisy.data
        cafe.location = edit_form.location.data
        cafe.map_url = edit_form.map_url.data
        cafe.img_url = edit_form.img_url.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit-cafe.html", form=edit_form)


@app.route("/delete/<int:cafe_id>")
@admin_required
def delete_cafe(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.btn_cancel.data:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user_email = form.email.data
        email_exists = User.query.filter_by(email=user_email).first()
        if email_exists:
            flash("You've already signed up with this email, log in instead!")
            return redirect(url_for('login'))
        else:
            hashed_password = generate_password_hash(form.password.data,
                                                     method='pbkdf2:sha256',
                                                     salt_length=8)
            new_user = User(
                email=form.email.data,
                password=hashed_password,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Thank you for registering!')
            return redirect(url_for('home'))
    return render_template("register-user.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.btn_cancel.data:
        return redirect(url_for('home'))
    if form.register.data:
        return redirect(url_for('register'))
    if form.validate_on_submit():
        user_email = form.email.data
        user = User.query.filter_by(email=user_email).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                flash('You were successfully logged in')
                return redirect(url_for('home'))
            else:
                flash('Password incorrect. Please try again.')
                return redirect(url_for('login'))
        else:
            flash("This user doesn't exist in our database")
            return redirect(url_for('login'))
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
