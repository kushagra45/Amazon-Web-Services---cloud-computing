from flask import Flask,request,redirect,render_template,make_response
import MySQLdb
from time import time
import memcache
import random
from random import randint
import hashlib


conn5 = MySQLdb.connect(host='kushilatest.c1pigjyomrxl.us-east-2.rds.amazonaws.com',
                       user='', passwd='', db='kushidb')

mc = memcache.Client(['kushimemcache.rgo9hi.0001.use2.cache.amazonaws.com:11211'], debug=0)

cursor = conn5.cursor()
cursor.execute('use kushidb;')

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')

#fetching data from database.
@app.route('/Normaldb', methods=['GET'])
def Database():
    mag =['1.9','1.2']
    start = time()
    for i in range( 0, 5000 ):
        a = random.choice( mag )
        sql_query = "SELECT * from kushidb.all_week where mag = " + ' " ' + a + ' " '
        hash_function = hashlib.md5( sql_query )
        f = hash_function.hexdigest()
        cursor.execute( sql_query )
        result = cursor.fetchall()
        mc.set( f, result )
    end = time()
    time_elapsed = end - start
    x = str( time_elapsed )
    return " Time elapsed in database " + x

#fetching data from memcache and calculating the time.
@app.route('/Memcache', methods=['POST'])
def Memcache():
    mag = ['1.9','1.2']
    start = time()
    for i in range( 0, 5000 ):
        a = random.choice( mag )
        sql_query = "SELECT * from kushidb.all_week where mag = " + ' " ' + a + ' " '
        hash_function = hashlib.md5( sql_query)
        f = hash_function.hexdigest()
        mcobj = mc.get( f )
        if mcobj:
            result = mc.get( f )
            print 'memcache'

        else:
            cursor.execute(sql_query)
            result=cursor.fetchall()
            print 'go to database'
            mc.set(f,result)
    end = time()
    time_elapsed = end - start
    y = str( time_elapsed )
    return y + " Time elapsed in memcache "


@app.route('/query4sec', methods=['GET', 'POST'])
def query4sec():
    cursor = conn5.cursor()
    time_end = time.time() + 10*1
    count = 0
    while time.time() < time_end:
        random_number = randint(10, 90)
        rns = str(random_number)
        # random_number = uniform(y, x)
        # rn = round(random_number, 2)
        # rns = str(rn)
        print rns
        cursor.execute('use dbname');
        sqlstmt = 'select name from boat where ' + 'age ' + ' = ' + rns
        h = hashlib.md5(sqlstmt)
        ah = h.hexdigest()
        cursor.execute(sqlstmt)
        print (ah)
        print sqlstmt
        count = count +1
    return str(count)

if __name__ == '__main__':
	#PORT = int(os.getenv('PORT', 8000))
    app.run(host='127.0.0.1', port=8067,debug=True)
