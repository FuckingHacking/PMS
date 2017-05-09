#! C:\Users\navch\AppData\Local\Programs\Python\Python35\python.exe

from http.server import HTTPServer, CGIHTTPRequestHandler
server_address = ("", 8000)
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
httpd.serve_forever()