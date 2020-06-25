import pymysql



def login(username,password):

    db = pymysql.connect("localhost", "root", "123456", "scams")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    
    # 使用 execute()  方法执行 SQL 查询
    # cursor.execute("SELECT VERSION()")
    # # 使用 fetchone() 方法获取单条数据.
    # data = cursor.fetchone()
    # print("Database version : %s " % data)
    sql =  "select username,password from user where username='%s' and password='%s' " % (username, password)
    cursor.execute(sql)
    userinfo = cursor.fetchone()
    if userinfo:
        result = 1
    # 关闭数据库连接
    else:
        result = 0
    db.close()
    return result



def register(userinfo):
    db = pymysql.connect("localhost", "root", "123456", "scams")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    sql_select =  "select id from user where id='%s' " % (userinfo[0])
    sql_insert = """ insert into user values('%s','%s','%s') """
    cursor.execute(sql_select)
    selectresult = cursor.fetchone()
    if selectresult:
        db.close()
        return 0
    # 关闭数据库连接
    else:  
        cursor.execute(sql_insert % (userinfo[0],userinfo[1],userinfo[2]))
        db.commit()
        db.close()
        return 1

