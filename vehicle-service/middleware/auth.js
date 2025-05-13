const jwt = require('jsonwebtoken');
const axios = require('axios');

// Middleware to verify JWT token
const auth = async (req, res, next) => {
  // Get token from header
  const token = req.header('x-auth-token');

  // Check if no token
  if (!token) {
    return res.status(401).json({ message: 'No token, authorization denied' });
  }

  try {
    // Verify token locally
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    // Add user from payload
    req.user = decoded;
    next();
  } catch (error) {
    // If local verification fails, try to verify with auth service
    try {
      const response = await axios.get(`${process.env.AUTH_SERVICE_URL}/api/auth/verify`, {
        headers: {
          'x-auth-token': token
        }
      });
      
      if (response.data.valid) {
        req.user = response.data.user;
        next();
      } else {
        res.status(401).json({ message: 'Token is not valid' });
      }
    } catch (authError) {
      console.error('Auth service verification error:', authError);
      res.status(401).json({ message: 'Token is not valid' });
    }
  }
};

// Middleware to check if user is admin
const adminOnly = (req, res, next) => {
  if (req.user.role !== 'admin') {
    return res.status(403).json({ message: 'Access denied. Admin only.' });
  }
  next();
};

// Middleware to check if user is police
const policeOnly = (req, res, next) => {
  if (req.user.role !== 'police') {
    return res.status(403).json({ message: 'Access denied. Police only.' });
  }
  next();
};

// Middleware to check if user is admin or police
const adminOrPolice = (req, res, next) => {
  if (req.user.role !== 'admin' && req.user.role !== 'police') {
    return res.status(403).json({ message: 'Access denied. Admin or Police only.' });
  }
  next();
};

module.exports = { auth, adminOnly, policeOnly, adminOrPolice };
