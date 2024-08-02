from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from model import UserModel, db
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)  # Initialize db with the Flask app
api = Api(app)

class Users(Resource):
    def get(self):
        users = UserModel.query.all()
        return users


api.add_resource(Users, '/api/users/')

@app.route('/')
def home():
    return '<h1> Flask REST API</h1>'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)