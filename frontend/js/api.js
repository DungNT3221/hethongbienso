// API URL
const API_URL = 'http://localhost:3000/api';

// Get token from localStorage
const getToken = () => {
    return localStorage.getItem('token');
};

// Auth API
const authAPI = {
    // Login
    login: async (username, password) => {
        try {
            const response = await fetch(`${API_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Login failed');
            }
            
            return data;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    },
    
    // Get current user
    getCurrentUser: async () => {
        try {
            const token = getToken();
            if (!token) {
                throw new Error('No token found');
            }
            
            const response = await fetch(`${API_URL}/auth/me`, {
                method: 'GET',
                headers: {
                    'x-auth-token': token
                }
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Failed to get user');
            }
            
            return data;
        } catch (error) {
            console.error('Get current user error:', error);
            throw error;
        }
    }
};

// Vehicle API
const vehicleAPI = {
    // Get all vehicles
    getAllVehicles: async () => {
        try {
            const token = getToken();
            if (!token) {
                throw new Error('No token found');
            }
            
            const response = await fetch(`${API_URL}/vehicles`, {
                method: 'GET',
                headers: {
                    'x-auth-token': token
                }
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Failed to get vehicles');
            }
            
            return data;
        } catch (error) {
            console.error('Get all vehicles error:', error);
            throw error;
        }
    },
    
    // Get vehicle by ID
    getVehicleById: async (id) => {
        try {
            const token = getToken();
            if (!token) {
                throw new Error('No token found');
            }
            
            const response = await fetch(`${API_URL}/vehicles/${id}`, {
                method: 'GET',
                headers: {
                    'x-auth-token': token
                }
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Failed to get vehicle');
            }
            
            return data;
        } catch (error) {
            console.error('Get vehicle by ID error:', error);
            throw error;
        }
    },
    
    // Get vehicle by license plate
    getVehicleByLicensePlate: async (licensePlate) => {
        try {
            const token = getToken();
            if (!token) {
                throw new Error('No token found');
            }
            
            const response = await fetch(`${API_URL}/vehicles/plate/${licensePlate}`, {
                method: 'GET',
                headers: {
                    'x-auth-token': token
                }
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Failed to get vehicle');
            }
            
            return data;
        } catch (error) {
            console.error('Get vehicle by license plate error:', error);
            throw error;
        }
    },
    
    // Create new vehicle
    createVehicle: async (vehicleData) => {
        try {
            const token = getToken();
            if (!token) {
                throw new Error('No token found');
            }
            
            const response = await fetch(`${API_URL}/vehicles`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-auth-token': token
                },
                body: JSON.stringify(vehicleData)
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Failed to create vehicle');
            }
            
            return data;
        } catch (error) {
            console.error('Create vehicle error:', error);
            throw error;
        }
    },
    
    // Update vehicle
    updateVehicle: async (id, vehicleData) => {
        try {
            const token = getToken();
            if (!token) {
                throw new Error('No token found');
            }
            
            const response = await fetch(`${API_URL}/vehicles/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'x-auth-token': token
                },
                body: JSON.stringify(vehicleData)
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Failed to update vehicle');
            }
            
            return data;
        } catch (error) {
            console.error('Update vehicle error:', error);
            throw error;
        }
    },
    
    // Delete vehicle
    deleteVehicle: async (id) => {
        try {
            const token = getToken();
            if (!token) {
                throw new Error('No token found');
            }
            
            const response = await fetch(`${API_URL}/vehicles/${id}`, {
                method: 'DELETE',
                headers: {
                    'x-auth-token': token
                }
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Failed to delete vehicle');
            }
            
            return data;
        } catch (error) {
            console.error('Delete vehicle error:', error);
            throw error;
        }
    }
};

// Export API
const API = {
    auth: authAPI,
    vehicle: vehicleAPI
};

// For use in browser
window.API = API;
