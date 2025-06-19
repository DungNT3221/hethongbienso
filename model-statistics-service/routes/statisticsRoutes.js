const express = require('express');
const StatisticsController = require('../controllers/statisticsController');

const router = express.Router();

/**
 * @route GET /api/statistics/overview
 * @desc Get overview statistics including summary, top models, and model type stats
 * @access Public
 */
router.get('/overview', StatisticsController.getOverview);

/**
 * @route GET /api/statistics/detailed
 * @desc Get detailed statistics with pagination and filters
 * @query limit - Number of records to return (default: 50)
 * @query offset - Number of records to skip (default: 0)
 * @query model_type - Filter by model type (optional)
 * @query status - Filter by status (optional)
 * @access Public
 */
router.get('/detailed', StatisticsController.getDetailed);

/**
 * @route GET /api/statistics/trends
 * @desc Get training trends over time
 * @query months - Number of months to include (default: 12)
 * @access Public
 */
router.get('/trends', StatisticsController.getTrends);

/**
 * @route GET /api/statistics/model-types
 * @desc Get model type comparison statistics
 * @access Public
 */
router.get('/model-types', StatisticsController.getModelTypeComparison);

/**
 * @route GET /api/statistics/top-models
 * @desc Get top performing models
 * @query limit - Number of top models to return (default: 10)
 * @access Public
 */
router.get('/top-models', StatisticsController.getTopModels);

/**
 * @route GET /api/statistics/summary
 * @desc Get quick summary for dashboard
 * @access Public
 */
router.get('/summary', StatisticsController.getSummary);

/**
 * @route GET /api/statistics/health
 * @desc Get service health status
 * @access Public
 */
router.get('/health', StatisticsController.getHealth);

/**
 * @route POST /api/statistics/training
 * @desc Add new training record (called by trainregion-service)
 * @body Training record data
 * @access Internal (from other services)
 */
router.post('/training', StatisticsController.addTrainingRecord);

module.exports = router;
