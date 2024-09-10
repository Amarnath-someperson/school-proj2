from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Integer, nullable=False)
    div = db.Column(db.String, nullable=False)
    admn_no = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    roll_no = db.Column(db.Integer, nullable=False)
