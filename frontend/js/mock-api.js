// Mock data
const mockUsers = [
    {
        id: '1',
        username: 'admin',
        password: 'admin123', // In a real app, passwords would be hashed
        role: 'admin',
        fullName: 'System Administrator'
    },
    {
        id: '2',
        username: 'police',
        password: 'police123',
        role: 'police',
        fullName: 'Police Officer'
    }
];

const mockVehicles = [
    {
        id: '1',
        licensePlate: '29A-12345',
        ownerName: 'Nguyễn Văn A',
        ownerID: '001234567890',
        vehicleType: 'Sedan',
        brand: 'Toyota',
        model: 'Camry',
        color: 'Đen',
        registrationDate: '2022-01-15',
        expiryDate: '2027-01-15',
        status: 'active'
    },
    {
        id: '2',
        licensePlate: '30A-54321',
        ownerName: 'Trần Thị B',
        ownerID: '001234567891',
        vehicleType: 'SUV',
        brand: 'Honda',
        model: 'CR-V',
        color: 'Trắng',
        registrationDate: '2021-05-20',
        expiryDate: '2026-05-20',
        status: 'active'
    },
    {
        id: '3',
        licensePlate: '31A-98765',
        ownerName: 'Lê Văn C',
        ownerID: '001234567892',
        vehicleType: 'Hatchback',
        brand: 'Mazda',
        model: 'Mazda3',
        color: 'Đỏ',
        registrationDate: '2020-11-10',
        expiryDate: '2025-11-10',
        status: 'active'
    }
];

// Get token from localStorage
const getToken = () => {
    return localStorage.getItem('token');
};

// Auth API
const authAPI = {
    // Login
    login: async (username, password) => {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Find user
        const user = mockUsers.find(u => u.username === username && u.password === password);
        
        if (!user) {
            throw new Error('Invalid credentials');
        }
        
        // Generate a mock token
        const token = `mock-token-${user.id}-${Date.now()}`;
        
        // Return user info and token
        return {
            token,
            user: {
                id: user.id,
                username: user.username,
                role: user.role,
                fullName: user.fullName
            }
        };
    },
    
    // Get current user
    getCurrentUser: async () => {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 500));
        
        const token = getToken();
        if (!token) {
            throw new Error('No token found');
        }
        
        // In a real app, we would decode the token
        // For mock, we'll extract the user ID from the token
        const userId = token.split('-')[2];
        const user = mockUsers.find(u => u.id === userId);
        
        if (!user) {
            throw new Error('User not found');
        }
        
        return {
            id: user.id,
            username: user.username,
            role: user.role,
            fullName: user.fullName
        };
    }
};

// Vehicle API
const vehicleAPI = {
    // Get all vehicles
    getAllVehicles: async () => {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Get vehicles from localStorage or use mock data
        const storedVehicles = localStorage.getItem('vehicles');
        return storedVehicles ? JSON.parse(storedVehicles) : mockVehicles;
    },
    
    // Get vehicle by ID
    getVehicleById: async (id) => {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Get vehicles from localStorage or use mock data
        const vehicles = localStorage.getItem('vehicles') 
            ? JSON.parse(localStorage.getItem('vehicles')) 
            : mockVehicles;
        
        const vehicle = vehicles.find(v => v.id === id);
        
        if (!vehicle) {
            throw new Error('Vehicle not found');
        }
        
        return vehicle;
    },
    
    // Get vehicle by license plate
    getVehicleByLicensePlate: async (licensePlate) => {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Get vehicles from localStorage or use mock data
        const vehicles = localStorage.getItem('vehicles') 
            ? JSON.parse(localStorage.getItem('vehicles')) 
            : mockVehicles;
        
        const vehicle = vehicles.find(v => v.licensePlate.toLowerCase().includes(licensePlate.toLowerCase()));
        
        if (!vehicle) {
            throw new Error('Vehicle not found');
        }
        
        return vehicle;
    },
    
    // Create new vehicle
    createVehicle: async (vehicleData) => {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Get vehicles from localStorage or use mock data
        const vehicles = localStorage.getItem('vehicles') 
            ? JSON.parse(localStorage.getItem('vehicles')) 
            : [...mockVehicles];
        
        // Check if license plate already exists
        if (vehicles.some(v => v.licensePlate === vehicleData.licensePlate)) {
            throw new Error('License plate already registered');
        }
        
        // Generate new ID
        const newId = (Math.max(...vehicles.map(v => parseInt(v.id))) + 1).toString();
        
        // Create new vehicle
        const newVehicle = {
            id: newId,
            ...vehicleData,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };
        
        // Add to vehicles array
        vehicles.push(newVehicle);
        
        // Save to localStorage
        localStorage.setItem('vehicles', JSON.stringify(vehicles));
        
        return newVehicle;
    },
    
    // Update vehicle
    updateVehicle: async (id, vehicleData) => {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Get vehicles from localStorage or use mock data
        const vehicles = localStorage.getItem('vehicles') 
            ? JSON.parse(localStorage.getItem('vehicles')) 
            : [...mockVehicles];
        
        // Find vehicle index
        const index = vehicles.findIndex(v => v.id === id);
        
        if (index === -1) {
            throw new Error('Vehicle not found');
        }
        
        // Check if license plate is being changed and already exists
        if (vehicleData.licensePlate && vehicleData.licensePlate !== vehicles[index].licensePlate) {
            if (vehicles.some(v => v.licensePlate === vehicleData.licensePlate && v.id !== id)) {
                throw new Error('License plate already registered to another vehicle');
            }
        }
        
        // Update vehicle
        const updatedVehicle = {
            ...vehicles[index],
            ...vehicleData,
            updatedAt: new Date().toISOString()
        };
        
        vehicles[index] = updatedVehicle;
        
        // Save to localStorage
        localStorage.setItem('vehicles', JSON.stringify(vehicles));
        
        return updatedVehicle;
    },
    
    // Delete vehicle
    deleteVehicle: async (id) => {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Get vehicles from localStorage or use mock data
        const vehicles = localStorage.getItem('vehicles') 
            ? JSON.parse(localStorage.getItem('vehicles')) 
            : [...mockVehicles];
        
        // Find vehicle index
        const index = vehicles.findIndex(v => v.id === id);
        
        if (index === -1) {
            throw new Error('Vehicle not found');
        }
        
        // Remove vehicle
        vehicles.splice(index, 1);
        
        // Save to localStorage
        localStorage.setItem('vehicles', JSON.stringify(vehicles));
        
        return { message: 'Vehicle deleted successfully' };
    }
};

// Export API
const API = {
    auth: authAPI,
    vehicle: vehicleAPI
};

// For use in browser
window.API = API;
