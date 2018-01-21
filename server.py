#!/usr/bin/env python
from __future__ import print_function

import getopt
import sys
import datetime

from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource

from logic import trigger_activated, toggle_activated, set_length, disable, enable, status
import settings

from models import Session, Device

class FillableResource(Resource):
    def __init__(
        self, name="FillableResource", coap_server=None,
        GET=None, PUT=None, DELETE=None
    ):
        super(FillableResource, self).__init__(
            name, coap_server, visible=True, observable=True, allow_children=True)
        self.content_type = "text/plain"
        if GET:
            self.render_GET = lambda request: GET(self, request)
        if PUT:
            self.render_PUT = lambda request: PUT(self, request)
        if DELETE:
            self.render_DELETE = lambda request: DELETE(self, request)

class CoAPServer(CoAP):
    def __init__(self, host, port, multicast=False):
        CoAP.__init__(self, (host, port), multicast)
        self.add_resource("trigger", FillableResource())
        self.add_resource("toggle", FillableResource())

    def add_node(self, path, **kwargs):
        self.add_resource(path, FillableResource(**kwargs))

    def add_trigger(self, name):
        self.add_node("trigger/{}".format(name))
        self.add_node("trigger/{}/activated".format(name), PUT=trigger_activated(name))
        self.add_node("trigger/{}/length".format(name), PUT=set_length(name))
        self.add_node("trigger/{}/enable".format(name), PUT=enable(name))
        self.add_node("trigger/{}/disable".format(name), PUT=disable(name))
        self.add_node("trigger/{}/status".format(name), GET=status(name))

    def add_toggle(self, name):
        self.add_node("toggle/{}".format(name))
        self.add_node("toggle/{}/activated".format(name), PUT=toggle_activated(name))
        self.add_node("toggle/{}/length".format(name), PUT=set_length(name))
        self.add_node("toggle/{}/enable".format(name), PUT=enable(name))
        self.add_node("toggle/{}/disable".format(name), PUT=disable(name))
        self.add_node("toggle/{}/status".format(name), GET=status(name))


if __name__ == "__main__":  # pragma: no cover
    server = CoAPServer(settings.ip, settings.port, settings.multicast)

    # create missing rows in db
    s = Session()
    for name, length in settings.triggers + settings.toggles:
        if not s.query(Device).filter_by(dev_id=name).first():
            d = Device(dev_id=name, length=length, timestamp=datetime.datetime.now(), enabled=True)
            s.add(d)
    s.commit()
    s.close()

    # create endpoints
    for name, _ in settings.triggers:
        server.add_trigger(name)
    for name, _ in settings.toggles:
        server.add_toggle(name)

    for e in sorted(server.root.dump()):
        print(e)

    # run server
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")
