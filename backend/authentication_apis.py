from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import utils, auth_token_required, roles_required
from backend.user_datastore import user_datastore
from datetime import datetime
from backend.database import db

class LoginAPI(Resource):
    def post(self):
        login_credentials = request.get_json()
        if not login_credentials:
            result = {
                'message': 'Login credentials are required.'
            }
            return make_response(jsonify(result), 400)
        email = login_credentials.get('email',None)
        password = login_credentials.get('password',None)

        if not email or not password:
            result = {
                'message':'Both Email and Password are required.'
            }
            return make_response(jsonify(result), 400)
        
        user = user_datastore.find_user(email=email)
        if not user:
            result = {
                'message':'User Not Found.'
            }
            return make_response(jsonify(result), 404)
        
        if not utils.verify_password(password, user.password):
            result = {
                'message': 'Invalid Password.'
            }
            return make_response(jsonify(result), 401)
        
        auth_token = user.get_auth_token()
        

        response = {
            'message': 'Login Successful.',
            'user_details' : {
                'email': user.email,
                'roles': [role.name for role in user.roles],
                'name': user.name,
                'auth_token': auth_token
            }
        }

        return make_response(jsonify(response), 200)

class LogoutAPI(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()

        response = {
            'message': 'Logout Successful.'
        }
        return make_response(jsonify(response), 200)

class CheckEmailAPI(Resource):
    def post(self):
        credential = request.get_json()

        if not credential :
            result = {
                'message': 'Request body is required'
            }
            return make_response(jsonify(result),400)
        
        email = credential.get('email',None)

        if not email:
            result = {
                'message': 'Email is required'
            }
            return make_response(jsonify(result),400)
        
        user = user_datastore.find_user(email=email)
        if user:
            return make_response(jsonify({'available': False}), 200)
        else:
            return make_response(jsonify({'available': True}), 200)
        
class RegisterAPI(Resource):
    def post(self):
        credential = request.get_json()

        if not credential:
            result = {
                'message': 'Registration credentials are required.'
            }
            return make_response(jsonify(result), 400)
        
        email = credential.get('email', None)
        name = credential.get('name', None)
        password = credential.get('password', None)
        qualification = credential.get('qualification', None)
        DOB = credential.get('DOB', None)
        
        if not email or not name or not password or not qualification or not DOB:
            result = {
                'message': 'All the credentials are required.'
            }
            return make_response(jsonify(result), 409)
        
        if not email.endswith('@gmail.com'):
            result = {
                'message': 'Enter valid Gmail ID only.'
            }
            return make_response(jsonify(result), 400)
        
        if len(password) < 8:
            result = {
                'message': 'Password should contain atleast 8 characters.'
            }
            return make_response(jsonify(result), 409)
        
        try:
            dob = datetime.strptime(DOB, "%Y-%m-%d").date()
        except ValueError:
            result = {
                'message': "DOB must be in yyyy-mm-dd format"
            }
            return make_response(jsonify(result), 400)

        if user_datastore.find_user(email=email):
            result = {
                'message': 'User already exists.'
            }
            return make_response(jsonify(result), 409)
        
        user_role = user_datastore.find_or_create_role('user')
        
        user_datastore.create_user(

            email = email,
            name = name,
            password = password,
            qualification = qualification,
            DOB = dob,
            roles = [user_role]
        )

        db.session.commit()

        response = {
            'message': 'Registration Successful!',
            'user_details': {
                'email': email,
                'roles': [user_role.name]
            }
        }
        return make_response(jsonify(response), 201)
    
