import http.client
import sys
from helpers import config
from helpers import helpers

class HTTPClient:
    socket = None
    host = None
    protocol = None
    port = None
    out_lck = None
    int_option = None
    counter = 0

    def __init__(self, host, port, protocol, out_lock):
        self.host = "%s%s" % (config._base, host)
        self.port = int(port)
        self.out_lck = out_lock

    def send(self):
        output(out_lck, "enter the number required to be sent: ")
        try:
            option = input()
        except SyntaxError:
            option = None
        if option is None:
            output(out_lck, "Please select an option")
        elif option == 'e':
            output(out_lck, "Bye bye")
            sys.exit()
        else:
            try:
                int_option = int(option)
            except ValueError:
                output(out_lck, "A number is required")

        for counter in range(0, int_option):
            try:
                conn = http.clinet.HTTPConnection(self.host, self.port)
                conn.request("HTTP", "", counter)
                res = conn.getresponse()
                output(out_lck, "send message: " + counter)
            except Exception as e:
                output(out_lck, str(e))
            else:
                output(out_lck, "error connection")
