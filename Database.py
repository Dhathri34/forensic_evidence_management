import pymysql

def connection():
    con=pymysql.connect(host='localhost',user='root',password='Dhathri@2004',database='forensic_evidence', charset='utf8')
    return con

