from flask import Flask, jsonify
from datetime import datetime
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource , reqparse
import re
from sqlalchemy.orm import validates

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True

db = SQLAlchemy(app)
@app.before_first_request
def create_tables():
    db.create_all()

class UserRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', help = 'This field cannot be blank', required = True)
        parser.add_argument('password', help = 'This field cannot be blank', required = True)
        parser.add_argument('mob_no', help = 'This field cannot be blank', required = True)
        parser.add_argument('created_on', default=datetime.now())
        parser.add_argument('last_seen', onupdate=datetime.now)
        data = parser.parse_args()

        if User.find_by_email(data['email']):
            return {'message': 'User {} already exists'.format(data['email'])}

        new_user = User(            
            email=data['email'],
            password=data['password'],
            mob_no=data['mob_no'],
            created_on=data['created_on'],
            last_seen=data['last_seen']
        )


        if not data['email']:
            raise AssertionError('No email provided')

        if not data['password']:
            raise AssertionError('Please Provide Password')

        if not re.match(r'[^@]+@[^@]+\.[^@]+', data['email']):
            raise AssertionError('Provided email is not an email address')

        if not data['mob_no']:
            print("enter the number")

        if not re.match(r'^!(0)\d[1-9]\d{10,10}\d', data['mob_no']):
            print("valid number")
            
        try:
            new_user.save_to_db()
            return {
                'message': 'User {} was created'.format(data['email']),
                'Status_Code':'200 Good Request'
            }
            
        except:
            return {'message': 'Something went wrong'} , 500

class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', help = 'This field cannot be blank', required = True)
        parser.add_argument('password', help = 'This field cannot be blank', required = True)
        parser.add_argument('last_seen', default=datetime.now())
        data = parser.parse_args()
        
        current_user = User.find_by_email(data['email'])
        user_pswd = User.match_password(data['password'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['email']), 'Status_Code':'400 Bad Request'} 
        elif not user_pswd:
            return {'message': 'Please Enter Correct Password'.format(data['password'])}


        if data['email'] == current_user.email:
            return {'message': 'Logged in as {}'.format(current_user.email), 'Status_Code':'200 Good Request'}
        else:
            return {'message': 'Incorrect Email {}'.format(current_user.email), 'Status_Code':'400 Bad Request'}

        if User.update(data['last_seen']):
            return last_seen.datetime.now()  
            db.session.update(update)
            db.session.commit()

       
class User(db.Model):
    __tablename__ = 'hello'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    mob_no = db.Column(db.BIGINT, nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.now())
    last_seen = db.Column(db.TIMESTAMP, onupdate=datetime.now)    
 
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def match_password(cls,password):
        return cls.query.filter_by(password=password).first()


    @classmethod
    def update(cls,last_seen):
        return cls.query.last_seen(last_seen=last_seen.datetime.now).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'email': x.email,
            }
        return {'users': list(map(lambda x: to_json(x), User.query.all()))}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

@app.route('/',methods=['GET','POST'])
def index():
    return jsonify({'message': 'Hello, World!'})

class AllUsers(Resource):
    @staticmethod
    def get():
        return User.return_all()

api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(AllUsers, '/users')

if __name__ == '__main__':
    print("Restarting Server")
    app.run(debug=True, threaded=True)
    print("Stoping Server")