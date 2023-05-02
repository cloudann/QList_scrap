from Database import *
class Sqlite(Database):
    #********
    #private
    #********
    import sqlite3 as sql3
    def __init__(self,db = "123.db",table = "kid"):
        self.db = self.sql3.connect(db)
        self.cursor = self.db.cursor()
        self.table = table
        self.type_db = 1
        self.create()
    #********
    #Public
    #********
    def create(self):
        try:
            self.cursor.execute("create table %s(id char(20),name varchar(255),origin char(20),init_id char(20));"%(self.table))
        except:
            print("表已存在")
    def get_attr(self):
        cmd = "pragma table_info(%s);"%(self.table)
        return super().get_attr(cmd)
    def Find(self,origin,init_id):
        return super().find("id",r'origin="%s" and init_id = "%s"'%(origin,init_id))
    def insert(self,lst):
        super().insert(lst)