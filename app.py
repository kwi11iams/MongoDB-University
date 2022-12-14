from flask import Flask, render_template, request, url_for, redirect, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import re

app = Flask(__name__)
app.secret_key='2049'
app.config["MONGO_URI"] = "mongodb://localhost:27017/variantsdb"
mongo = PyMongo(app)


@app.route('/', methods=('GET', 'POST'))
def home():
    '''
    render homepage usine home.html template
    '''
    return render_template('home.html')


@app.route('/view', methods=('GET', 'POST'))
def viewdb():
    '''
    View the whole MongoDB database in /view page.
    The variants are shown in a paginated, searchable table.
    '''
    record = mongo.db.variants.find()
    return render_template('datatable.html', r = record)


@app.route('/search', methods=('GET', 'POST'))
def searchdb():
    '''
    Search the database. The variants can be filtered based on various
    attributes.
    '''
    # Var class options
    var_classes = mongo.db.variants.distinct("var_class")
    # Chr options
    chr_options = mongo.db.variants.distinct("mappings.0.seq_region_name")
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    chr_options = sorted(chr_options, key = alphanum_key)

    # Most severe consequence options
    consequence = mongo.db.variants.distinct("most_severe_consequence")

    if request.method == "POST":

        # Accept querys from form on web page and add them to a dictionary
        var_type = request.form.getlist("variant_type_search")
        chrom = request.form["chromosome_search"]
        rsID = request.form["rsID"]
        var_cons = request.form.getlist("var_cons")
        start = request.form["start_search"]
        end = request.form["end_search"]

        q_dict = {}
        q_dict["$and"] = []
        if var_type and var_type != "NULL":
            or_qdict = {}
            or_qdict["$or"] = []
            for i in var_type:
                q = {"var_class":i}
                or_qdict["$or"].append(q)
            q_dict["$and"].append(or_qdict)

        if chrom and chrom != "NULL":
            q_dict["mappings.0.seq_region_name"] = chrom
        else: pass

        if rsID:
            q_dict["name"] = rsID
        else: pass

        if var_cons and var_cons != "NULL":
            or_qdict = {}
            or_qdict["$or"] = []
            for i in var_cons:
                q = {"most_severe_consequence":i}
                or_qdict["$or"].append(q)
            q_dict["$and"].append(or_qdict)
        else: pass

        if start and end:
            q_dict["mappings.0.start"] = {"$gte": int(start)}
            q_dict["mappings.0.end"] = {"$lte": int(end)}
        else: pass

        # Submit query to MongoDB database
        if q_dict["$and"] == []:
            q_dict.pop("$and",None)
        print(q_dict)
        query = mongo.db.variants.find(q_dict)
        count = mongo.db.variants.count_documents(q_dict)
        
        flash(f"Query returned {count} records",'info')
        query = query.limit(200)

    else:
        query = None

    # Render results on /search page
    return render_template('search.html',
                            r=query,
                            var_classes=var_classes,
                            chr_options=chr_options,
                            var_cons=consequence,
                            )


@app.route('/variant/<ObjectId:oid>', methods=('POST','GET'))
def getvar(oid):
    '''
    Display a single variant from MongoDB database in a table
    The url is the unique object ID for the variant
    '''
    record = mongo.db.variants.find_one_or_404(oid)
    return render_template('single_variant.html', variant = record)


@app.route('/edit/<ObjectId:oid>', methods=('POST','GET'))
def editvar(oid):
    '''
    Edit a single variant from the MongoDB database and display the edited
    variant
    '''
    if request.method == "POST":
        # Extract changes from form and add to query dictionary
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

        # Check chromosome is valid
        chrom_poss = list(range(1,22))
        chrom_poss = [str(x) for x in chrom_poss]
        chrom_poss.append(['X', 'Y'])
        if request.form["chrom"] not in chrom_poss:
            flash('Chromosome entry not valid, edits rejected and not saved.')
            return redirect(url_for('editvar', oid=o_id))

        # Update variant in MongoDB using the query dictionary
        mongo.db.variants.update_one({"_id":o_id},{"$set": q_dict})
        record = mongo.db.variants.find_one_or_404(oid)

        # Redirect to variant page to display output
        return redirect(url_for('getvar', oid=oid))

    # Display current variant, even if not changed
    record = mongo.db.variants.find_one_or_404(oid)
    return render_template('edit_variant.html', variant=record)
