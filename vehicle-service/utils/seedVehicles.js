const Vehicle = require('../models/Vehicle');

// Function to seed sample vehicles
const seedVehicles = async () => {
  try {
    // Check if vehicles already exist
    const count = await Vehicle.countDocuments();
    
    // Only seed if no vehicles exist
    if (count === 0) {
      const sampleVehicles = [
        {
          licensePlate: '29A-12345',
          ownerName: 'Nguyễn Văn A',
          ownerID: '001234567890',
          vehicleType: 'Sedan',
          brand: 'Toyota',
          model: 'Camry',
          color: 'Black',
          registrationDate: new Date('2022-01-15'),
          expiryDate: new Date('2027-01-15'),
          status: 'active',
        },
        {
          licensePlate: '30A-54321',
          ownerName: 'Trần Thị B',
          ownerID: '001234567891',
          vehicleType: 'SUV',
          brand: 'Honda',
          model: 'CR-V',
          color: 'White',
          registrationDate: new Date('2021-05-20'),
          expiryDate: new Date('2026-05-20'),
          status: 'active',
        },
        {
          licensePlate: '31A-98765',
          ownerName: 'Lê Văn C',
          ownerID: '001234567892',
          vehicleType: 'Hatchback',
          brand: 'Mazda',
          model: 'Mazda3',
          color: 'Red',
          registrationDate: new Date('2020-11-10'),
          expiryDate: new Date('2025-11-10'),
          status: 'active',
        },
      ];

      await Vehicle.insertMany(sampleVehicles);
      console.log('Sample vehicles seeded successfully');
    }
  } catch (error) {
    console.error('Error seeding vehicles:', error);
  }
};

module.exports = seedVehicles;
