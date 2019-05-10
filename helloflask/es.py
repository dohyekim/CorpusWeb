import pymysql

def get_conn(db):
    return pymysql.connect(
        host='127.0.0.1',
        user='dooo',
        password='1234',
        port=3306,
        db=db,
        cursorclass=pymysql.cursors.DictCursor,
        charset='utf8')


conn = get_conn('corpusdb')
cur = conn.cursor()
sql = 'select * from Talk where talk_id between 1 and 5'
cur.execute(sql)
rows = cur.fetchall()
# print(rows)

import elasticsearch

es_client = Elasticsearch()
doc = es_client.mget()

P Y / P I E CLASSIC