
from Scrap import *
from Database import *
from Sqlite import *
from OJ import *
from RemoteSql import *
class Scr_Qlist(Sqlite):
    #--------
    #Variable
    #--------
    
    regex_get = r'(.*\()[\s]*([\S]+[-\s])[-\s]*([\S]+(\s|\)))'
    regex_write = r'<span><span style="white-space:normal;">\[plist=[0-9,]*\].*\[/plist\]</span><br />'
    #Private
    #*******
    
    remote = RemoteSql()
    LG = scrLG()
    DF = scrDF()
    opj = scrOpJ()
    
    def __init__(self):
        super().__init__(db = "123.db",table = "kid123")
        self.regex_get = self.re.compile(self.regex_get)
        self.regex_write = self.re.compile(self.regex_write)
        self.introduce()
    #**********************************
    #Find 方法
    #**********************************
    def Find_origin(self,origin):
        print(self.find("*",r'origin="%s" '%(origin)))
    def Find(self,origin,init_id):
        #print("%s"%(init_id))
        return super().Find(origin,init_id)
    
    #**********************************
    #get 方法
    #**********************************
    def get(self,info):
        id = info["id"]
        name = info["name"]
        x = self.regex_get.findall(name)
        (origin,init_id) = ("None" for i in range(2))
        if x:
            try:
                (name,origin,init_id) = (i[:-1].strip() for i in x[0][:-1])

            except:
                init_id = name
        
        if origin == "openjudge":
            init_id = name
        return {"id":id,"name":name,"origin":origin,"init_id":init_id}
    def get_list(self,origin,List):

        lst = List["list"]
        if type(lst)!=list and type(lst)!=tuple:
            return ""

        #print(lst)
        for i in range(len(lst)):
            lst[i] = lst[i].strip()
           # print("strip[]",lst[i],lst)
            x = self.Find(origin,lst[i])
            try:
                lst[i] = x[0]
                lst[i] = lst[i][0]
            except:
                1
        if type(List["name"])==str:
            List["name"] = [List["name"]]
        return self.Tocode(lst,List["name"][0])

    
    ########### 杂七杂八工具方法
    
    def check_time(self,cur,Len,per):
        return int(cur/Len) == per        
    def Tocode(self,plist,title):
        title = str(title)
        plist = ",".join(plist)
        return self.formula(plist,title)
    def formula(self,plist,title):
        return r'<span><span style="white-space:normal;">[plist=%s]%s[/plist]</span><br />'%(plist,title)
    ###############

    
    #**********************************
    #方法继承
    #**********************************
    
    def check_id(self,info):
        id = info["id"]
        return self.check(id)
    
    def erase(self):
        super().release()
        
    def super(self):
        return super()
    
    def get_tab(self):
        super().get_tab() 
    
    #**********************************
    #put方法 一个顶层抽象与三个实例化
    #**********************************
    
    def put(self,origin,all_get,default = None):
        lst = []
        if default:
            data = all_get(default)
        else:
            data = all_get()
        for i in data:
            if not i:
                continue
            x = self.get_list(origin,i)
            if x:
                lst.append(x)
        return lst
    
    
    def put_DF(self,default = None):
        return self.put(self.DF.origin,self.DF.get_id)
    
    def put_OPJ(self,url=None):
        if url:
            self.opj.set_site(url)
        return self.put(self.opj.origin,self.opj.all_get) 
    
    def put_LG(self,lst = None):
        x = self.LG.all_get
        return self.put(self.opj.origin,self.LG.all_get,lst)
    
    #***************
    #只读数据库下载
    #***************
        
    def download(self):
        x = self.remote.get_data()
        result = []
        for i in x:
            result.append(self.get(i))
        return result
    def introduce(self):
        self.create()
        x = self.download()
        Len = len(x)
        cur = 0
        per = 0
        for i in x:
            if int(cur/Len *100) == per:
                print("完成%d%%"%(int(cur/Len*100)))
                per = per+5
            cur = cur+1
            info = list(i.values())
            info = self.to_str(info)
            #print(info)
            if self.check_id(i) == False:
                self.insert(info)
        print("完成")
        
        
    #***************
    #文件写入
    #***************
    def write_into(self,func,default=None):
        x = func(default)
        if not x:
            return
        a = open("plist","w")
        a.write("\n".join(x))
        a.close()
    def write_change(self,func,default=None):#default 缺省参数
        x = func(default)
        if not x:
            return
        a = open("plist","r")
        out = a.readlines()
        cur = 0
        Len = len(out)
        for i in x:
            while cur<Len:
                txt = out[cur]
                if self.regex_write.findall(txt):
                    break
                cur = cur+1
            if cur==Len:
                break
            out[cur] = i
            cur = cur+1
        a.close()
        a = open("plist","w")
        a.write("\n".join(out))
        a.close()
a = Scr_Qlist()