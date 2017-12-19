from PendaftaranTA.Database import ExecuteSql, CreateConnection, ExecuteNonQuery, ExecuteNonQueries
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
    deleteQuery = "delete from dosen_has_lingkup_keahlian where dosen_id = '{0}'".format(dosen.id)
    ExecuteNonQuery(deleteQuery)
    queries = []
    queries.append("update dosen set NIP = '{0}', nama = '{1}', jenis_kelamin = '{2}', email = '{3}' where id = '{4}'".format(dosen.NIP, dosen.nama, dosen.jenis_kelamin, dosen.email, dosen.id))
    for k in dosen.keahlian:
        queries.append("insert into dosen_has_lingkup_keahlian (dosen_id, lingkup_keahlian_id) values ('{0}','{1}')".format(dosen.id, k))
    ExecuteNonQueries(queries)
    return

def getKeahlianDosen(NIP):
    query = """select lingkup_keahlian.id, lingkup_keahlian.keahlian from lingkup_keahlian
            join dosen_has_lingkup_keahlian on dosen_has_lingkup_keahlian.lingkup_keahlian_id = lingkup_keahlian.id
            join dosen on dosen.id = dosen_has_lingkup_keahlian.dosen_id
            where dosen.NIP = '{0}'""".format(NIP)
    cursor = ExecuteSql(query)
    results  = cursor.fetchall()
    keahlian = mapKeahlian(results)
    return keahlian

def getDosenByKeahlian(keahlian_id):
    query = """select dosen.id, dosen.NIP, dosen.Nama from dosen
                join dosen_has_lingkup_keahlian on dosen_has_lingkup_keahlian.dosen_id = dosen.id
                join lingkup_keahlian on lingkup_keahlian.id = dosen_has_lingkup_keahlian.lingkup_keahlian_id
                where lingkup_keahlian.id = '{0}'""".format(keahlian_id)
    cursor = ExecuteSql(query)
    return cursor.fetchall()

def getAllDosen():
    query = "select dosen.id, dosen.NIP, dosen.Nama from dosen"
    cursor = ExecuteSql(query)
    return cursor.fetchall()


def mapKeahlian(results):
    keahlians = []
    for row in results:
        keahlian = Keahlian()
        keahlian.id = row[0]
        keahlian.keahlian = row[1]
        keahlians.append(keahlian)
    return keahlians

def getAllKeahlian():
    query = "select id, keahlian from lingkup_keahlian"
    cursor = ExecuteSql(query)
    results  = cursor.fetchall()
    keahlian = mapKeahlian(results)
    return keahlian

def insertKeahlian(name):
    q1 = """INSERT INTO `lingkup_keahlian` (`keahlian`) VALUES ('{0}')""".format(name)
    ExecuteNonQuery(q1)
    return

class Dosen():
    id = 0
    NIP = ''
    nama = ''
    jenis_kelamin = ''
    email = ''
    keahlian = []

class Keahlian():
    id = 0
    keahlian = ''
    _ui_checked = ''

def getTugasAkhirBimbingan(NIP):
    query = """select 
			mahasiswa.id_mahasiswa,
            nama_mahasiswa,
            tugas_akhir.Judul,
            tugas_akhir.status,
            tugas_akhir.id
            from mahasiswa
            join tugas_akhir on mahasiswa.Tugas_Akhir_id = tugas_akhir.id
            join dosen on tugas_akhir.id_dosen = dosen.id
            where dosen.NIP = '{0}'""".format(NIP)
    cursor = ExecuteSql(query)
    return cursor.fetchall()

def updateTaMhs(taid, status):
    query = "update tugas_akhir set status = '{0}' where id = '{1}'".format(status, taid)
    return ExecuteNonQuery(query)