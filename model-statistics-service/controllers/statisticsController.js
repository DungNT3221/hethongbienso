const TrainingHistory = require('../models/trainingHistory');
const { getDatabaseStats } = require('../utils/database');

class StatisticsController {
    /**
     * Get overview statistics
     */
    static async getOverview(req, res) {
        try {
            const summary = await TrainingHistory.getStatsSummary();
            const topModels = await TrainingHistory.getTopModels(5);
            const modelTypeStats = await TrainingHistory.getModelTypeStats();

            res.json({
                success: true,
                data: {
                    summary: {
                        total_models: summary.total_models || 0,
                        completed_models: summary.completed_models || 0,
                        failed_models: summary.failed_models || 0,
                        stopped_models: summary.stopped_models || 0,
                        success_rate: parseFloat(summary.success_rate || 0),
                        avg_map50: parseFloat(summary.avg_map50 || 0),
                        avg_map95: parseFloat(summary.avg_map95 || 0),
                        avg_training_time: parseFloat(summary.avg_training_time || 0),
                        best_map50: parseFloat(summary.best_map50 || 0),
                        best_map95: parseFloat(summary.best_map95 || 0)
                    },
                    top_models: topModels.map(model => model.toJSON()),
                    model_type_stats: modelTypeStats
                }
            });

        } catch (error) {
            console.error('Error getting overview statistics:', error);
            res.status(500).json({
                success: false,
                error: 'Failed to fetch overview statistics',
                message: error.message
            });
        }
    }

    /**
     * Get detailed statistics
     */
    static async getDetailed(req, res) {
        try {
            const { limit = 50, offset = 0, model_type, status } = req.query;

            let allTrainings = await TrainingHistory.findAll(parseInt(limit), parseInt(offset));

            // Filter by model type if specified
            if (model_type) {
                allTrainings = allTrainings.filter(training => training.model_type === model_type);
            }

            // Filter by status if specified
            if (status) {
                allTrainings = allTrainings.filter(training => training.status === status);
            }

            const trends = await TrainingHistory.getTrainingTrends(12);

            res.json({
                success: true,
                data: {
                    trainings: allTrainings.map(training => training.toJSON()),
                    trends: trends,
                    pagination: {
                        limit: parseInt(limit),
                        offset: parseInt(offset),
                        total: allTrainings.length
                    }
                }
            });

        } catch (error) {
            console.error('Error getting detailed statistics:', error);
            res.status(500).json({
                success: false,
                error: 'Failed to fetch detailed statistics',
                message: error.message
            });
        }
    }

    /**
     * Get training trends
     */
    static async getTrends(req, res) {
        try {
            const { months = 12 } = req.query;
            const trends = await TrainingHistory.getTrainingTrends(parseInt(months));

            res.json({
                success: true,
                data: {
                    trends: trends,
                    period_months: parseInt(months)
                }
            });

        } catch (error) {
            console.error('Error getting training trends:', error);
            res.status(500).json({
                success: false,
                error: 'Failed to fetch training trends',
                message: error.message
            });
        }
    }

    /**
     * Get model type comparison
     */
    static async getModelTypeComparison(req, res) {
        try {
            const modelTypeStats = await TrainingHistory.getModelTypeStats();

            res.json({
                success: true,
                data: {
                    model_types: modelTypeStats.map(stat => ({
                        model_type: stat.model_type,
                        total_count: stat.total_count,
                        completed_count: stat.completed_count,
                        success_rate: stat.total_count > 0 ? 
                            Math.round((stat.completed_count / stat.total_count) * 100) : 0,
                        avg_map50: parseFloat(stat.avg_map50 || 0),
                        best_map50: parseFloat(stat.best_map50 || 0),
                        avg_training_time_minutes: parseFloat(stat.avg_training_time || 0) / 60
                    }))
                }
            });

        } catch (error) {
            console.error('Error getting model type comparison:', error);
            res.status(500).json({
                success: false,
                error: 'Failed to fetch model type comparison',
                message: error.message
            });
        }
    }

    /**
     * Get top performing models
     */
    static async getTopModels(req, res) {
        try {
            const { limit = 10 } = req.query;
            const topModels = await TrainingHistory.getTopModels(parseInt(limit));

            res.json({
                success: true,
                data: {
                    top_models: topModels.map(model => ({
                        ...model.toJSON(),
                        composite_score: model.composite_score,
                        performance_rank: topModels.indexOf(model) + 1
                    })),
                    limit: parseInt(limit)
                }
            });

        } catch (error) {
            console.error('Error getting top models:', error);
            res.status(500).json({
                success: false,
                error: 'Failed to fetch top models',
                message: error.message
            });
        }
    }

    /**
     * Add new training record (called by trainregion-service)
     */
    static async addTrainingRecord(req, res) {
        try {
            const {
                model_id,
                model_name,
                model_type,
                dataset_name,
                dataset_size,
                epochs,
                batch_size,
                learning_rate,
                training_time,
                map50,
                map95,
                status,
                is_approved,
                model_path
            } = req.body;

            // Validate required fields
            if (!model_name || !model_type || !status) {
                return res.status(400).json({
                    success: false,
                    error: 'Missing required fields',
                    required: ['model_name', 'model_type', 'status']
                });
            }

            const trainingRecord = await TrainingHistory.create({
                model_id,
                model_name,
                model_type,
                dataset_name,
                dataset_size,
                epochs,
                batch_size,
                learning_rate,
                training_time,
                map50,
                map95,
                status,
                is_approved,
                model_path
            });

            res.status(201).json({
                success: true,
                message: 'Training record added successfully',
                data: trainingRecord.toJSON()
            });

        } catch (error) {
            console.error('Error adding training record:', error);
            res.status(500).json({
                success: false,
                error: 'Failed to add training record',
                message: error.message
            });
        }
    }

    /**
     * Get database health
     */
    static async getHealth(req, res) {
        try {
            const dbStats = await getDatabaseStats();

            res.json({
                success: true,
                service: 'model-statistics-service',
                database: 'healthy',
                stats: dbStats,
                timestamp: new Date().toISOString()
            });

        } catch (error) {
            console.error('Error getting health status:', error);
            res.status(500).json({
                success: false,
                service: 'model-statistics-service',
                database: 'unhealthy',
                error: error.message,
                timestamp: new Date().toISOString()
            });
        }
    }

    /**
     * Get summary for dashboard
     */
    static async getSummary(req, res) {
        try {
            const summary = await TrainingHistory.getStatsSummary();

            res.json({
                success: true,
                data: {
                    total_models: summary.total_models || 0,
                    completed_models: summary.completed_models || 0,
                    success_rate: parseFloat(summary.success_rate || 0),
                    best_map50: parseFloat(summary.best_map50 || 0),
                    avg_map50: parseFloat(summary.avg_map50 || 0)
                }
            });

        } catch (error) {
            console.error('Error getting summary:', error);
            res.status(500).json({
                success: false,
                error: 'Failed to fetch summary',
                message: error.message
            });
        }
    }
}

module.exports = StatisticsController;
