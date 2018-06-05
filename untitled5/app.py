from flask import Flask,session,redirect
from flask import request,url_for,jsonify
from exts import cursor

import redis



from  exts import  db

import config
cur = db.cursor()

app = Flask(__name__)
app.config.from_object(config)



@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        xuehao = request.form['xuehao']
        password = request.form['password']
        sql = "select * from users WHERE xuehao = '%s'and password = '%s'"
        try:
            cur.execute(sql % (xuehao,password))  # 执行sql语句

            results = cur.fetchall()  # 获取查询的所有记录
            s = []
            # 遍历结果
            for row in results:
                xuehao = row[0]
                password = row[1]

                date = {"xuehao": xuehao, "passworde":password}
                s.append(date)
            if s!=[]:
                #登陆成功
                return '1'
            else:
                #登陆失败
                return '0'


        except:

            return ("Error: unable to fetch data")
    else:
        return '404'


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':

        #获取文章，加入数据库
        xuehao = request.form['xuehao']
        title = request.form['title']
        article = request.form['article']
        # SQL 插入语句

        sql_insert = "INSERT INTO opus(xuehao,title,article) VALUES ('%s','%s', '%s')"
        try:
            # 执行sql语句
            cursor.execute(sql_insert % (xuehao, title,article ))
            # 执行sql语句
            db.commit()
            return '上传成功'
        except:
            # 发生错误时回滚
            db.rollback()

            return 'no'
    else:

        return '404'

@app.route('/search', methods=['POST', 'GET'])
def search():
    #搜索 ok
    if request.method == 'POST':
        title = request.form['title']
        sql = "select * from writing WHERE title like '%s' "

        cur.execute(sql % (title))  # 执行sql语句

        results = cur.fetchall()  # 获取查询的所有记录

        s = []
        # 遍历结果
        for row in results:
            author = row[0]
            title = row[1]
            article = row[2]
            date = {"author": author, "title": title, "article": article}
            s.append(date)
        return jsonify(date=s)
    else:
        return '404'


@app.route('/search/classify', methods=['POST', 'GET'])
def classify():
    #搜索分类 ok

    if request.method == 'POST':
        classify = request.form['classify']

        sql = "select * from writing WHERE classify = '%s'"

        cur.execute(sql % (classify))  # 执行sql语句

        results = cur.fetchall()  # 获取查询的所有记录
        s=[]
        # 遍历结果
        for row in results:
            author = row[0]
            title = row[1]
            article = row[2]
            date={"author":author,"title":title,"article":article}
            s.append(date)
        return jsonify(date=s)
    else:
        return '404'


@app.route('/collection', methods=['POST', 'GET'])
def collection():
    if request.method == 'POST':
        #获得文章网址 收藏ok
        xuehao = request.form['xuehao']
        collection = request.form['collection']

        sql_insert = """INSERT INTO collection(xuehao,collection) VALUES ('%s','%s')"""
        try:
            # 执行sql语句
            cursor.execute(sql_insert % (xuehao, collection))
            # 执行sql语句
            db.commit()
            return '收藏成功'
        except:
            # 发生错误时回滚
            db.rollback()

            return 'no'
    else:

        return '404'


@app.route('/like', methods=['POST', 'GET'])
def like():
    #点赞
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        likes = request.form['like']
        sql_update = "update writing set likes = '%s' where author = '%s' and title = '%s'"


        try:
            cur.execute(sql_update % (likes,author,title))  # 像sql语句传递参数
            # 提交
            db.commit()

            return '点赞成功'
        except:

            return ("Error: unable to fetch data")
    else:
        return '404'



@app.route('/search/collection', methods=['POST', 'GET'])
def searchcollection():
    #搜索 收藏ok
    if request.method == 'POST':
        xuehao = request.form['xuehao']

        sql = "select * from collection WHERE xuehao = '%s' "
        try:
            cur.execute(sql % (xuehao))  # 执行sql语句

            results = cur.fetchall()  # 获取查询的所有记录
            s = []
            # 遍历结果
            for row in results:
                collection = row[1]
                date = {"collection": collection}
                s.append(date)
            return jsonify(date=s)
        except:

                return ("Error: unable to fetch data")
    else:
        return '404'

@app.route('/search/my', methods=['POST', 'GET'])
def my():
    #搜索我的作品 ok
    if request.method == 'POST':
        xuehao = request.form['xuehao']

        sql = "select * from opus WHERE xuehao = '%s' "
        try:
            cur.execute(sql % (xuehao))  # 执行sql语句

            results = cur.fetchall()  # 获取查询的所有记录
            s = []
            # 遍历结果
            for row in results:
                title = row[1]
                article = row[2]
                date={"title":title,"article":article}
                s.append(date)
            return jsonify(date=s)
        except:

            return ("Error: unable to fetch data")
    else:
        return '404'

if __name__ == '__main__':
    app.run()
