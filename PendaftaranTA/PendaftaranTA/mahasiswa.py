from PendaftaranTA.Database import ExecuteSql, CreateConnection
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
            {0},
            {1},
            {2},
            {3},
            {4},
            {5},
            {6},
            {7};
            """.format(mhs.NIM, mhs.nama,mhs.semester, mhs.angkatan, mhs.password, mhs.email, mhs.sex, mhs.ta_id)
            rowcount = ExecuteSql(query)
            return rowcount
