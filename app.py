from flask import Flask, render_template
from extensions import db

def create_app():
    """
    Application factory function
    """
    app = Flask(__name__)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database with app
    db.init_app(app)

    # Import models AFTER db initialization
    import models

    @app.route('/')
    def home():
        return render_template('index.html')

    return app


# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)