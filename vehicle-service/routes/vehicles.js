const express = require("express");
const router = express.Router();
const vehicleController = require("../controllers/vehicleController");
const { auth, adminOnly, adminOrPolice } = require("../middleware/auth");

// @route   GET /api/vehicles
// @desc    Get all vehicles
// @access  Private (admin or police)
router.get("/", auth, adminOrPolice, vehicleController.getAllVehicles);

// @route   GET /api/vehicles/plate/:licensePlate
// @desc    Get vehicle by license plate
// @access  Private (admin or police)
router.get(
  "/plate/:licensePlate",
  auth,
  adminOrPolice,
  vehicleController.getVehicleByLicensePlate
);

// @route   GET /api/vehicles/:id
// @desc    Get vehicle by ID
// @access  Private (admin or police)
router.get("/:id", auth, adminOrPolice, vehicleController.getVehicleById);

// @route   POST /api/vehicles
// @desc    Create a new vehicle
// @access  Private (admin only)
router.post("/", auth, adminOnly, vehicleController.createVehicle);

// @route   PUT /api/vehicles/:id
// @desc    Update a vehicle
// @access  Private (admin only)
router.put("/:id", auth, adminOnly, vehicleController.updateVehicle);

// @route   DELETE /api/vehicles/:id
// @desc    Delete a vehicle
// @access  Private (admin only)
router.delete("/:id", auth, adminOnly, vehicleController.deleteVehicle);

module.exports = router;
