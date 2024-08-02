from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from model import UserModel, db  # Import UserModel from model.py

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)
api = Api(app)

# Define output fields for marshalling
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String
}

# Create reqparse for input validation
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help='Username cannot be blank')
user_parser.add_argument('email', type=str, required=True, help='Email cannot be blank')

class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = UserModel.query.all()
        if not users:
            abort(404, message="No users found")
        return users

    def post(self):
        args = user_parser.parse_args()
        new_user = UserModel(username=args['username'], email=args['email'])
        db.session.add(new_user)
        db.session.commit()
        return marshal_with(user_fields)(new_user), 201

api.add_resource(Users, '/api/users/')

@app.route('/')
def home():
    return '<h1> Flask REST API</h1>'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables for our data models
    app.run(debug=True)
