# Implementing a very simple HTTP server that's designed to receive 
# one type of request.
# Our goal here is to accept a request which has two different
# HTTP queries embedded in the URL, one that's called user
# and one that's called password.
# If we received this request, we're going to print out the username and password.
# On the terminal and then send 300 redirect response saying to go to google.com


from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

hostName = "localhost"
serverPort = 8443


class MyServer(BaseHTTPRequestHandler):
    def do_Get(self):
        queries = parse_qs(urlparse(self.path).query)
        print("Username: %s, Password: %s" %(queries["user"][0],queries["password"][0]))
        self.send_response(300)
        self.send_header("Location", "http://google.com")
        self.end_headers()

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server Stopped.")
