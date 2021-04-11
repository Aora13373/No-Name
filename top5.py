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
bp = Blueprint('top5', __name__)
app = Flask(__name__)
rcParams.update({'figure.autolayout': True})

@bp.route('/top5', methods=('POST','GET'))
def top5(params = ['GDP']):

    # Each plot should be generated from standalone functions,  no plot generating code should be in this function in the end.
    db = get_db()

    properties = list(db.country_data.find_one({}).keys())
    remove = ['Country', "_id", "iso"]
    for rem in remove:
        properties.remove(rem)
    properties.sort()


    if request.method == 'POST':


        plots = generate_top_5(request.form)

        return render_template("top5/bar.html", images=plots, props=properties)
    else:
        return render_template("top5/welcome.html", props=properties)


def generate_top_5(props):

    db = get_db()
    return_list = []

    units = db.units.find({})
    prop_units = dict()
    
    for unit in units:
        prop_units[unit["property"]] = unit["unit"]

    for prop in props:

        df = pd.DataFrame(db.country_data.find({}, {prop: 1, 'Country': 1}).sort(prop, -1)[:5])



        # Defines the plot
        ax = df.plot.bar()
        ax.get_legend().remove()

        ax.set_xticklabels(df['Country'],fontsize=15,color='red',
                                fontfamily='sans-serif',fontstyle='italic',
                                fontvariant='small-caps',fontweight='heavy', rotation=15, ha='right')

        ax.set_title(prop,
                        fontsize=15,fontweight='heavy',fontvariant='normal',
                        fontfamily='sans-serif',color='green')
        if prop in prop_units.keys():
            ax.set_ylabel(prop_units[prop])  




        fig = ax.get_figure()

        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)

        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        return_list.append(pngImageB64String)

    return return_list
