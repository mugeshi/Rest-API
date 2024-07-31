from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from model import User
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)
api = Api(app)


@app.route('/')
def home():
    return '<h1> Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True)
