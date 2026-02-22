# Import Flask class from flask package
from flask import Flask, render_template

# Create Flask application instance
app = Flask(__name__)

# Route for home page
@app.route('/')
def home():
    """
    This function handles the home page request.
    It returns the index.html page from templates folder.
    """
    return render_template('index.html')

# Main driver function
if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)