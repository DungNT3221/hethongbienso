from flask import Flask, request, jsonify
import jwt
import datetime
import bcrypt
from functools import wraps

app = Flask(__name__)

# Configuration
SECRET_KEY = 'your_jwt_secret_key'
PORT = 3001

# In-memory users database
users = [
    {
        'id': '1',
        'username': 'admin',
        'password': '$2b$12$rQQTjJeUdK8bLBg9.YDjWO0n0AC5Kh3CHnf2q9RfFE3PJdQFcNdZu',  # admin123
        'role': 'admin',
        'fullName': 'System Administrator',
        'createdAt': datetime.datetime.now(),
        'updatedAt': datetime.datetime.now()
    },
    {
        'id': '2',
        'username': 'police',
        'password': '$2b$12$Ht0vLKyzQkWk8MIkRZZ1/.8WjMQiKcADUZLO3ZmVXsYvRNQJA5UAO',  # police123
        'role': 'police',
        'fullName': 'Police Officer',
        'createdAt': datetime.datetime.now(),
        'updatedAt': datetime.datetime.now()
    }
]

# Auth middleware
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-auth-token')

        if not token:
            return jsonify({'message': 'No token, authorization denied'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = next((user for user in users if user['id'] == data['id']), None)

            if not current_user:
                return jsonify({'message': 'User not found'}), 404

            request.user = data
        except:
            return jsonify({'message': 'Token is not valid'}), 401

        return f(*args, **kwargs)

    return decorated

# Routes
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400

    user = next((user for user in users if user['username'] == data['username']), None)

    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    if bcrypt.checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):
        token = jwt.encode({
            'id': user['id'],
            'username': user['username'],
            'role': user['role'],
            'exp': datetime.datetime.now() + datetime.timedelta(days=1)
        }, SECRET_KEY)

        return jsonify({
            'token': token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'role': user['role'],
                'fullName': user['fullName']
            }
        }), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user():
    user = next((user for user in users if user['id'] == request.user['id']), None)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_without_password = {k: v for k, v in user.items() if k != 'password'}

    return jsonify(user_without_password), 200

@app.route('/api/auth/verify', methods=['GET'])
@token_required
def verify_token():
    return jsonify({'valid': True, 'user': request.user}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'Auth service is running'}), 200

# Enable CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,x-auth-token')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    print(f"Auth service running on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=True)
