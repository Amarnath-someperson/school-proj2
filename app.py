import os

from flask import Flask, render_template, url_for, redirect
from flask import session, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,  SubmitField
from wtforms.validators import InputRequired, Length
from flask_bcrypt import Bcrypt
import pandas as pd
from models import Students

db = SQLAlchemy(model_class=Students)


app = Flask(__name__)
# secret key used for production must be a good one. TODO: CHANGE IN PROD.
app.secret_key = 'cde18620caeb39db4dff9c291d4fb1c2b2f0e32f5df691f69b2dee1ad47c4e7d'
db_name = 'student'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}.db'
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'

db.init_app(app)
bcrypt = Bcrypt(app)


def is_admin():
    """Checks if the user is an adminuser.

    Returns:
        bool: if the user is authorised to view admin pages.
    """
    try:
        if session['logged_in'] is True:
            return True
    except:
        return False
    return False


class AdminPage(AdminIndexView):
    def is_accessible(self):
        return is_admin()

    @expose('/', methods=('GET', 'POST'))
    def index(self):
        if self.is_accessible():
            return self.render("admin/index.html")


admin = Admin(index_view=AdminPage(name='Home',
              url='/admin'))


class StudentsView(ModelView):
    def is_accessible(self):
        return is_admin()

    @expose('/student', methods=('GET', 'POST'))
    def index(self):
        if self.is_accessible():
            pass


admin.add_view(StudentsView(Students, db.session))

admin.init_app(app)


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={
                           "placeholder": "username", "class": " m-3 p-2 bg-slate-900 border-orange-400 border-4"})

    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={
        "placeholder": "password", "class": " m-3 p-2 bg-slate-900 border-orange-400 border-4"})

    submit = SubmitField('Login', render_kw={
                         'class': " m-3 p-2 bg-slate-900 border-orange-400 border-4"})


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def admin_login():
    try:
        session['logged_in']
    except:
        session['logged_in'] = False
    if not session['logged_in']:
        form = LoginForm(request.form)

        if form.validate_on_submit():
            username = request.form.get("username")
            pwhash = bcrypt.generate_password_hash(
                request.form.get("password"))
            print(
                f'\033[0;33m[LOGIN CREDS] someone with username \'{username}\' just tried to log in.\033[0;0m')
            user_table = pd.read_sql_table(
                table_name="user", con='sqlite:///users.db')
            if (username in user_table.values):
                saltedpw = ''
                for i in user_table.values:
                    if i[1] == username:
                        saltedpw = i[2]
                if bcrypt.check_password_hash(saltedpw[2:len(saltedpw)-1], form.password.data):
                    session['logged_in'] = True
                    session['username'] = username
                    print(
                        f'\033[0;42m[LOGIN SUCCESSFUL] user logged in successfully\033[0;0m')
                    return redirect('/admin')
                else:
                    errors = "wrong password"
            else:
                print('\033[0;41m[NOT FOUND] User was not found.\033[0;0m')
        else:
            print('\033[0;41m[INVALID FORM] Form was not validated.\033[0;0m')

        return render_template('login.html', form=form), 200
    return render_template('logged_in.html'), 200


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in')
    session.pop('username')
    return redirect(url_for('admin_login'))


# @app.after_request
# def add_header(r):
#     r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     r.headers["Pragma"] = "no-cache"
#     r.headers["Expires"] = "0"
#     r.headers['Cache-Control'] = 'public, max-age=0'
#     return r
if __name__ == '__main__':
    app.app_context().push()
    if not os.path.exists(f'./instance/{db_name}'):
        db.create_all()
    app.run(debug=True)
