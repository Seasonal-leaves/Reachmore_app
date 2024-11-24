from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from flask_security import hash_password, utils, auth_token_required
from applications.user_datastore import user_datastore
from applications.database import db
from applications.models import User


VALID_ROLES = ["influencer", "sponsor", "admin"]


class UserRegistration(Resource):
    def post(self): 
        user_data = request.get_json()

        email = user_data.get('email', None)
        password = user_data.get('password', None)
        #company_name = user_data.get('company_name', None)
        #industry = user_data.get('industry', None)
        #budget = user_data.get('budget', None)
        username = user_data.get('username', None)
        role = user_data.get('role', None)# "influencer" or "sponsor"
        #Backend data validation
        if not username or not username.isalnum():
            return make_response(jsonify({'message': 'username is must and should only have alphanumeric characters'}), 401)
        
        if not email or '@' not in email:
            return make_response(jsonify({'message': 'email is must or Invalid email Entered '}), 401)
        
        if not password or len(password) < 8:
            return make_response(jsonify({'message': 'password is must and should be atleast 8 characters'}), 401)
        
        if not role or role not in VALID_ROLES:
            return make_response(jsonify({'message': 'role is required for registraion and should be either influencer or sponsor'}), 401)

        useremail = user_datastore.find_user(email=email)
        if useremail: 
            return make_response(jsonify({'message': 'Same email ID associated with other account'}), 401)
        
        # user = user_datastore.find_user(email=email)
        # if user: 
        #     return make_response(jsonify({'message': 'User already exists with this email'}), 401)
        # Hash the password
        # hashed_password = generate_password_hash(password)

        # Role-Specific Validation
        if role == "influencer":
            category = user_data.get('category', None)
            niche = user_data.get('niche', None)
            reach = user_data.get('reach', None)

            if not category or not niche or not isinstance(reach, int) or reach <= 0:
                return make_response(jsonify({
                    'message': 'Influencers must provide valid "category", "niche", and "reach" (positive integer)'
                }), 400)

        elif role == "sponsor":
            company_name = user_data.get('company_name', None)
            industry = user_data.get('industry', None)
            budget = user_data.get('budget', None)

            if not company_name or not industry or not isinstance(budget, (int, float)) or budget <= 0:
                return make_response(jsonify({
                    'message': 'Sponsors must provide valid "company_name", "industry", and "budget" (positive number)'
                }), 400)

        try:
            role = user_datastore.find_role(role)
            user = user_datastore.create_user(username = username,
                                              email = email,
                                              password = hash_password(password),
                                              roles = [role],
                                              # Role-specific fields
                                              niche=niche if role == "influencer" else None,
                                              category=category if role == "influencer" else None,
                                              reach=reach if role == "influencer" else None,
                                              company_name=company_name if role == "sponsor" else None,
                                              industry=industry if role == "sponsor" else None,
                                              budget=budget if role == "sponsor" else None
                                              )
            
            
            user_datastore.commit()

            response = {
                'message': 'User successfully registered',
                'user' :{
                    'username': user.username,
                    'email': user.email,
                    'roles': [role.name for role in user.roles]
                }
            }

            return make_response(jsonify(response), 201)
        except Exception as e:
            response = {
                'message': 'Internal Error',
                'error': str(e)
            }
            return make_response(jsonify(response), 500)
