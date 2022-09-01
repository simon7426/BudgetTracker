from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from project import db


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.String(128))
    birth_date = db.Column(db.Date)
    blood_group = db.Column(db.String(10))
    about = db.Column(db.Text)
    image = db.Column(db.String(128), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow()
    )

    def __init__(
        self,
        user_id,
        first_name,
        last_name,
        gender=None,
        birth_date=None,
        blood_group=None,
        about=None,
    ):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birth_date = birth_date
        self.blood_group = blood_group
        self.about = about

    @hybrid_property
    def name(self):
        return f"{self.first_name} {self.last_name}"
