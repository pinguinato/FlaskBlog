# Inizio del progetto

Creazione della cartella del progetto:

        mkdir flask-blog

        cd flask-blog/

Settaggio di un ambiente virtuale:

        python -m venv venv

Installazione di Flask:

        pip install flask

        pip list

Frezziamo le dipendenze del progetto:

        pip freeze > requirements.txt

        cat requirements.txt

Creazione di una nuova cartella dentro il progetto del blog:

        mkdir blog

Configurazione di questa cartella come se fosse un package:

        cd blog

Creiamo un file __init__.py dentro la cartella blog

Sviluppiamo il nostro progetto del blog con il concetto della **separation of concern**, quindi organizziamo l'intero progetto strutturandolo in cartelle, come si fa in una vera applicazione professionale.

## Struttura corretta della nostra applicazione (App Skeleton iniziale)

/flask-blog

- **run.py** è il punto di ingresso della nostra applicazione blog
- settiamo da /flask-blog la var d'ambiente FLASK_APP=run.py

                export FLASK_APP=run.py

- da qui possiamo lanciare il comando:

                flask run

per far startare il server web.

/flask-blog/blog

- **__init__.py** contiene l'istanza di Flask(app)
- **routes.py** contiene le rotte (view) della nostra applicazione blog

## Aggiornamento del file delle dipendenze

Aggiungiamo la libreria dotenv per non dover ogni volta memorizzare la var d'ambiente FLASK_APP

                pip install python-dotenv

Andiamo a frizzare il file delle librerie:

                python freeze > requirements.txt

                $ cat requirements.txt 
                click==8.0.1
                colorama==0.4.4
                Flask==2.0.1
                itsdangerous==2.0.1
                Jinja2==3.0.1
                MarkupSafe==2.0.1
                python-dotenv==0.19.0
                Werkzeug==2.0.1

## Settaggio definitivo delle Variabili di ambiente del progetto

Posizioniamoci dentro /flask-blog e creiamo un file **.flaskenv**, li dentro
scriviamo i nomi delle nostre variabili di ambiente:

                FLASK_APP=run.py
                FLASK_ENV=development

In questo modo non dobbiamo ogni volta risettarle.

## Database e Flask

### Flask SQLAlchemy (ORM = Obejct Relational Mapping)

Estensione di Flask che permette di usare comodamente SQLAlchemy un ORM molto famoso per Python. SQLAlchemy permette 
la gestione del database tramite entità di alto livello come le Classi, Oggetti e Metodi invece che tabelle dei DB. Offre una astrazione che ci permette di interigire con i Database tramite Python. SQLAlchemy supporta tutti i principali DB relazionali come PostGre, SQLite e MySql.

### Flask Migrate

Estensione che permette di gestire facilmente i cambiamenti dello schema del DB.

### Installazione Pacchetti

                pip install flask-sqlalchemy

                pip list

                pip freeze > requirements.txt

                pip install flask-migrate

### Operazioni per la creazione e messa a punto della Base di dati in Flask (Sqlite)

1) Creazione di un file **models.py** dove mettiamo i nostri modelli(in Flask i modelli sono esattamente delle classi che contengono le colonne delle rispettive tabelle nella base di dati)

Es.


                class User(db.Model):
                        __tablename__ = "user"
                        id = db.Column(db.Integer, primary_key=True)
                        created_at = db.Column(db.DateTime, default=datetime.now)
                        username = db.Column(db.String(12), unique=True, nullable=False)
                        email = db.Column(db.String(50), unique=True, nullable=False)
                        password = db.Column(db.String(255), nullable=False)
                        posts = db.relationship('Post', backref="author", lazy="dynamic")


                class Post(db.Model):
                        __tablename__ = "post"
                        id = db.Column(db.Integer, primary_key=True)
                        user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False) 
                        created_at = db.Column(db.DateTime, default=datetime.now)
                        title = db.Column(db.String(255), nullable=False)
                        description = db.Column(db.String(255))
                        body = db.Column(db.Text(), nullable=False)


2) Dopo aver creato tutti i nostri modelli che ci servono, dobbiamo andare a collegare in init il nostro file dei modelli Flask:


                from blog import models

Allo stesso modo di come abbiamo importato il file delle rotte(routes.py) per impedire l'errore di import circolari.

3) A questo punto siamo pronti ad effettuare la migrazione ed attivare il nostro database dell'applicazione con il comando:


                flask db init

Eseguirlo direttamente dal terminale, questo crea la cartella **/migrations** all'interno del nostro progetto ed inizializza il database per l'utilizzo.

4) Adesso diamo sempre dal terminale il comando per effettuare la migrazione(creazione delle tabelle vera e propria), questo comando permettera' di scrivere dentro la cartella **/migrations/versions**, che al momento risulta vuota.

                flask db migrate -m "Creazione delle tabelle Post e User"

