import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'blog.db')
    # permette di mantenere l'applicazione più veloce impendendo l'invio di segnali se non ne abbiamo bisogno
    SQLALCHEMY_TRACK_MODIFCATIONS =  False 