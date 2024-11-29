from flask import Flask, render_template, request, session, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "your_secret_key"

# configure sql Alchemy to work with flask
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
"""to not track the database"""
app.config["SQLALCHEMY_TRACKMODIFICATIONS"] = False
db = SQLAlchemy(app)

# Database Model ~ Single Row in pur DataBase
class User(db.Model):
    # class Variable
    id = db.Column(db.Integer, primary_key=True)
    """ unique=true stand for that can't have this same username and the nullable=False stand for can't let it empty """
    username = db.Column(db.String(25), unique=True, nullable=False)
    password_hash = db.Column(db.String(151), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)



# Routes
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')
# Login route
@app.route("/login", methods=["POST"])
def login():
    # collect info from in the form
    username = request.form['username']
    password = request.form['password']
    """create the user"""
    user = User.query.filter_by(username=username).first()
     #check if its in the db
    if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    # otherwise show home page
    else:
        return render_template('index.html')
    

# Register route
@app.route("/register", methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("index.html", erro="you are already here!")
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('dashboard'))

# Dashboard route
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html", username=session['username'])
    return redirect(url_for('home'))
# Logout route
"""the idea here is just to remove the user from the session list"""
@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect(url_for('home'))



if __name__ in "__main__":
    """when you gonna run the code the database filse gonna create automaticly"""
    with app.app_context():
        db.create_all()
    app.run(debug=True)