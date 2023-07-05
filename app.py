# RahulRaj Vardhanapu --8813996

# Importing various Modules
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_sqlalchemy import SQLAlchemy

# Initializing the Flask Application an Configure the database connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Creating Model's User and Todo_List
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

class Todo_List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

#Creating Routes for Home Page
@app.route("/")
def index():
    return render_template("index.html")

#Routes for Login Page
@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        
        login = User.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            return redirect(url_for("lists"))
    return render_template("login.html")

#Routes for Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = User(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

#Routes for Lists Page
@app.route("/lists", methods=["GET", "POST"])
def lists():
    todo_list = db.session.query(Todo_List).all()
    return render_template("lists.html", todo_list=todo_list)

#Routes for Add Lists Page
@app.post("/addList")
def addList():
    title = request.form.get("title")
    new_todo = Todo_List(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("lists"))

#Routes for Update Lists
@app.get("/updateStatus/<int:todo_id>")
def updateStatus(todo_id):
    todo = db.session.query(Todo_List).filter(Todo_List.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("lists"))

#Routes for Delete Lists 
@app.get("/deleteList/<int:todo_id>")
def deleteList(todo_id):
    todo = db.session.query(Todo_List).filter(Todo_List.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("lists"))

#Routes for Display Tables 
@app.route('/display_tables')
def display_tables():
    # Get the table names
    table_names = db.Model.metadata.tables.keys()
    # Print the table names
    for table_name in table_names:
        print(table_name)

    return 'Tables displayed in console'

#Table creation should happen only when the script is run, not when imported as a module 
if __name__ == "__main__":
    with app.app_context():
        {
    #Method to create all tables defined in the above models
    db.create_all() 
        }
    app.run(debug=True)



