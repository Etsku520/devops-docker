from application import db
from application.models import Base
from sqlalchemy.sql import text
from application.auth.models import User

class Groups(Base):
    heading = db.Column(db.String(20), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    messages = db.relationship("Message", backref='Groups', lazy=True)

    def __init__(self, heading):
        self.heading = heading

    @staticmethod
    def findMessagesByGroup(group_id):

        stmt = text(
            "SELECT DISTINCT Message.text, Message.account_id, Message.group_id, Message.id, Message.date_created, Message.date_modified FROM Groups, Message WHERE Message.group_id = :id ORDER BY message.date_created").params(id = group_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[3], "text":row[0], "account_id":row[1], "group_id":row[2], "date_created":row[4], "date_modified":row[5]})

        return response

    @staticmethod
    def categories(group_id):
        stmt = text(
            "SELECT DISTINCT Category.id, Category.name FROM Groups, Group_category, Category WHERE Category.id = Group_category.category_id AND Group_category.group_id = :id").params(id = group_id)

        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1]})

        return response

class GroupCategory(Base):
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = False)



class Category(Base):
    name = db.Column(db.String(15), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

class Book(Base):
    name = db.Column(db.String(40), nullable=False, unique=True)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable = False)

    def __init__(self, name):
        self.name = name
