from flask import Flask, render_template, request
from problog.engine import DefaultEngine
from custom_predicates import find_user_prob
app = Flask(__name__)

engine = DefaultEngine()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/view', methods=['POST'])
def view_prob():
    id = request.form['id']
    query = 'infect("'+id+'")'
    r = find_user_prob(query, engine)
    l = list(r.keys())  # Bisogna manualmente estrarre la chiave perchèì è in un formato strano (non stringa)
    return render_template("view_prob.html", id=id, prob=r[l[0]])


@app.route('/view_all', methods=['GET'])
def view_all():
    query = "infect(_)"
    r = find_user_prob(query, engine)
    items = []
    for key, value in r.items():
        start = "infect("
        end = ")"
        result = str(key)[len(start):-len(end)]
        items.append((result, value))

    return render_template("view_all.html", items=items)
