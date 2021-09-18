# qui teniamo i modelli delle tabelle che verrano aggiunte al nostro DB

from datetime import datetime
from blog import db

#questa classe estende db.Model e rappresenta le colonne nel nostro database
# il campo posts e cio che viene definito campo relazionale, non sta di fatto nella tabella ma ci permette di filtrare i dati
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    posts = db.relationship('Post', backref="author", lazy="dynamic")


    def __repr__(self):
        return f"User('{ self.id }', '{ self.created_at }', '{ self.username }', '{ self.email }')"


# user_id e un campo di tipo chiave esterna -> per ogni posdt ci sta un utente associato
class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.now)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    body = db.Column(db.Text(), nullable=False)


    def __repr__(self):
        return f"User('{ self.id }', '{ self.user_id }', '{ self.created_at }', '{ self.title }', '{ self.description }', '{ self.body }')"

