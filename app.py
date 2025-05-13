from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
import mysql.connector
import logging
import subprocess
import json
from math import radians, sin, cos, sqrt, atan2
from flask import jsonify  
import os


app = Flask(__name__)
app.secret_key = 'root@123'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'scammersanju@gmail.com'
app.config['MAIL_PASSWORD'] = 'ec3enD1y'
app.config['MAIL_DEFAULT_SENDER'] = 'scammersanju@gmail.com'
# Add after app.secret_key
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',  # Allows cross-origin session sharing
    SESSION_COOKIE_SECURE=True      # If using HTTPS
)

# Add this before route definitions
from flask import session

@app.before_request
def make_session_permanent():
    session.permanent = True

mail = Mail(app)

# Replace with your actual MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "@Sampath2004",
    "database": "login_details",
    "autocommit": True  
}

@app.route('/run_script')
def run_script():
    if os.path.exists("detections.txt"):
        os.remove("detections.txt")
    subprocess.Popen(['python', 'backup.py'])
    return redirect(url_for('results'))

@app.route('/results')
def results():
    return render_template('results.html')


@app.route('/aboutus.html')
def about():
    return render_template("aboutus.html")

logging.basicConfig(level=logging.DEBUG)  # Use a proper logging configuration

def get_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve username and password from form data
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate that username and password were provided
        if not username or not password:
            error_message = "Please provide both username and password."
            return render_template('index2.html', error=error_message)

        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)

            # Ensure your query and table column names match exactly
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            cursor.close()
            connection.close()

            if user:
                # Store user info in session and redirect to home
                session['user'] = {'id': user['id'], 'username': user['username']}
                # Use redirect to ensure the session is properly updated
                return redirect(url_for('home'))
            else:
                error_message = ("Login failed. The username and password do not match. "
                                 "Don't have an account? <a href='/signup'>Register now</a>.")
                return render_template('index2.html', error=error_message)

        except mysql.connector.Error as err:
            logging.error("Error during login: %s", err)
            error_message = "An error occurred during login. Please try again."
            return render_template('index2.html', error=error_message)

    # For GET requests, render the login page (consistent template used)
    return render_template('index2.html')


