const express = require("express");
const cors = require("cors");
const axios = require("axios");
const dotenv = require("dotenv");
const jwt = require("jsonwebtoken");
const { createProxyMiddleware } = require('http-proxy-middleware');

// JWT verification middleware (moved to very top)
function verifyToken(req, res, next) {
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
}
console.log('verifyToken function defined and available at top.'); // Added for debugging

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Service URLs
const AUTH_SERVICE_URL =
  process.env.AUTH_SERVICE_URL || "http://localhost:3001";
const VEHICLE_SERVICE_URL =
  process.env.VEHICLE_SERVICE_URL || "http://localhost:3002";
const TRAINREGION_SERVICE_URL =
  process.env.TRAINREGION_SERVICE_URL || "http://localhost:3003";
const JWT_SECRET = process.env.JWT_SECRET || "your_jwt_secret_key";

// Middleware
app.use(cors());

// Special handling for multipart/form-data routes (before express.json())
// This ensures the raw request body is forwarded
app.post('/api/dataset/upload-images', verifyToken, createProxyMiddleware({
  target: TRAINREGION_SERVICE_URL,
  changeOrigin: true, // Needed for virtual hosted sites
  onProxyReq: (proxyReq, req) => {
    // Add x-auth-token to the proxy request headers
    proxyReq.setHeader('x-auth-token', req.header('x-auth-token'));
    // No need to set Content-Type or Content-Length here, as it's handled by piping the raw stream
  },
  onError: (err, req, res) => {
    console.error('Proxy error (upload-images):', err);
    res.status(500).json({ success: false, message: 'Failed to upload images via proxy.' });
  },
  bodyParser: false, // Crucial: tell proxy not to parse the body itself, just pipe it
}));

app.post('/api/dataset/upload-zip', verifyToken, createProxyMiddleware({
  target: TRAINREGION_SERVICE_URL,
  changeOrigin: true,
  onProxyReq: (proxyReq, req) => {
    proxyReq.setHeader('x-auth-token', req.header('x-auth-token'));
  },
  onError: (err, req, res) => {
    console.error('Proxy error (upload-zip):', err);
    res.status(500).json({ success: false, message: 'Failed to upload ZIP via proxy.' });
  },
  bodyParser: false,
}));

// Global middleware for JSON body parsing for all other routes
app.use(express.json());

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

// TrainRegion Service routes
app.post("/api/predict", verifyToken, async (req, res) => {
  try {
    const response = await axios.post(
      `${TRAINREGION_SERVICE_URL}/api/predict`,
      req.body,
      {
        headers: {
          ...req.headers,
          "Content-Type": "multipart/form-data",
        },
      }
    );
    res.status(response.status).json(response.data);
  } catch (error) {
    res
      .status(error.response?.status || 500)
      .json(error.response?.data || { message: "Prediction error" });
  }
});

app.post("/api/train", verifyToken, async (req, res) => {
  try {
    const response = await axios.post(
      `${TRAINREGION_SERVICE_URL}/api/train/`,
      req.body,
      {
        headers: {
          ...req.headers,
        },
      }
    );
    res.status(response.status).json(response.data);
  } catch (error) {
    res
      .status(error.response?.status || 500)
      .json(error.response?.data || { message: "Training error" });
  }
});

app.get("/api/train/jobs", verifyToken, async (req, res) => {
  try {
    const response = await axios.get(
      `${TRAINREGION_SERVICE_URL}/api/train/jobs`,
      {
        headers: {
          ...req.headers,
        },
      }
    );
    res.status(response.status).json(response.data);
  } catch (error) {
    res
      .status(error.response?.status || 500)
      .json(error.response?.data || { message: "Training jobs fetch error" });
  }
});

app.post("/api/predict", verifyToken, async (req, res) => {
  try {
    const response = await axios.post(
      `${TRAINREGION_SERVICE_URL}/api/predict/`,
      req.body,
      {
        headers: {
          ...req.headers,
        },
      }
    );
    res.status(response.status).json(response.data);
  } catch (error) {
    res
      .status(error.response?.status || 500)
      .json(error.response?.data || { message: "Predict error" });
  }
});

