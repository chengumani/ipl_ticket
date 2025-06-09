
from flask import Flask, render_template, request, redirect,flash,session,url_for
import mysql.connector

from datetime import datetime
import MySQLdb


app = Flask(__name__)
app.secret_key = '1234'

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ipl_ticket_booking"
    
)



# --- Main Index Route ---
@app.route('/')
def index():
    return render_template('index.html')



# (You already have /admin_login and /login implemented)

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        if cursor.fetchone():
            flash("Email already registered. Please login.")
            return redirect('/register')  # Stay on registration page to show message

        cursor.execute("INSERT INTO user (name, phone, email, password) VALUES (%s, %s, %s, %s)",
                       (name, phone, email, password))
        db.commit()
        flash("Registered successfully. Please login.")
        return redirect('/login')
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]     # userid
            session['user_name'] = user[1]   # name
            session['phone']=user[2]
            session['email'] = user[3]       # ✅ Save email in session
            
            return redirect('/dashboard')
        else:
            flash("Invalid email or password.")
            return redirect('/login')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', username=session['user_name'])
    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/users')
def users():
    cursor = db.cursor()
    cursor.execute("SELECT userid, name, phone, email FROM user")
    users = cursor.fetchall()
    return render_template('users.html', users=users)



    
# Hardcoded single admin credentials
ADMIN_EMAIL = 'admin@gmail.com'
ADMIN_PASSWORD = 'admin123'

#@app.route('/')
#def home():
 #   return redirect('/admin_login')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['admin'] = email
            return redirect('/admin_dashboard')
        else:
            flash('Invalid email or password.')
            return redirect('/admin_login')
    
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' in session:
        return render_template('admin_dashboard.html', admin_email=session['admin'])
    else:
        return redirect('/admin_login')

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin', None)
    return redirect('/admin_login')




@app.route('/add_team', methods=['GET', 'POST'])
def add_team():
    if request.method == 'POST':
        name = request.form['name']
        captain = request.form['captain']
        coach = request.form['coach']

        cursor = db.cursor()

        # Check if team already exists
        cursor.execute("SELECT * FROM teams WHERE name = %s", (name,))
        existing_team = cursor.fetchone()

        if existing_team:
            flash("Team already exists", "error")
        else:
            query = "INSERT INTO teams (name, captain, coach) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, captain, coach))
            db.commit()
            flash("Team added successfully", "success")

        cursor.close()
        return render_template('add_team.html')

    return render_template('add_team.html')


@app.route('/teams')
def view_teams():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM teams")
    teams = cursor.fetchall()
    cursor.close()
    return render_template('teams.html', teams=teams)


# @app.route('/add_team', methods=['GET', 'POST'])
# def add_team():
#     if request.method == 'POST':
#         name = request.form['name']
#         captain = request.form['captain']
#         coach = request.form['coach']

#         cursor = db.cursor()
#         query = "INSERT INTO teams (name, captain, coach) VALUES (%s, %s, %s)"
#         cursor.execute(query, (name, captain, coach))
#         db.commit()
#         cursor.close()
#         return redirect('/teams')
#     return render_template('add_team.html')

# @app.route('/teams')
# def view_teams():
#     cursor = db.cursor()
#     cursor.execute("SELECT * FROM teams")
#     teams = cursor.fetchall()
#     cursor.close()
#     return render_template('teams.html', teams=teams)






@app.route('/add_stadium', methods=['GET', 'POST'])
def add_stadium():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        capacity = request.form['capacity']

        cursor = db.cursor()

        # Check if stadium name already exists
        cursor.execute("SELECT * FROM stadium WHERE name = %s", (name,))
        existing = cursor.fetchone()

        if existing:
            flash("Stadium name already exists", "error")
        else:
            query = "INSERT INTO stadium (name, location, capacity) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, location, capacity))
            db.commit()
            flash("Stadium added successfully", "success")

        cursor.close()
        return render_template('add_stadium.html')

    return render_template('add_stadium.html')

@app.route('/view_stadiums')
def view_stadiums():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM stadium")
    stadiums = cursor.fetchall()
    cursor.close()
    return render_template('view_stadiums.html', stadiums=stadiums)



# @app.route('/add_stadium', methods=['GET', 'POST'])
# def add_stadium():
#     if request.method == 'POST':
#         name = request.form['name']
#         location = request.form['location']
#         capacity = request.form['capacity']

#         cursor = db.cursor()
#         query = "INSERT INTO stadium (name, location, capacity) VALUES (%s, %s, %s)"
#         cursor.execute(query, (name, location, capacity))
#         db.commit()
#         cursor.close()
#         return redirect('/stadiums')
#     return render_template('add_stadium.html')

# @app.route('/stadiums')
# def view_stadiums():
#     cursor = db.cursor()
#     cursor.execute("SELECT * FROM stadium")
#     stadiums = cursor.fetchall()
#     cursor.close()
#     return render_template('view_stadiums.html', stadiums=stadiums)







