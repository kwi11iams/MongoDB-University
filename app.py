from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/variantsdb"
mongo = PyMongo(app)
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
        else: pass

        if chrom: 
            q_dict["mappings.0.seq_region_name"] = chrom
        else: pass

        if start and end:
            q_dict["mappings.0.start"] = {"$gte": int(start)}            
            q_dict["mappings.0.end"] = {"$lte": int(end)}
        else: pass
            
        query = variants.find(q_dict)
        query = query.limit(20)

    else:
        query = None
    return render_template('search.html', r=query)

@app.route('/variant/<ObjectId:oid>', methods=('POST','GET'))
def getvar(oid):    
    if request.method == "POST":
        q_dict = {}
        q_dict["source"] = request.form["source"]
        q_dict["mappings.0.location"] = request.form["position"]
        q_dict["mappings.0.assembly_name"] = request.form["assembly"]
        q_dict["mappings.0.seq_region_name"] = request.form["chrom"]
        q_dict["mappings.0.strand"] = request.form["strand"]
        q_dict["name"] = request.form["name"]
        q_dict["MAF"] = request.form["MAF"]
        q_dict["ambiguity"] = request.form["ambiguity"]
        q_dict["var_class"] = request.form["var_class"]
        q_dict["synonyms"] = request.form["synonyms"]
        q_dict["evidence"] = request.form["evidence"]
        q_dict["ancestral_allele"] = request.form["a_allele"]
        q_dict["minor_allele"] = request.form["min_allele"]
        q_dict["consequence"] = request.form["consequence"]
        o_id = ObjectId(f'{oid}')
        mongo.db.variants.update_one({"_id":o_id},{"$set": q_dict})

    record = mongo.db.variants.find_one_or_404(oid)
    return render_template('single_variant.html', variant = record)

@app.route('/edit/<ObjectId:oid>', methods=('POST','GET'))
def editvar(oid):  
    record = mongo.db.variants.find_one_or_404(oid)
    return render_template('edit_variant.html', variant=record)