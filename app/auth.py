from flask_restx import Namespace, Resource, fields
from functools import wraps
from flask import request
import jwt
import datetime

ns = Namespace("auth", description="Authentication operations")

# Simple in-memory user store (replace with database in production)
users = {
    "admin@example.com": {"password": "admin123", "name": "Admin User"}
}

SECRET_KEY = "your-secret-key-change-in-production"

login_model = ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@ns.route('/login')
class Login(Resource):
    @ns.expect(login_model)
    def post(self):
        """User login"""
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        user = users.get(email)
        if user and user['password'] == password:
            token = jwt.encode({
                'email': email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, SECRET_KEY, algorithm='HS256')
            
            return {
                'token': token,
                'user': {'email': email, 'name': user['name']}
            }, 200
        
        return {'message': 'Invalid credentials'}, 401
