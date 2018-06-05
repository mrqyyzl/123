import pymysql



db= pymysql.connect(host="47.106.168.80",user="root",
    password="pass",db="study",port=3306,charset='utf8')

cursor = db.cursor()

#47.106.168.80