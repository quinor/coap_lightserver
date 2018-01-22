#!/usr/bin/env python2
from __future__ import print_function

import socket
import sys

from multiprocessing import Queue
from Queue import Empty

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri

def send(path, op, payload=None, timeout=2):
    print("{}, {}, {}".format(path, op, payload))
    host, port, path = parse_uri(path)
    try:
        tmp = socket.gethostbyname(host)
        host = tmp
    except socket.gaierror:
        pass
    client = HelperClient(server=(host, port))

    try:
        if op == "GET":
            response = client.get(path, timeout=timeout)
        elif op == "DELETE":
            response = client.delete(path, timeout=timeout)
        elif op == "POST":
            response = client.post(path, payload, timeout=timeout)
        elif op == "PUT":
            response = client.put(path, payload, timeout=timeout)
        client.stop()
        print(response.pretty_print())
    except Empty:
        client.stop()
        return None
    return response


if __name__ == "__main__":
    if len(sys.argv) == 4:
        path, method, payload = sys.argv[1:]
    elif len(sys.argv) == 3:
        path, method = sys.argv[1:]
        payload = None
    else:
        sys.exit(2)
    send(path, method, payload)
