import requests
import json
import os
from . import RTC_PORT

class InvalidNetNameError(Exception):
    pass

class InvalidScopePointForNetNameError(Exception):
    pass


class Mux:
    def __init__(self, scope_point):
        self.scope_point = scope_point

    def clear(self):
        data = [
            {
                'current_state': [{
                    'scope': self.scope_point,
                    'dut': None,
                }],
            },
        ]
        resp = requests.post(f'http://rtc:{RTC_PORT}/mux', json=data)
        resp.raise_for_status()



    def connect(self, net, *, role=None):
        scope_point = self.scope_point
        net_name = net.name
        muxes = json.loads(os.getenv('LAGER_MUXES', '[]'))
        pin = None

        for mux in muxes:
            if mux['role'] == role or role is None:
                for mapping in mux['mappings']:
                    if mapping['net'] == net_name:
                        for pin, name in mux['scope_points']:
                            if name == scope_point:
                                pin = mapping['pin']
                                break
                        else:
                            raise InvalidScopePointForNetNameError()

        if pin is None:
            raise InvalidNetNameError()

        data = [
            {
                'current_state': [{
                    'scope': scope_point,
                    'dut': pin,
                }],
            },
        ]
        resp = requests.post(f'http://rtc:{RTC_PORT}/mux', json=data)
        resp.raise_for_status()
