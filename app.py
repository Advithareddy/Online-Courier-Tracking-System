from flask import Flask, render_template, request, redirect, url_for, session
from database import create_tables
import sqlite3
import uuid

app = Flask(__name__)

# Secret key for sessions
app.secret_key = "online-courier-secret-key"

# Create database tables
create_tables()


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("database/courier.db")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE email = ? AND password = ?
        """, (email, password))

        user = cursor.fetchone()

        connection.close()

        if user:

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]

            return redirect(url_for("dashboard"))

        else:

            return render_template(
                "login.html",
                error="Invalid email or password!"
            )

    return render_template("login.html")
@app.route("/driver-login", methods=["GET", "POST"])
def driver_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("database/courier.db")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM drivers
            WHERE email = ? AND password = ?
        """, (email, password))

        driver = cursor.fetchone()

        connection.close()

        if driver:
            # Store driver information in session
            session["driver_id"] = driver["id"]
            session["driver_name"] = driver["name"]
            session["driver_email"] = driver["email"]

            return redirect(url_for("driver_dashboard"))

        else:
            return render_template(
                "driver_login.html",
                error="Invalid driver email or password!"
            )

    return render_template("driver_login.html")
@app.route("/driver-dashboard")
def driver_dashboard():

    if "driver_id" not in session:
        return redirect(url_for("driver_login"))

    driver_id = session["driver_id"]

    connection = sqlite3.connect("database/courier.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM drivers
        WHERE id = ?
    """, (driver_id,))

    driver = cursor.fetchone()

    cursor.execute("""
        SELECT *
        FROM couriers
        WHERE driver_id = ?
        ORDER BY rowid DESC
    """, (driver_id,))

    couriers = cursor.fetchall()

    connection.close()

    return render_template(
        "driver_dashboard.html",
        driver=driver,
        couriers=couriers
    )


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        try:

            connection = sqlite3.connect("database/courier.db")
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO users
                (name, email, password)
                VALUES (?, ?, ?)
            """, (name, email, password))

            connection.commit()
            connection.close()

            return render_template(
                "register.html",
                success="Registration successful! You can now login."
            )

        except sqlite3.IntegrityError:

            return render_template(
                "register.html",
                error="Email already registered!"
            )

    return render_template("register.html")


# =========================================================
# USER DASHBOARD
# =========================================================

# =========================================================
# USER DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("database/courier.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Get all courier bookings
    cursor.execute("""
        SELECT *
        FROM couriers
        ORDER BY rowid DESC
    """)

    couriers = cursor.fetchall()

    connection.close()

    return render_template(
        "dashboard.html",
        couriers=couriers
    )

# =========================================================
# BOOK COURIER
# =========================================================

@app.route("/book-courier", methods=["GET", "POST"])
def book_courier():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        sender_name = request.form["sender_name"]
        sender_phone = request.form["sender_phone"]

        receiver_name = request.form["receiver_name"]
        receiver_phone = request.form["receiver_phone"]

        pickup_address = request.form["pickup_address"]
        delivery_address = request.form["delivery_address"]

        package_type = request.form["package_type"]
        weight = request.form["weight"]

        # Generate unique tracking ID
        tracking_id = "CT" + uuid.uuid4().hex[:8].upper()

        connection = sqlite3.connect("database/courier.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO couriers (
                tracking_id,
                sender_name,
                sender_phone,
                receiver_name,
                receiver_phone,
                pickup_address,
                delivery_address,
                package_type,
                weight,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tracking_id,
            sender_name,
            sender_phone,
            receiver_name,
            receiver_phone,
            pickup_address,
            delivery_address,
            package_type,
            weight,
            "Booked"
        ))

        connection.commit()
        connection.close()

        # Open courier details page
        return redirect(
            url_for(
                "courier_details",
                tracking_id=tracking_id
            )
        )

    return render_template("book_courier.html")


# =========================================================
# COURIER DETAILS
# =========================================================

