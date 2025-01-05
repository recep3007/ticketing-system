from flask import Flask, jsonify, send_from_directory
from config import Config
from models import db
from routes import ticket_blueprint

app = Flask(__name__, static_folder="static")  # Ensure Flask serves static files

# Load the config
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Register the blueprint
app.register_blueprint(ticket_blueprint)

@app.route("/")
def home():
    return "Hello, Flask with a Config!"

# Route to serve React's index.html (if the build folder is present)
@app.route('/<path:path>')
def serve(path):
    return send_from_directory(app.static_folder, path)

# Error handler for resource not found
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify({"error": "Resource not found"}), 404

# Error handler for bad request
@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad request"}), 400

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)  # This will run the app locally in development
