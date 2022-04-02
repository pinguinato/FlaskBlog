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

## Installazione di Flask Misaka per la gestione del markdown nei nostri Post

                        pip install flask-misaka

**Importante**

Richiede l'installazione aggiuntiva del pacchetto Visual C++ 2014 o superiore, altrimenti Misaka non si installa!!

## Implementazione delle funzionalità di aggiornamento dei post (update)

Dobbiamo importare 2 nuove funzioni all'interno del file **routes.py**:
- la funzione request
- la funzione abort

quindi:

                from flask import abort, request

Poi dobbiamo creare una nuova view, sempre nello stesso file:

                @app.route('/posts/<int:post_id>/update', methods=["GET", "POST"])
                @login_required
                def post_update(post_id):
                        pass

Ricordiamo che per aggiornareu n post abbiamo bisogno della sua chiave primaria quindi:

                /posts/<int:post_id>/update

Usiamo questo per recuperarci dal db il Post che dobbiamo aggiornare:

                post_instance = Post.query.get_or_404(post_id)

Aggiungiamo un ulteriore livello di sicurezza inserendo un controllo che se non è l'autore del post ti becchi un errore 403:

                if post_instance.author != current_user:
                        abort(403)

La funzione blocchera la richiesta mostrandoci una pagina di errore.

                @app.route('/posts/<int:post_id>/update', methods=["GET", "POST"])
                @login_required
                def post_update(post_id):
                        post_instance = Post.query.get_or_404(post_id)
                        if post_instance.author != current_user:
                                abort(403)
                        form = PostForm()
                        if form.validate_on_submit():
                                post_instance.title = form.title.data
                                post_instance.description = form.description.data
                                post_instance.body = form.body.data
                                db.session.commit()
                                return redirect(url_for('post_details', post_id=post_instance.id))
                        elif request.method == "GET":
                                form.title.data = post_instance.title
                                form.description.data = post_instance.description
                                form.body.data = post_instance.body
                        return render_template("post_editor.html", form=form)

Aggiungere la possibilità di aggiornamento:

                {% if current_user.is_authenticated and current_user == post.author %}
                    <a class="btn btn-sm btn-outline-success" href="{{url_for('post_update', post_id=post.id)}}">Aggiorna</a>
                {% endif %}

## Implementazione della funzionalità di cancellamento dei posts

Dobbiamo creare una nuova view che ci permetta di cancellare cose dal database. Sarà una view molto simile alla post di update.

Accetteremo per questa rotta soltanto richieste di tipo POST perchè non abbiamo nulla da mostrare.

Esempio:

                @app.route('/posts/<int:post_id>/delete', methods=["POST"])
                @login_required
                def post_delete(post_id):
                        post_instance = Post.query.get_or_404(post_id)
                        if post_instance.author != current_user:
                                abort(403)
                        db.session.delete(post_instance)
                        db.session.commit()
                        return redirect(url_for('homepage'))

E poi in **post_detail.html** inseriamo una modale Boostrap per permettere la cancellazione, però quello che andiamo a fare in realtà è prenderci il codice della modale Boostrap da qui: https://getbootstrap.com/docs/4.5/components/modal/ e poi andiamo a creare un nuovo template .html dentro la cartella /templates e questo file 
**post_delete_modal.html** sarà il contenitore della nostra modale di cancellazione.

Esempio: vedi file **post_delete_modal.html**

Poi bisogna richiamare la modale in **post_details.html** in questo modo:


                {% include "post_delete_modal.html" %}

E aggiungere il pulsante di cancellazione dei Post:

                <!-- Button trigger modal -->
                <button type="button" class="btn btn-sm btn-outline-danger" data-toggle="modal" data-target="#deletePostModal">
                    Cancella
                </button>

## Ottimizzazione SEO, aggiunta del campo slug

Al momento per come abbiamo configurato i link del nostro blog, purtroppo non sono esplicativi, nel senso che viene passato l'id e questo non 
è come un titolo, quindi non è parlante e il SEO ne risente sicuramente.

Andiamo quindi a modificare il modello Post, aggiungendo il campo slug basato sul titolo del nostro post, in modo che il link diventi più parlante e riconoscibile. Con il termine slug di solito si indica una stringa di caratteri alfanumerici, a cui vengono tolti i caratteri di spazi bianchi tra le parole, sostituiti con dei trattini in modo che possa generare un vero URL, che verrà tenuto in considerazione dai motori di ricerca come Google.

- Modifichiamo il **models.py**
- Modifichiamo la **routes.py**

Abbiamo bisogno di alcune funzioni del file **utils.py** in grado di trasformare il titolo di un campo in un url.

Es.

1) Modifica del modello Post: andiamo ad aggiungere questo campo in più e rifacciamo le migrazioni

Nel file dei modelli dentro la classe Post aggiungo:

                slug = db.Column(db.String(255))

