from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from model import UserModel, db  

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
        """Get a list of all users."""
        users = UserModel.query.all()
        if not users:
            abort(404, message="No users found")
        return users

    def post(self):
        """Create a new user."""
        args = user_parser.parse_args()
        new_user = UserModel(username=args['username'], email=args['email'])
        db.session.add(new_user)
        db.session.commit()
        return marshal_with(user_fields)(new_user), 201

class User(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        """Get a single user by ID."""
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        return user

    def patch(self, id):
        """Update a user's information partially."""
        args = user_parser.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        # Update only the fields that are provided
        if args['username']:
            user.username = args['username']
        if args['email']:
            user.email = args['email']
        db.session.commit()
        return marshal_with(user_fields)(user), 200

    def delete(self, id):
        """Delete a user by ID."""
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        return '', 204  # No content to return after deletion

# Register resources with the API
api.add_resource(Users, '/api/users')
api.add_resource(User, '/api/users/<int:id>')

@app.route('/')
def home():
    """Home route."""
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables for our data models
    app.run(debug=True)
