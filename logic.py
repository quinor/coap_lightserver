from __future__ import print_function
import datetime
import json
from models import Session, Device, Light

def get_devices(fn):
    def dev_wrapper(name):
        def inner(self, request):
            s = Session()
            dev = s.query(Device).filter_by(dev_id=name).first()
            light = s.query(Light).first()
            self.payload = fn(light, dev, request)
            s.commit()
            return self
        return inner
    return dev_wrapper


def get_light(fn):
    def inner(self, request):
        s = Session()
        light = s.query(Light).first()
        self.payload = fn(light, request)
        s.commit()
        return self
    return inner


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


@get_devices
def trigger_activate(light, device, request):
    if not device.enabled:
        return ""
    light.activate_for(device.length)
    device.timestamp = datetime.datetime.now()
    return ""

@get_devices
def toggle_activate(light, device, request):
    if not device.enabled:
        return ""
    if light.active_for() > 0:
        light.deactivate()
    else:
        light.activate_for(device.length)
    device.timestamp = datetime.datetime.now()
    return ""

@get_devices
def set_length(light, device, request):
    try:
        device.length = int(request.payload)
        return "OK"
    except ValueError:
        return "Value is not an integer!"
    
@get_devices
def enable(light, device, request):
    device.enabled = True

@get_devices
def disable(light, device, request):
    device.enabled = False

@get_devices
def status(light, device, request):
    return json.dumps({
        "id": device.dev_id,
        "length": device.length,
        "enabled": device.enabled,
        "timestamp": str(device.timestamp)
    })