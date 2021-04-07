from flask import(
    Flask, Response, Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('index', __name__)
app = Flask(__name__)

@bp.route('/')
def index():    
    return render_template('index/index.html')