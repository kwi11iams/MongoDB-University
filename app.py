from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField)
from wtforms.validators import InputRequired, Length

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/variantsdb"
mongo = PyMongo(app)


@app.route('/', methods=('GET', 'POST'))
def home():
    return render_template('home.html')

@app.route('/add', methods=('GET', 'POST'))
def add():
    return render_template('add.html')

@app.route('/view', methods=('GET', 'POST'))
def viewdb():
    record = mongo.db.variants.find()
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
            
        print(q_dict)
        query = mongo.db.variants.find(q_dict)
        query = query.limit(20)

    else:
        query = None
    return render_template('search.html', r=query)

# class variant_form(FlaskForm):
#     def __init__():
#         ObjectId = StringField('ID')
#         source = StringField('source')
#         name = StringField('rsID')

@app.route('/variant/<ObjectId:oid>')
def getvar(oid):
    record = mongo.db.variants.find_one_or_404(oid)
    return render_template('single_variant.html', variant = record)
