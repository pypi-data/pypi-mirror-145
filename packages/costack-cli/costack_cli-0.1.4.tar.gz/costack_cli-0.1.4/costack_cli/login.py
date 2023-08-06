# https://hackersandslackers.com/python-poetry-package-manager/
import json
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from costack_cli.config import save_user_credentials
from costack_cli.constants import FRONTEND_ENDPOINT
KEEP_RUNNING = True

class Serv(BaseHTTPRequestHandler):
    stopped = False
    def do_GET(self):
        # print("do get????")
        if self.path == '/':
            # print("ever in the path")
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes("<body><p>This is a test.</p>", "utf-8"))
            self.wfile.close()
        else:
            print("in other path")
    
    # Remove logging information
    def log_message(self, format, *args):
        return

    def do_OPTIONS(self):
        # print("doing options")
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'HEAD, GET, POST, PUT, PATCH, DELETE, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        post_data_json = json.loads(post_data)
        # print(post_data_json)
        if "user_id" in post_data_json:
            print("Login succeeded!")
            save_user_credentials(post_data_json)
        # print("going to send response")
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'HEAD, GET, POST, PUT, PATCH, DELETE, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        success = {"success": True}
        self.wfile.write(b'{"ss":"sss"}')
        # stop the server
        global KEEP_RUNNING
        KEEP_RUNNING=False
        # print("stop running temp server")

def do_login_with_web_portal():
    # redirect to page
    # localserver address
    PORT = 9200
    redirect = f"https://localhost:{PORT}"
    url_login = f"{FRONTEND_ENDPOINT}/login/?redirect_url={redirect}"
    webbrowser.open(url_login, new = 2)
    # get access token and secret key ?
    httpd = HTTPServer(('localhost', PORT), Serv)
    while KEEP_RUNNING:
        httpd.handle_request()
