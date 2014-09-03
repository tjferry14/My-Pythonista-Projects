'''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>BaseValues</key>
    <string>7.1.2 iPad 2.7.5 2.1 Original</string>
    <key>WarnedValues</key>
    <string></string>
</dict>
</plist>
'''
import cgi, console, editor, os, platform, plistlib, ui, urlparse, urllib
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class CaptureMedia(ui.View):
    def __init__(self):
        console.hide_output()
        self._make_self()
        self._do_warnings()
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
        self.version = '2.1'
        self.source = 'Original posted on Pythonista forum'
        self.name = 'Capture'
        self.message = None
        self.file_name = None
        self.https = HTTPServer(('', 0), TransferRequestHandler)

    def _do_warnings(self):
        s = Settings().open_settings()
        lB = s.get_setting('BaseValues')['value'].split()
        lW = s.get_setting('WarnedValues')['value'].split()
        sN = platform.mac_ver()[0] + ' ' + platform.mac_ver()[2][0:4] + ' ' + platform.python_version() + ' ' + self.version + ' ' + self.source[0:8]
        lN = sN.split()
        if lN != lW:
            if platform.mac_ver()[0] != lB[0]:
                console.hud_alert('Warning: only tested on iOS ' + lB[0])
            if platform.mac_ver()[2][0:4] != lB[1]:
                console.hud_alert('Warning: only tested on ' + lB[1])
            if platform.python_version() != lB[2]:
                console.hud_alert('Warning: only tested on Python ' + lB[2])
            if self.version != lB[3]:
                console.hud_alert('Warning: update to version ' + lB[3])
            if self.source[0:8] != lB[4]:
                console.hud_alert('Warning: not original source')
            s.set_setting('WarnedValues', sN)
            s.close_settings()

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

class Settings (object):
    def open_settings(self):
        self.version = '1.0'
        self.source = 'Original posted on Pythonista forum'
        with open(os.path.split(__file__)[1], 'r') as fS:
            self._sA = fS.read()
        self._iS = self._sA.find('<?xml')
        self._iF = self._sA.find('</plist>') + 8
        self.plSettings = plistlib.readPlistFromString(self._sA[self._iS:self._iF])
        return self

    def get_setting(self, sK):
        return {'setting': sK , 'value': self.plSettings[sK]}

    def set_setting(self, sK, sV):
        self.plSettings[sK] = sV

    def close_settings(self):
        sPl = plistlib.writePlistToString(self.plSettings)
        sN = self._sA[0:self._iS] + sPl[:-1] + self._sA[self._iF:-1]
        with open(self._f, 'w') as fS:
            fS.write(sN)
        if os.path.split(editor.get_path())[1] == self._f:
            editor.replace_text(0, len(editor.get_text()), sN)

class TransferRequestHandler(BaseHTTPRequestHandler):
    '''--------from OMZ's File Transfer script--------'''
    HTML = ('<!DOCTYPE html><html><head></head><body>' +
#    '<link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/3.2.0/'+
#    'css/bootstrap-combined.min.css" rel="stylesheet"></head><body>' +
#    '<div class="container">' +
#    '<h2>Upload File</h2>{{ALERT}}'
    '<form id="form" action="/" method="POST" enctype="multipart/form-data">' +
#    '<div class="form-actions">' +
    '<input id="file" type="file" name="file"></input>' +
    '<button id="submit" type="submit" class="btn btn-primary">Upload</button>' +
#    '</div></form></p><hr/>' +
    '</form></body></html>')

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
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML)


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
#        file_len = len(file_data)
        uploaded_filename = field_item.filename     
        dest_filename = self.get_unused_filename(uploaded_filename)
        with open(dest_filename, 'w') as f:
            f.write(file_data)
        editor.reload_files()
        del file_data
#        html = TEMPLATE
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
        self.lHelp = ui.Label(frame=(30, 10, 180, 30))
        self.lHelp.text = 'Please choose media...'
        self.add_subview(self.lHelp)
        super(MyCaptureMedia, self).did_load()

    def layout(self):
        self.width = 320
        self.height = 200

if __name__ == "__main__":
    mcm = MyCaptureMedia()
    mcm.wait_modal()
    console.hud_alert(str(mcm.message))
