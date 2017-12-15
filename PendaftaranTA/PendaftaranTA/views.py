"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, request, session, url_for, escape, redirect
from PendaftaranTA import app
from PendaftaranTA.Database import ExecuteSql
from PendaftaranTA.Mahasiswa import Mahasiswa, DaftarTA
from PendaftaranTA.Dosen import *

app.secret_key = 'gua kece karna gua kece'

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        loginInfo = checkLoginInfo()
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
    if(checkLoginInfo()=='login'):
        return render_template(
            'login.html',
            title='About',
            year=datetime.now().year,
            message='Your application description page.'
        )
    else:
        return logout()

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
    dosen = getDosenProfile(session['username'])
    keahlian = getKeahlian(dosen.id)
    return render_template(
        'biodata_dosen.html',
        title='About',
        year=datetime.now().year,
        profile = dosen
    )

@app.route('/biodata-mhs')
def biodata_mhs():
    mhss = Mahasiswa()
    pria = ''
    wanita = ''
    if(session['username']):
        mhss = mhss.getMahasiswaInfo(session['username'])
        if mhss.sex=='L':
            pria = 'checked'
        else:
            wanita = 'checked'
        return render_template(
            'biodata_mhs.html',
            title='Biodata Mahasiswa',
            mhs = mhss,
            Pria = pria,
            Wanita = wanita)
    else:
        return redirect(url_for('loginForm'))


@app.route('/input-ta')
def input_ta():
    "ambil daftar dosen"
    "ambil daftar ke"
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
    mahasiswa  = Mahasiswa()
    talist = mahasiswa.getListTa()
    return render_template(
        'ta.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.',
        daftarTA = talist
    )

@app.route('/actionLogin', methods=['POST'])
def actionLogin():
    if request.method=='POST':
        username =  request.form['username']
        password = request.form['password']
        loginAs = request.form['asRadio']
        if login(username, password, loginAs):
            return render_template(
            'index.html',
            title='login failed',
            message='Login Success'
            )
        else:
            return render_template(
            'login.html',
            title='login failed',
            message='Login Failed.'
            )
    return render_template(
        'about.html',
        title='fail',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/biodata-mhs-update', methods=['POST'])
def biodata_mhs_update():
    if request.method=='POST':
        mhss = Mahasiswa()
        mhss.id = request.form['mhsId']
        mhss.NIM = request.form['NRP']
        mhss.nama = request.form['nama']
        mhss.semester = request.form['semester']
        mhss.angkatan = request.form['angkatan']
        mhss.sex = request.form['sex']
        mhss.email = request.form['email']
        mhss.updateMahasiswa(mhss)
        
    return redirect(url_for('biodata_mhs'))
    


def logout():
    session.pop('username', None)
    session.pop('login', None)
    return redirect(url_for('home'))

def login(username, password, loginAs):

    query = ''
    if loginAs=='mahasiswa':
       query = "select count(*) from {0} where {1} = '{2}' AND password = '{3}' ".format('mahasiswa','id_mahasiswa' ,username, password)
    elif loginAs == 'dosen':
       query = "select count(*) from {0} where {1} = '{2}' AND password = '{3}' ".format('dosen', 'NIP',username, password)
    else:
       query = "select count(*) from {0} where {1} = '{2}' AND password = '{3}' ".format('admin', 'NIP',username, password)
    try:
        cursor =ExecuteSql(query)
        row = cursor.fetchone()
    except :
        pass
    if row[0]<=0:         
        return False
    session['username'] = username
    session['login'] = loginAs
    return True

def checkLoginInfo():
    if 'username' in session:
        return session['username']
    else:
        return 'login'

