!pip install flask-ngrok

from flask import Flask, request, send_from_directory, redirect, url_for,flash
from flask_ngrok import run_with_ngrok
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/content/uploaded_files'
run_with_ngrok(app)

homePageHtml = '''
<!doctype html>
<title>Upload files</title>
<h1>Please Upload files here</h1>
<form method=post enctype=multiplart/form-data>
    <input type=file name=file>
    <input type=submit value=upload>
</form>
'''
def downloadFiles(file_list):
    
    # if file_list is empty, redirect user to home page
    if not file_list:
        flash('No file selected!')
        # return redirect(url_for('home'))
    
    # if file_list contains some files, save the files
    if file_list:
        # flash('There are files selected')
        print('There are files selected')

        # create the uploaded_files directory if it doesn't exist
        if not os.path.exists('/content/uploaded_files'):
            os.mkdir('/content/uploaded_files')

        for file in file_list:
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        # return redirect(url_for('home'))

@app.route("/",methods=['GET','POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('home'))
        
        # ------------------------------------------------------------------------
        # The code below only allows for multi-file uploads  
        # and it also allows upload of a folder but not the 'structure' of the folder
        # The question now is, how cna we upload the structure of the folder as well? 
        # ------------------------------------------------------------------------
        file_list = request.files.getlist('file')
        # return downloadFiles(file_list)

        folder = request.files.getlist('folder')
        downloadFiles(file_list)
        downloadFiles(folder)
        # return downloadFiles(file_list)
        return redirect(url_for('home'))


        # ------------------------------------------------------------------------
        # The code below only allows for single-file upload, very inefficient
        # ------------------------------------------------------------------------
        # file = request.files['file']
        # # if user does not select file, browser also 
        # # submit an empty part without filename
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(url_for('home'))
        # if file:
        #     # print('file detected')
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        #     return redirect(url_for('home'))


    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
        <input type="file" name="folder" webkitdirectory="" directory="" multiple>
        <input type="file" name="file" multiple>
        <input type=submit value=Upload>
    </form>
    '''

app.run()