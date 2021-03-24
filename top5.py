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


bp = Blueprint('top5', __name__)
app = Flask(__name__)

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

@bp.route('/top5', methods=('POST','GET'))
def top5(params = ['GDP']):

    # Each plot should be generated from standalone functions,  no plot generating code should be in this function in the end.
    db = get_db()
    df = pd.DataFrame(db.country_data.find({}, {'GDP': 1, 'Country': 1}).sort('GDP', -1)[:5])

    ax = df.plot.bar()
    ax.set_xticklabels(df['Country'], rotation=45)
    
    fig = ax.get_figure()
    
    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    
    return render_template("top5/bar.html", image=pngImageB64String)