Con questo comando eseguito dal terminale, se non ci sono errori, viene popolata la cartella **versions** con un file che contiene le create table per le nostre tabelle del progetto.

5) Ora per andare a scrivere e usare il nostro database dobbiamo dare il comando:

                flask db upgrade

Succede che:

                Running upgrade  -> 1f33cf782904, Creazione delle tabelle Post e User

6) Se vogliamo rimuovere il db:

                flask db downgrade

**Riassumendo**: ogni volta che vogliamo apportare delle modifiche al nostro database dobbiamo usare il comando **flask db migrate** e por apportare effettivamente le modifiche al db usiamo **flask db upgrade** e **flask db downgrade**.

### Creazione di una istanza di User o Post dalla flask shell

Da terminal diamo il comando:

                flask shell

Apre di fatto una Python Shell vera e propria:

                Python 3.8.6 (tags/v3.8.6:db45529, Sep 23 2020, 15:52:53) [MSC v.1927 64 bit (AMD64)] on win32
                App: blog [development]
                Instance: C:\progetti\python-flask\FlaskBlog\flask-blog\instance
                >>>

Creiamo un nuovo User nel database dalla shell flask in questo modo:

                >>> from blog import db
                >>> from blog.models import Post, User
                >>> u = User(username="test", email="email@test.com", password="password")
                >>> db.session.add(u)
                >>> db.session.commit()

Creiamo anche una istanza di Post:

                >>> p = Post(title="Primo Post", body="Lorem Ipsum dolor sin amet some random content", author=u)
                >>> db.session.add(p)
                >>> db.session.commit()

### Implementazione di un sistema di password hashing (sicreuzza dell'aopplicazione)

- Avvio di una flask shell e import del modulo db e dei modelli creati in precedenza:

                flask shell

                from blog import db
                from blog.models import User, Post

- Operazioni da shell direttamente sul DB:

                >>> Post.query.all()
                [<Post 1>]

                >>> User.query.all()
                [<User 1>

                >>> u = User.query.get(1)
                >>> print(u)
                <User 1>
                >>> u   
                <User 1>
                >>> u.email
                'email@test.com'
                >>> u.username
                'test'
                >>> p = Post(title="Secondo Post", body="Body del secondo post ...", author=u)
                >>> db.session.add(p)
                >>> db.session.commit()
                >>> Post.query.all()
                [<Post 1>, <Post 2>]

**Importante**

Nell'uso di un ORM, cosi come anche in Django (object), la parola **query** nel comando indica che vogliamo eseguire una query sul database.

#### Come migliorare la rappresentazione in shell delle singole istanze 

Da come si vede quando stampiamo i record nella flask shell, non e' di grande aiuto avere listate le istanze cosi':

                [<Post 1>, <Post 2>]

Per far si che possiamo ritornare il contenuto delle singole istanze dobbiamo andare ad aggiungere un importante metodo speciale nei singoli modelli che abbiamo definito per il database del nostro progetto:

                def __repr__(self):
                        return f"User('{ self.id }', '{ self.created_at }', '{ self.username }', '{ self.email }')"

Questo metodo speciale ha la caratteristica di esplicitare i campi dell'istanza memorizzata a database!!

Es.

                $ flask shell
                c:\progetti\python-flask\flaskblog\flask-blog\venv\lib\site-packages\flask_sqlalchemy\__init__.py:872: FSADeprecationWarning:           SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress            this warning.
                  warnings.warn(FSADeprecationWarning(
                Python 3.8.6 (tags/v3.8.6:db45529, Sep 23 2020, 15:52:53) [MSC v.1927 64 bit (AMD64)] on win32
                App: blog [development]
                Instance: C:\progetti\python-flask\FlaskBlog\flask-blog\instance
                >>> from blog import db
                >>> from blog.models import User, Post
                >>> Post.query.all()
                [User('1', '1', '2021-09-18 12:22:00.664872', 'Primo Post', 'None', 'Lorem Ipsum dolor sin amet some random content'), User('2', '1',           '2021-09-18 14:10:45.584596', 'Secondo Post', 'None', 'Body del secondo post ...')]

**Importante**

Refactoring per evitare di importare in flask shell tutte le volte i moduli del progetto:

- editiamo il file run.py in questo modo:

                from blog import app, db
                from blog.models import User, Post

                @app.shell_context_processor
                def make_shell_context():
                        return {'db': db, 'User': User, 'Post': Post}

- riavviamo a questo punto la flask shell:

                >>> User.query.all()
                [User('1', '2021-09-18 12:18:43.640810', 'test', 'email@test.com')]

I dati ci vengono ritornati senza dover prima andar a fare gli import dei moduli!!