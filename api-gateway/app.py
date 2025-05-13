from flask import Flask, request, jsonify
import jwt
import requests
from functools import wraps

app = Flask(__name__)

# Configuration
SECRET_KEY = 'your_jwt_secret_key'
PORT = 3000
AUTH_SERVICE_URL = 'http://localhost:3001'
VEHICLE_SERVICE_URL = 'http://localhost:3002'

# JWT verification middleware
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Skip token verification for login route
        if request.path == '/api/auth/login':
            return f(*args, **kwargs)
        
        token = request.headers.get('x-auth-token')
        
        if not token:
            return jsonify({'message': 'No token, authorization denied'}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user = data
        except:
            return jsonify({'message': 'Token is not valid'}), 401
            
        return f(*args, **kwargs)
    
    return decorated

# Auth routes
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        response = requests.post(
            f"{AUTH_SERVICE_URL}/api/auth/login",
            json=request.get_json()
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'message': f'Server error: {str(e)}'}), 500

@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user():
    try:
        response = requests.get(
            f"{AUTH_SERVICE_URL}/api/auth/me",
            headers={'x-auth-token': request.headers.get('x-auth-token')}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'message': f'Server error: {str(e)}'}), 500

@app.route('/api/auth/verify', methods=['GET'])
@token_required
def verify_token():
    try:
        response = requests.get(
            f"{AUTH_SERVICE_URL}/api/auth/verify",
            headers={'x-auth-token': request.headers.get('x-auth-token')}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'message': f'Server error: {str(e)}'}), 500

# Vehicle routes
@app.route('/api/vehicles', methods=['GET'])
@token_required
def get_all_vehicles():
    try:
        response = requests.get(
            f"{VEHICLE_SERVICE_URL}/api/vehicles",
            headers={'x-auth-token': request.headers.get('x-auth-token')}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'message': f'Server error: {str(e)}'}), 500

@app.route('/api/vehicles/<id>', methods=['GET'])
@token_required
def get_vehicle_by_id(id):
    try:
        response = requests.get(
            f"{VEHICLE_SERVICE_URL}/api/vehicles/{id}",
            headers={'x-auth-token': request.headers.get('x-auth-token')}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'message': f'Server error: {str(e)}'}), 500

@app.route('/api/vehicles/plate/<license_plate>', methods=['GET'])
@token_required
def get_vehicle_by_license_plate(license_plate):
    try:
        response = requests.get(
            f"{VEHICLE_SERVICE_URL}/api/vehicles/plate/{license_plate}",
            headers={'x-auth-token': request.headers.get('x-auth-token')}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'message': f'Server error: {str(e)}'}), 500

@app.route('/api/vehicles', methods=['POST'])
@token_required
def create_vehicle():
    try:
        response = requests.post(
            f"{VEHICLE_SERVICE_URL}/api/vehicles",
            json=request.get_json(),
            headers={'x-auth-token': request.headers.get('x-auth-token')}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'message': f'Server error: {str(e)}'}), 500

@app.route('/api/vehicles/<id>', methods=['PUT'])
@token_required
def update_vehicle(id):
    try:
        response = requests.put(
            f"{VEHICLE_SERVICE_URL}/api/vehicles/{id}",
            json=request.get_json(),
            headers={'x-auth-token': request.headers.get('x-auth-token')}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'message': f'Server error: {str(e)}'}), 500

@app.route('/api/vehicles/<id>', methods=['DELETE'])
@token_required
def delete_vehicle(id):
    try:
        response = requests.delete(
            f"{VEHICLE_SERVICE_URL}/api/vehicles/{id}",
            headers={'x-auth-token': request.headers.get('x-auth-token')}
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'message': f'Server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'API Gateway is running'}), 200

# Enable CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,x-auth-token')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    print(f"API Gateway running on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=True)
