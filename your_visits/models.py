from sqlalchemy.orm import backref
from your_visits import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


class Ip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(20), nullable=False)
    count = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="ips")

    def __repr__(self) -> str:
        return f"<Ip {self.ip}>"
