"""OpenAQ Air Quality Dashboard with Flask."""
import openaq
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from decouple import config

api = openaq.OpenAQ()


'''Create and configure an instance of the Flask application'''
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Record {}>'.format(self.datetime, self.value)


@APP.route('/')
def root():
    """Base view."""
    status, body = api.measurements(city='Los Angeles', parameter='pm25')

    aq_results = body['results']

    for observation in aq_results:
        observation_view = ()

        observation_view += observation['date']['utc'], observation['value']

    return observation_view


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    # This is where I use observation_view to add Records into the database
    # my thought is it would be a for loop like this:
    
    # for observation in observation_view:
    #   Record(observation) - I don't think this is how you do it
        
    # maybe I need to turn it into a dataframe first with an index
    # I am also aware that these should be separated into different .py files
    
    # I was getting errors every time I tried to import for the file
    # via .(filename) so I figured it would be better to put all the code
    # I could do on this one file for ease of view
    # this is as far as I got. Sorry Michael

    DB.session.commit()
    return 'Data refreshed!'
