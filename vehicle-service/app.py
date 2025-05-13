from flask import Flask, request, jsonify
import jwt
import datetime
import requests
from functools import wraps

app = Flask(__name__)

# Configuration
SECRET_KEY = 'your_jwt_secret_key'
PORT = 3002
AUTH_SERVICE_URL = 'http://localhost:3001'

# In-memory vehicles database
vehicles = [
    {
        'id': '1',
        'licensePlate': '29A-12345',
        'ownerName': 'Nguyễn Văn A',
        'ownerID': '001234567890',
        'vehicleType': 'Sedan',
        'brand': 'Toyota',
        'model': 'Camry',
        'color': 'Black',
        'registrationDate': datetime.datetime(2022, 1, 15),
        'expiryDate': datetime.datetime(2027, 1, 15),
        'status': 'active',
        'createdAt': datetime.datetime.now(),
        'updatedAt': datetime.datetime.now()
    },
    {
        'id': '2',
        'licensePlate': '30A-54321',
        'ownerName': 'Trần Thị B',
        'ownerID': '001234567891',
        'vehicleType': 'SUV',
        'brand': 'Honda',
        'model': 'CR-V',
        'color': 'White',
        'registrationDate': datetime.datetime(2021, 5, 20),
        'expiryDate': datetime.datetime(2026, 5, 20),
        'status': 'active',
        'createdAt': datetime.datetime.now(),
        'updatedAt': datetime.datetime.now()
    },
    {
        'id': '3',
        'licensePlate': '31A-98765',
        'ownerName': 'Lê Văn C',
        'ownerID': '001234567892',
        'vehicleType': 'Hatchback',
        'brand': 'Mazda',
        'model': 'Mazda3',
        'color': 'Red',
        'registrationDate': datetime.datetime(2020, 11, 10),
        'expiryDate': datetime.datetime(2025, 11, 10),
        'status': 'active',
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
            request.user = data
        except:
            # If local verification fails, try to verify with auth service
            try:
                response = requests.get(
                    f"{AUTH_SERVICE_URL}/api/auth/verify",
                    headers={'x-auth-token': token}
                )
                
                if response.status_code == 200:
                    request.user = response.json()['user']
                else:
                    return jsonify({'message': 'Token is not valid'}), 401
            except:
                return jsonify({'message': 'Token is not valid'}), 401
            
        return f(*args, **kwargs)
    
    return decorated

# Role middleware
def admin_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.user['role'] != 'admin':
            return jsonify({'message': 'Access denied. Admin only.'}), 403
        return f(*args, **kwargs)
    return decorated

def admin_or_police(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.user['role'] != 'admin' and request.user['role'] != 'police':
            return jsonify({'message': 'Access denied. Admin or Police only.'}), 403
        return f(*args, **kwargs)
    return decorated

# Helper function to convert datetime to string
def format_vehicle(vehicle):
    formatted = vehicle.copy()
    formatted['registrationDate'] = formatted['registrationDate'].isoformat()
    formatted['expiryDate'] = formatted['expiryDate'].isoformat()
    formatted['createdAt'] = formatted['createdAt'].isoformat()
    formatted['updatedAt'] = formatted['updatedAt'].isoformat()
    return formatted

# Routes
@app.route('/api/vehicles', methods=['GET'])
@token_required
@admin_or_police
def get_all_vehicles():
    return jsonify([format_vehicle(v) for v in vehicles]), 200

@app.route('/api/vehicles/<id>', methods=['GET'])
@token_required
@admin_or_police
def get_vehicle_by_id(id):
    vehicle = next((v for v in vehicles if v['id'] == id), None)
    
    if not vehicle:
        return jsonify({'message': 'Vehicle not found'}), 404
    
    return jsonify(format_vehicle(vehicle)), 200

@app.route('/api/vehicles/plate/<license_plate>', methods=['GET'])
@token_required
@admin_or_police
def get_vehicle_by_license_plate(license_plate):
    vehicle = next((v for v in vehicles if v['licensePlate'] == license_plate), None)
    
    if not vehicle:
        return jsonify({'message': 'Vehicle not found'}), 404
    
    return jsonify(format_vehicle(vehicle)), 200

@app.route('/api/vehicles', methods=['POST'])
@token_required
@admin_only
def create_vehicle():
    data = request.get_json()
    
    # Check if license plate already exists
    if any(v['licensePlate'] == data['licensePlate'] for v in vehicles):
        return jsonify({'message': 'License plate already registered'}), 400
    
    new_vehicle = {
        'id': str(len(vehicles) + 1),
        **data,
        'registrationDate': datetime.datetime.fromisoformat(data['registrationDate']),
        'expiryDate': datetime.datetime.fromisoformat(data['expiryDate']),
        'createdAt': datetime.datetime.now(),
        'updatedAt': datetime.datetime.now()
    }
    
    vehicles.append(new_vehicle)
    
    return jsonify(format_vehicle(new_vehicle)), 201

@app.route('/api/vehicles/<id>', methods=['PUT'])
@token_required
@admin_only
def update_vehicle(id):
    data = request.get_json()
    
    vehicle_index = next((i for i, v in enumerate(vehicles) if v['id'] == id), None)
    
    if vehicle_index is None:
        return jsonify({'message': 'Vehicle not found'}), 404
    
    # Check if license plate is being changed and already exists
    if 'licensePlate' in data and data['licensePlate'] != vehicles[vehicle_index]['licensePlate']:
        if any(v['licensePlate'] == data['licensePlate'] and v['id'] != id for v in vehicles):
            return jsonify({'message': 'License plate already registered to another vehicle'}), 400
    
    # Update vehicle
    updated_vehicle = vehicles[vehicle_index].copy()
    for key, value in data.items():
        if key in ['registrationDate', 'expiryDate'] and value:
            updated_vehicle[key] = datetime.datetime.fromisoformat(value)
        else:
            updated_vehicle[key] = value
    
    updated_vehicle['updatedAt'] = datetime.datetime.now()
    vehicles[vehicle_index] = updated_vehicle
    
    return jsonify(format_vehicle(updated_vehicle)), 200

@app.route('/api/vehicles/<id>', methods=['DELETE'])
@token_required
@admin_only
def delete_vehicle(id):
    vehicle_index = next((i for i, v in enumerate(vehicles) if v['id'] == id), None)
    
    if vehicle_index is None:
        return jsonify({'message': 'Vehicle not found'}), 404
    
    vehicles.pop(vehicle_index)
    
    return jsonify({'message': 'Vehicle deleted successfully'}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'Vehicle service is running'}), 200

# Enable CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,x-auth-token')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    print(f"Vehicle service running on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=True)
