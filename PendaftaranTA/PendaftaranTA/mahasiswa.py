from PendaftaranTA.Database import *
from PendaftaranTA.views import *

class Mahasiswa(object):
    """description of class"""
    id = 0
    NIM = ''
    nama = ''
    semester = 0
    angkatan = 0
    sex = ''
    dosen_pembimbing = ''
    judul_TA = ''
    email = ''
    ta_id = 0
    password = ''

    def mapToMhs(self ,mhs):
        mhss = Mahasiswa()
        mhss.id = mhs[0]
        mhss.NIM = mhs[1]
        mhss.nama = mhs[2]
        mhss.semester = mhs[3]
        mhss.angkatan = mhs[4]
        mhss.dosen_pembimbing = mhs[6]
        mhss.judul_TA = mhs[7]
        mhss.sex = mhs[5]
        mhss.email = mhs[8]
        ta_id = mhs[9]
        return mhss

    def getMahasiswas(self):
        cursor = ExecuteSql("""
        SELECT mahasiswa.id as id, 
        id_mahasiswa as NIM, 
        nama_mahasiswa as nama,
        semester,
        angkatan,
        mahasiswa.jenis_kelamin as sex,
        dosen.Nama as dosen_pembimbing,
        Judul as judul,
        mahasiswa.email as email,
        mahasiswa.Tugas_Akhir_id as ta_id
        FROM mahasiswa
        left join tugas_akhir on mahasiswa.Tugas_Akhir_id = tugas_akhir.id
        left join dosen on tugas_akhir.id_dosen = dosen.id
        """)
        result = cursor.fetchall()
        mahasiswas = []
        for mhs in result:
            mhss = self.mapToMhs(mhs)
            mahasiswas.append(mhss)
    
    def getMahasiswaInfo(self,NRP):
        query = """
        SELECT mahasiswa.id as id, 
        id_mahasiswa as NIM, 
        nama_mahasiswa as nama,
        semester,
        angkatan,
        mahasiswa.jenis_kelamin as sex,
        dosen.Nama as dosen_pembimbing,
        Judul as judul,
        mahasiswa.email as email,
        mahasiswa.Tugas_Akhir_id
        FROM mahasiswa
        left join tugas_akhir on mahasiswa.Tugas_Akhir_id = tugas_akhir.id
        left join dosen on tugas_akhir.id_dosen = dosen.id
        where mahasiswa.id_mahasiswa = '{0}'""".format(NRP)
        result = ExecuteSql(query).fetchone()
        return self.mapToMhs(result)

    def updateMahasiswa(self, mhs):
            query = """
            UPDATE `pendaftaranta`.`mahasiswa`
            SET
            `id_mahasiswa` = '{0}',
            `nama_mahasiswa` = '{1}',
            `semester` = '{2}',
            `angkatan` = '{3}',
            `email` = '{4}',
            `jenis_kelamin` = '{5}'
            WHERE `id` = '{6}';
            """.format(mhs.NIM, mhs.nama,mhs.semester, mhs.angkatan, mhs.email, mhs.sex, mhs.id)
            db = CreateConnection()
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()
            db.close()
            return

   
    def insertMahasiswa():
            query = """
            INSERT INTO `pendaftaranta`.`mahasiswa`
            (`id_mahasiswa`,
            `nama_mahasiswa`,
            `semester`,
            `angkatan`,
            `password`,
            `email`,
            `jenis_kelamin`,
            `Tugas_Akhir_id`)
            VALUES
            '{0}',
            '{1}',
            '{2}',
            '{3}',
            '{4}',
            '{5}',
            '{6}',
            '{7}';
            """.format(mhs.NIM, mhs.nama,mhs.semester, mhs.angkatan, mhs.password, mhs.email, mhs.sex, mhs.ta_id)
            rowcount = ExecuteSql(query)
            return rowcount
      
    def getListTa(self):
         query = """
         select 
			mahasiswa.id_mahasiswa,
            nama_mahasiswa,
            semester,
            angkatan,
            tugas_akhir.Judul,
            dosen.Nama,
            dosen.NIP,
            tugas_akhir.status,
            tugas_akhir.id
            from mahasiswa
            join tugas_akhir on mahasiswa.Tugas_Akhir_id = tugas_akhir.id
            join dosen on tugas_akhir.id_dosen = dosen.id order by tugas_akhir.id desc
         """
         cursor = ExecuteSql(query)
         result = cursor.fetchall()
         hasil = []
         for hsl in result:
            daftarTA = DaftarTA()
            daftarTA.id_mahasiswa = hsl[0]
            daftarTA.nama_mahasiswa = hsl[1]
            daftarTA.semester = hsl[2]
            daftarTA.angkatan = hsl[3]
            daftarTA.judul = hsl[4]
            daftarTA.namaDosen = hsl[5]
            daftarTA.nipDosen=hsl[6]
            daftarTA.statusTA = hsl[7]
            daftarTA.idTa = hsl[8]
            hasil.append(daftarTA)
         return hasil

