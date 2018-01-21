from __future__ import print_function
import datetime
import json
from models import Session, Device, Light

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


def get_light(fn):
    def dev_wrapper(name):
        def inner(self, request):
            s = Session()
            light = s.query(Light).first()
            self.payload = fn(light, request)
            s.commit()
            return self
        return inner
    return dev_wrapper


@get_light
def light_status(light, request):
    return str(light.active_for())

@get_light
def light_on(light, request):
    try:
        if not request.payload:
            light.activate_for(60*60*24*365) # 1 year
        else:
            light.activate_for(int(request.payload))
        return "OK"
    except:
        return "Value is not an integer!"

@get_light
def light_off(light, request):
    light.deactivate()
    return ""


@get_device
def trigger_activate(device, request):
    if not device.enabled:
        return ""
    device.light.activate_for(device.length)
    device.timestamp = datetime.datetime.now()
    return ""

@get_device
def toggle_activate(device, request):
    if not device.enabled:
        return ""
    if device.light.active_for() > 0:
        device.light.deactivate()
    else:
        device.light.activate_for(device.length)
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
        "timestamp": str(device.timestamp),
        "light": light_id
    })