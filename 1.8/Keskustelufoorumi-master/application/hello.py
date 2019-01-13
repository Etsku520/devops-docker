from flask import render_template, url_for
from application import app

class Item:
    def __init__(self, nimi):
        self.nimi = nimi

nimi = "Richard Smith"

lista = [1, 3, 5, 11, 6, 17, 28]

esineet = []
esineet.append(Item("Kivi"))
esineet.append(Item("Tuoli"))
esineet.append(Item("Vaasi"))
esineet.append(Item("Juustoraastin"))
esineet.append(Item("Kukkakaali"))

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/demo")
def content():
    return render_template("demo.html", nimi = nimi, lista=lista, esineet=esineet)
    