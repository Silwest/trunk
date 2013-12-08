#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc

def add(a, b):
    """Test function"""
    return a + b

def check(user_id):
    """Test function"""
    for line in open('doors.txt', 'r'):
        if line[0] == user_id:
            return line[2]
    return 0

def openDoor(user_id):
    with open('doors.txt', 'r') as file:
        data = file.readlines()
    for (counter, line) in enumerate(data):
        if line[0] == user_id:
            data[counter] = str(user_id + ' 1\n')
    with open('doors.txt', 'w') as file:
        file.writelines(data)
    return 1

def closeDoor(user_id):
    with open('doors.txt', 'r') as file:
        data = file.readlines()
    for (counter, line) in enumerate(data):
        if line[0] == user_id:
            data[counter] = str(user_id + ' 0\n')
    with open('doors.txt', 'w') as file:
        file.writelines(data)
    return 1

class RequestHandler(pyjsonrpc.HttpRequestHandler):

    # Register public JSON-RPC methods
    methods = {
        "check": check,
        "openDoor": openDoor,
        "closeDoor": closeDoor,

    }

# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('localhost', 8080),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://localhost:8080"
http_server.serve_forever()