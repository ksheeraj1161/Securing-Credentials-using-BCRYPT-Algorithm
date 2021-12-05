from flask import Flask, render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
import re

app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'
bcrypt = Bcrypt(app)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("register.html")

@app.route("/")
def index():
    valid=checklogin()
    if valid :
       return render_template("index.html")
    else :
       return redirect('/login')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

@app.route("/signup", methods=["POST"])
def registration():
    is_valid = True
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("<div class='ohno'>Please enter valid email</div>")
    if not NAME_REGEX.match(request.form['first_name']):
        is_valid = False
        flash("<div class='ohno'>First name must contain only letters</div>")
    if len(request.form['first_name']) < 2:
        is_valid = False
        flash("<div class='ohno'>First name must contain at least two letters</div>")
    if not NAME_REGEX.match(request.form['last_name']):
        is_valid = False
        flash("<div class='ohno'>Last name must contain only letters</div>")
    if len(request.form['last_name']) < 2:
        is_valid = False
        flash("<div class='ohno'>Last name must contain at least two letters</div>")
    
    if len(request.form['password']) < 8:
        is_valid = False
        flash("<div class='ohno'>Password must be between 8-15 characters</div>")
    if len(request.form['password']) > 15:
        is_valid = False
        flash("<div class='ohno'>Password must be between 8-15 characters</div>")
    if request.form['confirmpassword'] != request.form['password']:
        is_valid = False
        flash("<div class='ohno'>Passwords must match</div>")
    if is_valid == False:
        return redirect('/signup')
    else:
     
        pw_hash = bcrypt.generate_password_hash(request.form['password'])  
        mysql = connectToMySQL("login")
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password_hash": pw_hash,
        }
        querynow = "SELECT * FROM accounts WHERE email= %(email)s"
        result=mysql.query_db(querynow, data)
        if len(result):
            flash("<div class='ohno'>Email alredy exist </div>") 
            return redirect('/signup')
        else:
            mysql = connectToMySQL("login")
            query = "INSERT INTO accounts (firstname, lastname, email, password, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s, %(email)s, %(password_hash)s, NOW(), NOW());"
            new_user_id = mysql.query_db(query, data)
            session["email"]=request.form["email"]
            session['lastname'] = request.form['last_name']
            session['firstname'] = request.form['first_name']
            return redirect('/')


@app.route("/login", methods=['POST'])
def loginup():
    mysql = connectToMySQL("login")
    # we should have some logic to prevent duplicates of usernames when we create account
    query ="SELECT * FROM accounts WHERE email=%(email)s;"
    data ={
        "email": request.form["email"]
    }
    result=mysql.query_db(query, data)
    if len(result):
        # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            # if we get True after checking the password, we may put the user id in session
            session['email'] = result[0]['email']
            session['lastname'] = result[0]['lastname']
            session['firstname'] = result[0]['firstname']
            return redirect('/')
        else:
            flash("<div class='ohno'>Username or Password do not match</div>") 
            return redirect('/login')
    else:
        flash("<div class='ohno'>Username or Password do not match</div>") 
        return redirect('/login')
    

@app.route("/logout")
def logout():
    if "email" in session:
        session.pop("email")
    print(session)
    return redirect ("/login")

def checklogin():
    print(session)
    if "email" not in session:
        return False
    return True

@app.route("/profile", methods=['GET'])
def profile():
    valid=checklogin()
    if valid :
       return render_template("profile.html")
    else :
       return redirect('/login')


@app.route("/modify",methods=['POST'])
def modify():
    mysql = connectToMySQL("login")
    data = {
            "fname": request.form["fn"],
            "lname": request.form["ln"],
            "email":session.get('email')
        }
    print(data)
    query="UPDATE accounts SET firstname = %(fname)s,lastname= %(lname)s WHERE email =%(email)s ;"
    result=mysql.query_db(query, data)
    session['lastname'] =request.form["ln"]
    session['firstname'] =  request.form["fn"]
    return redirect('/profile')

@app.route("/edit")
def edit():
    valid=checklogin()
    if valid :
       return render_template("edit.html")
    else :
       return redirect('/login')

@app.route("/delete")
def delete():
  mysql = connectToMySQL("login")
  data = {
            "email":session.get('email')
        }
  query="DELETE FROM accounts WHERE email =%(email)s ;"
  result=mysql.query_db(query, data)
  session.pop("email")
  return redirect('/login')

@app.route("/pasw")
def modifyp():
    return render_template("pasw.html")
    
@app.route("/update",methods=['POST'])
def updatep():
    is_valid = True
    if len(request.form['pasw']) < 8:
        is_valid = False
        flash("<div class='ohno'>Password must be between 8-15 characters</div>")
    if len(request.form['pasw']) > 15:
        is_valid = False
        flash("<div class='ohno'>Password must be between 8-15 characters</div>")
    if request.form['cpasw'] != request.form['pasw']:
        is_valid = False
        flash("<div class='ohno'>Passwords must match</div>")
    if is_valid == False:
        return redirect('/signup')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['pasw'])  
        mysql = connectToMySQL("login")
        data = {
            "email":session.get('email'),
            "password_hash": pw_hash,
        }
        mysql = connectToMySQL("login")
        query = "UPDATE accounts SET password = %(password_hash)s WHERE email =%(email)s"
        result=mysql.query_db(query, data)
        session.pop("email")
        return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)