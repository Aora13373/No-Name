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
    properties = list(db.country_data.find_one({}).keys())[2:-1]   

    if request.method == 'POST':
        plots = generate_scandinavian(request.form)
        return render_template("scandinavian/bar.html", images=plots, props=properties)
    else:
        return render_template("scandinavian/welcome.html", props=properties)

def generate_scandinavian(props):
    '''Docstring'''

    db = get_db()
    countries = ['Norway', 'Sweeden', 'Denmark', 'Finland', 'Iceland']
    return_list = []
    
    for prop in props:
        df = pd.DataFrame(db.country_data.find({'Country': {
            "$in": countries}}, {prop: 1, 'Country': 1}))

        # Plot modifications
        ax = df.plot.bar(rot=0)
        ax.set_xticklabels(df['Country'],fontsize=20,color='red',
                            fontfamily='sans-serif',fontstyle='italic',
                            fontvariant='small-caps',fontweight='heavy')
        ax.set_title('Scandinavian Countries', 
                            fontsize=20,fontweight='heavy',fontvariant='normal',
                            fontfamily='sans-serif',color='green')
        fig = ax.get_figure()
  
        # Converts plot --> PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        
        # Encodes PNG image --> base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        return_list.append(pngImageB64String)
    return return_list