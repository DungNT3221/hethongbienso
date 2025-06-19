const { executeQuery, executeTransaction } = require('../utils/database');

class TrainingHistory {
    constructor(data = {}) {
        this.id = data.id;
        this.model_id = data.model_id;
        this.model_name = data.model_name;
        this.model_type = data.model_type;
        this.dataset_name = data.dataset_name;
        this.dataset_size = data.dataset_size || 0;
        this.epochs = data.epochs;
        this.batch_size = data.batch_size;
        this.learning_rate = data.learning_rate;
        this.training_time = data.training_time || 0;
        this.map50 = data.map50 || 0;
        this.map95 = data.map95 || 0;
        this.status = data.status;
        this.is_approved = data.is_approved || false;
        this.model_path = data.model_path;
        this.created_at = data.created_at;
        this.updated_at = data.updated_at;
    }

    /**
     * Create new training history record
     */
    static async create(data) {
        const query = `
            INSERT INTO training_history (
                model_id, model_name, model_type, dataset_name, dataset_size,
                epochs, batch_size, learning_rate, training_time, map50, map95,
                status, is_approved, model_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        `;

        const params = [
            data.model_id || null,
            data.model_name || '',
            data.model_type || '',
            data.dataset_name || null,
            data.dataset_size || 0,
            data.epochs || 0,
            data.batch_size || 0,
            data.learning_rate || 0.0,
            data.training_time || 0.0,
            data.map50 || 0.0,
            data.map95 || 0.0,
            data.status || 'completed',
            data.is_approved || false,
            data.model_path || ''
        ];

        try {
            const result = await executeQuery(query, params);
            return new TrainingHistory({ ...data, id: result.insertId });
        } catch (error) {
            console.error('Error creating training history:', error);
            throw error;
        }
    }

    /**
     * Get all training history records
     */
    static async findAll(limit = 100, offset = 0) {
        const query = `
            SELECT * FROM training_history 
            ORDER BY created_at DESC 
            LIMIT ? OFFSET ?
        `;

        try {
            const rows = await executeQuery(query, [limit, offset]);
            return rows.map(row => new TrainingHistory(row));
        } catch (error) {
            console.error('Error fetching training history:', error);
            throw error;
        }
    }

    /**
     * Get training history by ID
     */
    static async findById(id) {
        const query = 'SELECT * FROM training_history WHERE id = ?';

        try {
            const rows = await executeQuery(query, [id]);
            return rows.length > 0 ? new TrainingHistory(rows[0]) : null;
        } catch (error) {
            console.error('Error fetching training history by ID:', error);
            throw error;
        }
    }

    /**
     * Get training history by model type
     */
    static async findByModelType(modelType) {
        const query = `
            SELECT * FROM training_history 
            WHERE model_type = ? 
            ORDER BY created_at DESC
        `;

        try {
            const rows = await executeQuery(query, [modelType]);
            return rows.map(row => new TrainingHistory(row));
        } catch (error) {
            console.error('Error fetching training history by model type:', error);
            throw error;
        }
    }

    /**
     * Get statistics summary
     */
    static async getStatsSummary() {
        const query = 'SELECT * FROM v_model_stats_summary';

        try {
            const rows = await executeQuery(query);
            return rows[0] || {};
        } catch (error) {
            console.error('Error fetching stats summary:', error);
            throw error;
        }
    }

    /**
     * Get top performing models
     */
    static async getTopModels(limit = 10) {
        const query = `SELECT * FROM v_top_models LIMIT ${parseInt(limit)}`;

        try {
            const rows = await executeQuery(query);
            return rows.map(row => new TrainingHistory(row));
        } catch (error) {
            console.error('Error fetching top models:', error);
            throw error;
        }
    }

    /**
     * Get model type statistics
     */
    static async getModelTypeStats() {
        const query = 'SELECT * FROM v_model_type_stats';

        try {
            const rows = await executeQuery(query);
            return rows;
        } catch (error) {
            console.error('Error fetching model type stats:', error);
            throw error;
        }
    }

    /**
     * Get training trends by month
     */
    static async getTrainingTrends(months = 12) {
        const query = `
            SELECT
                DATE_FORMAT(created_at, '%Y-%m') as month,
                COUNT(*) as total_trainings,
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
                COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed,
                AVG(CASE WHEN status = 'completed' THEN map50 END) as avg_map50,
                AVG(CASE WHEN status = 'completed' THEN training_time END) as avg_training_time
            FROM training_history
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL ${parseInt(months)} MONTH)
            GROUP BY DATE_FORMAT(created_at, '%Y-%m')
            ORDER BY month DESC
        `;

        try {
            const rows = await executeQuery(query);
            return rows.map(row => ({
                ...row,
                avg_map50: parseFloat(row.avg_map50 || 0),
                avg_training_time: parseFloat(row.avg_training_time || 0),
                success_rate: row.total_trainings > 0 ?
                    Math.round((row.completed / row.total_trainings) * 100) : 0
            }));
        } catch (error) {
            console.error('Error fetching training trends:', error);
            throw error;
        }
    }

    /**
     * Update training history record
     */
    async update(data) {
        const query = `
            UPDATE training_history 
            SET model_name = ?, model_type = ?, dataset_name = ?, dataset_size = ?,
                epochs = ?, batch_size = ?, learning_rate = ?, training_time = ?,
                map50 = ?, map95 = ?, status = ?, is_approved = ?, model_path = ?
            WHERE id = ?
        `;

        const params = [
            data.model_name || this.model_name,
            data.model_type || this.model_type,
            data.dataset_name || this.dataset_name,
            data.dataset_size || this.dataset_size,
            data.epochs || this.epochs,
            data.batch_size || this.batch_size,
            data.learning_rate || this.learning_rate,
            data.training_time || this.training_time,
            data.map50 || this.map50,
            data.map95 || this.map95,
            data.status || this.status,
            data.is_approved !== undefined ? data.is_approved : this.is_approved,
            data.model_path || this.model_path,
            this.id
        ];

        try {
            await executeQuery(query, params);
            Object.assign(this, data);
            return this;
        } catch (error) {
            console.error('Error updating training history:', error);
            throw error;
        }
    }

    /**
     * Delete training history record
     */
    async delete() {
        const query = 'DELETE FROM training_history WHERE id = ?';

        try {
            await executeQuery(query, [this.id]);
            return true;
        } catch (error) {
            console.error('Error deleting training history:', error);
            throw error;
        }
    }

    /**
     * Convert to JSON
     */
    toJSON() {
        return {
            id: this.id,
            model_id: this.model_id,
            model_name: this.model_name,
            model_type: this.model_type,
            dataset_name: this.dataset_name,
            dataset_size: this.dataset_size,
            epochs: this.epochs,
            batch_size: this.batch_size,
            learning_rate: this.learning_rate,
            training_time: this.training_time,
            map50: this.map50,
            map95: this.map95,
            status: this.status,
            is_approved: this.is_approved,
            model_path: this.model_path,
            created_at: this.created_at,
            updated_at: this.updated_at
        };
    }
}

module.exports = TrainingHistory;
