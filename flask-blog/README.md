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

Altri usi della flask shell con le query (uso di **filter**):

                Post.query.filter(User.username=="test").all()
                <console>:1: SAWarning: SELECT statement has a cartesian product between FROM element(s) "post" and FROM element "user".  Apply join condition(s) between each element to resolve.
                [User('1', '1', '2021-09-18 12:22:00.664872', 'Primo Post', 'None', 'Lorem Ipsum dolor sin amet some random content'), User('2', '1', '2021-09-18 14:10:45.584596', 'Secondo Post', 'None', 'Body del secondo post ...')]

Altri usi della flask shell con le query (uso di **filter_by**)

                >>> User.query.filter_by(username="test").all()       
                [User('1', '2021-09-18 12:18:43.640810', 'test', 'email@test.com')]

Filter_by e' un po' piu' semplice da usare. 

Aggiornamento di un titolo di un post da shell:

                >>> p = Post.query.first()
                >>> p
                Post('1', '1', '2021-09-18 12:22:00.664872', 'Primo Post', 'None', 'Lorem Ipsum dolor sin amet some random content')

                >>> p.title = "Titolo Aggiornato"
                >>> db.session.commit()
                >>> p
                Post('1', '1', '2021-09-18 12:22:00.664872', 'Titolo Aggiornato', 'None', 'Lorem Ipsum dolor sin amet some random content')

Cancellazione dei Post (esempio da shell):

                >>> Post.query.all()
                [Post('1', '1', '2021-09-18 12:22:00.664872', 'Titolo Aggiornato', 'None', 'Lorem Ipsum dolor sin amet some random content'), Post('2', '1', '2021-09-18 14:10:45.584596', 'Secondo Post', 'None', 'Body del secondo post ...')]
                >>> p = Post.query.first()
                >>> p
                Post('1', '1', '2021-09-18 12:22:00.664872', 'Titolo Aggiornato', 'None', 'Lorem Ipsum dolor sin amet some random content')
                >>> db.session.delete(p)
                >>> db.session.commit()
                >>> Post.query.all()
                [Post('2', '1', '2021-09-18 14:10:45.584596', 'Secondo Post', 'None', 'Body del secondo post ...')]

## Hashing delle Password

Potrebbe servirci per alzare il livello di protezione del nostro database. Per effettuare cio' ci conviene andare a definire dei nuovi metodi nelle nostre classi di Modello. Questi metodi oscureranno le noster password e si serviranno di metodi e funzioni del core di Flask(Werzeug). Nel progetto Flask Market ho usato invece Flask Bcrypt, che e' una estensione di Flask  che usa per lo stesso scopo.

Es.

- importiamo i pacchetti ncessari:

                from werkzeug.security import generate_password_hash, check_password_hash

- dentro la classe User:

                def set_password_hash(self, password):
                        self.password = generate_password_hash(password)

                def check_password(self, password):
                        return check_password_hash(self.password, password)

- esempio di utilizzo(sempre da shell flask):

                >>> u = User.query.first()
                >>> u
                User('1', '2021-09-18 12:18:43.640810', 'test', 'email@test.com')
                >>> u.password
                'password'
                >>> u.set_password_hash(u.password)
                >>> u.password
                'pbkdf2:sha256:260000$8vesm46JYIkUeWkQ$5a1f5b408e2c39e5b509f4d7e6d6a9a27ef6159a84e5e248c4cb3bb47d09a292'

                >>> u.check_password('password')
                True

## Far arrivare i post dal database alla pagina web

Modifichiamo il file delle rotte in questo modo:

from blog.models import Post


                @app.route('/')
                def homepage():
                        # i post sono ordinati per data di creazione decrescente                        
                        posts = Post.query.order_by(Post.created_at.desc()).all()
                        return render_template("homepage.html", posts=posts)

## Come renderizzare singoli Post del nostro blog

- ci serve una nuova funzione **routes**
- ci serve un nuovo file dentro **/templates**

