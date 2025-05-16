const jwt = require("jsonwebtoken");

// Middleware để xác thực JWT token
const auth = (req, res, next) => {
  const token = req.header("x-auth-token");

  if (!token) {
    return res.status(401).json({ message: "No token, authorization denied" });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ message: "Token is not valid" });
  }
};

// Middleware dùng chung để kiểm tra vai trò
const allowRoles = (...allowedRoles) => {
  return (req, res, next) => {
    if (!req.user || !allowedRoles.includes(req.user.role)) {
      return res.status(403).json({
        message: `Access denied. Allowed roles: ${allowedRoles.join(", ")}`,
      });
    }
    next();
  };
};

// Định nghĩa các middleware phân quyền cụ thể
const adminOnly = allowRoles("admin");
const policeOnly = allowRoles("police");
const adminOrPolice = allowRoles("admin", "police");

module.exports = { auth, adminOnly, policeOnly, adminOrPolice };
