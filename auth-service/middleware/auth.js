const jwt = require('jsonwebtoken');

// Middleware to verify JWT token
const auth = (req, res, next) => {
  // Get token from header
  const token = req.header('x-auth-token');

  // Check if no token
  if (!token) {
    return res.status(401).json({ message: 'No token, authorization denied' });
  }

  try {
    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    // Add user from payload
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ message: 'Token is not valid' });
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
