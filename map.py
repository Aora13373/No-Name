import functools
import pymongo
import pandas as pd
from plotnine import (
    ggplot, geom_point, geom_bar, theme, element_text, aes
)
from flask import(
    Response, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import io
import base64
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import random
from worldfacts.db import get_db

bp = Blueprint('map', __name__)

@bp.route('/')
def index():
    return render_template('map/index.html', test="testing")

@bp.route('/country', methods=('POST','GET'))
def country_stat():
    # If there is a POST request to this url, we generate content to return

    if request.method == 'POST':
        data = request.get_json()
        data = data['cname']
        conn = pymongo.MongoClient()
        db = get_db()
        df = pd.DataFrame(db.country_data.find({
            "Country":data
        }))

        # Testing placeholder.  Create a plot, store it as an image and call the template with the url to the image as argument.  
        import os
        try:
            os.unlink('worldfacts/static/figure.jpg')
        except:
            pass
        plot = ( 
        ggplot(df)  
        + aes(x="Country", y="Life Expectancy At Birth")  
        + geom_point()  
        + theme(axis_text_x=element_text(rotation=90, hjust=1))
        )
        plot.save("worldfacts/static/figure.jpg")
        nocache_url = url_for('static', filename="figure.jpg") + "?" + str(random.randint(10000, 5000000))
        return render_template('map/country.html', url=nocache_url)

    # If no POST request, redirect to the map index
    return redirect(url_for('map.index'))