# @app.route('/add_match', methods=['GET', 'POST'])
# def add_match():
#     cursor = db.cursor()

#     # Get team and stadium list for dropdowns
#     cursor.execute("SELECT teamid, name FROM teams")
#     teams = cursor.fetchall()

#     cursor.execute("SELECT stadiumid, name FROM stadium")
#     stadiums = cursor.fetchall()

#     if request.method == 'POST':
#         team1 = request.form['team1']
#         team2 = request.form['team2']
#         match_date = request.form['match_date']
#         stadiumid = request.form['stadium']

#         if team1 == team2:
#             return "Error: Teams must be different."

#         query = "INSERT INTO matches (team1_id, team2_id, match_date, stadiumid) VALUES (%s, %s, %s, %s)"
#         cursor.execute(query, (team1, team2, match_date, stadiumid))
#         db.commit()
#         return redirect('/matches')

#     return render_template('add_match.html', teams=teams, stadiums=stadiums)

# @app.route('/matches')
# def view_matches():
#     cursor = db.cursor()
#     cursor.execute("""
#         SELECT m.matchid, t1.name, t2.name, m.match_date, s.name
#         FROM matches m
#         JOIN teams t1 ON m.team1_id = t1.teamid
#         JOIN teams t2 ON m.team2_id = t2.teamid
#         JOIN stadium s ON m.stadiumid = s.stadiumid
#     """)
#     matches = cursor.fetchall()
#     return render_template('view_matches.html', matches=matches)


@app.route('/add_match', methods=['GET', 'POST'])
def add_match():
    cursor = db.cursor()

    # Fetch teams and stadiums for dropdowns
    cursor.execute("SELECT teamid, name FROM teams")
    teams = cursor.fetchall()

    cursor.execute("SELECT stadiumid, name FROM stadium")
    stadiums = cursor.fetchall()

    if request.method == 'POST':
        team1 = request.form['team1']
        team2 = request.form['team2']
        match_date = request.form['match_date']
        stadiumid = request.form['stadium']

        # Validation: Teams must be different
        if team1 == team2:
            flash("Error: Teams must be different.", "error")
            return render_template('add_match.html', teams=teams, stadiums=stadiums)

        # Insert match
        query = "INSERT INTO matches (team1_id, team2_id, match_date, stadiumid) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (team1, team2, match_date, stadiumid))
        db.commit()

        flash("Match added successfully.", "success")
        return redirect('/add_match')

    return render_template('add_match.html', teams=teams, stadiums=stadiums)

@app.route('/view_matches')
def view_matches():
    cursor = db.cursor()
    cursor.execute("""
        SELECT m.matchid, t1.name, t2.name, m.match_date, s.name
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.teamid
        JOIN teams t2 ON m.team2_id = t2.teamid
        JOIN stadium s ON m.stadiumid = s.stadiumid
    """)
    matches = cursor.fetchall()
    return render_template('view_matches.html', matches=matches)



# @app.route('/add_ticket', methods=['GET', 'POST'])
# def add_ticket():
#     cursor = db.cursor()
#     cursor.execute("SELECT userid, name FROM user")
#     users = cursor.fetchall()

#     cursor.execute("""
#         SELECT m.matchid, t1.name, t2.name, m.match_date 
#         FROM matches m 
#         JOIN teams t1 ON m.team1_id = t1.teamid 
#         JOIN teams t2 ON m.team2_id = t2.teamid
#     """)
#     matches = cursor.fetchall()

#     if request.method == 'POST':
#         userid = request.form['userid']
#         matchid = request.form['matchid']
#         seat_no = request.form['seat_no']
#         price = request.form['price']

#         cursor.execute(
#             "INSERT INTO ticket (userid, matchid, seat_no, price) VALUES (%s, %s, %s, %s)",
#             (userid, matchid, seat_no, price)
#         )
#         db.commit()
#         return redirect('/tickets')

#     return render_template('add_ticket.html', users=users, matches=matches)

# @app.route('/tickets')
# def view_tickets():
#     cursor = db.cursor()
#     cursor.execute("""
#         SELECT t.ticketid, u.name, CONCAT(tm1.name, ' vs ', tm2.name), m.match_date, t.seat_no, t.price
#         FROM ticket t
#         JOIN user u ON t.userid = u.userid
#         JOIN matches m ON t.matchid = m.matchid
#         JOIN teams tm1 ON m.team1_id = tm1.teamid
#         JOIN teams tm2 ON m.team2_id = tm2.teamid
#     """)
#     tickets = cursor.fetchall()
#     return render_template('view_tickets.html', tickets=tickets)



# @app.route('/add_ticket', methods=['GET', 'POST'])
# def add_ticket():
#     cursor = db.cursor()
#     if request.method == 'POST':
#         matchid = request.form['matchid']
#         seat_no = request.form['seat_no']
#         price = request.form['price']

