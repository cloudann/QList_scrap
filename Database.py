import init
init.init()
class Database:
     
    #Variable
    #---------
    
    #Public
    #********
    db = None
    cursor = None
    #Private
    #********
    out_str = None
    host = None
    user = None
    pwd = None
    database = None
    port = None
    type_db = None
    table = None
    import pymysql as Sql
    import re
    import threading as thread
    #++++++++
    #Function
    #++++++++
    
    #********
    #Private
    #********
    def __init__(self,host,user,pwd,database,port=3306):

        self.set(host,user,pwd,database,port)
        self.connect()
    def __del__(self):
        self.cursor.close()
        self.db.close()
        print("数据库关闭")
    def to_list(self,x):
        lst = []
        for i in x:
            lst.append(i[self.type_db])
        return lst
    def to_str(self,Str):
        return str(Str)[1:-1]
    def check(self,id):
        return len(self.find("*",' id = "%s"'%(str(id))))>0

    #*******
    #public
    #*******
    def set(self,host,user,pwd,database,port=3306):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.database = database
        self.port = port
    def connect(self):
        self.db = self.Sql.connect(host = self.host,user = self.user,password = self.pwd,database= self.database,port = self.port)
        self.cursor = self.db.cursor()
        print("开启%s数据库"%(self.database))
    #执行
    def commit(self):
        self.db.commit()
    def execute(self,cmd):
        self.cursor.execute(cmd)
        
    #获取
    def output(self):
        return self.cursor.fetchall()
    def show(self):
        print(self.output())
            #print(x)
            #此处缓存就没有问题
    def get_tab(self):
        self.execute(r'select * from %s;'%(self.table))
        self.show()
    def get_attr(self,cmd):
        self.execute(cmd)
        return self.to_str(self.to_list(self.output()))
        
    #创建表
    def create(self):
        name = input("请输入新建表名")
        try:
            num = int(input("请输入表的元素个数"))
        except:
            print("请输入数字请重新执行创建操作")
            return
        lst = []
        regex = r'[\S]+\s[a-zA-Z]+\([0-9]+\)'
        pattern = self.re.compile(regex)
        for i in range(num):
            info = input("请输入属性信息 如 id char(20)")
            if pattern.findall(info):
                lst.append(info)
            else:
                print("输入格式错误,创建失败")
                return
        lst = self.to_str(lst)
        lst = r'create table %s(%s);'%(name,lst)
        self.execute(lst)
        self.commit()
    #删除表数据    
    def del_tab(self):
        name = input("请输入要删除的表名")
        self.execute('drop table %s;'%(name))
        self.commit()
    
    #插入
    def insert(self,info):
        #print(self.table)
        attr = None
        attr = self.get_attr()
        if type(info)!=str:
            for i in range(len(info)):
                info[i] = str(info[i])
            info = self.to_str(info)
        cmd = r'insert into %s(%s) values( %s )'%(self.table,attr,info)
        #print(cmd)
        self.execute(cmd)
        self.commit()
    def release(self):
        self.execute("delete from %s;"%(self.table))
        self.commit()
    def find(self,info,check="True"):
        self.execute("select %s from %s where %s;"%(info,self.table,check))

        return self.output() 
    
    def set_tab(self,table):
        self.table = table