Poi apro un terminale e digito il seguente comando per ripetere le migrations:

                flask db migrate

Si può osservare intanto che è stato generato un nuovo file delle migrazioni.

E poi digitiamo subito dopo:

                flask db upgrade

Per applicare il cambiamento. Adesso intanto andiamo a generare uno slug per tutti i nostri Posts che sono già 
in database, quindi devo aprire la flask shell. Quindi:

                flask shell

E andiamo a fare la import delle clasis che ci servono.

                >>> from blog.utils import title_slugifier
                >>> for post in Post.query.all():
                ...     post.slug = title_slugifier(post.title)
                ...     db.session.commit()

E ne visualizziamo il risultato a database della nostra modifica:

                for post in Post.query.all():
                        post.slug

                '- --vm5wdb'
                '- - - --6dpwet'
                '- - - --qjebs4'
                '- - - --1a0sl2'

Adesso bisogna modificare in tutti i punti il file delle rotte e il template della homepage.html:

In homespage.html:

                <a class="custom-link" href="{{ url_for('post_details', post_id=post.id) }}">
                <a class="custom-link" href="{{ url_for('post_details', post_slug=post.slug) }}">

alla dicitura post_id sostituire post_slug.

Nel file delle rotte implemtnare i seguenti cambiamenti:

IMportare nel file delle rotte:

                from blog.utils import title_slugifier

La chiamata del dettaglio del post:

                @app.route('/posts/<string:post_slug>')
                def post_details(post_slug):
                        post_instance = Post.query.filter_by(slug=post_slug).first_or_404()

La creazione del post:

                slug = title_slugifier(form.title.data)
                new_post = Post(title=form.title.data, body=form.body.data, slug=slug, description=form.description.data, author=current_user)

                return redirect(url_for('post_details', post_slug=slug))

L'aggiornamento del post:

                return redirect(url_for('post_details', post_slug=post_instance.slug))


## Includere delle immagini e farne l'upload in Flask

La prima cosa che dobbiamo fare innanzitutto è andare a modificare il nostro modello aggiungendo un nuovo campo per ospitare le immagini.

Delle immagini salviamo **il nome** non l'immagine vera e propria, questa verrà preservata in una cartella del sistema, ma a database andremo a salvare soltanto il nome di questa. Questo meccanismo ci serve per recuperarla poi dal disco. L'immagine sarà salvata all'interno di una sottocartella dentro **/static**.

Quindi aggiungere questa riga di codice alla classe del nostro modello **Post**:

                image = db.Column(db.String(120))

Quindi rilanciamo di nuovo le migration per aggiornare la situazione a livello di database.

                flask db migrate -m "Aggiunta campo immagine"

E poi:

                flask db upgrade

Possiamo chiudere il nostro terminale e andare ad aggiungere una nuova varibile globale nel nostro file di configurazione **config.py**:

                UPLOAD_FOLDER = "static/img/posts"

Qui sarà la locazione dove verrano salvate le immagini che caricheremo nei nostri posts.

A questo punto creo fisicamente la nuova location.

Inoltre ricordo che è necessario modificare la rotta di creazione e di update dei posts, per andare ad ispezionare il campo image per vedere se ci sono dei cambiamenti in merito. Ma intanto per fare questo andiamo a definire una nuova funzione all'interno del file **utils.py**.

Dentro utils.py:
                
                import os

                from flask import current_app
                from blog import app

                UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']

In modo da dire a Flask dove caricare le immagini.

Dobbiamo inoltre installare il package **pillow**, che è una libreria python per la gestione delle immagini.

                pip install pillow

e aggiorniamo il file dei requirements:

                pip freeze > requirements.txt

e sempre in **utils.py** importiamo il pacchetto image:

                from PIL import Image

e poi definire questa nuova funzione per il salvataggio dell'immagine:

                def save_picture(form_data):
                        filename = form_data.filename
                        picture_name = generate_random_string() + "-" + filename
                        picture_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, picture_name) 
                        image = Image.open(form_data)
                        image.save(picture_path)
                        return picture_name

Ricordiamoci di importare anche la nuova funzione dentro il file delle rotte:

                from blog.utils import title_slugifier, save_picture

E poi di modificare all'occasione anche **forms.py**:

                from flask_wtf.file import FileField, FileAllowed

                image = FileField('Copertina Articolo', validators=[FileAllowed['jpg', 'jpeg', 'png']])

Questo perché così nel nostro form di creazione/update di un Post siamo in grado di avere un campo immagine, che accetta solo 3 precisi formati di mmagine che gli diciamo noi quali devono essere.

Ora passiamo a modificare le rotte di creazione e aggiornamento di un Post:

Nel  codice della create post:

                if form.image.data:
                        try:
                                image = save_picture(form.image.data)
                                new_post.image = image
                        except Exception:
                                db.session.add(new_post)
                                db.session.commit()
                                flash("C'è stato un problema con l'upload dell'immagine, cambia immagine e riprova.")
                                return redirect(url_for('post_update', post_id=new_post.id))

