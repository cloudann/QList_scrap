from Scrap import *
class scrDF(scrOJ):
    def __init__(self):
        self.set("http://oj.ilingxin.cn/lists/index")
        self.origin = "东方博宜"
    def get_id(self):
        regex = r'[0-9]\.(\S{0,9})'
        regex2 = r'value="([0-9].*[0-9])"'
        x = super().get_id([regex,regex2])
        return x
    
    
class scrLG(scrOJ):
    typeof  = None
    lst = None
    #*******
    #Private
    #*******
    def __init__(self):
        self.set_site(r'https://www.luogu.com.cn')
        self.origin = "洛谷"
        #x =  r'/%s/%d#problems'%(100)
    def get_list(self):
        url = self.site
        x = input("请输入网址")
        try:
            self.typeof = self.re.compile(r'\b(training)\b').findall(x)[0]
            print(self.typeof)
        except:
            print("当前网址不是题单")
            return
        self.set_site(x)
        self.set(self.site)
        #self.show()
        regex = r'<a href="([0-9]+)">([\S]+)</a>'
        result = super().get_list(regex)
        self.set_site(url)
        return result 
    def make_list(self,regex):
        x = self.all_match(regex)
        if x:
            x = [i for i in self.all_match(regex)]
            #self.show()
        else:
            x = []
        return x

    def get_id(self,url):
        self.set_listurl(url)
        regex = r'<a href="/problem/([\S]{1,20})">'
        regex2 = r'<h1>([\S]+)</h1>'
        title = self.all_match(regex2)
        lst = self.all_match(regex)
        return {"name":[title],"list":lst}
    def set_listurl(self,x):#爬取对应编号的题单
        self.url = r'https://www.luogu.com.cn/%s/%s#problems'%(self.typeof,x)
        
    def all_get1(self):
        regex =  r'<a href="/problem/([\S]+)">'
        return super().all_get(regex = regex)
    #********
    #Public
    #********
    def all_get(self,lst=None,typeof=None):
        if lst==None:
            return self.all_get1()
        
        if typeof == None:
            x = input("请输入题单类型 1-题单 2-比赛")
            if x == "1":
                self.typeof = "training"
            else:
                self.typeof = "contest"
        if type(lst)!=list:
            lst = [lst]
        result = []
        for i in lst:
            result.append(self.get_id(i))
            self.show()
        print(result)
        return result

class scrOpJ(scrOJ):
    #*******
    #private
    #*******
    def __init__(self):
        self.set_site("http://noi.openjudge.cn/")
        self.origin = "openjudge"
    def get_list(self):
        regex = r'<span>»</span><a href="/([\S]{3,9})/">([\S]+)</a>'
        return super().get_list(regex)
    def make_list(self,regex):
        return [i[1:-1] for i in self.all_match(regex)]
    #*******
    #Public
    #*******
    def all_get(self,url = None):
        regex = r'<td class="title"><a href="[\S]+"(>.*<)/a></td>'
        return super().all_get(regex = regex)