#         cursor.execute("INSERT INTO ticket (matchid, seat_no, price) VALUES (%s, %s, %s)", (matchid, seat_no, price))
#         db.commit()
#         flash("Ticket added successfully!", "success")
#         return redirect('/add_ticket')

#     # Fetch match info
#     cursor.execute("""SELECT m.matchid, t1.name, t2.name, m.match_date 
#                       FROM matches m 
#                       JOIN teams t1 ON m.team1_id = t1.teamid 
#                       JOIN teams t2 ON m.team2_id = t2.teamid""")
#     matches = cursor.fetchall()
#     return render_template('add_ticket.html', matches=matches)



@app.route('/add_ticket', methods=['GET', 'POST'])
def add_ticket():
    cursor = db.cursor()
    if request.method == 'POST':
        matchid = request.form['matchid']
        seat_no = request.form['seat_no']
        price = request.form['price']

        try:
            cursor.execute("INSERT INTO ticket (matchid, seat_no, price) VALUES (%s, %s, %s)", (matchid, seat_no, price))
            db.commit()
            flash("Ticket added successfully!", "success")
        except Exception as e:
            db.rollback()
            flash("Failed to add ticket.", "error")
            print(f"Error: {e}")

    cursor.execute("""
        SELECT m.matchid, t1.name, t2.name, m.match_date 
        FROM matches m 
        JOIN teams t1 ON m.team1_id = t1.teamid 
        JOIN teams t2 ON m.team2_id = t2.teamid
    """)
    matches = cursor.fetchall()
    return render_template('add_ticket.html', matches=matches)



@app.route('/view_tickets')
def view_tickets():
    cursor = db.cursor()
    cursor.execute("""SELECT t.ticketid, team1.name, team2.name, m.match_date, t.seat_no, t.price 
                      FROM ticket t
                      JOIN matches m ON t.matchid = m.matchid
                      JOIN teams team1 ON m.team1_id = team1.teamid
                      JOIN teams team2 ON m.team2_id = team2.teamid""")
    tickets = cursor.fetchall()
    return render_template('view_tickets.html', tickets=tickets)


@app.route('/buy_ticket/<int:ticketid>', methods=['GET', 'POST'])
def buy_ticket(ticketid):
    if 'email' not in session:
        return redirect('/login')

    email = session['email']
    cursor = db.cursor()

    # Fetch user details
    cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
    user = cursor.fetchone()
    if not user:
        return "User not found", 404

    # Fetch detailed ticket + match + team info
    cursor.execute("""
        SELECT t.ticketid, t.seat_no, t.price,
               m.matchid, m.match_date,
               team1.name AS team1_name,
               team2.name AS team2_name
        FROM ticket t
        JOIN matches m ON t.matchid = m.matchid
        JOIN teams team1 ON m.team1_id = team1.teamid
        JOIN teams team2 ON m.team2_id = team2.teamid
        WHERE t.ticketid = %s
    """, (ticketid,))
    ticket = cursor.fetchone()
    if not ticket:
        return "Ticket not found", 404

    # Handle booking
    if request.method == 'POST':
        payment_status = request.form['payment_status']
        cursor.execute(
            "INSERT INTO payment (userid, ticketid, payment_status) VALUES (%s, %s, %s)",
            (user[0], ticket[0], payment_status)
        )
        db.commit()
        return "<h2 style='text-align:center; color:green;'>Ticket Booked Successfully!</h2><br><center><a href='/view_tickets'>Back to Tickets</a></center>"

    return render_template("buy_ticket.html", user=user, ticket=ticket)


# @app.route('/buy_ticket/<int:ticketid>', methods=['GET', 'POST'])
# def buy_ticket(ticketid):
#     cursor = db.cursor()

#     # Get the current user's ID from session (already set at login)
#     userid = session['userid']  # No need to check login

#     # Fetch user details from 'user' table
#     cursor.execute("SELECT userid, name, phone, email FROM user WHERE userid = %s", (userid,))
#     user = cursor.fetchone()

#     # Fetch ticket details
#     cursor.execute("""
#         SELECT t.ticketid, team1.name, team2.name, m.match_date, t.seat_no, t.price 
#         FROM ticket t
#         JOIN matches m ON t.matchid = m.matchid
#         JOIN teams team1 ON m.team1_id = team1.teamid
#         JOIN teams team2 ON m.team2_id = team2.teamid
#         WHERE t.ticketid = %s
#     """, (ticketid,))
#     ticket = cursor.fetchone()

#     if request.method == 'POST':
#         payment_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#         # Insert payment info
#         cursor.execute("""
#             INSERT INTO payment (userid, ticketid, payment_date, payment_status)
#             VALUES (%s, %s, %s, %s)
#         """, (userid, ticketid, payment_date, 'Success'))
#         db.commit()

#         flash("Payment successful and ticket booked!", "success")
#         return redirect('/view_tickets')  # Redirect to booked tickets page

#     return render_template('buy_ticket.html', ticket=ticket, user=user)



if __name__ == '__main__':
    app.run(debug=True)



