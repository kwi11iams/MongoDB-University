from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.variantsdb
variants = db.variants


@app.route('/', methods=('GET', 'POST'))
def home():
    return render_template('base.html')

@app.route('/add', methods=('GET', 'POST'))
def add():
    return render_template('add.html')

@app.route('/view', methods=('GET', 'POST'))
def viewdb():
    record = variants.find()
    return render_template('datatable.html', r = record)


@app.route('/search', methods=('GET', 'POST'))
def searchdb():

    if request.method == "POST":
        var_cons = request.form["variant_consequence_search"]
        chrom = request.form["chromosome_search"]
        start = request.form["start_search"]
        end = request.form["end_search"]

        q_dict = {}
        if var_cons:
            q_dict["var_class"] = var_cons
        else:
            q_dict["var_class"] = ""
        if chrom:

        if chrom: 
            q_dict["mappings.0.seq_region_name"] = chrom
        else:
            q_dict["mappings.0.seq_region_name"] = ""

        if start and end:
            q_dict["mappings.0.start"] = {"$gte": int(start)}
            
            q_dict["mappings.0.end"] = {"$lte": int(end)}
            
        print(q_dict)
        query = variants.find(q_dict)
        query = query.limit(20)

    else:
        query = None
    return render_template('search.html', r=query)
