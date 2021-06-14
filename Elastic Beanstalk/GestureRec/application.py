from flask import Flask, request, send_file, abort, render_template
from flask_restful import Resource, Api
import json, os

# import get_video

# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username

# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>Jon Bad</title> </head>\n<body>'''
instructions = '''
    <p><em>Gesture Recognition</em>: This is a RESTful web service! It like took forever to get this running, but now it's on AWS's Elastic Beanstalk.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.
application = app = Flask(__name__)
api = Api(app)

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text +
    say_hello() + instructions + footer_text))

@app.route('/newclip', methods=['GET'])
def newclip():
   cID  = request.args.get('cID', None)
   title  = request.args.get('title', None)
   cstart  = request.args.get('cstart', None)
   cend  = request.args.get('cend', None)
   print('cID',cID,'title',title,'cstart',cstart,'cend',cend)
   mstring =  {'cID':  cID , 'title' : title , 'cstart' : cstart, 'cend': cend}
   with open('output.txt','w') as fout:
       fout.write(json.dumps(mstring))
#    video = get_video.vid(cID,title,cstart,cend)
#    video.detect()
   return json.dumps({'success':True, 'input':mstring}), 200, {'ContentType':'application/json'}


@app.route('/files')
def dir_listing():
    # BASE_DIR = '/'



    # # Return 404 if path doesn't exist
    # if not os.path.exists(abs_path):
    #     return abort(404)

    # Check if path is a file and serve


    # Show directory contents
    files = os.listdir(os.getcwd())
    return render_template('files.html', files=files)

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing2(req_path):
    BASE_DIR = os.getcwd()
    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # # Joining the base and the requested path
    # abs_path = os.path.join(BASE_DIR, req_path)
    if os.path.isfile(abs_path):
        return send_file(abs_path)
    else:
        return abs_path


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    
    application.run()