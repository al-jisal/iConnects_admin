from flask import Blueprint, render_template, redirect, url_for

main_blueprint = Blueprint('index', __name__)

@main_blueprint.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@main_blueprint.route('/submit_query', methods=['GET', 'POST'])
def submit_query():
    pass