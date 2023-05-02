from Database import *
class RemoteSql(Database):
    def __init__(self):
        super().__init__()
        self.type_db = 0
        self.table = "problem"
    #只读操作修正
    def insert(self,info):
        print("添加操作违法")
    def release(self):
        print("释放操作违法")
    def create(self):
        print("新建操作违法")
    def commit(self):
        print("提交操作违法")
    def del_tab(self):
        print("删除操作违法")
    
    def get_attr(self):
        cmd = "describe %s;"%(self.table)
        return super().get_attr(cmd)
    def Find(self):
        return super().find("problem_id,title","True")
    def get_data(self):
        lst = []
        #print(self.Find())
        for i in self.Find():#可以向上抽象
            cur = list(i)
            for j in range(len(cur)):
                if type(cur[j]) == str:
                    cur[j] = cur[j].strip()
            lst.append({"id":cur[0],"name":cur[1]})
        return lst 