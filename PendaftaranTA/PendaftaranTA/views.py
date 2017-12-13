"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, request, session, url_for, escape, redirect
from PendaftaranTA import app

app.secret_key = 'gua kece karna gua kece'

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/login')
def loginForm():
    """Renders the about page."""
    return render_template(
        'login.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/approve-dosen')
def approve_dosen():
    """Renders the about page."""
    return render_template(
        'approve_dosen.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/biodata-dosen')
def biodata_dosen():
    """Renders the about page."""
    return render_template(
        'biodata_dosen.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/biodata-mhs')
def biodata_mhs():
    """Renders the about page."""
    return render_template(
        'biodata_mhs.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/input-ta')
def input_ta():
    """Renders the about page."""
    return render_template(
        'input_ta.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/lab')
def lab():
    """Renders the about page."""
    return render_template(
        'lab.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/ta')
def ta():
    """Renders the about page."""
    return render_template(
        'ta.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/actionLogin', methods=['POST'])
def actionLogin():
    if request.method=='POST':
        username =  request.form['username']
        password = request.form['password']
        loginAs = request.form['asRadio']
        session['username'] = username
        session['login'] = loginAs
        return redirect(url_for('home'))
    return render_template(
        'about.html',
        title='fail',
        year=datetime.now().year,
        message='Your application description page.'
    )

def clearSession():
    session.pop('username', None)
    session.pop('login', None)
