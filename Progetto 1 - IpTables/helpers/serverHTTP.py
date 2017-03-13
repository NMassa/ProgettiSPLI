import http.server
import socketserver

class HTTPServer:

    def __init__(self, port, out_lock):
        self.port = port

    def receive(self):
        PORT = 8000
        Handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", PORT), Handler)
        print("serving at port: ", PORT)
        httpd.serve_forever()
