#python code to create a MySQL database on AWS. Create a schema, upload a .csv file on the database and fire queries to fetch information from the database.

from flask import Flask,request,redirect,render_template,make_response
import MySQLdb
import csv
from time import clock
from flask import session
import os
from time import time
import random
mydb = MySQLdb.connect(host='.....us-east-2.rds.amazonaws.com',
                       user='username',passwd='',db='dbname')

cursor = mydb.cursor()
app=Flask(__name__)
@app.route('/')
def main():
    return app.send_static_file('result1.html')

#creating schema on the database.
@app.route('/schema', methods=['GET','POST'])
def schema():
    file = request.files['file']
    fileName = file.filename
    filePath = os.path.abspath(fileName)
    tableName = os.path.splitext(file.filename)[0]
    print tableName

    with open(file.filename, "rb") as f:
        reader = csv.reader(f)
        for row in reader:
            rest = row
            break

    sql = "create table " + 'dbname.'+tableName + "(" + rest[0] + " varchar(500),"
    n = len(rest) - 1
    for i in range(1, n):
        sql += rest[i] + " varchar(100),"
    sql += rest[n] + " varchar(100));"
    print(sql)
    cursor.execute(sql);
    return 'Schema created'

#link = '/Users/kushagrapanchal/Desktop'
#uploading .csv file on the database.
@app.route('/upload', methods=['GET','POST'])
def upload():
    start = clock()
    op = 'mysqlimport -h ......c1pigjyomrxl.us-east-2.rds.amazonaws.com --fields-terminated-by=, --ignore-lines=1 --verbose --local -u username -ppassword dbname /Users/kushagrapanchal/Desktop/filename.csv'
    #op = 'mysqlimport --ignore-lines=1 --fields-terminated-by=, --verbose --local -u [user] -p [database] /path/to/address.csv'
    print op

    a=os.system(op)
    print  a
    end = clock()
    elapsed1 = end - start
    b = str(elapsed1)
    return 'time'+ b


@app.route('/query1', methods=['GET','POST'])
def query1():
    cursor= mydb.cursor()
    cursor.execute('use dbname;');
    param1 = request.form['param1']
    print param1
    param1_value = request.form['param1_value']
    print param1_value
    #param2_value = request.form['param2_value']
    #print param2_value
    clause = "" + str(param1_value)
    #clause1 = "" + str(param2_value)
    print clause
    sql1 = 'select * from dbname.all_week where ' + param1 + '=' + convert + ';'
    # +param1+ '=' +param1_value+ ';'
    print sql1
    cursor.execute(sql1)

#displaying the query result on the webpage.
    result = cursor.fetchall()
    if len(result)>0:
        list = "<tr><td><h3>Results</h3></td>"
        for row in result:
            print row[0],
            list = list+ "<tr><td>"+str(row[0])+"</td></tr>"
        return '''<!DOCTYPE html>
        <html>
            <body>
            <head>
                    <title>Python Flask Application</title>
                    <h3> SQL Result</h3>
            </head>
            <body>
                 <table class="table table-bordered">''' + list + '''</table>
            </body>
            </body>
        </html>'''


if __name__ == '__main__':
	#PORT = int(os.getenv('PORT', 8000))
    app.run(host='127.0.0.1', port=8050,debug=True)
