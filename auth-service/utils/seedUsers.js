const { User } = require("../models");

// Function to seed default users
const seedUsers = async () => {
  try {
    // Check if users already exist
    const adminCount = await User.count({ where: { role: "admin" } });
    const policeCount = await User.count({ where: { role: "police" } });

    // Create default admin if none exists
    if (adminCount === 0) {
      await User.create({
        username: "admin",
        password: "admin123",
        role: "admin",
        fullName: "System Administrator",
      });
      console.log("Default admin user created");
    }

    // Create default police if none exists
    if (policeCount === 0) {
      await User.create({
        username: "police",
        password: "police123",
        role: "police",
        fullName: "Police Officer",
      });
      console.log("Default police user created");
    }
  } catch (error) {
    console.error("Error seeding users:", error);
  }
};

module.exports = { seedUsers };
