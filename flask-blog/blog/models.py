# qui teniamo i modelli delle tabelle che verrano aggiunte al nostro DB

from datetime import datetime
from blog import db
from werkzeug.security import generate_password_hash, check_password_hash
from blog import login_manager
from flask_login import UserMixin



# funzione necessaria affinchè il login manager possa funzionare, così tengo traccia dell'utente connesso
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


#questa classe estende db.Model e rappresenta le colonne nel nostro database
# il campo posts e cio che viene definito campo relazionale, non sta di fatto nella tabella ma ci permette di filtrare i dati
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    posts = db.relationship('Post', backref="author", lazy="dynamic")


    def __repr__(self):
        return f"User('{ self.id }', '{ self.created_at }', '{ self.username }', '{ self.email }')"

    
    def set_password_hash(self, password):
        self.password = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password, password)


# user_id e un campo di tipo chiave esterna -> per ogni posdt ci sta un utente associato
class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.now)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    body = db.Column(db.Text(), nullable=False)
    slug = db.Column(db.String(255))


    def __repr__(self):
        return f"Post('{ self.id }', '{ self.user_id }', '{ self.created_at }', '{ self.title }', '{ self.description }', '{ self.body }')"

