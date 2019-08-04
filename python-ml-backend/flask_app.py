import os
from flask import Flask, flash, request, jsonify
from werkzeug.utils import secure_filename
import os

import config
from parse_receipt import extract_info

# UPLOAD_FOLDER = './files/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({"message": "Couldnt find a file"})
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return jsonify({"message": "No file selected"})

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            indexing_status = extract_info(file_path)
            if indexing_status == 200:
                return jsonify({"message": "Uploaded Successfully"})
            else: return jsonify({"message": "Couldn't save the details"})
    else:
        return jsonify({"message":"upload didn't work"})

app.run(host=config.HOST,port=config.PORT)
