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

