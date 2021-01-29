#  coding: utf-8 
import socketserver
import os
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # self.request.send(self.data)
        # print ("Got a request of: %s\n" % self.data)

        #get request
        request_ = self.data.decode("utf-8")
        cmd,R_url = self.parsedata(request_)
        #defult is root page
        status = "root"
        #only can process GET
        if cmd ==  "GET":
            #if css in url, let text content be css
            if "css" in R_url:
                type_text = "text/css"                  
            else:
                type_text = "text/html"
            #if deep in R_url, mean go deeper page
            if "deep" in R_url: 
                status = "deep"
            #return index.html if end of /
            if R_url[-1] == "/":
                if "index.html" not in R_url:
                    R_url += "index.html"     
            path = "./www"+R_url
            self.response(path,status,type_text)
        #if post,put,delete, then 405-not allowed
        else:
            status = "405"
            path = None
            type_text = None
            self.response(path,status,type_text)           


        # self.request.sendall(self.data)
    def parsedata(self,request):
        #parsedata to commond and url
        request = request.strip().split('\n')
        requestHttp = request[0]
        cmd = requestHttp.split(" ")[0]
        R_url = requestHttp.split(" ")[1]
        return (cmd,R_url)
    
    def response(self,path,status,type_text):
        #response to different situation
        if os.path.exists(path):
            file = open(path,"r")
            data = file.read()   
            if "root" in status:
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n"+"Content-Type:"+type_text+"\r\n\r\n" +data, "utf-8"))
            elif "deep" in status:
                self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\n"+"content-type:"+type_text+"\r\n\r\n"+data, "utf-8"))
            elif status == "405":
                self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n" ,"utf-8"))
        else:
            self.request.sendall(bytearray("HTTP/1.1 404 File not found"+"\r\n\r\n The page not find! 404" , "utf-8"))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
