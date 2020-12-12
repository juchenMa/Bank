import math
import random
import pymysql


def create():
    name1 = input('姓名：')
    id1 = input('身份证号：')
    phone1 = input('手机号：')
    account = math.floor(1e5 * random.random())
    # 检测是否有误重复
    password1 = input('请设置您的密码：')
    user = {'name': name1, 'id': id1, 'phone': phone1, 'balance': 0.0, 'account': account, 'password': password1}
    print('恭喜注册成功，您的账户为%d' % account)
    return user


def login():
    account = input('请输入您的账号:')
    password = input('请输入您的密码:')
    result = checkexist(account, password)
    if result == 'null':
        print('你的账号不存在2')
        login()
    elif result is True:
        operation(account)
    elif result is False:
        login()
    return


def operation(account):
    print('1:存钱')
    print('2:取钱')
    print('3:改密码')
    print('4:修改个人信息')
    print('5:查询余额')
    print('6:查询个人信息')
    print('7:销户')
    opt = input('请输入您接下来要进行的操作：')
    if opt == '1':
        money = input('请输入您要存入的金额:')
        savemoney(account, money)
        operation(account)
    elif opt == '2':
        money = input('请输入您要取出的金额:')
        drawmoney(account, money)
        operation(account)
    elif opt == '3':
        newpas = input('请输入您的新密码:')
        changepassword(account, newpas)
        operation(account)
    elif opt == '4':
        changinfo(account)
        operation(account)
    elif opt == '5':
        lookbalance(account)
        operation(account)
    elif opt == '6':
        lookpersoninfo(account)
        operation(account)
    elif opt == '7':
        deleteaccount(account)
    else:
        print('您的输入有误，请重试')
        operation(account)
        return


def savemoney(account, data):
    conn = pymysql.connect(
        host='cdb-mbgezdxm.bj.tencentcdb.com',
        port=10165,
        user='outerroot',
        password='5caonimaA',
        database='mjc',
        charset='utf8')
    cursor = conn.cursor()
    sql = "UPDATE bankaccount SET balance = balance + '%s' WHERE account = '%s' " % (data, account)
    cursor.execute(sql)
    conn.commit()
    print('存钱成功')
    lookbalance(account)
    conn.close()
    return


def drawmoney(account, data):
    conn = pymysql.connect(
        host='cdb-mbgezdxm.bj.tencentcdb.com',
        port=10165,
        user='outerroot',
        password='5caonimaA',
        database='mjc',
        charset='utf8')
    cursor = conn.cursor()
    sql = "UPDATE bankaccount SET balance = balance - '%s' WHERE account = '%s' " % (data, account)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print('取钱成功')
    lookbalance(account)
    return


def changepassword(account, newpas):
    conn = pymysql.connect(
        host='cdb-mbgezdxm.bj.tencentcdb.com',
        port=10165,
        user='outerroot',
        password='5caonimaA',
        database='mjc',
        charset='utf8')
    cursor = conn.cursor()
    sql = "UPDATE bankaccount SET password = '%s' WHERE account = '%s' " % (newpas, account)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print('密码修改成功！')
    return


def changinfo(account):
    conn = pymysql.connect(
        host='cdb-mbgezdxm.bj.tencentcdb.com',
        port=10165,
        user='outerroot',
        password='5caonimaA',
        database='mjc',
        charset='utf8')
    cursor = conn.cursor()
    print('1: 手机')
    print('2: id')
    print('3: 姓名')
    op = input('请输入您要更改的内容：')
    if op == '1':
        newphone = input('请输入新的手机号')
        sql = "UPDATE bankaccount SET phone = '%s' WHERE account = '%s' " % (newphone, account)
    elif op == '2':
        newid = input('请输入新的id')
        sql = "UPDATE bankaccount SET id = '%s' WHERE account = '%s' " % (newid, account)
    elif op == '3':
        newname = input('请输入新的姓名')
        sql = "UPDATE bankaccount SET name = '%s' WHERE account = '%s'" % (newname, account)
    else:
        print('输入错误请重新输入')
        changinfo(account)
    cursor.execute(sql)
    conn.commit()
    print('修改成功')
    lookpersoninfo(account)
    conn.close()
    return


def checkexist(account, password):
    conn = pymysql.connect(
        host='cdb-mbgezdxm.bj.tencentcdb.com',
        port=10165,
        user='outerroot',
        password='5caonimaA',
        database='mjc',
        charset='utf8')
    cursor = conn.cursor()
    sql = "select * from bankaccount where account = %s;" % account

    cursor.execute(sql)
    info = cursor.fetchone()
    if password == info[6]:
        cursor.close()
        conn.close()
        return True
    elif info[6] == ():
        cursor.close()
        conn.close()
        print('用户名错误')
        return False
    else:
        cursor.close()
        conn.close()
        print('密码输入错误')
        return False


def lookpersoninfo(account):
    conn = pymysql.connect(
        host='cdb-mbgezdxm.bj.tencentcdb.com',
        port=10165,
        user='outerroot',
        password='5caonimaA',
        database='mjc',
        charset='utf8')
    cursor = conn.cursor()
    sql = "select * from bankaccount where account = %s;" % account
    cursor.execute(sql)
    info = cursor.fetchone()
    cursor.close()
    conn.close()
    print('您的手机为：%s' % info[0])
    print('您的身份证号为：%s' % info[2])
    print('您的姓名为：%s' % info[3])
    print('您的账号为：%s' % info[4])
    return


def lookbalance(account):
    conn = pymysql.connect(
        host='cdb-mbgezdxm.bj.tencentcdb.com',
        port=10165,
        user='outerroot',
        password='5caonimaA',
        database='mjc',
        charset='utf8')
    cursor = conn.cursor()
    sql = "select * from bankaccount where account = '%s';" % account
    cursor.execute(sql)
    info = cursor.fetchone()
    cursor.close()
    conn.close()
    print('您的余额为：%s' % info[1])
    return


def uploadnewinfo(info):
    conn = pymysql.connect(
        host='cdb-mbgezdxm.bj.tencentcdb.com',
        port=10165,
        user='outerroot',
        password='5caonimaA',
        database='mjc',
        charset='utf8')
    name1 = info['name']
    id1 = info['id']
    phone1 = info['phone']
    balance1 = info['balance']
    account1 = info['account']
    password1 = info['password']

    cursor = conn.cursor()
    sql = "INSERT INTO bankaccount (name,id,phone,balance,account,password)VALUES (%s,%s,%s,%s,%s,%s);"
    try:
        cursor.execute(sql, (name1, id1, phone1, balance1, account1, password1))
        conn.commit()
    except:
        conn.rollback()
    conn.rollback()
    cursor.close()
    conn.close()
    return


def deleteaccount(account):
    conn = pymysql.connect(
        host='cdb-mbgezdxm.bj.tencentcdb.com',
        port=10165,
        user='outerroot',
        password='5caonimaA',
        database='mjc',
        charset='utf8')
    cursor = conn.cursor()
    sql = "DELETE FROM bankaccount WHERE account = %s;" % account
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print('删除成功')
    return


print('1.创建账户')
print('2.登陆账户')
option = input("请输入您要进行的操作:")
if option == '1':
    user1 = create()
    uploadnewinfo(user1)
    login()
elif option == '2':
    login()
else:
    print('输入错误请重新输入')
