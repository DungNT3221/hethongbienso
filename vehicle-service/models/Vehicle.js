const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
  const Vehicle = sequelize.define(
    "Vehicle",
    {
      id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true,
      },
      licensePlate: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true,
      },
      ownerName: {
        type: DataTypes.STRING,
        allowNull: false,
      },
      ownerID: {
        type: DataTypes.STRING,
        allowNull: false,
      },
      vehicleType: {
        type: DataTypes.STRING,
        allowNull: false,
      },
      brand: {
        type: DataTypes.STRING,
        allowNull: false,
      },
      model: {
        type: DataTypes.STRING,
        allowNull: false,
      },
      color: {
        type: DataTypes.STRING,
        allowNull: false,
      },
      registrationDate: {
        type: DataTypes.DATEONLY,
        allowNull: false,
      },
      expiryDate: {
        type: DataTypes.DATEONLY,
        allowNull: false,
      },
      status: {
        type: DataTypes.ENUM("active", "expired", "suspended"),
        allowNull: false,
        defaultValue: "active",
      },
    },
    {
      timestamps: true,
    }
  );

  return Vehicle;
};
