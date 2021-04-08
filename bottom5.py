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


bp = Blueprint('bottom5', __name__)
app = Flask(__name__)

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

@bp.route('/bottom5', methods=('POST','GET'))
def bottom5(params = ['GDP']):

    db = get_db()

    properties = list(db.country_data.find_one({}).keys())
    remove = ['Country', "_id", "iso"]
    for rem in remove:
        properties.remove(rem)
    properties.sort()


    if request.method == 'POST':
        

        plots = generate_bottom_5(request.form)
        
        return render_template("bottom5/bar.html", images=plots, props=properties)
    else:
        return render_template("bottom5/welcome.html", props=properties)


def generate_bottom_5(props):

    db = get_db()
    return_list = []
    for prop in props:

        df = pd.DataFrame(db.country_data.find({prop: {"$ne": None}}, {prop: 1, 'Country': 1}).sort(prop, 1)[:5])

        # Defines the plot
        ax = df.plot.bar(rot=0)
        
        ax.set_xticklabels(df['Country'],fontsize=20,color='red',
                                fontfamily='sans-serif',fontstyle='italic',
                                fontvariant='small-caps',fontweight='heavy')
        ax.set_title('Bottom 5 Countries', 
                        fontsize=20,fontweight='heavy',fontvariant='normal',
                        fontfamily='sans-serif',color='green')
        
        fig = ax.get_figure()
        
        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        
        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        return_list.append(pngImageB64String)

    return return_list