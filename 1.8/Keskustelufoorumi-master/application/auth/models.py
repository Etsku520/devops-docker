from application  import db, bcrypt
from application.models import Base
from sqlalchemy.sql import text

class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), unique=True, nullable=False)
    username = db.Column(db.String(144), unique=True, nullable=False)
    password = db.Column(db.String(144), nullable=False)

    messages = db.relationship("Message", backref='account', lazy=True)
    groups = db.relationship("Groups", backref='account', lazy=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable = False)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
        print(type(password))

        if (Role.query.count() == 0):
            ra = Role("ADMIN")
            rn = Role("NORMAL")
            db.session().add(ra)
            db.session().commit()
            db.session().add(rn)
            db.session().commit()
            stmt = text("SELECT id FROM Role WHERE role = 'ADMIN'")
            rid = db.engine.execute(stmt).first()
            self.role_id = rid[0]
        else:
            stmt = text("SELECT id FROM Role WHERE role = 'NORMAL'")
            rid = db.engine.execute(stmt).first()
            self.role_id = rid[0]
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def check_password(self, plaintext):
        return bcrypt.checkpw(plaintext.encode('utf-8'), self.password.encode('utf-8'))
    
    def get_role(self):
        return Role.query.get(self.role_id)

class Role(Base):
    role = db.Column(db.String(80), unique = True, nullable = False)
    users = db.relationship("User", backref='Role', lazy=True)

    def __init__(self, role):
        self.role = role