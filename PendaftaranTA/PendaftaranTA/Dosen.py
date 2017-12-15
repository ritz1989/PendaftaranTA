from PendaftaranTA.Database import ExecuteSql, CreateConnection, ExecuteNonQuery
from PendaftaranTA.views import *

def getDosenProfile(NIP):
    queryDosen = "select id, NIP ,nama, jenis_kelamin, email from dosen where NIP = '{0}'".format(NIP)
    cusrsor = ExecuteSql(queryDosen)
    result = cusrsor.fetchone()
    dosen = Dosen()
    dosen.id = result[0]
    dosen.NIP = result[1]
    dosen.nama = result[2]
    dosen.jenis_kelamin = result[3]
    dosen.email = result[4]
    return dosen;


def updateProfileDosen(dosen):
    updateQuery = "update dosen set NIP = '{0}', nama = '{1}', jenis_kelamin = '{2}', email = '{3}' where id = '{4}'".format(dosen.NIP, dosen.nama, dosen.jenis_kelamin, dosen.email, dosen.id)
    ExecuteNonQuery(updateQuery)
    return

def getKeahlian(id):
    query = ""

class Dosen():
    id = 0
    NIP = ''
    nama = ''
    jenis_kelamin = ''
    email = ''