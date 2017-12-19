"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, request, session, url_for, escape, redirect, jsonify
from PendaftaranTA import app
from PendaftaranTA.Database import ExecuteSql
from PendaftaranTA.Mahasiswa import *
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
    tas = getTugasAkhirBimbingan(session['username'])
    return render_template(
        'approve_dosen.html',
        title='Manajemen Tugas Akhir Mahasiswa',
        year=datetime.now().year,
        message='Your application description page.',
        datas = tas
    )

@app.route('/update-ta', methods=['POST', 'GET'])
def update_ta():
    if request.method=='POST':
        data = request.form['taId']
        updateTaMhs(request.form['taId'],request.form['aksi'])
    elif request.method=='GET':
        taid = request.args.get('taid')
        aksi = request.args.get('aksi')
        updateTaMhs(taid,aksi)
    return redirect(url_for('approve_dosen'))


@app.route('/biodata-dosen')
def biodata_dosen():
    pria = ''
    wanita = ''
    dosen = getDosenProfile(session['username'])
    dosen.keahlian = getKeahlianDosen(dosen.NIP)
    if dosen.jenis_kelamin=='L':
            pria = 'checked'
    else:
            wanita = 'checked'
    keahlian = getAllKeahlian()
    for ahli in keahlian:
        for d in dosen.keahlian:
            if d.id == ahli.id:
                ahli._ui_checked = "checked"
    return render_template(
        'biodata_dosen.html',
        title='About',
        year=datetime.now().year,
        profile = dosen,
        keahlians = keahlian,
        Pria = pria,
        Wanita = wanita
    )

@app.route('/tambah-keahlian')
def tambah_keahlian():
    if request.method=='POST':
        keahlian = request.form['keahlian']
        insertKeahlian(keahlian)
    return keahlian

@app.route('/biodata-dosen-update', methods=['POST'])
def biodata_dosen_update():
    if request.method=='POST':
        dosen = Dosen()
        dosen.id = request.form['dsnId']
        dosen.NIP = request.form['NIP']
        dosen.nama = request.form['nama']
        dosen.jenis_kelamin = request.form['sex']
        dosen.email = request.form['email']
        dosen.keahlian = request.form.getlist('keahlian')
        updateProfileDosen(dosen)
    return redirect(url_for('biodata_dosen'))

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
    if validasi_pendaftaranTA(session['username']):
        Keahlian = getAllKeahlian()
        dsn = getAllDosen()
        return render_template(
            'input_ta.html',
            title='About',
            keahlian=Keahlian,
            year=datetime.now().year,
            dosen = dsn
        )
    else:
        talist = getTaMhs(session['username'])
    return render_template(
        'ta.html',
        title='Daftar Tugas Akhir',
        year=datetime.now().year,
        message='Anda tidak dapat mendaftar tugas akhir. silahkan hubungi dosen anda untuk membatalkan tugas akhir yang telah terdaftar.',
        daftarTA = talist
    )

@app.route('/input-ta-pilih-dosen', methods=['POST'])
def input_ta_pilih_dosen():
    if request.method=='POST':
        dat = dataTa()
        dat.judul = request.form['judul']
        dat.id_keahlian = request.form['keahlian']
        dat.overview = request.form['overview']
        dosen = getDosenByKeahlian(dat.id_keahlian)
    return render_template(
        'pilih_dosen.html',
        title='Pilih Pembimbing',
        daftarDosen=dosen,
        year=datetime.now().year,
        data = dat
    )

@app.route('/daftar-ta', methods=['POST'])
def daftar_ta():
    if request.method=='POST':
        dat = dataTa()
        dat.judul = request.form['judul']
        dat.id_keahlian = request.form['keahlian']
        dat.overview = request.form['overview']
        dat.id_dosen = request.form['id_dosen']
        daftarTa(dat, session['username'])
    return (redirect(url_for('ta')))



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
        message='Daftar Tugas Akhir Mahasiswa.',
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

