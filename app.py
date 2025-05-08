import os
from flask import Flask, render_template
from routes import predictions, scheduling
from routes.historical import historical_bp
from routes.devices import devices_bp
from routes.analytics import analytics_bp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
ROOT_PATH = os.getenv("ROOT_PATH")
DB_PATH = os.path.join(ROOT_PATH, "database", "database.db")

# Explicitly set the template folder
TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=TEMPLATES_PATH)

app.config['SECRET_KEY'] = 'energy_optimization_secret_key'
app.config['DB_PATH'] = DB_PATH

# Register blueprints
app.register_blueprint(predictions.bp)
app.register_blueprint(scheduling.bp)
app.register_blueprint(historical_bp)
app.register_blueprint(devices_bp)
app.register_blueprint(analytics_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


