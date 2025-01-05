from flask import Flask
from config import Config
from models import db
from routes import ticket_blueprint

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Register the blueprint
app.register_blueprint(ticket_blueprint)

@app.route("/")
def home():
    return "Hello, Flask with a Config!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)
