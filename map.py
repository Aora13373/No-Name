import functools
import pymongo
import pandas as pd
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
from bson.json_util import dumps

bp = Blueprint('map', __name__)

@bp.route('/worldmap')
def index():
    db = get_db()
    mapjson = dumps(list(db.countries.geo.find({})))
    return render_template('map/index.html', geojson = mapjson)

@bp.route('/country', methods=('POST','GET'))
def country_stat():
    # If there is a POST request to this url, we generate content to return

    if request.method == 'POST':
        data = request.get_json()
        data = data['cname']
        db = get_db()
        country = db.country_data.find_one({"iso":data})
        units = db.units.find({})
        prop_units = dict()
        
        for unit in units:
            prop_units[unit["property"]] = unit["unit"]
            
        return render_template('map/country.html', data=country, units=prop_units)
    # If no POST request, redirect to the map index
    return redirect(url_for('map.index'))