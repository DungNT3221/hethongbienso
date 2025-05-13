const { Sequelize } = require('sequelize');
const dotenv = require('dotenv');

dotenv.config();

// Database configuration
const DB_HOST = process.env.DB_HOST || 'localhost';
const DB_PORT = process.env.DB_PORT || 3306;
const DB_USER = process.env.DB_USER || 'user';
const DB_PASSWORD = process.env.DB_PASSWORD || 'password';
const DB_NAME = process.env.DB_NAME || 'license_plate_system';

// Create Sequelize instance
const sequelize = new Sequelize(DB_NAME, DB_USER, DB_PASSWORD, {
  host: DB_HOST,
  port: DB_PORT,
  dialect: 'mysql',
  logging: false,
});

// Import models
const Vehicle = require('./Vehicle')(sequelize);

// Export models and sequelize instance
module.exports = {
  sequelize,
  Vehicle,
};
