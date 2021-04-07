import pandas as pd
from flask import(
    Flask, Response, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import io
import base64
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from worldfacts.db import get_db


bp = Blueprint('scandinavian', __name__)
app = Flask(__name__)

from matplotlib import rcParams
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
    #df = pd.read_csv('FactBook2.v3.csv')
    #t1 = df[df['Country'] == 'Norway']
    #t2 = df[df['Country'] == 'Sweden']
    #t3 = df[df['Country'] == 'Finland']
    #t4 = df[df['Country'] == 'Denmark']
      
    db = get_db()
    return_list = []
    

    countries = ['Norway', 'Sweeden', 'Denmark', 'Finland', 'Iceland']
    for prop in props:
        df = pd.DataFrame(db.country_data.find({'Country': {
            "$in": countries
        }}, {prop: 1, 'Country': 1}))

# Fjerner alle row's som er i dataframen men beholder columnsa og structuren
        #df = pd.DataFrame(columns=df.columns)
        #df = df.append(t1)
        #df = df.append(t2)
        #df = df.append(t3)
        #df = df.append(t4)
        
        ax = df.plot.bar()
        ax.set_xticklabels(df['Country'], rotation=45)
        fig = ax.get_figure()
  
        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        
        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        return_list.append(pngImageB64String)
    return return_list