#!/usr/bin/env python2
from __future__ import print_function

import socket
import sys

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri

def send(path, op, payload=None):
    print("{}, {}, {}".format(path, op, payload))
    host, port, path = parse_uri(path)
    try:
        tmp = socket.gethostbyname(host)
        host = tmp
    except socket.gaierror:
        pass
    client = HelperClient(server=(host, port))

    if op == "GET":
        response = client.get(path)
        client.stop()
    elif op == "DELETE":
        response = client.delete(path)
        client.stop()
    elif op == "POST":
        response = client.post(path, payload)
        client.stop()
    elif op == "PUT":
        response = client.put(path, payload)
        client.stop()
    elif op == "DISCOVER":
        response = client.discover()
        client.stop()
    return response


if __name__ == "__main__":
    if len(sys.argv) == 4:
        path, method, payload = sys.argv[1:]
    elif len(sys.argv) == 3:
        path, method = sys.argv[1:]
        payload = None
    else:
        sys.exit(2)
    print(send(path, method, payload).pretty_print())
