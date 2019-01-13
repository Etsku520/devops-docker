from application import db
from application.models import Base
from sqlalchemy.sql import text
from application.auth.models import User

class Message(Base):
    text = db.Column(db.String(10000), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable = False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable = False)

    def __init__(self, text):
        self.text = text

    def get_account():
        return User.query.get(self.account_id)