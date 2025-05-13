const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
const vehicleRoutes = require("./routes/vehicles");
const { sequelize, Vehicle } = require("./models");

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3002;

// Middleware
app.use(cors());
app.use(express.json());

// Use vehicle routes
app.use("/api/vehicles", vehicleRoutes);

// Health check endpoint
app.get("/health", (req, res) => {
  res.status(200).json({ status: "Vehicle service is running" });
});

// Database connection and server start
const startServer = async () => {
  try {
    // Test database connection
    await sequelize.authenticate();
    console.log("Database connection established successfully");

    // Sync models with database
    await sequelize.sync();
    console.log("Database models synchronized");

    // Seed default vehicles if needed
    // You can add a seedVehicles function here similar to auth-service

    // Start the server
    app.listen(PORT, () => {
      console.log(`Vehicle service running on port ${PORT}`);
    });
  } catch (error) {
    console.error("Unable to connect to the database:", error);
  }
};

// Start the server
startServer();

module.exports = app;
