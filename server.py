# coding: utf-8

import os
import SocketServer
import re


# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Nhu Bui
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
	wwwDirectory = "/www"
	urlExtentions =""

	#parse the url request
	self.data = self.request.recv(1024).strip()
        results = re.search('(?<=GET )(.*)(?= HTTP/)', self.data)
	if results:
	    urlExtentions =results.group(0)

	#set default path to same path of this (server.py) file
        root = os.getcwd()
	self.fullPath = root + wwwDirectory + urlExtentions

	#check if the path exist
	if not os.path.exists(self.fullPath):
	    self.request.sendall(self.error())
	    return

	self.handleResponse(self.fullPath)

    def handleResponse(self, fullPath):
	indexHTMLFile = "/index.html"
	response = ""
	mimetype= ""

	#check the file type and set the mimetype
	response_good = True
	if fullPath.endswith(".css"):
	    mimetype = "text/css"
	elif fullPath.endswith(".html"):
	    mimetype = "text/html"
	elif fullPath.endswith("/") :
	    mimetype = "text/html"
	    fullPath = fullPath + indexHTMLFile
	else:
	    response_good = False
	
	if response_good:
	    response = self.displayFile(fullPath, mimetype)
	else:
	    response = self.error()	

	self.request.sendall(response)


    def error(self):
	return ("HTTP/1.1 404 NOT FOUND\r\n" +
		"Content-Type: text/html\n\n" +
		"<h3>404 NOT FOUND</h3>")
    

    def displayFile(self, fullPath, mimetype):
	return ("HTTP/1.1 200 OK\r\n" +
	        "Content-Type: %s\n\n" % mimetype +
		open(fullPath).read());

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
