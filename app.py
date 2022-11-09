from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.variantsdb
variants = db.variants


@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

@app.route('/view', methods=('GET', 'POST'))
def viewdb():
    record = variants.find()
    return render_template('index.html', r = record)


@app.route('/search', methods=('GET', 'POST'))
def searchdb():
    if request.method == "POST":
        search = request.form["s_para"]
        result = variants.find({"var_class":search})
    else:
        result = ["nothin to see ere"]
    return render_template('search.html', records = result)