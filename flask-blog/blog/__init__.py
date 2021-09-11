from flask import Flask

app = Flask(__name__)

# TODO: qui dentro andiamo ad inizializzare il db ecc...le view saranno contenuto all'interno di routes.py

# è molto importante scrivere qui al fondo questo import per prevenire errore di Circular Import
from blog import routes