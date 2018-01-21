from __future__ import print_function
import datetime
import json
from models import Session, Device

def get_device(fn):
    def dev_wrapper(name):
        def inner(self, request):
            s = Session()
            dev = s.query(Device).filter_by(dev_id=name).first()
            self.payload = fn(dev, request)
            s.commit()
            return self
        return inner
    return dev_wrapper


def activate_for(t):
    print("light turned on for {} seconds".format(t))

def active():
    return True

def deactivate():
    print("light turned off")


@get_device
def trigger_activated(device, request):
    if not device.enabled:
        return ""
    activate_for(device.length)
    device.timestamp = datetime.datetime.now()
    return ""

@get_device
def toggle_activated(device, request):
    if not device.enabled:
        return ""
    if active():
        deactivate()
    else:
        activate_for(device.length)
    device.timestamp = datetime.datetime.now()
    return ""

@get_device
def set_length(device, request):
    try:
        device.length = int(request.payload)
        return "OK"
    except ValueError:
        return "Value is not an integer!"
    
@get_device
def enable(device, request):
    device.enabled = True

@get_device
def disable(device, request):
    device.enabled = False

@get_device
def status(device, request):
    return json.dumps({
        "id": device.dev_id,
        "length": device.length,
        "enabled": device.enabled,
        "timestamp": str(device.timestamp)
    })