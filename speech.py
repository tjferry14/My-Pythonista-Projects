import speech, ui, sound
from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse, urllib
import cgi, editor, console
from socket import gethostname
import os, webbrowser
from cStringIO import StringIO

lang = 'en-GB'
speed = 0.1

def brit_switch_action(sender):
    global lang
    lang = 'en-GB' if sender.value else 'en-US'
    v['au_switch'].enabled = not sender.value

def aus_switch_action(sender):
    global lang
    lang = 'en-AU' if sender.value else 'en-US'
    v['brit_switch'].enabled = not sender.value

def slider_action(sender):
    global speed
    speed = v['slider1'].value

def button_speak_action(sender):
    global speed
    text = v['user_text'].text
    if text == 'Enter your text here':
        text = 'Please tell me something to say.'
    speech.say(text, lang, speed)

TEMPLATE = '''<!DOCTYPE html>
<html>
  <head>
     <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/3.2.0/css/bootstrap-combined.min.css" rel="stylesheet">
  </head>
  <body>
    <div class="container">
      <h2>Upload File</h2>
      {{ALERT}}
      <p>
      <form action="/" method="POST" enctype="multipart/form-data">
        <div class="form-actions">
          <input id="file" type="file" name="file"></input><br/><br/>
          <button type="submit" class="btn btn-primary">Upload</button>
        </div>
      </form>
      </p>
      <hr/>
    </div>
  </body>
</html>'''

class TransferRequestHandler(BaseHTTPRequestHandler):
    def get_unused_filename(self, filename):
        if not os.path.exists(filename):
            return filename
        basename, ext = os.path.splitext(filename)
        suffix_n = 1
        while True:
            alt_name = basename + '-' + str(suffix_n) + ext
            if not os.path.exists(alt_name):
                return alt_name
            suffix_n += 1

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        path = parsed_path.path
        if path == '/':
            html = TEMPLATE.replace('{{ALERT}}', '')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(html)
            return
        file_path = urllib.unquote(path)[1:]
        if os.path.isfile(file_path):
            self.send_response(200)
            self.send_header('Content-Type', 'application/x-python')
            self.send_header('Content-Disposition',
                             'attachment; filename=%s' % file_path)
            self.end_headers()
            with open(file_path, 'r') as f:
                data = f.read()
                self.wfile.write(data)
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(html)

    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                environ={'REQUEST_METHOD':'POST',
                               'CONTENT_TYPE':self.headers['Content-Type']})
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        field_item = form['file']
        uploaded_filename = None
        dest_filename = None
        file_data = field_item.file.read()
        file_len = len(file_data)
        uploaded_filename = field_item.filename
        dest_filename = self.get_unused_filename(uploaded_filename)
        with open(dest_filename, 'w') as f:
            f.write(file_data)
        editor.reload_files()
        del file_data
        html = TEMPLATE
        if uploaded_filename != dest_filename:
            message = '%s uploaded (renamed to %s).' % (uploaded_filename,
                                                       dest_filename)
        else:
            message = '%s uploaded.' % (uploaded_filename)

    ######
    def log_message(self, format, *args):
        pass 
    ######

def record_action(sender):
        ######
        #sender.superview['webview1'].hidden = False
        sender.superview['webview1'].evaluate_javascript('document.getElementById("file").click()')
        def loop():
            if sender.superview['webview1'].evaluate_javascript('document.forms["form"]["file"].value') == '':
                sound.play_effect('Beep')
                ui.delay(loop,2)
            else:
                sender.superview['webview1'].evaluate_javascript('document.getElementById("submit").click()')
        loop()
        ######
        #console.clear()
        #from BaseHTTPServer import HTTPServer
        #server = HTTPServer(('', 8080), TransferRequestHandler)
        #URL = 'http://localhost:8080' 
        #webbrowser.open('http://localhost:8080', stop_when_done = True)
        #webview = v['webview1']
        #webview.load_url('http://localhost:8080')
        #server.serve_forever()

v = ui.load_view('speech')
v['au_switch'].enabled = v['au_switch'].value = False

speech.say('Greetings!', lang, 0.1)
v.present(style='full_screen', hide_title_bar=True)

from BaseHTTPServer import HTTPServer
######
server = HTTPServer(('', 0), TransferRequestHandler)
def f():
    pass
gport = server.server_address[1]
ui.delay(f,0)
webview = v['webview1']
webview.hidden = True
webview.load_url('http://localhost:'  + str(gport))
server.serve_forever()
######
