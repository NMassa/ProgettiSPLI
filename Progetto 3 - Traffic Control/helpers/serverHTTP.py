import http.server
import socketserver
from helpers import config
from helpers import helpers

class HTTPServer:

    def __init__(self, port, out_lock):
        self.port = port
        self.out_lck = out_lock

    def receive(self):
        PORT = 8000
        Handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", PORT), Handler)
        helpers.output(self.out_lck, "serving at port: ", PORT)
        httpd.serve_forever()