@app.route('/home')
def home():
    return render_template('index2.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        logging.debug("Received signup POST request")
        username = request.form['username']
        password = request.form['password']
        confirmpass = request.form['confirmpass']  # Updated to match the HTML form
        email = request.form['email']
        phone = request.form['phone']

        # Check if passwords match
        if password != confirmpass:
            return render_template('signup.html', error="Passwords do not match. Please try again.")

        try:
            connection = get_connection()
            cursor = connection.cursor()

            # Check if the username already exists
            query_check = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query_check, (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                return render_template('signup.html', error="Username already exists. Please choose a different one.")

            # Replace 'users' with your actual table name
            query = "INSERT INTO users (username, password, email, phone) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (username, password, email, phone))
            connection.commit()
            logging.debug("Data committed to the database successfully")

            cursor.close()
            connection.close()

            # Redirect to login after successful signup
        except mysql.connector.Error as err:
            logging.error("Error during signup: %s", err)
            # Handle the case when the username is already taken
            return render_template('signup.html', error="An error occurred during signup. Please try again.")

    return render_template('signup.html')

def send_registration_email(user_email):
    subject = 'Welcome to Your Website'
    body = 'Thank you for registering on Your Website. We look forward to having you!'
    recipients = [user_email]

    message = Message(subject=subject, body=body, recipients=recipients)

    try:
        mail.send(message)
    except Exception as e:
        # Handle email sending errors
        print(f"Error sending email: {e}")

@app.route('/userservices', methods=['POST'])
def userservices():
    if request.method == 'POST':
        
        # Retrieve form data
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        phone_number = request.form['positiveNumber']
        address = request.form['address']
        battery = request.form['Battery']
        keyboard = request.form['Keyboard']
        microwave = request.form['Microwave']
        mobile = request.form['Mobile']
        washing_machine = request.form['Washing-Machine']
        mouse = request.form['Mouse']
        pcb = request.form['PCB']
        music_player = request.form['Music-Player']
        printer = request.form['Printer']
        television = request.form['Television']
        delivery_type = request.form['Type of delivery']
        card_number = request.form['Card-Number']
        cvv = request.form['CVV']
        

        try:
            connection = get_connection()
            cursor = connection.cursor()

            # Replace 'orders' with your actual table name
            query = """
                    INSERT INTO user_orders 
                    (first_name, last_name, email, phone_number, address, 
                    battery, keyboard, microwave, mobile, washing_machine, 
                    mouse, pcb, music_player, printer, television, 
                    delivery_type, card_number, cvv) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

            cursor.execute(query, (first_name, last_name, email, phone_number, address,
                                   battery, keyboard, microwave, mobile, washing_machine,
                                   mouse, pcb, music_player, printer, television,
                                   delivery_type, card_number, cvv))
            connection.commit()
            logging.debug("Data committed to the database successfully")
            

            cursor.close()
            connection.close()


        except mysql.connector.Error as err:
            logging.error("Error during form submission: %s", err)
            # Handle the case when there's an error during form submission
            return render_template('index2.html', error="An error occurred. Please try again.")

    return render_template('redirect.html')

def update_credits():
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Update 'credits' column with the product of each e-waste item and quantity
            update_query = """
                UPDATE user_orders
                SET credits = battery * 10 +
                              keyboard * 5 +
                              microwave * 10 +
                              mobile * 7 +
                              washing_machine * 20 +
                              mouse * 2 +
                              pcb * 2 +
                              music_player * 15 +
                              printer * 6 +
                              television * 25
            """
            cursor.execute(update_query)

            # Commit the changes
            connection.commit()

            print("Credits updated successfully!")

        finally:
            cursor.close()
            connection.close()
    else:
        print("Unable to connect to the database")

@app.route('/update_credits')
def flask_update_credits():
    update_credits()
    return "Credits updated successfully!"

@app.route('/success')

@app.route('/index2')
def index2():
    # Check if the user is logged in
    if 'user' in session:
        user = session['user']
        return render_template('index2.html', username=user['username'])

    return render_template('index2.html')
@app.route('/success')
def success():
    if 'user' in session:
        user = session['user']
        # You can render a success page or redirect to the main website
        return render_template('success.html', username=user['username'])
    else:
        # Redirect to login if the user is not in session
        return redirect(url_for('index'))
@app.route('/services')
def services():
    return render_template('services.html')
    # Your view logic here

@app.route('/location')
def location():
    # Your view logic goes here
    return render_template('location.html')

# @app.route('/redirect_page')
# def redirect_page():
#     return render_template('redirect.html')

# Add to existing imports
# import json
# from math import radians, sin, cos, sqrt, atan2
# @app.route('/detection_status')
# def detection_status():
#     return jsonify({
#         'detected': 'detected_items' in session,
#         'items': session.get('detected_items', [])
#     })
# # Add after existing routes
# @app.route('/detected_objects', methods=['POST'])
# def handle_detection():
#     # 1. Read JSON body
#     data = request.get_json(silent=True) or {}
#     detected_items = [item.lower().replace(" ", "_") for item in data.get('objects', [])]
#     session['detected_items'] = detected_items
#     session.modified = True 
#     session.permanent = True  # optional, makes the session last across browser restarts

#     # Debugging log
#     print(f"Detected items stored in session: {session.get('detected_items')}")
#     # 3. Return a pure 302 redirect so browsers will navigate there
#     return '', 302, {'Location': url_for('detection_results')}

# @app.route('/detection_results')
# def detection_results():
#     if 'detected_items' not in session:
#         return redirect(url_for('index2'))

#     items = session['detected_items']
#     credits = 0
#     credits_data = {}
#     error = None

#     try:
#         # 2. Connect and fetch credit values
#         conn = get_connection()
#         cur = conn.cursor(dictionary=True)

#         placeholders = ', '.join(['%s'] * len(items))
#         query = """
#             SELECT item_name, credit_value
#             FROM e_waste_items
#             WHERE item_name IN ({placeholders})
#         """
#         cur.execute(query % placeholders, items)
#         results = cur.fetchall()

#         # 3. Build a map and total
#         credits_data = {r['item_name']: r['credit_value'] for r in results}
#         credits = sum(credits_data.values())

#     except mysql.connector.Error as err:
#         error = f"Database error: {err}"
#         logging.error(error)

#     finally:
#         # 4. Clean up
#         if 'cur' in locals(): cur.close()
#         if 'conn' in locals(): conn.close()

#     # 5. Render your page with items, per-item credits, total credits, and any error
#     return render_template(
#         'detection_results.html',
#         items=items,
#         credits=credits,
#         credits_data=credits_data,
#         error=error
#     )


@app.route('/get_credits')
def get_credits():
    try:
        if not os.path.exists("detections.txt"):
            return jsonify({"status": "processing"})
        
        with open("detections.txt", "r") as f:
            items = [line.strip() for line in f.readlines()]
            
        credits_data = {}
        total = 0
        
        if items:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            placeholders = ', '.join(['%s'] * len(items))
            query = f"""
                SELECT item_name, credit_value 
                FROM e_waste_items 
                WHERE item_name IN ({placeholders})
            """
            cursor.execute(query, items)
            results = cursor.fetchall()
            credits_data = {row['item_name']: row['credit_value'] for row in results}
            total = sum(credits_data.values())
            
        return jsonify({
            "status": "ready",
            "items": items,
            "credits": credits_data,
            "total": total
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })
    
    
@app.route('/complete_payment')
def complete_payment():
    # Add actual payment processing logic here
    session.pop('detected_items', None)
    return redirect(url_for('shopping'))

@app.route('/shopping')
def shopping():
    return render_template('shopping.html')

if __name__ == '__main__':
    app.run(debug=True)