Es. la nuova rotta (dove passiamo come parametro l'id del singolo Post)


                @app.route('/posts/<int:post_id>')
                def post_details(post_id):
                        post_instance = Post.query.get_or_404(post_id)
                        return render_template("post_details.html", post=post_instance)


**Importante**: l'id viene passato come intero, specifichiamo il tipo, inoltre usiamo il metodo **get_or_404()** che ci permette in caso di chiamata di ID che non esiste a db di restituire automaticamente un 404 invece di un None type. 

## Autenticazioni utenti: LOGIN e LOGOUT in Flask

Si usano 2 estensioni di Flask:
- Flask-Login
- Flask-WTF

Il primo gestisce le fasi di login e logout degli utenti, mentre il secondo ci permetterà di creare dei form di login necessar in maniera sicura e rapida.

Installiamo le 2 estensioni:

                pip install flask-login

                pip install flask-wtf

                pip freeze > requirements.txt

Creo una SECRET_KEY:

- creo un file .env che metto nel .gitignore
- apro un terminale python e immetto i seguenti comandi:
  
                import uuid

                print(uuid.uuid4().hex)

Prendo la stringa che compare a terminale e la copio nella SECRET_KEY

La variabile SECRET_KEY serve per la generazione dei token e la messa in sicurezza dell'applicazione.

Il contentu odel file .env non deve essere condiviso!!

Creiamo ora un nuovo file all'interno del package **/blog**. Il file si chiamerà **forms.py**

Il file che abbiamo creato ci serve per implementare il nostro form di login.

## Creazione del form di LOGIN e validazione

Creiamo il file **forms.py** e ci mettiamo questo codice

                from flask_wtf import FlaskForm
                from wtforms import BooleanField, PasswordField, StringField, SubmitField
                from wtforms.validators import DataRequired

                class LoginForm(FlaskForm):
                        username = StringField('Username', validators=[DataRequired()])
                        password = PasswordField('Password', validators=[DataRequired()])
                        remember_me = BooleanField('Ricordami')
                        submit = SubmitField('Login')

A questo punto abbiamo bisogno di un template per redenrizzare questo form di login!! Quindi creiamo un file **login.html** dentro la cartella dei templates, ovvero /templates.

Il codice del file **login.html**:

                {% extends 'base.html' %}
                {% block title %}Login - Coding Wiz{% endblock %}
                {% block content %}

                <div class="container text-center mt-3 ">
                        <h2>Admin Login</h2>
                                <div class="row no-gutters justify-content-center">
                                <div class="col-md-4">
                                        <div class="about-page-block">
                                                <form method="POST" novalidate>
                                                {{ form.hidden_tag() }}
                                                <div class="form-group">
                                                        {{ form.username.label }}
                                                        {{ form.username(class="form-control") }}
                                                </div>
                                                <div class="form-group">
                                                        {{ form.password.label }}
                                                        {{ form.password(class="form-control") }}
                                                </div>
                                                <p>
                                                        {{ form.remenber_me() }} {{ form.remenber_me.label }}
                                                </p>
                                                {{ form.submit(class="btn btn-outline-secondary") }}
                                                </form>
                                        </div>
                                </div>
                                </div>
    
                                {% if boolean_flag %}
                                        <p>Boolean Flag: True</p>
                                {% endif %}
                                </div>    
                                {% endblock %}

**Importante**

                {{ form.hidden_tag() }}

Ci protegge dalla vulnerabilità Cross-site request forgery!! è il token CSRF.

## Settaggio del Login Manager

Dentro il file init.py:

                from flask_login import LoginManager

e poi:

                login_manager = LoginManager(app)

Invece dentro il file **models.py**:

                from blog import login_manager
                from flask_login import UserMixin


                # funzione necessaria affinchè il login manager possa funzionare, così tengo traccia dell'utente connesso
                @login_manager.user_loader
                def load_user(id):
                        return User.query.get(int(id))

Infine andiamo a ritoccare il nostro modello User:

                class User(UserMixin, db.Model):

## Gestione dei messaggi FLASH per i form ddegli utenti

Dobbiamo modificare la pagina del **login.html** inserendo uina nuova classe per il DIV:


                <div class="mt-3">
                {% with messages = get_flashed_messages() %}
                        {% if messages %}
                                {% for message in messages %}
                                        <p style="color: #dc3545;">{{ message }}</p>
                                {% endfor %}
                        {% endif%}
                {% endwith %}
                </div>

In questo modo compariranno i messaggi di errore in caso di errato Login.

## Come si creano nuovi utenti usando la flask shell

Apriamo la flask shell e digitiamo i seguenti comandi da shell:

                >>> u = User(username="admin", email="admin@localhost")
                >>> u.set_password_hash('string-password')
                >>> u.password
                'pbkdf2:sha256:260000$ANakz00Aq5JaVY6I$aac7528fad64b7e685006f2d05523bdc45226836695badef11db66986c9dedc3'
                >>> db.session.add(u)
                >>> db.session.commit()

In questo modo creo un nuovo utente in grado di scrivere nuovi posts.

## Costruire l'interfaccia per la creazione di nuovi posts

Per dare la possibilita' di aggiungere nuovi posts al nostro blog ci serviamo di 2 estensioni di Flask:
- flask-wtf per costruire il nostro form di inserimento dei nuovi post
- flask-misaka una estensione nuova che da' supporto markdown per scrivere i nostri nuovi post

Prima di tutto andiamo a definire una nuova classe per il form.

                from wtforms import TextAreaField
                from wtforms.validators import Length


                class PostForm(FlaskForm):
                        title = StringField('Titolo', validators=[DataRequired("Campo Obbligatorio!"), Length(min=3, max=120, message="Assicurati che il titolo abbia tra i 3 e i 120 caratteri")])
                        description = TextAreaField('Descrizione', validators=[Length(max=240, message="Assicurati che la descrizione abbia al massimo 240 caratteri")])
                        body = TextAreaField('Contenuto', validators=[DataRequired("Campo Obbligatorio!")])
                        submit = SubmitField('Pubblica Post')

Importiamo la nuova classe dentro il file delle rotte:

                from blog.forms import LoginForm, PostForm

Adesso non ci resta che creare una nuova view per la creazione dei posts!

Inseriamo questo codice nel file **routes.py**:

                @app.route('/create-post', methods=["GET", "POST"])
                def post_create():
                        form = PostForm()
                        if form.validate_on_submit():
                                new_post = Post(title=form.title.data, body=form.body.data, description=form.description.data, author=current_user)
                                db.session.add(new_post)
                                db.session.commit()
                                return redirect(url_for('post_detail', post_id=new_post.id))
                        return render_template("post_editor.html", form=form)

Ricordiamoci di importare: 

                from blog import db

Ma non basta perché dobbiamo proteggere la nostra view in modo da essere soltanto noi amminstratori del blog a poter postare dei post, abbiamo bisogno di importare un nuovo decoratore e aggiungerlo nella rotta in questo modo:

                from flask_login import login_required

e poi aggiungere al decorator della rotta:

                @login_required

A questo punto andiamo a definire dentro **/templates** il nuovo file di template per l'editing dei post:

- creiamo il file **post_editor.html** con questo codice Jinja2:


                {% extends 'base.html' %}

                {% block title %}Post Editor - CondingWiz{% endblock %}

                {% block content %}
                <div class="container content-container">
                        <h2>Crea un nuovo Post</h2>
                        <div class="row no-gutters">
                                <div class="col">
                                <form method="POST" novalidate>
                                {{ form.hidden_tag() }} <!-- csrf token -->
                                <div class="form-group">
                                {{ form.title.label }}
                                {{ form.title(class="form-control") }}
                                        {% if form.title.errors %}
                                                {% for error in for.title.errors %}
                                                <span class="text-danger">{{ error }}</span>
                                        <br>
                                        {% endfor %}
                                        {% endif %}
                                </div>
                                <div class="form-group">
                                {{ form.description.label }}
                                {{ form.description(class="form-control") }}
                                        {% if form.description.errors %}
                                        {% for error in for.description.errors %}
                                                <span class="text-danger">{{ error }}</span>
                                        <br>
                                        {% endfor %}
                                        {% endif %}
                                </div>
                        <div class="form-group">
                        {{ form.body.label }}
                        {{ form.body(class="form-control", rows=15) }}
                        {% if form.body.errors %}
                        {% for error in for.body.errors %}
                            <span class="text-danger">{{ error }}</span>
                            <br>
                        {% endfor %}    
                        {% endif %}
                        </div>
                        <hr>
                        {{ form.submit(class="btn btn-sm btn-outline-secondary") }}
                        </form>
                </div>
                </div>    
                </div>
                {% endblock %}

**Importante**

Ricordarsi di mettere il 

                {{ form.hidden_tag() }} <!-- csrf token -->

altrimenti non funziona la creazione dei post!!!

Adesso aggiungiamo la voce di menu per l'inserimento di nuovi posts:

- dentro **base.html**

                {% if current_user.is_authenticated %}
                    <a class="nav-link" href="{{ url_for('post_create') }}">Crea Post</a>
                    <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
                {% endif %}

## Fix degli errori del form di Login

Andiamo ad aggiungere questo pezzo di codice dentro il template della login:

                        ...
                        {% if form.password.errors %}
                        {% for error in form.password.errors %}
                            <span class="text-danger">{{ error }}</span>
                            <br>
                        {% endfor %}
                        {% endif %}
                        ...
