def init():
    import subprocess as sub
    try:
        sub.check_call("pip install pymysql")
    except:
        print("请自行安装 pymysql")