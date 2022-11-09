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
        var_cons = request.form["variant_consequence_search"]
        chrom = request.form["chromosome_search"]

        # if var_cons:
        #     query = query.find({"var_class":var_cons})
        # if chrom:
        #     query = query.find({"mappings.0.seq_region_name":chrom})
        if var_cons:
            q1 = f'"var_class":{var_cons}'
        else: q1 = ""
        if chrom:
            q2 = f'"mappings.0.seq_region_name":{chrom}'
        else: q2 = ""

        query = variants.find({q1})
    else:
        query = ["nothin to see ere"]
    return render_template('search.html', records = query)
