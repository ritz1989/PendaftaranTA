import MySQLdb
class DatabaseHandler(object):
    """description of class"""
    def CreateConnection():
        database = "pendaftaran_TA"
        username = 'sa'
        password = 'sa123*'
        host = 'localhost'
        # Open database connection
        db = MySQLdb.connect(host=host, user=username, passwd=password, db=database )
        return db;

    def ExecuteSql(query, handle):
        db = CreateConnection()
        cursor = db.cursor
        cursor.execute(query)
        handle
        return cursor
    
