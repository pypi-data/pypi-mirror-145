import requests
import json
from lager.lager_pcb.lager_pcb.visa_enum import EnumEncoder
from lager.lager_pcb.lager_pcb import rigol_mso5000_defines
from lager.lager_pcb.lager_pcb import rigol_dm3000_defines
from . import RTC_PORT

ALL_ENUMS = (
    rigol_mso5000_defines,
    rigol_dm3000_defines,
)

class ConnectionFailed(Exception):
    pass

class DeviceError(Exception):
    pass

def enum_decoder(obj):
    if '__enum__' in obj:
        cls, name = obj['__enum__']['type'], obj['__enum__']['value']
        for enum_holder in ALL_ENUMS:
            if hasattr(enum_holder, cls):
                return getattr(enum_holder, cls).from_cmd(name)

    return obj

class Device:
    def __init__(self, device_name):
        self.device_name = device_name

    def invoke(self, func, *args, **kwargs):
        data = {
            'device': self.device_name,
            'function': func,
            'args': args,
            'kwargs': kwargs,
        }
        try:
            resp = requests.post(f'http://rtc:{RTC_PORT}/invoke', headers={'Content-Type': 'application/json'}, data=json.dumps(data, cls=EnumEncoder))
        except Exception as exc:
            raise ConnectionFailed from exc
        if not resp.ok:
            try:
                raise DeviceError(resp.json())
            except:
                raise DeviceError(resp.content)
        return json.loads(resp.content, object_hook=enum_decoder)

    def __getattr__(self, func):
        def wrapper(*args, **kwargs):
            return self.invoke(func, *args, **kwargs)
        return wrapper
