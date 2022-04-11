from flask import Flask, render_template, url_for, request, redirect
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import InputRequired, URL
import datetime
from flask_sqlalchemy import SQLAlchemy
from typing import Callable
# from sqlalchemy import or_

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
Bootstrap(app)
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class MySQLAlchemy(SQLAlchemy):
    Column: Callable
    String: Callable
    Float: Callable
    Integer: Callable
    Boolean: Callable


# Initialize the Database
db = MySQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    seats = db.Column(db.String(100), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(100), nullable=True)


class PlacesForm(FlaskForm):
    placename = StringField('Place Name', validators=[InputRequired()])
    mapurl = StringField('Map URL', validators=[URL()])
    imgurl = StringField('Image URL', validators=[URL()])
    location = StringField('Location', validators=[InputRequired()])
    seats = StringField('Seats', validators=[InputRequired()])
    price = StringField('Coffee Price')
    toilet = BooleanField('Has Toilet')
    wifi = BooleanField('Has Wi-Fi')
    socket = BooleanField('Has Socket')
    calls = BooleanField('Can take Calls')
    submit = SubmitField('Submit')


dat = datetime.datetime.now()
year = dat.year


@app.route('/', methods=['GET', 'POST'])
def home():
    cafes = db.session.query(Cafe).all()

    # Get filters work
    if request.method == 'POST':
        if request.form.get('socket') == 'socket':
            cafes = Cafe.query.filter_by(has_sockets=1).all()
        if request.form.get('toilet') == 'toilet':
            cafes = Cafe.query.filter_by(has_toilet=1).all()
        if request.form.get('wifi') == 'wifival':
            cafes = Cafe.query.filter_by(has_wifi=1).all()
        if request.form.get('calls') == 'callsval':
            cafes = Cafe.query.filter_by(can_take_calls=1).all()
        # search_key = 0
        # search_args =['has_sockets', 'has_toilet', 'has_wifi', 'can_take_calls']
        # cafes = Cafe.query.filter(or_(*search_args))
        #session.execute(query).fetchall()

    #     cafes = Cafe.query.order_by(Cafe.has_toilet).all()
    return render_template('index.html', year=year, cafes=cafes)


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = PlacesForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.placename.data,
            map_url=form.mapurl.data,
            img_url=form.imgurl.data,
            location=form.location.data,
            seats=form.seats.data,
            has_toilet=form.toilet.data,
            has_wifi=form.wifi.data,
            has_sockets=form.socket.data,
            can_take_calls=form.calls.data,
            coffee_price=form.price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('cafe_form.html', year=year, form=form)


if __name__ == ("__main__"):
    app.run(debug=True)