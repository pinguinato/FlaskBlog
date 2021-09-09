# Appunti Importanti Flask

/c/progetti/python-flask/FlaskBlog

        pip list

        Package    Version
        ---------- -------
        pip        20.2.1
        setuptools 49.2.1

        pip install Flask

        pip list

        Package      Version
        ------------ -------
        click        8.0.1
        colorama     0.4.4
        Flask        2.0.1
        itsdangerous 2.0.1
        Jinja2       3.0.1
        MarkupSafe   2.0.1
        pip          20.2.1
        setuptools   49.2.1
        Werkzeug     2.0.1

        

## Attivazione ambiente virtuale (virtual env)

Dentro la cartella del nostro progetto:

        python -m venv venv

        source venv/Scripts/activate

Far puntare VsCode al virtual env creato: CTRL + SHIFT + P e ti cerchi il virtual env (venv/Scripts/python.exe)

Creo un file **application.py** dentro il percorso -> /c/progetti/python-flask/FlaskBlog/hello_flask

per avviarlo, prima di tutto settare la var di ambiente APP_FLASK in un terminale git-bash:

        export FLASK_APP=application.py

per avviarlo e attivare le modifiche senza dover riavviare il server, bisogna dire a Flask che siamo in ambiente di sviluppo, quindi bisogna creare una seconda variabile d'ambiente e settarla(debug mode ON):

        export FLASK_ENV=development

A questo punto dare il comando:

        flask run

Output previsto:

        * Serving Flask app 'application.py' (lazy loading)
        * Environment: development
        * Debug mode: on
        * Restarting with stat
        * Debugger is active!
        * Debugger PIN: 521-492-981
        * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)