@app.route("/courier-details")
def courier_details():

    # Allow both normal users and admin
    if "user_id" not in session and not session.get("admin_logged_in"):
        return redirect(url_for("login"))

    tracking_id = request.args.get("tracking_id")

    if not tracking_id:
        return redirect(url_for("dashboard"))

    connection = sqlite3.connect("database/courier.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM couriers
        WHERE tracking_id = ?
    """, (tracking_id,))

    courier = cursor.fetchone()

    connection.close()

    if not courier:

        return render_template(
            "error.html",
            message="Courier not found!"
        )

    return render_template(
        "courier_details.html",
        courier=courier
    )


# =========================================================
# TRACK COURIER
# =========================================================

@app.route("/track-courier", methods=["GET", "POST"])
def track_courier():

    courier = None
    error = None

    if request.method == "POST":

        tracking_id = request.form["tracking_id"].strip().upper()

        connection = sqlite3.connect("database/courier.db")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM couriers
            WHERE tracking_id = ?
        """, (tracking_id,))

        courier = cursor.fetchone()

        connection.close()

        if not courier:

            error = "Courier not found. Please check your tracking ID."

    return render_template(
        "track_courier.html",
        courier=courier,
        error=error
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        # Admin credentials
        if email == "admin@gmail.com" and password == "admin123":

            session["admin_logged_in"] = True

            return redirect(url_for("admin_dashboard"))

        else:

            return render_template(
                "admin_login.html",
                error="Invalid admin email or password!"
            )

    return render_template("admin_login.html")

@app.route("/add-driver", methods=["GET", "POST"])
def add_driver():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["password"]
        vehicle_number = request.form["vehicle_number"]

        connection = sqlite3.connect("database/courier.db")
        cursor = connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO drivers (
                    name,
                    phone,
                    email,
                    password,
                    vehicle_number
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                name,
                phone,
                email,
                password,
                vehicle_number
            ))

            connection.commit()
            connection.close()

            return render_template(
                "add_driver.html",
                success="Driver added successfully!"
            )

        except sqlite3.IntegrityError:
            connection.close()

            return render_template(
                "add_driver.html",
                error="Driver email already exists!"
            )

    return render_template("add_driver.html")

