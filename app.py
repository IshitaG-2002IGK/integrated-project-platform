from flask import Flask, render_template, request, flash, redirect
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)

ADMIN_USERNAME  = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD  = os.environ.get('ADMIN_PASSWORD')
PORT            = os.environ.get('PORT')
app.config["UPLOAD_FOLDER"] = "static/"

@app.route('/', methods=['GET', 'POST'])
def start():

    if request.method == 'POST':

        uname = request.values.get('uname')
        psw = request.values.get('psw')
        login_type = request.form.getlist('checkbox')

        if uname == ADMIN_USERNAME and psw == ADMIN_PASSWORD:
                return render_template('home.html')

        else:
            return render_template('index.html', error='Invalid username or password')

    return render_template('index.html')

@app.route('/home', methods = ['GET', 'POST'])
def home():

    return render_template('home.html') 


@app.route('/project', methods=['GET', 'POST'])
def get_project_details():

    if request.method == 'POST':

        project_name        = request.values.get('project_name')
        project_description = request.values.get('project_description')
        project_tags        = request.values.get('project_tags')
        resource_link       = request.values.get('resource_link')
        github_link         = request.values.get('github_link')

        # above details to be stored in mongo db or something like that


        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('project_upload.html')


@app.route('/ping')
def ping():

    result = {
        "ping"  : "pong"
    }
    return result


if __name__== "__main__":
    app.run(host = "0.0.0.0", debug = True, port = PORT)