import MySQLdb
class Database(object):
    """description of class"""
    
def CreateConnection():
        database = "pendaftaranta"
        username = 'sa'
        password = 'sa123*'
        host = 'localhost'
        # Open database connection
        db = MySQLdb.connect(host=host, user=username, passwd=password, db=database )
        return db;

def ExecuteSql(query):
        db = CreateConnection()
        cursor = db.cursor()
        cursor.execute(query)
        return cursor

