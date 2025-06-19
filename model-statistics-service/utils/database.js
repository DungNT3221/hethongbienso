const mysql = require('mysql2/promise');

// Database configuration
const dbConfig = {
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 3306,
    user: process.env.DB_USER || 'modelstats_user',
    password: process.env.DB_PASSWORD || '123456',
    database: process.env.DB_NAME || 'modelstats_db',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0,
    acquireTimeout: 60000,
    timeout: 60000,
    reconnect: true
};

// Create connection pool
const pool = mysql.createPool(dbConfig);

/**
 * Test database connection
 */
async function testDatabaseConnection() {
    try {
        const connection = await pool.getConnection();
        await connection.ping();
        connection.release();
        return true;
    } catch (error) {
        console.error('Database connection failed:', error);
        throw error;
    }
}

/**
 * Execute a query with parameters
 */
async function executeQuery(query, params = []) {
    try {
        const [rows] = await pool.execute(query, params);
        return rows;
    } catch (error) {
        console.error('Query execution failed:', error);
        console.error('Query:', query);
        console.error('Params:', params);
        throw error;
    }
}

/**
 * Execute multiple queries in a transaction
 */
async function executeTransaction(queries) {
    const connection = await pool.getConnection();
    
    try {
        await connection.beginTransaction();
        
        const results = [];
        for (const { query, params } of queries) {
            const [result] = await connection.execute(query, params || []);
            results.push(result);
        }
        
        await connection.commit();
        return results;
        
    } catch (error) {
        await connection.rollback();
        throw error;
    } finally {
        connection.release();
    }
}

/**
 * Get database statistics
 */
async function getDatabaseStats() {
    try {
        const queries = [
            'SELECT COUNT(*) as total_records FROM training_history',
            'SELECT COUNT(*) as completed_models FROM training_history WHERE status = "completed"',
            'SELECT COUNT(*) as failed_models FROM training_history WHERE status = "failed"',
            'SELECT AVG(map50) as avg_map50 FROM training_history WHERE status = "completed"',
            'SELECT MAX(map50) as best_map50 FROM training_history WHERE status = "completed"'
        ];

        const results = await Promise.all(
            queries.map(query => executeQuery(query))
        );

        return {
            total_records: results[0][0]?.total_records || 0,
            completed_models: results[1][0]?.completed_models || 0,
            failed_models: results[2][0]?.failed_models || 0,
            avg_map50: parseFloat(results[3][0]?.avg_map50 || 0),
            best_map50: parseFloat(results[4][0]?.best_map50 || 0)
        };

    } catch (error) {
        console.error('Failed to get database stats:', error);
        throw error;
    }
}

/**
 * Close database connection pool
 */
async function closePool() {
    try {
        await pool.end();
        console.log('Database connection pool closed');
    } catch (error) {
        console.error('Error closing database pool:', error);
    }
}

module.exports = {
    pool,
    testDatabaseConnection,
    executeQuery,
    executeTransaction,
    getDatabaseStats,
    closePool
};
