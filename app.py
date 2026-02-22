from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

# Import db and models
from models import db, User
from models import Admin, Room

# Create Flask app
app = Flask(__name__)

# Secret key for sessions
app.secret_key = "3de589839c19ab6e6540ad4d8c1856d7"

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with app
db.init_app(app)

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_password = generate_password_hash(request.form['password'])

        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()

        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect('/dashboard')

        return "Invalid credentials"

    return render_template('login.html')

# ---------------- ADMIN LOGIN ----------------
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """
    Handles admin login
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch admin from database
        admin = Admin.query.filter_by(username=username).first()

        # Simple password check (hashed can be added later)
        if admin and admin.password == password:
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            return redirect('/admin/dashboard')
        else:
            return "Invalid Admin Credentials"

    return render_template('admin_login.html')

# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    return render_template('dashboard.html', name=session['user_name'])

# ---------------- ADMIN DASHBOARD ----------------
@app.route('/admin/dashboard')
def admin_dashboard():
    """
    Admin dashboard (protected)
    """
    if 'admin_id' not in session:
        return redirect('/admin/login')

    return render_template('admin_dashboard.html')

# ---------------- ADMIN ADD-ROOM ----------------
@app.route('/admin/add-room', methods=['GET', 'POST'])
def add_room():
    """
    Admin can add new rooms
    """
    if 'admin_id' not in session:
        return redirect('/admin/login')

    if request.method == 'POST':
        room_type = request.form['room_type']
        price = request.form['price']

        new_room = Room(
            room_type=room_type,
            price=price,
            status="Available"
        )

        db.session.add(new_room)
        db.session.commit()

        return redirect('/admin/rooms')

    return render_template('add_room.html')

# ---------------- VIEW ALL ROOMS(ADMIN) ----------------
@app.route('/admin/rooms')
def view_rooms():
    """
    View all rooms
    """
    if 'admin_id' not in session:
        return redirect('/admin/login')

    rooms = Room.query.all()
    return render_template('view_rooms.html', rooms=rooms)

# ---------------- Update Room Status (Maintenance / Available) ----------------
@app.route('/admin/update-room/<int:room_id>')
def update_room_status(room_id):
    """
    Toggle room status
    """
    if 'admin_id' not in session:
        return redirect('/admin/login')

    room = Room.query.get(room_id)

    if room.status == "Available":
        room.status = "Maintenance"
    else:
        room.status = "Available"

    db.session.commit()
    return redirect('/admin/rooms')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------------- CREATE TABLES ----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)