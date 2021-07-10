from flask import Flask, flash, redirect, request, send_file, abort, render_template, Response
from flask_restful import Resource, Api, url_for
from werkzeug.utils import secure_filename
import json, os

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp4'}

from get_video import *

# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>Gesture Recognition</title> </head>\n<body>'''
instructions = '''
    <p><em>Gesture Recognition</em>:</p>'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.
application = app = Flask(__name__)
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # add a rule for the index page.
# application.add_url_rule('/', 'index', (lambda: header_text +
#     say_hello() + instructions + footer_text))

@app.route('/newclip', methods=['GET'])
def newclip():
   cID  = request.args.get('cID', None)
   title  = request.args.get('title', None)
   cstart  = request.args.get('cstart', None)
   cend  = request.args.get('cend', None)
   print('cID',cID,'title',title,'cstart',cstart,'cend',cend)
   mstring =  {'cID':  cID , 'title' : title , 'cstart' : cstart, 'cend': cend}
   with open('output.txt','a+') as fout:
       fout.write(json.dumps(mstring))
       fout.write('\n')
#    video = get_video.vid(cID,title,cstart,cend)
#    video.detect()
   return json.dumps({'success':True, 'input':mstring}), 200, {'ContentType':'application/json'}

def gen():
    while True:
        image_path = os.path.join(os.getcwd(),'live.jpeg')
        image = cv2.imread(image_path)
        img_str = cv2.imencode('.jpg', image)[1].tostring()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img_str + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            options = {'side':'right', 'save_vid':True}
            vid_processor = Vid_Stream('Fortnite_Emotes')
            # vid_processor.extract(vids, options=options)
            # vid_processor.train_model()

            Detect('Fortnite_Emotes',source = 'qZEElv92rLM')
            return redirect(url_for('download_file'))
    return '''
    <!doctype html>
    <title>Gesture recognition</title>
    <h1>Upload MP4 video for Fortnite dance gesture recognition</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/files')
def dir_listing():
    files = os.listdir(os.getcwd())
    return render_template('files.html', files=files)

@app.route('/download')
def download_file():
    files = os.listdir(os.path.join(os.getcwd(),'static/uploads'))
    return render_template('files.html', files=files)    


@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing2(req_path):
    BASE_DIR = os.getcwd()
    abs_path = os.path.join(BASE_DIR, req_path)
    if os.path.isfile(abs_path):
        return send_file(abs_path)
    else:
        return abs_path


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    
    application.run(host='0.0.0.0')