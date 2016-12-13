from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
import datetime

from mockdbhelper import MockDBHelper as DBHelper
from passwordHelper import PasswordHelper
from bitlyHelper import BitlyHelper
from forms import RegistrationForm
from forms import LoginForm
from forms import CreateTableForm
from user import User
import config

app = Flask(__name__)
login_manager = LoginManager(app)
app.secret_key = 'tPXJY3X37Qybz4QykV+hOyUxVQeEXf1Ao2C8upz+fGQXKsM'
DB = DBHelper()
PH = PasswordHelper()
BH = BitlyHelper()


@app.route('/')
def home():
    return render_template("home.html", regForm=RegistrationForm(), logForm=LoginForm())


@app.route('/account')
@login_required
def account():
    # list all tables of the user to him/her
    tables = DB.get_tables(current_user.get_id())
    return render_template("account.html", tables=tables)


@app.route('/dashboard')
@login_required
def dashboard():
    now = datetime.datetime.now()
    requests = DB.get_request(current_user.get_id())
    for req in requests:
        deltaseconds = (now - req['time']).seconds
        req['wait_minutes'] = "{}.{}".format((deltaseconds / 60), str(deltaseconds % 60).zfill(2))
    return render_template("dashboard.html", requests=requests)


@app.route('/account/createtable', methods=['POST'])
@login_required
def account_createtable():
    form = CreateTableForm(request.form)
    if form.validate():
        tableid = DB.add_table(form.tableNumber.data, current_user.get_id())
        new_url = config.base_url + "/newrequest/" + tableid
        DB.update_table(tableid, new_url)
        return redirect(url_for('account'))


    tablename = request.form.get("tablenumber")
    tableid = DB.add_table(tablename, current_user.get_id())
    new_url = config.base_url + "/newrequest/" + tableid
    # new_url = BH.shortenUrl(new_urli)  for bitly url shortening
    DB.update_table(tableid, new_url)
    return redirect(url_for('account'))


# delete the table when the user click the delete button
@app.route('/account/deletetable', methods=['GET'])
@login_required
def account_deletetable():
    # form action is get
    table_id = request.args.get("tableid")
    DB.delete_table(table_id)
    return redirect(url_for('account'))


@app.route("/dashboard/resolve")
@login_required
def dashboard_resolve():
    request_id = request.args.get("request_id")
    DB.delete_request(request_id)
    return redirect(url_for('dashboard'))


@app.route('/login', methods=["POST"])
def login():
    form = LoginForm(request.form)
    if form.validate():
        stored_user = DB.get_user(form.LoginEmail.data)
        if stored_user and PH.validate_password(form.LoginPwd.data, stored_user['salt'], stored_user['hashed']):
            user = User(form.LoginEmail.data)
            login_user(user, remember=True)
            return redirect(url_for('account'))
        form.LoginEmail.errors.append("Email or password invalid")
    return render_template("home.html", logForm=form, regForm=RegistrationForm())

    """
    email = request.form.get("email")
    password = request.form.get("password")
    stored_user = DB.get_user(email)
    if stored_user and PH.validate_password(password, stored_user['salt'], stored_user['hashed']):
        user = User(email)
        login_user(user, remember=True)  # to handle authentication and remembering the logged in Users
        return redirect(url_for('account'))
    return home()
"""


""" to get the cookies for the logged in user that are sent by Flask_login"""


@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)


# log out the user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))


# displaying request from table id
@app.route('/newrequest/<tid>')
def new_request(tid):
    DB.add_request(tid)
    return "Your request has been logged and a waiter will be with you shortly"


@app.route('/register', methods=['POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        if DB.get_user(form.email.data):
            form.email.errors.append("Email address already registered")
            return render_template('home.html', regForm=form, logForm=LoginForm())
        salt = (PH.get_salt()).decode('utf-8')
        hashed = PH.get_hash(form.password2.data + salt)
        DB.add_user(form.email.data, salt, hashed)
        return render_template('home.html', regForm=form, logForm=LoginForm(),
                               onsuccessmessage="Registration successful. Please log in.")
    return render_template('home.html', regForm=RegistrationForm(), logForm=LoginForm())


"""
    email = request.form.get("email")
    pw1 = request.form.get("password")
    pw2 = request.form.get("password2")
    # if passwod and confirmation doesnt match
    if not pw2 == pw1:
        return redirect(url_for("home"))
    # if entered email already exist in database
    if DB.get_user(email):
        return redirect(url_for("home"))
    salt = (PH.get_salt()).decode('utf-8')  # get a string type of salt
    hashed = PH.get_hash(pw1 + salt)
    DB.add_user(email, salt, hashed)
    return redirect(url_for("home"))
"""

if __name__ == '__main__':
    app.run(port=5000, debug=True)
