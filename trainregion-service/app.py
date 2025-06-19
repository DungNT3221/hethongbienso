from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import logging
import os
from config.config import engine, Base
from routes.dataset_routes import dataset_bp
from routes.training_routes import training_bp
from routes.model_routes import model_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """
    Create and configure Flask application
    """
    app = Flask(__name__)

    # Configure CORS - Allow all origins for debugging
    CORS(app, origins=['*'], methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")

    # Add request logging
    @app.before_request
    def log_request_info():
        from flask import request
        logger.info(f"Request: {request.method} {request.url}")
        if request.method == 'POST':
            logger.info(f"Request data: {request.get_data()}")

    # Register blueprints
    app.register_blueprint(dataset_bp, url_prefix='/api/dataset')
    app.register_blueprint(training_bp, url_prefix='/api/training')
    app.register_blueprint(model_bp, url_prefix='/api/model')

    # Static file serving for dataset images
    @app.route('/static/datasets/<path:filename>')
    def serve_dataset_files(filename):
        """Serve dataset images and files"""
        try:
            return send_from_directory('uploads', filename)
        except Exception as e:
            logger.error(f"Error serving file {filename}: {e}")
            return jsonify({'error': 'File not found'}), 404

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'trainregion-service',
            'version': '1.0.0'
        }), 200

    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'message': 'TrainRegion Service API',
            'version': '1.0.0',
            'endpoints': {
                'datasets': '/api/dataset',
                'training': '/api/training',
                'models': '/api/model',
                'health': '/health'
            }
        }), 200

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400

    return app

if __name__ == '__main__':
    # Tạo thư mục cần thiết
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('runs/train', exist_ok=True)
    os.makedirs('models', exist_ok=True)

    # Create app
    app = create_app()

    # Get configuration from environment
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 3003))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'

    logger.info(f"Starting TrainRegion Service on {host}:{port}")
    logger.info(f"Debug mode: {debug}")

    # Run app
    app.run(host=host, port=port, debug=debug)
