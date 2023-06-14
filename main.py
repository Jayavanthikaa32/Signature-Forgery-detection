from flask import Flask, request, render_template,send_from_directory
import os
import cv2
from numpy import result_type
from signature import match


# Mach Threshold
THRESHOLD = 85

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file1 = request.files.get('file1')
        file2 = request.files.get('file2')
        fname1="1."+file1.filename.rsplit('.', 1)[1].lower()
        fname2="2."+file2.filename.rsplit('.', 1)[1].lower()
        if file1 and file2:
            file1.save(os.path.join('uploads', fname1))
            file2.save(os.path.join('uploads', fname2))
            return checkSimilarity(fname1,fname2)
        return "File(s) missing"
    return render_template('index.html')

@app.route('/uploads/<filename>')
def serve_image(filename):
    return send_from_directory('uploads', filename)

def checkSimilarity(path1, path2):
    result = match(path1=path1, path2=path2)
    msg=""
    if(result <= THRESHOLD):
        msg= f"Failure: Signatures Do Not Match, Signatures are {result} % similar!!"
    else:
        msg=f"Success: Signatures Match, Signatures are {result} % similar!!"
    return render_template('compare.html',fname1=path1, fname2=path2 ,msg = msg)    

if __name__ == '__main__':
    app.run()