Aggiorniamo anche la **post_detail.html**:

                {% if post.image %}
                <div>
                    <img class="img-fluid" src="{{ url_for('static', filename='img/posts/' + post.image) }}" alt="">
                </div>
                {% endif %}

Nota: la classe Boostrap class="img-fluid" ci permette di responsivizzare automagicamente l'immagine del Post.

E modificare anche **post_editor.html**:


Aggiungiamo questo codice: 

                        <div class="form-group">
                        {{ form.image.label }}
                                {{ form.image(class="form-control-file") }}
                                {% if form.image.errors %}
                                {% for error in form.image.errors %}
                                <span class="text-danger">{{ error }}</span>
                                <br>
                                {% endfor %}
                        {% endif %}
                        </div>


                        <div class="mb-3">
                        {% with messages = get_flashed_messages() %}
                        {% if messages %}
                        {% for message in messages %}
                            <p style="color: #dc3545;">{{ message }}</p>
                        {% endfor %}
                        {% endif%}
                        {% endwith %}
                        </div>

                        <form method="POST" enctype="multipart/form-data" novalidate>

Il form deve essere **multipart/form-data** per poter gestire l'upload delle immagini.

## Rifinitura degli aspetti grafici di insieme

1) Settare l'URL dell'home page:

                <a class="navbar-brand" href="{{ url_for('homepage') }}">CodingWiz</a>

2) Settare la classe "active" sugli url del menù:

                <div class="navbar-nav ml-auto">
                        <a class="nav-item nav-link
                        {% if request.path == '/' %} 
                        active 
                        {% endif %}" 
                        ....>...

3) Modifica della classe "nav-link":

                @media (min-width: 768px) {
                        .nav-link {
                                padding-right: 0px !important;
                                padding-left: 1rem !important;
                        }
                }

4) Modifica di about_me_snippet.html:

                <div class="about-snippet-block text-center">
                        <img class="img-fluid" width="150" alt="artificial intelligence" src="{{ url_for('static', filename='img/ai.png') }}">
                        <div class="mt-3">
                                <p class="p-small-one">Ridiculus vulputate rhoncus potenti platea, dapibus nunc amet.</p>
                                <p class="p-small-one">Ridiculus vulputate rhoncus potenti platea, dapibus nunc amet.</p>
                                <p class="p-small-one">Ridiculus vulputate rhoncus potenti platea, dapibus nunc amet.</p>
                                <hr>
                                <p class="p-small-one text-muted">Eleifend maecenas platea montes cursus inceptos, dictumst neque pretium.</p>
                                <p class="p-small-one text-muted">Eleifend maecenas platea montes cursus inceptos, dictumst neque pretium.</p>
                        </div>    
                </div>

5) Sistemazione dell'area dei Posts:

dentro il file post_details.html:

                {% if post.image %}
                <div class="post-image-block">
                    <img class="img-fluid post-image" src="{{ url_for('static', filename='img/posts/' + post.image) }}" alt="">
                </div>
                <div class="post-page-block no-border-top">
                {% else %}    
                <div class="post-page-block">
                {% endif %}

e nal css del blog:

                .no-border-top {
                        border-top: 0;
                        border-top-left-radius: 0;
                        border-top-right-radius: 0;
                }

                .post-image {
                        border: 1px solid #d3d3d3;
                        border-top-left-radius: 5px;
                        border-top-right-radius: 5px;
                }

                aggiungere:

                .post-image-block {
                        margin-left: 30px;
                } 

                dentro la media query: @media (min-width: 768px) { ...

6) Aggiunta di un READ MORE all'elenco dei posts:

                <a class="read-more" href="{{ url_for('post_details', post_slug=post.slug) }}">Leggi articolo</a>

                .read-more {
                        color: #6c757d;
                        text-decoration: none;
                }

                .read-more:hover {
                        color: #343a40 !important;
                }

7) Aggiunta tasto di ritorno alla homepage in tutti i posts, aprire post_details.html e sotto la sezione del body inserire:

                <a class="btn btn-sm btn-outline-secondary" href="{{url_for('homepage')}}">Tutti i post</a>

8) Sistemazione area di aggiornamento del post:

                nel file pot_editor.html modificare in alto la sezione container in questo modo:

                <div class="container content-container mt-3 px-3 px-lg-0">

                in modo da aggiungere dello spazio ai margini in visualizzazione mobile.

9) Inserimento immagine in aggiornamento del post:

                {% if post_image  %}
                        <img class="img-fluid mb-3" src="{{ url_for( 'static', filename='img/posts/' + post_image )}}" alt="">
                {% endif%}

                modifica della rotta di update del post:

                post_image = post_instance.image or None
                return render_template("post_editor.html", form=form, post_image=post_image)











