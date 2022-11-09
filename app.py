from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.variantsdb
variants = db.variants


@app.route('/', methods=('GET', 'POST'))
def home():
    return render_template('base.html')

@app.route('/view', methods=('GET', 'POST'))
def viewdb():
    record = variants.find()
    return render_template('datatable.html', r = record)
