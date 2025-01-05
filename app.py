from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from config import Config
from models import db
from routes import ticket_blueprint
import os

# Initialize the Flask app
app = Flask(__name__, static_folder="static")

# Enable CORS
CORS(app)

# Load configuration
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Register the blueprint for API routes
app.register_blueprint(ticket_blueprint)

# Serve the React app's main entry point
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

# Serve static files for React
@app.route("/<path:path>")
def serve_static_files(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad request"}), 400

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
