const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
const authRoutes = require("./routes/auth");
const { sequelize, User } = require("./models");
const { seedUsers } = require("./utils/seedUsers");

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Use auth routes
app.use("/api/auth", authRoutes);

// Health check endpoint
app.get("/health", (req, res) => {
  res.status(200).json({ status: "Auth service is running" });
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

    // Seed default users
    await seedUsers();

    // Start the server
    app.listen(PORT, () => {
      console.log(`Auth service running on port ${PORT}`);
    });
  } catch (error) {
    console.error("Unable to connect to the database:", error);
  }
};

// Start the server
startServer();

module.exports = app;
