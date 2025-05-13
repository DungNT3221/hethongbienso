const { Vehicle } = require("../models");
const { Op } = require("sequelize");

// Get all vehicles
exports.getAllVehicles = async (req, res) => {
  try {
    const vehicles = await Vehicle.findAll({
      order: [["createdAt", "DESC"]],
    });
    res.status(200).json(vehicles);
  } catch (error) {
    console.error("Get all vehicles error:", error);
    res.status(500).json({ message: "Server error" });
  }
};

// Get vehicle by ID
exports.getVehicleById = async (req, res) => {
  try {
    const vehicle = await Vehicle.findByPk(req.params.id);
    if (!vehicle) {
      return res.status(404).json({ message: "Vehicle not found" });
    }
    res.status(200).json(vehicle);
  } catch (error) {
    console.error("Get vehicle by ID error:", error);
    res.status(500).json({ message: "Server error" });
  }
};

// Get vehicle by license plate
exports.getVehicleByLicensePlate = async (req, res) => {
  try {
    const vehicle = await Vehicle.findOne({
      where: { licensePlate: req.params.licensePlate },
    });
    if (!vehicle) {
      return res.status(404).json({ message: "Vehicle not found" });
    }
    res.status(200).json(vehicle);
  } catch (error) {
    console.error("Get vehicle by license plate error:", error);
    res.status(500).json({ message: "Server error" });
  }
};

// Create new vehicle
exports.createVehicle = async (req, res) => {
  try {
    // Check if license plate already exists
    const existingVehicle = await Vehicle.findOne({
      where: { licensePlate: req.body.licensePlate },
    });
    if (existingVehicle) {
      return res
        .status(400)
        .json({ message: "License plate already registered" });
    }

    const newVehicle = await Vehicle.create(req.body);
    res.status(201).json(newVehicle);
  } catch (error) {
    console.error("Create vehicle error:", error);
    res.status(500).json({ message: "Server error" });
  }
};

// Update vehicle
exports.updateVehicle = async (req, res) => {
  try {
    // Check if license plate is being changed and already exists
    if (req.body.licensePlate) {
      const existingVehicle = await Vehicle.findOne({
        where: {
          licensePlate: req.body.licensePlate,
          id: { [Op.ne]: req.params.id },
        },
      });

      if (existingVehicle) {
        return res.status(400).json({
          message: "License plate already registered to another vehicle",
        });
      }
    }

    const vehicle = await Vehicle.findByPk(req.params.id);
    if (!vehicle) {
      return res.status(404).json({ message: "Vehicle not found" });
    }

    await vehicle.update(req.body);

    // Get the updated vehicle
    const updatedVehicle = await Vehicle.findByPk(req.params.id);
    res.status(200).json(updatedVehicle);
  } catch (error) {
    console.error("Update vehicle error:", error);
    res.status(500).json({ message: "Server error" });
  }
};

// Delete vehicle
exports.deleteVehicle = async (req, res) => {
  try {
    const vehicle = await Vehicle.findByPk(req.params.id);
    if (!vehicle) {
      return res.status(404).json({ message: "Vehicle not found" });
    }

    await vehicle.destroy();
    res.status(200).json({ message: "Vehicle deleted successfully" });
  } catch (error) {
    console.error("Delete vehicle error:", error);
    res.status(500).json({ message: "Server error" });
  }
};
