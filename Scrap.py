class scrap:
    #******
    #private
    import urllib.request as Req
    import re
    #******
    #pulic
    url = None
    
    
    #******
    #private
    #******
    
    def __init__(self,url=None):
        import subprocess as sub
        try:
            sub.call("mkdir Scrap",shell=True)
        except:
            print("目录已存在")
        self.url = url
    def match(self,s,regex):
        pattern = self.re.compile(regex)
        return pattern.findall(s)
    
    
    #******
    #public 
    #******
    
    def get(self):#如果存入文件需要解决进程问题 写入可能存在异步性
        response = self.Req.urlopen(self.url)
        return response.read().decode("utf-8").split("\n")
    def show(self):
        print("\n".join(self.get()))
            
    def set(self,url):
        self.url = url
    def all_match(self,regex):
        try:
            a = self.get()
        except:
            print("%s私密不可访问"%(self.url))
            return []
        lst = []
        for i in a:
            x = self.match(i,regex)
            if x:
                lst.append(x[0])
        return lst
class scrOJ(scrap):
    #--------#
    ##Variey##
    #--------#
    origin = None
    #=public:
    site = None
    
    #+++++++++#
    ##Function##
    #+++++++++#
    
    #********
    #+Private+
    #********
    
    def set_site(self,url):
        self.site = url
    def set_listurl(self,url):
        self.url = "%s/%s"%(self.site,url)
        print("%s设置成功"%(self.url))
        
    def get_list(self,regex):
        self.set(self.site)
        return self.all_match(regex)
    #子类继承时传入regex
    def make_list(self,regex=None):
        return
    #make_list 虚函数接口 需在实例化类时 写好对应的列表规则
    #regex传入正则列表
    def check_time(self,cur,Len,per):
        return int(cur/Len*100) == per
    def all_get(self,regex=None,url = None):
        if url:
            self.set_site(url)
        x = self.get_list()
        result = []
        cur = 0
        Len = len(x)
        per = 0
        for i in x:
            cur = cur + 1
            if self.check_time(cur,Len,per):
                print("爬取进度%d%%"%(per))
                per+=5
            self.set_listurl(i[0])
            result.append({"name":i[1],"list":self.make_list(regex)})
        return result
    def get_id(self,regex):
        for i in range(2):
            regex[i] = self.re.compile(regex[i])
        x = self.get()
        result = []
        temp = {"name":None,"list":None}
        import copy
        result.append(copy.deepcopy(temp))
        cur = 0
        per = 0
        Len = len(x)
        for i in x:
            cur = cur + 1
            if self.check_time(cur,Len,per):
                print("爬取进度%d%%"%(per))
                per+=5
            cnt = 0
            for j in temp:
                temp[j] = regex[cnt].findall(i)
                cnt = cnt+1
                if temp[j]:
                    result[-1][j] = temp[j][0].split(",")
                    temp[j] = None
            if result[-1]["name"] and result[-1]["list"]:
                result.append(copy.deepcopy(temp))
                
        return result