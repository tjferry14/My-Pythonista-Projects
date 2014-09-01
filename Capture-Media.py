import ui, console, editor, urlparse, urllib, cgi, os, platform
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class CaptureMedia(ui.View):
    def __init__(self):
        console.hide_output()
        self._make_self()
        self._do_warnings('7.1.2', 'iPad', '2.7.5', '2.0', 'Original')
        self._make_wv()
        self._make_bi()
        self.did_load()
        self.layout()
        self.present('popover')
        ui.delay(self._start, 0.5)
        self.https.serve_forever()

    def did_load(self):
        self._wv.hidden = True
        self._wv.load_url('http://localhost:'  + str(self.https.server_address[1]))

    def layout(self):
        self.width = 320
        self.height = 160

    def _start(self):
        self._wv.evaluate_javascript('''
        document.getElementById("file").click();
        function f(){
            if (document.forms["form"]["file"].value == '') {
            setTimeout(function(){f()}, 500);
            }
            else {
                document.getElementById("submit").click();
            }
        }
        setTimeout(function(){f()}, 500);
        ''')

    def _make_self(self):
        global gcm
        gcm = self
        self.version = '2.0'
        self.source = 'Original posted on Pythonista forum'
        self.name = 'Capture'
        self.message = None
        self.file_name = None 
        self.https = HTTPServer(('', 0), TransferRequestHandler)

    def _do_warnings(self, vO, vD, vP, vV, vS):
        if platform.mac_ver()[0] != vO:
            console.hud_alert('Warning: only tested on iOS ' + vO)
        if platform.mac_ver()[2][0:4] != vD:
            console.hud_alert('Warning: only tested on ' + vD)
        if platform.python_version() != vP:
            console.hud_alert('Warning: only tested on Python ' + vP)
        if self.version != vV:
            console.hud_alert('Warning: update to version ' + vV)
        if self.source[0:8] != vS:
            console.hud_alert('Warning: not original source')

    def _make_wv(self):
        self._wv = ui.WebView()
        self.add_subview(self._wv)

    def _make_bi(self):
        self.left_button_items = [ui.ButtonItem(image = ui.Image.named('ionicons-ios7-close-outline-32'), action = lambda sender: self.close())]

    def will_close(self):
        self.https.shutdown()

    def close(self):
        self.will_close()
        super(CaptureMedia, self).close()


class TransferRequestHandler(BaseHTTPRequestHandler):
    '''--------from OMZ's File Transfer script--------'''
    global TEMPLATE
    TEMPLATE = ('<!DOCTYPE html><html><head>' +
    '<link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/3.2.0/'+
    'css/bootstrap-combined.min.css" rel="stylesheet"></head><body>' +
    '<div class="container">' +
    '<h2>Upload File</h2>{{ALERT}}'
    '<p><form id="form" action="/" method="POST" enctype="multipart/form-data">' +
    '<div class="form-actions">' +
    '<input id="file" type="file" name="file"></input><br/><br/>' +
    '<button id="submit" type="submit" class="btn btn-primary">Upload</button>' +
    '</div></form></p><hr/>' +
    '</div></body></html>')

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
            html = TEMPLATE
            html = html.replace('{{ALERT}}', '')
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
        '''--------end omz--------'''
        gcm.message = message
        gcm.file_name = dest_filename
        ui.delay(gcm.close, 0)

    def log_message(self, format, *args):
        pass 

class MyCaptureMedia (CaptureMedia):
    def did_load(self):
        self.name = 'My Capture Media'
        self.lHelp = ui.Label()
        self.lHelp.text = 'Please choose media...'
        self.add_subview(self.lHelp)
        super(MyCaptureMedia, self).did_load()

    def layout(self):
        self.width = 320
        self.height = 200
        self.lHelp.x = 30
        self.lHelp.y = 10
        self.lHelp.width = 180
        self.lHelp.height = 30

if __name__ == "__main__":
    mcm = MyCaptureMedia()
    mcm.wait_modal()
    console.hud_alert(str(mcm.message))
