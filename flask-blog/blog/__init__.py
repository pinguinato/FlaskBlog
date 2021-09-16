from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# usiamo questo codice perché usiamo SQlite e per venire incontro alle specifiche limitazioni di questo database
# alcune operazioni non sono ammesse in questo database e quindi questo codice ci permette di creare un clone del DB
# in modo da poterlo modificare alla bisogna
with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

# TODO: qui dentro andiamo ad inizializzare il db ecc...le view saranno contenuto all'interno di routes.py

# è molto importante scrivere qui al fondo questo import per prevenire errore di Circular Import
from blog import routes