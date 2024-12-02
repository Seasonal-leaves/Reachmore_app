from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from flask_security import hash_password, utils, auth_token_required, current_user
from applications.user_datastore import user_datastore
from applications.database import db
from applications.models import User
import traceback

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
                    # Log the error for debugging
                    print(f"Error: {str(e)}")
                    print(f"Stacktrace: {traceback.format_exc()}")
                    db.session.rollback()
                    return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)





class CheckEmailAPI(Resource):
    def get(self):
        try:
            email = request.args.get('email')
            if not email:
                return {'message': 'Email parameter is required'}, 400

            user = user_datastore.find_user(email=email)
            if user:
                return {'message': 'Email already exists'}, 400
            return {'message': 'Email is available'}, 200
        except Exception as e:
            # Log the exception for debugging
            print(f"Error in /check-email: {e}")
            return {'message': 'Internal server error', 'error': str(e)}, 500



class UserLogin(Resource):
    def post(self):
        login_data = request.get_json()
        email = login_data.get('email', None)
        password = login_data.get('password', None)
        role = login_data.get('role')

        if not email or not password or not role:
            return make_response(jsonify({'message': 'Email, password, and role are required'}), 400)

        if role not in VALID_ROLES:
            return make_response(jsonify({'message': 'Invalid role specified'}), 400)

        user = user_datastore.find_user(email=email)
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 401)

        if not utils.verify_password(password, user.password):
            return make_response(jsonify({'message': 'Email and password do not match'}), 401)

        if role not in [r.name for r in user.roles]:
            return make_response(jsonify({'message': f'User is not authorized as {role}'}), 403)
        
        if user.is_approved == False and user.roles[0].name == 'sponsor':
            return make_response(jsonify({'message': 'Admin has not approved sposnor'}), 401)

        # Generating a role-specific token/session
        try:
            utils.login_user(user)
            token = user.get_auth_token()
            response={
                'message': 'User successfully logged in',
                "login_credentials": {
                    'username': user.username,
                    'roles': [role.name for role in user.roles],
                    'auth_token': token
                },
            }
            return make_response(jsonify(response), 200)
        except Exception as e:
            response = {
                'message': 'Bad request Error',
                'error': str(e)
            }
            return make_response(jsonify(response), 500)



class UpdateUserDetails(Resource):
    @auth_token_required
    def put(self):
        
        user = current_user

        # Parse input data
        user_data = request.get_json()

        # Common fields for all users
        username = user_data.get('username', None)
        email = user_data.get('email', None)

        if username and not username.isalnum():
            return make_response(jsonify({'message': 'Username should be alphanumeric'}), 400)
        
        if email and '@' not in email:
            return make_response(jsonify({'message': 'Invalid email format'}), 400)

        # Update common fields
        if username:
            user.username = username
        '''Email is supposed to be unique so can not update email'''

        # Role-specific updates
        if "sponsor" in [role.name for role in user.roles]:
            company_name = user_data.get('company_name', None)
            industry = user_data.get('industry', None)
            budget = user_data.get('budget', None)

            if company_name:
                user.company_name = company_name
            if industry:
                user.industry = industry
            if budget is not None:
                if not isinstance(budget, (int, float)) or budget <= 0:
                    return make_response(jsonify({'message': 'Budget must be a positive number'}), 400)
                user.budget = budget

        elif "influencer" in [role.name for role in user.roles]:
            category = user_data.get('category', None)
            niche = user_data.get('niche', None)
            reach = user_data.get('reach', None)

            if category:
                user.category = category
            if niche:
                user.niche = niche
            if reach is not None:
                if not isinstance(reach, int) or reach <= 0:
                    return make_response(jsonify({'message': 'Reach must be a positive integer'}), 400)
                user.reach = reach

        # Commit changes to the database
        try:
            db.session.commit()
            response = {
                'message': 'User details updated successfully',
                'updated_user': {
                    'username': user.username,
                    'roles': [role.name for role in user.roles]
                }
            }
            return make_response(jsonify(response), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)



class UserLogout(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()
        response = {
            'message': 'User successfully logged out'
        }
        return make_response(jsonify(response), 200)