# Imports
from flask import(
    Flask, Response, Blueprint, flash, g, redirect, render_template, request, session, url_for)
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams
from worldfacts.db import get_db
import io
import base64
import matplotlib
import pandas as pd

matplotlib.use('Agg')
bp = Blueprint('scandinavian', __name__)
app = Flask(__name__)
rcParams.update({'figure.autolayout': True})

@bp.route('/scandinavia', methods=('POST','GET'))
def scandinavia(params = ['GDP']):
    '''Docstring'''

    db = get_db()
    properties = list(db.country_data.find_one({}).keys())
    remove = ['Country', "_id", "iso"]
    for rem in remove:
        properties.remove(rem)
    properties.sort()

    if request.method == 'POST':
        plots = generate_scandinavian(request.form)
        return render_template("scandinavian/bar.html", images=plots, props=properties)
    else:
        return render_template("scandinavian/welcome.html", props=properties)

def generate_scandinavian(props):
    '''Docstring'''

    db = get_db()
    countries = ['Norway', 'Sweden', 'Denmark', 'Finland', 'Iceland', 'Faroe Islands']
    return_list = []
    units = db.units.find({})
    prop_units = dict()
    for unit in units:
        prop_units[unit["property"]] = unit["unit"]

    for prop in props:
        df = pd.DataFrame(db.country_data.find({'Country': {
            "$in": countries}}, {prop: 1, 'Country': 1}))

        # Plot modifications
        df = df.replace([None], 0)
        ax = df.plot.bar(rot=0)
        ax.get_legend().remove()
        ax.set_xticklabels(df['Country'],fontsize=15,color='red',
                            fontfamily='sans-serif',fontstyle='italic',
                            fontvariant='small-caps',fontweight='heavy', rotation=15, ha="right")
        ax.set_title(prop,
                            fontsize=15,fontweight='heavy',fontvariant='normal',
                            fontfamily='sans-serif',color='green')
        if prop in prop_units.keys():
            ax.set_ylabel(prop_units[prop])
        fig = ax.get_figure()

        # Converts plot --> PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)

        # Encodes PNG image --> base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        return_list.append(pngImageB64String)
    return return_list
