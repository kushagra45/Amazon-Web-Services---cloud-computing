#python code for uploading, displaying, deleting files on s3 bucket.

from base64 import b64encode
from flask import Flask, request, render_template, request, make_response, session
from time import clock
import os, json, boto3

# connection established between s3
s3 = boto3.resource('s3', aws_access_key_id='',
aws_secret_access_key='',
region_name='us-east-2')

app = Flask(__name__)

#APP_ROOT = os.path.dirname(os.path.abspath(_file_))

@app.route("/")
def main():
    return render_template('index.html')
#index.html is a simple html page that provides us a interface.


@app.route("/upload", methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        start = clock()
        file = request.files['file']
        filename = file.filename
        file1, file_ext = os.path.splitext(filename)
        if file_ext == '.txt':
            data = file.read()
            fileSize = int(len(data))
            if fileSize < 30 * 1024 * 1024:
                s3.create_bucket(Bucket='bucketname - text', CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
                s3.Bucket('bucketname - text').put_object(Key=filename, Body=data)
                end = clock()
                elapsed = end - start
                a = str(elapsed)
                return 'Text File Uploaded'
            else:
                return " file is big"
        else:
            data = file.read()
            fileSize = int(len(data))
            if fileSize < 30 * 1024 * 1024:
                s3.create_bucket(Bucket='imagebucketname', CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
                s3.Bucket('imagebucketname').put_object(Key=filename, Body=data)
                end = clock()
                elapsed = end - start
                a = str(elapsed)
                return 'Image File Uploaded'
            else:
                return 'file is too big'



# this section displays all the files in the bucket.
@app.route('/list_files', methods=['POST','GET'])
def list():
    if request.method == 'GET':
        # listing the buckets and files
        for bucket in s3.buckets.all():
            for key in bucket.objects.all():
                print(key.key)

        # Print out bucket names
        for bucket in s3.buckets.all():
            print(bucket.name)
            return 'List successfully displayed'


# deleting the files present in the bucket.
@app.route('/delete', methods=['POST', 'GET'])
def delete():
    #docID = request.args.get('id')
    document = my_database['']
    document.delete()
    return 'File Deleted Successfully'


@app.route('/download',methods=['POST', 'GET'])
def download():

     # downloading the file(first parameter is from file and second parameter is To file)
     files = request.form['file']
     #file_name = file.filename
     s3.Bucket('bucketname').download_file('source file', 'destination_file')
     return 'file downloaded'



port = os.getenv('VCAP_APP_PORT', '8050')
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=int(port), debug=True)

