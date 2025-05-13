const express = require("express");
const cors = require("cors");
const axios = require("axios");
const dotenv = require("dotenv");
const jwt = require("jsonwebtoken");

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Service URLs
const AUTH_SERVICE_URL =
  process.env.AUTH_SERVICE_URL || "http://localhost:3001";
const VEHICLE_SERVICE_URL =
  process.env.VEHICLE_SERVICE_URL || "http://localhost:3002";
const JWT_SECRET = process.env.JWT_SECRET || "your_jwt_secret_key";

// Middleware
app.use(cors());
app.use(express.json());

// JWT verification middleware
const verifyToken = (req, res, next) => {
  // Skip token verification for login route
  if (req.path === "/api/auth/login") {
    return next();
  }

  const token = req.header("x-auth-token");

  if (!token) {
    return res.status(401).json({ message: "No token, authorization denied" });
  }

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ message: "Token is not valid" });
  }
};

// Auth routes
app.post("/api/auth/login", async (req, res) => {
  try {
    const response = await axios.post(
      `${AUTH_SERVICE_URL}/api/auth/login`,
      req.body
    );
    res.status(response.status).json(response.data);
  } catch (error) {
    res
      .status(error.response?.status || 500)
      .json(error.response?.data || { message: "Server error" });
  }
});

app.get("/api/auth/me", verifyToken, async (req, res) => {
  try {
    const response = await axios.get(`${AUTH_SERVICE_URL}/api/auth/me`, {
      headers: {
        "x-auth-token": req.header("x-auth-token"),
      },
    });
    res.status(response.status).json(response.data);
  } catch (error) {
    res
      .status(error.response?.status || 500)
      .json(error.response?.data || { message: "Server error" });
  }
});

app.get("/api/auth/verify", verifyToken, async (req, res) => {
  try {
    const response = await axios.get(`${AUTH_SERVICE_URL}/api/auth/verify`, {
      headers: {
        "x-auth-token": req.header("x-auth-token"),
      },
    });
    res.status(response.status).json(response.data);
  } catch (error) {
    res
      .status(error.response?.status || 500)
      .json(error.response?.data || { message: "Server error" });
  }
});

// Vehicle routes
app.get("/api/vehicles", verifyToken, async (req, res) => {
  try {
    const response = await axios.get(`${VEHICLE_SERVICE_URL}/api/vehicles`, {
      headers: {
        "x-auth-token": req.header("x-auth-token"),
      },
    });
    res.status(response.status).json(response.data);
  } catch (error) {
    res
      .status(error.response?.status || 500)
      .json(error.response?.data || { message: "Server error" });
  }
});

app.get("/api/vehicles/:id", verifyToken, async (req, res) => {
  try {
    const response = await axios.get(
      `${VEHICLE_SERVICE_URL}/api/vehicles/${req.params.id}`,
      {
        headers: {
          "x-auth-token": req.header("x-auth-token"),
        },
      }
    );
    res.status(response.status).json(response.data);
  } catch (error) {
    res
      .status(error.response?.status || 500)
      .json(error.response?.data || { message: "Server error" });
  }
});

app.get("/api/vehicles/plate/:licensePlate", verifyToken, async (req, res) => {
  try {
    const response = await axios.get(
      `${VEHICLE_SERVICE_URL}/api/vehicles/plate/${req.params.licensePlate}`,
      {
        headers: {
          "x-auth-token": req.header("x-auth-token"),
        },
      }
    );
    res.status(response.status).json(response.data);
  } catch (error) {
    res
      .status(error.response?.status || 500)
      .json(error.response?.data || { message: "Server error" });
  }
});

app.post("/api/vehicles", verifyToken, async (req, res) => {
  try {
    const response = await axios.post(
      `${VEHICLE_SERVICE_URL}/api/vehicles`,
      req.body,
      {
        headers: {
          "x-auth-token": req.header("x-auth-token"),
        },
      }
    );
    res.status(response.status).json(response.data);
  } catch (error) {
    res
      .status(error.response?.status || 500)
      .json(error.response?.data || { message: "Server error" });
  }
});

app.put("/api/vehicles/:id", verifyToken, async (req, res) => {
  try {
    const response = await axios.put(
      `${VEHICLE_SERVICE_URL}/api/vehicles/${req.params.id}`,
      req.body,
      {
        headers: {
          "x-auth-token": req.header("x-auth-token"),
        },
      }
    );
    res.status(response.status).json(response.data);
  } catch (error) {
    res
      .status(error.response?.status || 500)
      .json(error.response?.data || { message: "Server error" });
  }
});

app.delete("/api/vehicles/:id", verifyToken, async (req, res) => {
  try {
    const response = await axios.delete(
      `${VEHICLE_SERVICE_URL}/api/vehicles/${req.params.id}`,
      {
        headers: {
          "x-auth-token": req.header("x-auth-token"),
        },
      }
    );
    res.status(response.status).json(response.data);
  } catch (error) {
    res
      .status(error.response?.status || 500)
      .json(error.response?.data || { message: "Server error" });
  }
});

// Health check endpoint
app.get("/health", (req, res) => {
  res.status(200).json({ status: "API Gateway is running" });
});

// Start the server
app.listen(PORT, () => {
  console.log(`API Gateway running on port ${PORT}`);
});

module.exports = app;