class DaftarTA():
    id_mahasiswa = 0
    nama_mahasiswa = ''
    semester = 0
    angkatan = 0
    judul = ''
    namaDosen = ''
    nipDosen=''
    statusTA = ''
    idTa = ''

class dataTa():
    judul=''
    id_keahlian = 0
    overview = ''
    id_dosen = ''

def daftarTa(dataTa, nrp):
    query = "select id from mahasiswa where id_mahasiswa = '{0}'".format(nrp)
    res = ExecuteSql(query).fetchone()
    idMhs = res[0]
    queries = []
    queries.append("INSERT INTO `tugas_akhir`(`id_dosen`,`Judul`,`Topik`,`status`,`overview`,`id_mahasiswa`) VALUES ('{0}', '{1}', '{2}', 'baru', '{3}', '{4}')".format(dataTa.id_dosen, dataTa.judul, dataTa.id_keahlian, dataTa.overview, idMhs))
    queries.append("update mahasiswa set tugas_akhir_id = LAST_INSERT_ID() where id_mahasiswa = '{0}'".format(nrp))
    return ExecuteNonQueries(queries)

def validasi_pendaftaranTA(nrp):
    query = """select count(*) from tugas_akhir
            join mahasiswa on tugas_akhir.id_mahasiswa = mahasiswa.id
            where mahasiswa.id_mahasiswa = '{0}' AND (tugas_akhir.status='aktif' OR tugas_akhir.status='baru');
            """.format(nrp)
    cur = ExecuteSql(query)
    res = cur.fetchone()
    if(res[0]>0):
        return False
    else:
        return True

def getTaMhs(nrp):
    query = """select 
			mahasiswa.id_mahasiswa,
            nama_mahasiswa,
            semester,
            angkatan,
            tugas_akhir.Judul,
            dosen.Nama,
            dosen.NIP,
            tugas_akhir.status,
            tugas_akhir.id
            from mahasiswa
            join tugas_akhir on mahasiswa.Tugas_Akhir_id = tugas_akhir.id or tugas_akhir.id_mahasiswa = mahasiswa.id
            join dosen on tugas_akhir.id_dosen = dosen.id 
            where mahasiswa.id_mahasiswa = '{0}' order by tugas_akhir.id desc;""".format(nrp)
    cur = ExecuteSql(query)
    res = cur.fetchall()
    hasil = []
    for hsl in res:
            daftarTA = DaftarTA()
            daftarTA.id_mahasiswa = hsl[0]
            daftarTA.nama_mahasiswa = hsl[1]
            daftarTA.semester = hsl[2]
            daftarTA.angkatan = hsl[3]
            daftarTA.judul = hsl[4]
            daftarTA.namaDosen = hsl[5]
            daftarTA.nipDosen=hsl[6]
            daftarTA.statusTA = hsl[7]
            daftarTA.idTa = hsl[8]
            hasil.append(daftarTA)
    return hasil