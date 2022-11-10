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
<<<<<<< HEAD
    return render_template('index.html', r = record)
=======
    return render_template('datatable.html', r = record)
>>>>>>> 11be5ef6c886853a3de63ecbaa52bf9ac8e6a014


@app.route('/search', methods=('GET', 'POST'))
def searchdb():
<<<<<<< HEAD
    if request.method == "POST":
        var_cons = request.form["variant_consequence_search"]
        chrom = request.form["chromosome_search"]

        # if var_cons:
        #     query = query.find({"var_class":var_cons})
        # if chrom:
        #     query = query.find({"mappings.0.seq_region_name":chrom})
=======

    if request.method == "POST":
        var_cons = request.form["variant_consequence_search"]
        chrom = request.form["chromosome_search"]
        start = request.form["start_search"]
        end = request.form["end_search"]

>>>>>>> 11be5ef6c886853a3de63ecbaa52bf9ac8e6a014
        q_dict = {}
        if var_cons:
            q_dict["var_class"] = var_cons
        else:
            q_dict["var_class"] = ""
<<<<<<< HEAD
=======


>>>>>>> 11be5ef6c886853a3de63ecbaa52bf9ac8e6a014
        if chrom: 
            q_dict["mappings.0.seq_region_name"] = chrom
        else:
            q_dict["mappings.0.seq_region_name"] = ""

<<<<<<< HEAD

        query = variants.find(q_dict)
        query = query.limit(20)
        print(type(query))
    else:
        query = ["nothin to see ere"]
    return render_template('search.html', records = query)
=======
        if start and end:
            q_dict["mappings.0.start"] = {"$gte": int(start)}
            
            q_dict["mappings.0.end"] = {"$lte": int(end)}
            
        print(q_dict)
        query = variants.find(q_dict)
        query = query.limit(20)

    else:
        query = None
    return render_template('search.html', r=query)
>>>>>>> 11be5ef6c886853a3de63ecbaa52bf9ac8e6a014
