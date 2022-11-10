from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from flask_pymongo import PyMongo

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

    # Var class options
    var_classes = mongo.db.variants.distinct("var_class")
    # Chr options
    chr_options = mongo.db.variants.distinct("mappings.0.seq_region_name")
    chr_options = [int(x) for x in chr_options]
    chr_options = sorted(chr_options)
    chr_options = [str(x) for x in chr_options]

    if request.method == "POST":
        var_cons = request.form["variant_consequence_search"]
        chrom = request.form["chromosome_search"]
        start = request.form["start_search"]
        end = request.form["end_search"]

        q_dict = {}
        if var_cons and var_cons != "NULL":
            q_dict["var_class"] = var_cons
        else: pass


        if chrom and chrom != "NULL":
            q_dict["mappings.0.seq_region_name"] = chrom
        else: pass

        if start and end:
            q_dict["mappings.0.start"] = {"$gte": int(start)}

            q_dict["mappings.0.end"] = {"$lte": int(end)}
        else: pass

        print(q_dict)
        query = variants.find(q_dict)
        query = query.limit(20)

    else:
        query = None
    return render_template('search.html',
                            r=query,
                            var_classes=var_classes,
                            chr_options=chr_options)

@app.route('/variant/<ObjectId:oid>')
def getvar(oid):
    q = {"_id":oid}
    print(q)
    record = mongo.db.variants.find_one_or_404(oid)
    print(list(record))
    return render_template('single_variant.html', variant = record)