app.get("/api/predict/history", verifyToken, async (req, res) => {
  try {
    const response = await axios.get(
      `${TRAINREGION_SERVICE_URL}/api/predict/history`,
      {
        headers: {
          ...req.headers,
        },
      }
    );
    res.status(response.status).json(response.data);
  } catch (error) {
    res
      .status(error.response?.status || 500)
      .json(error.response?.data || { message: "Predict history fetch error" });
  }
});

app.get("/api/models", verifyToken, async (req, res) => {
  try {
    const response = await axios.get(
      `${TRAINREGION_SERVICE_URL}/api/model/`,
      {
        headers: {
          ...req.headers,
        },
      }
    );
    res.status(response.status).json(response.data);
  } catch (error) {
    res
      .status(error.response?.status || 500)
      .json(error.response?.data || { message: "Model fetch error" });
  }
});

app.get("/api/dataset", verifyToken, async (req, res) => {
  try {
    console.log("API Gateway: Receiving GET /api/dataset request. Forwarding to TrainRegion Service.");
    
    const token = req.header("x-auth-token");
    if (!token) {
      console.error("API Gateway: No token provided for /api/dataset");
      return res.status(401).json({ success: false, message: "No token, authorization denied" });
    }

    console.log(`API Gateway: Forwarding GET /api/dataset to ${TRAINREGION_SERVICE_URL}/api/dataset with token: ${token ? 'present' : 'missing'}`);
    const response = await axios.get(
      `${TRAINREGION_SERVICE_URL}/api/dataset`,
      {
        headers: {
          "x-auth-token": token,
        },
        timeout: 10000, // 10 second timeout
      }
    );
    console.log(`API Gateway: Received response from TrainRegion Service for /api/dataset with status ${response.status}`);
    res.status(response.status).json(response.data);
  } catch (error) {
    console.error("API Gateway Error: Error fetching datasets from TrainRegion service:", error.message);
    if (error.code === 'ECONNREFUSED') {
      return res.status(503).json({ 
        success: false,
        message: "TrainRegion service is not available" 
      });
    }
    // Log detailed error response if available
    if (error.response) {
      console.error("API Gateway Error: TrainRegion Service responded with status:", error.response.status);
      console.error("API Gateway Error: TrainRegion Service response data:", error.response.data);
    }
    res
      .status(error.response?.status || 500)
      .json({ 
        success: false,
        message: error.response?.data?.message || "Failed to fetch datasets" 
      });
  }
});

app.get("/api/dataset/:id/preview", verifyToken, async (req, res) => {
  try {
    const response = await axios.get(
      `${TRAINREGION_SERVICE_URL}/api/dataset/${req.params.id}/preview`,
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
      .json(error.response?.data || { message: "Failed to get dataset preview" });
  }
});

app.delete("/api/dataset/:id", verifyToken, async (req, res) => {
  try {
    const response = await axios.delete(
      `${TRAINREGION_SERVICE_URL}/api/dataset/${req.params.id}`,
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
      .json(error.response?.data || { message: "Failed to delete dataset" });
  }
});

// Training routes
app.post("/api/training/start", verifyToken, async (req, res) => {
  try {
    const response = await axios.post(
      `${TRAINREGION_SERVICE_URL}/api/training/start`,
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

app.get("/api/training/jobs/:jobId/status", verifyToken, async (req, res) => {
  try {
    const response = await axios.get(
      `${TRAINREGION_SERVICE_URL}/api/training/jobs/${req.params.jobId}/status`,
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

app.post("/api/training/jobs/:jobId/save-model", verifyToken, async (req, res) => {
  try {
    const response = await axios.post(
      `${TRAINREGION_SERVICE_URL}/api/training/jobs/${req.params.jobId}/save-model`,
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

app.post("/api/training/jobs/:jobId/discard-model", verifyToken, async (req, res) => {
  try {
    const response = await axios.post(
      `${TRAINREGION_SERVICE_URL}/api/training/jobs/${req.params.jobId}/discard-model`,
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

// Health check endpoint
app.get("/health", (req, res) => {
  res.status(200).json({ status: "API Gateway is running" });
});

// Start the server
app.listen(PORT, () => {
  console.log(`API Gateway running on port ${PORT}`);
});

module.exports = app;