@app.route("/edit-driver/<int:driver_id>", methods=["GET", "POST"])
def edit_driver(driver_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    connection = sqlite3.connect("database/courier.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Get driver
    cursor.execute("""
        SELECT *
        FROM drivers
        WHERE id = ?
    """, (driver_id,))

    driver = cursor.fetchone()

    if not driver:
        connection.close()
        return render_template(
            "error.html",
            message="Driver not found!"
        )

    # Update driver
    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["password"]
        vehicle_number = request.form["vehicle_number"]

        try:

            cursor.execute("""
                UPDATE drivers
                SET name = ?,
                    phone = ?,
                    email = ?,
                    password = ?,
                    vehicle_number = ?
                WHERE id = ?
            """, (
                name,
                phone,
                email,
                password,
                vehicle_number,
                driver_id
            ))

            connection.commit()
            connection.close()

            return redirect(url_for("admin_dashboard"))

        except sqlite3.IntegrityError:

            connection.close()

            return render_template(
                "edit_driver.html",
                driver=driver,
                error="Email already belongs to another driver!"
            )

    connection.close()

    return render_template(
        "edit_driver.html",
        driver=driver
    )
@app.route("/admin-dashboard")
def admin_dashboard():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    connection = sqlite3.connect("database/courier.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Get all couriers
    cursor.execute("""
        SELECT
            couriers.*,
            drivers.name AS driver_name,
            drivers.vehicle_number AS driver_vehicle
        FROM couriers
        LEFT JOIN drivers
        ON couriers.driver_id = drivers.id
        ORDER BY couriers.rowid DESC
    """)

    couriers = cursor.fetchall()

    # Get all drivers
    cursor.execute("""
        SELECT *
        FROM drivers
        ORDER BY id DESC
    """)

    drivers = cursor.fetchall()

    connection.close()

    return render_template(
        "admin_dashboard.html",
        couriers=couriers,
        drivers=drivers
    )
# =========================================================
# ADMIN UPDATE COURIER STATUS
# =========================================================

@app.route("/update-status", methods=["POST"])
def update_status():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    tracking_id = request.form["tracking_id"]
    status = request.form["status"]

    connection = sqlite3.connect(
        "database/courier.db"
    )

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE couriers
        SET status = ?
        WHERE tracking_id = ?
    """, (
        status,
        tracking_id
    ))

    connection.commit()
    connection.close()

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# UPDATE COURIER STATUS
# =========================================================

@app.route("/driver-update-status", methods=["POST"])
def driver_update_status():

    if "driver_id" not in session:
        return redirect(url_for("driver_login"))

    driver_id = session["driver_id"]

    tracking_id = request.form["tracking_id"]
    status = request.form["status"]

    connection = sqlite3.connect("database/courier.db")
    cursor = connection.cursor()

    # Update only if this courier belongs to the logged-in driver
    cursor.execute("""
        UPDATE couriers
        SET status = ?
        WHERE tracking_id = ?
        AND driver_id = ?
    """, (
        status,
        tracking_id,
        driver_id
    ))

    connection.commit()

    updated = cursor.rowcount

    connection.close()

    if updated == 0:
        return "Unauthorized courier or tracking ID", 403

    return redirect(url_for("driver_dashboard"))
@app.route("/assign-driver", methods=["POST"])
def assign_driver():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    tracking_id = request.form["tracking_id"]
    driver_id = request.form["driver_id"]

    connection = sqlite3.connect("database/courier.db")
    cursor = connection.cursor()

    # Assign driver to courier
    cursor.execute("""
        UPDATE couriers
        SET driver_id = ?
        WHERE tracking_id = ?
    """, (
        driver_id,
        tracking_id
    ))

    connection.commit()
    connection.close()

    return redirect(url_for("admin_dashboard"))


@app.route("/update-location", methods=["POST"])
def update_location():

    # Allow logged-in user or admin
    if "user_id" not in session and not session.get("admin_logged_in"):
        return {
            "success": False,
            "message": "Unauthorized"
        }, 401

    # Get JSON data from driver_tracking.html
    data = request.get_json(silent=True)

    if data:
        tracking_id = str(
            data.get("tracking_id", "")
        ).strip().upper()

        latitude = data.get("latitude")
        longitude = data.get("longitude")

    else:
        # Also support the old admin form
        tracking_id = request.form.get(
            "tracking_id", ""
        ).strip().upper()

        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

    # Check required data
    if not tracking_id or latitude is None or longitude is None:
        return {
            "success": False,
            "message": "Missing GPS data"
        }, 400

    # Convert coordinates to numbers
    try:
        latitude = float(latitude)
        longitude = float(longitude)

    except (TypeError, ValueError):
        return {
            "success": False,
            "message": "Invalid coordinates"
        }, 400

    # Validate latitude
    if latitude < -90 or latitude > 90:
        return {
            "success": False,
            "message": "Invalid latitude"
        }, 400

    # Validate longitude
    if longitude < -180 or longitude > 180:
        return {
            "success": False,
            "message": "Invalid longitude"
        }, 400

    # Update database
    connection = sqlite3.connect(
        "database/courier.db"
    )

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE couriers
        SET latitude = ?,
            longitude = ?
        WHERE tracking_id = ?
    """, (
        latitude,
        longitude,
        tracking_id
    ))

    connection.commit()

    updated = cursor.rowcount

    connection.close()

    # Tracking ID does not exist
    if updated == 0:
        return {
            "success": False,
            "message": "Tracking ID not found"
        }, 404

    # Response for JavaScript
    if data:
        return {
            "success": True,
            "message": "Location updated successfully"
        }

    # Response for old admin form
    return redirect(url_for("admin_dashboard"))
@app.route("/get-location")
def get_location():

    tracking_id = request.args.get(
        "tracking_id",
        ""
    ).strip().upper()

    if not tracking_id:
        return {
            "success": False,
            "message": "Tracking ID is required"
        }, 400

    connection = sqlite3.connect(
        "database/courier.db"
    )

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT latitude, longitude, status
        FROM couriers
        WHERE tracking_id = ?
    """, (tracking_id,))

    courier = cursor.fetchone()

    connection.close()

    if not courier:
        return {
            "success": False,
            "message": "Tracking ID not found"
        }, 404

    return {
        "success": True,
        "latitude": courier["latitude"],
        "longitude": courier["longitude"],
        "status": courier["status"]
    }


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin-logout")
def admin_logout():

    session.pop("admin_logged_in", None)

    return redirect(url_for("admin_login"))

@app.route("/driver-tracking")
def driver_tracking():

    # Allow driver login
    if "driver_id" not in session:
        return redirect(url_for("driver_login"))

    tracking_id = request.args.get("tracking_id", "")

    return render_template(
        "driver_tracking.html",
        tracking_id=tracking_id
    )

    return render_template("driver_tracking.html")

@app.route("/driver-logout")
def driver_logout():

    session.pop("driver_id", None)
    session.pop("driver_name", None)
    session.pop("driver_email", None)

    return redirect(url_for("driver_login"))
# =========================================================
# USER LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================================================
# 404 ERROR
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template("error.html"), 404


# =========================================================
# RUN FLASK APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )