import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mysql
import stripe
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from Backend.Database.db_connection import get_database_connection
from datetime import datetime, timedelta, date
import random
import hashlib
import time
import logging
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

# ---------- MAIL CONFIG ----------

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'youremail@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your_app_password'  # Use App Password if using Gmail

mail = Mail(app)
db = SQLAlchemy()


class OTP(db.Model):
    __tablename__ = 'otp_attempts'  # Change this to your actual table name
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    otp_hash = db.Column(db.String(255), nullable=False)
    otp_sent_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    otp_expiry_time = db.Column(db.TIMESTAMP, nullable=False)
    otp_attempts = db.Column(db.Integer, nullable=True, default=0)

    def __repr__(self):
        return f'<OTP for {self.email}>'


EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
SENDER_EMAIL = "bilaltalha0095@gmail.com"
SENDER_PASSWORD = "mwvv kmwm dghe mymp"


def send_email(recipient_email, otp):
    subject = "Your OTP for Verification"
    body = f"Your OTP is: {otp}"

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Setup the server connection
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")


# ---------- OTP CONFIGURATION ----------
OTP_EXPIRATION_TIME = 5  # OTP expires in 5 minutes
MAX_OTP_ATTEMPTS = 3  # Max 3 OTP requests in 15 minutes
OTP_ATTEMPT_RESET_TIME = 15  # Reset OTP attempt count after 15 minutes


# ---------- SEND OTP ----------

@app.route("/api/send-otp", methods=["POST"])
def send_otp():
    email = request.json.get("email")

    if not email:
        return jsonify({"error": "Email is required."}), 400

    # Validate email format
    email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.match(email_regex, email):
        return jsonify({"error": "Invalid email format."}), 400

    # Generate OTP (6 digits)
    otp = random.randint(100000, 999999)
    otp_hash = hashlib.sha256(str(otp).encode()).hexdigest()

    # Set OTP expiry time (15 minutes)
    otp_expiry_time = datetime.now() + timedelta(minutes=15)

    # Save OTP hash, expiry time, and attempt count in DB
    connection = get_database_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM otp_attempts WHERE email = %s", (email,))
        record = cursor.fetchone()

        if record:
            # Update OTP and expiration time
            cursor.execute("""
                UPDATE otp_attempts 
                SET otp_hash = %s, otp_expiry_time = %s, otp_attempts = 0 
                WHERE email = %s
            """, (otp_hash, otp_expiry_time, email))
        else:
            # Insert new OTP record for the user
            cursor.execute("""
                INSERT INTO otp_attempts (email, otp_hash, otp_sent_time, otp_expiry_time, otp_attempts)
                VALUES (%s, %s, %s, %s, %s)
            """, (email, otp_hash, datetime.now(), otp_expiry_time, 0))

        connection.commit()

        # Send OTP via email
        send_email(email, otp)

        return jsonify({"message": "OTP sent successfully."}), 200

    except mysql.connector.Error as db_error:
        print(f"Database error: {db_error}")
        connection.rollback()
        return jsonify({"error": f"Database error: {str(db_error)}"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        connection.rollback()
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    finally:
        cursor.close()
        connection.close()


# ---------- VERIFY OTP ----------

@app.route("/api/verify-otp", methods=["POST"])
def verify_otp():
    email = request.json.get("email")
    otp = request.json.get("otp")

    if not email or not otp:
        return jsonify({"error": "Email and OTP are required."}), 400

    # Validate email format
    email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.match(email_regex, email):
        return jsonify({"error": "Invalid email format."}), 400

    connection = get_database_connection()
    cursor = connection.cursor()

    try:
        # Fetch OTP details for the provided email
        cursor.execute("SELECT * FROM otp_attempts WHERE email = %s", (email,))
        record = cursor.fetchone()

        if not record:
            return jsonify({"error": "No OTP record found for this email."}), 404

        otp_hash = record[2]  # Stored OTP hash
        otp_expiry_time = record[4]  # Expiry time
        otp_attempts = record[5]  # OTP attempts counter

        # Check if OTP has expired
        if datetime.now() > otp_expiry_time:
            return jsonify({"error": "OTP has expired."}), 400

        # Hash the provided OTP and compare with stored hash
        otp_hash_input = hashlib.sha256(str(otp).encode()).hexdigest()

        if otp_hash_input != otp_hash:
            # Wrong OTP
            if otp_attempts + 1 >= 3:
                # If 3rd wrong attempt, delete record
                cursor.execute("DELETE FROM otp_attempts WHERE email = %s", (email,))
            else:
                # Otherwise, increment attempts
                cursor.execute("""
                    UPDATE otp_attempts 
                    SET otp_attempts = otp_attempts + 1 
                    WHERE email = %s
                """, (email,))
            connection.commit()
            return jsonify({"error": "Invalid OTP."}), 400

        # OTP is correct
        # Delete OTP record after successful verification
        cursor.execute("DELETE FROM otp_attempts WHERE email = %s", (email,))
        connection.commit()

        return jsonify({"message": "OTP verified successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# ---------- ATTENDANCE WITH FINE ----------
@app.route('/api/attendance', methods=['GET'])
def get_attendance_with_fine():
    try:
        roll_no = request.args.get('roll_no')
        if not roll_no:
            return jsonify({"error": "Missing roll_no"}), 400

        conn = get_database_connection()
        cursor = conn.cursor()

        # Step 1: Get student_id from roll number
        cursor.execute("SELECT student_id FROM student WHERE student_rollno = %s", (roll_no,))
        student_row = cursor.fetchone()
        if not student_row:
            return jsonify({"error": "Student not found"}), 404

        student_id = student_row[0]

        # Step 2: Get attendance records
        cursor.execute("""
            SELECT date, status FROM attendance
            WHERE student_id = %s
        """, (student_id,))
        attendance_records = cursor.fetchall()
        print("Raw Attendance:", attendance_records)

        if not attendance_records:
            return jsonify({
                "roll_no": roll_no,
                "total_days": 0,
                "present_days": 0,
                "percentage": 0,
                "fine": 500
            })

        # Parse records into datetime.date and filter only weekdays (Mon-Fri)
        parsed_attendance = []
        for date_obj, status in attendance_records:
            if isinstance(date_obj, datetime):
                date_only = date_obj.date()
            else:
                date_only = date_obj
            parsed_attendance.append((date_only, status))
        print("Parsed Attendance Records:", parsed_attendance)

        # Step 3: Fetch holidays
        cursor.execute("SELECT date FROM holidays")
        holiday_rows = cursor.fetchall()
        holidays = {row[0] for row in holiday_rows}
        print("Parsed Holidays:", holidays)

        # Step 4: Filter valid attendance days
        valid_attendance_days = [
            (date, status)
            for date, status in parsed_attendance
            if date.weekday() < 5 and date not in holidays
        ]
        print("Valid Attendance Records (Mon–Fri, not holidays):", valid_attendance_days)

        # Step 5: Calculate total and present
        total_days = len(valid_attendance_days)
        present_days = sum(1 for _, status in valid_attendance_days if status.lower() == "present")
        percentage = (present_days / total_days) * 100 if total_days > 0 else 0
        fine = 0 if percentage >= 75 else 500

        conn.close()

        return jsonify({
            "roll_no": roll_no,
            "total_days": total_days,
            "present_days": present_days,
            "percentage": round(percentage, 2),
            "fine": fine
        })

    except Exception as e:
        print("Server Error:", str(e))
        return jsonify({"error": str(e)}), 500


# ---------- STUDENT ATTENDANCE WITH PROFILE INFO ----------
@app.route('/api/student/attendance', methods=['GET', 'POST', 'OPTIONS'])
def get_student_attendance_with_profile():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204

    try:
        # Check if the email is provided either via query parameter or JSON body
        student_email = None

        if request.method == 'GET':
            student_email = request.args.get('email')
        elif request.method == 'POST':
            data = request.get_json()
            student_email = data.get('email') if data else None

        # Validate email
        if not student_email:
            return jsonify({"error": "Email is required"}), 400

        # Connect to the database
        conn = get_database_connection()
        cursor = conn.cursor()

        # Fetch student profile details using email
        cursor.execute("""
            SELECT student_id, Name, student_rollno, Student_email, Phone, Address
            FROM student
            WHERE Student_email = %s
        """, (student_email,))
        student_data = cursor.fetchone()

        # If student not found
        if not student_data:
            conn.close()
            return jsonify({"error": "No student found with this email."}), 404

        # Fetch attendance records for the found student
        student_id = student_data[0]
        cursor.execute("""
            SELECT date, status
            FROM attendance
            WHERE student_id = %s
            ORDER BY date DESC
        """, (student_id,))
        attendance_records = cursor.fetchall()

        # Close database connection
        conn.close()

        # Format the profile data
        student_profile = {
            "student_id": student_data[0],
            "name": student_data[1],
            "roll_no": student_data[2],
            "email": student_data[3],
            "phone": student_data[4],
            "address": student_data[5],
        }

        # Format the attendance data
        attendance_data = [
            {"date": str(record[0]), "status": record[1]}
            for record in attendance_records
        ]

        # Return profile and attendance
        return jsonify({
            "profile": student_profile,
            "attendance": attendance_data
        }), 200

    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": "An internal server error occurred."}), 500


# ---------- ADMIN LOGIN ----------
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Check username and password in the database
        conn = get_database_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM admin WHERE username = %s", (username,))
        admin = cursor.fetchone()

        if not admin or not check_password_hash(admin[2], password):
            return jsonify({"error": "Invalid credentials"}), 401

        conn.close()
        return jsonify({"message": "Login successful"})

    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ---------- ADMIN ATTENDANCE ----------
@app.route('/api/admin/attendance', methods=['GET'])
def get_attendance_for_admin():
    try:
        # Connect to the database
        conn = get_database_connection()
        cursor = conn.cursor()

        # Fetch all students and their attendance
        cursor.execute("""
            SELECT s.student_rollno, s.Name, a.date, a.status
            FROM attendance a
            JOIN student s ON a.student_id = s.student_id
            ORDER BY s.student_rollno, a.date
        """)

        # Fetch attendance records
        attendance_records = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Format the attendance data
        attendance_data = [
            {
                "student_rollno": record[0],
                "student_name": record[1],
                "date": str(record[2]),
                "status": record[3]
            }
            for record in attendance_records
        ]

        return jsonify(attendance_data)

    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ---------- HOLIDAYS ----------
@app.route('/api/add_holiday', methods=['POST'])
def add_holiday():
    try:
        data = request.json
        holiday_date = data.get('date')
        description = data.get('description', '')

        if not holiday_date:
            return jsonify({"error": "Date is required"}), 400

        conn = get_database_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO holidays (date, description) VALUES (%s, %s)", (holiday_date, description))
        conn.commit()
        conn.close()

        return jsonify({"message": "Holiday added successfully"}), 201

    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/get_holidays', methods=['GET'])
def get_holidays():
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, description FROM holidays ORDER BY date")
        holidays = cursor.fetchall()
        conn.close()

        return jsonify([{"id": h[0], "date": str(h[1]), "description": h[2]} for h in holidays])
    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/delete_holidays/<int:holiday_id>', methods=['DELETE'])
def delete_holiday(holiday_id):
    try:
        # Connect to the database
        conn = get_database_connection()
        cursor = conn.cursor()

        # Check if the holiday exists
        cursor.execute("SELECT * FROM holidays WHERE id = %s", (holiday_id,))
        holiday = cursor.fetchone()

        if not holiday:
            return jsonify({"error": "Holiday not found"}), 404

        # Delete the holiday
        cursor.execute("DELETE FROM holidays WHERE id = %s", (holiday_id,))
        conn.commit()

        # Close the connection
        conn.close()

        return jsonify({"message": "Holiday deleted successfully"})
    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ---------- STRIPE CHECKOUT ----------
@app.route('/api/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.get_json()
        amount = data.get('amount', 0)

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(amount) * 100,
                    'product_data': {
                        'name': 'Attendance Fine Payment',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:5173/success',
            cancel_url='http://localhost:5173/cancel',
        )

        return jsonify({'url': session.url})
    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = request.json
        amount = data.get('amount')  # e.g., 500 for ₹500
        currency = data.get('currency', 'inr')
        if not amount:
            return jsonify({'error': 'Amount is required'}), 400

        intent = stripe.PaymentIntent.create(
            amount=amount * 100,  # Stripe accepts amounts in the smallest currency unit
            currency=currency,
            automatic_payment_methods={"enabled": True},
        )

        return jsonify({'clientSecret': intent['client_secret']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('stripe-signature')
    endpoint_secret = 'your_stripe_webhook_secret'

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except stripe.error.SignatureVerificationError as e:
        return jsonify({'error': 'Invalid signature'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Save payment_intent.id and metadata (like roll number) in DB here if needed

    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(debug=True)
