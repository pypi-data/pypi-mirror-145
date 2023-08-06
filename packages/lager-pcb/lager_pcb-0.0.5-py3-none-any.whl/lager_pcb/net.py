from enum import Enum, auto
import os
import json
import requests
from .device import Device
from .mux import Mux
from . import RTC_PORT
from .defines import (
    TriggerType,
)
from .mappers.rigol_mso5000 import RigolMSO5000FunctionMapper

def list_muxes():
    return json.loads(os.getenv('LAGER_MUXES', '[]'))

def get_state():
    resp = requests.get(f'http://rtc:{RTC_PORT}/equipment')
    resp.raise_for_status()
    return resp.json()

class InvalidNet(Exception):
    def __str__(self):
        return f"Invalid Net: {self.args[0]}"

    def __repr__(self):
        return str(self)



def mapper_factory(net, device_type):
    if device_type == 'rigol_mso5000':
        return RigolMSO5000FunctionMapper(net, Device(device_type))
    elif device_type in ('rigol_dp800', 'rigol_dl3000', 'keithley'):
        return PassThroughMapper(net, Device(device_type))
    raise TypeError(f'Invalid mapper type {device_type}')

class PassThroughMapper:
    def __init__(self, net, device):
        self.net = net
        self.device = device

    def __getattr__(self, attr):
        return getattr(self.device, attr)


class InvalidNetError(Exception):
    def __str__(self):
        return f"Invalid Net: {self.args[0]}"

    def __repr__(self):
        return str(self)

class SetupFunctionRequiredError(Exception):
    def __str__(self):
        return f"Setup function required for Net {self.args[0]} (type {self.args[1]})"

    def __repr__(self):
        return str(self)

def channel_name_to_number(name):
    if name not in ('A', 'B', 'C', 'D'):
        raise ValueError(f'Invalid channel: {name}')
    return ord(name) - ord('A') + 1


class NetType(Enum):
    Analog = auto()
    Logic = auto()
    Waveform = auto()
    Battery = auto()
    ELoad = auto()
    PowerSupply = auto()

    @classmethod
    def from_role(cls, role):
        mapping = {
            'analog': cls.Analog,
            'logic': cls.Logic,
            'waveform': cls.Waveform,
            'battery': cls.Battery,
            'power-supply': cls.PowerSupply,
            'e-load': cls.ELoad,
        }
        return mapping[role]

    @property
    def device_type(self):
        mapping = {
            self.Analog: 'rigol_mso5000',
            self.Logic: 'rigol_mso5000',
            self.Waveform: 'rigol_mso5000',
            self.Battery: 'keithley',
            self.ELoad: 'rigol_dl3000',
            self.PowerSupply: 'rigol_dp800',

        }
        return mapping[self]

class Net:
    def __init__(self, name, type, *, setup_function=None, teardown_function=None):
        if type is not None and not isinstance(type, NetType):
            raise TypeError('Net type must be NetType enum')

        muxes = list_muxes()
        self.name = name
        self.mapping = None
        self.setup_commands = []
        self.teardown_function = teardown_function
        for mux in muxes:
            mux_role = NetType.from_role(mux['role'])
            for mapping in mux['mappings']:
                if mapping['net'] == name and (type is None or type == mux_role):
                    _, letter = mux['scope_points'][0]
                    self.type = mux_role
                    self.device_type = mux_role.device_type
                    self.mapping = mapping
                    self.mux = Mux(letter)
                    self.channel = channel_name_to_number(letter)

        if self.mapping is None:
            raise InvalidNetError(name)

        if self.needs_mux and setup_function is None:
            raise SetupFunctionRequiredError(name, self.type)
        self.setup_function = setup_function
        self.device = mapper_factory(self, self.device_type)

    def __str__(self):
        return f'<Net name="{self.name}" type={self.type} device_type={self.device_type}>'

    @property
    def needs_mux(self):
        return self.type in (NetType.Analog, NetType.Logic, NetType.Waveform)

    def enable(self):
        self.disable(teardown=False)

        if self.setup_function:
            self.setup_function(self, self.device)

        self.mux.connect(self)
        self.device.enable_channel(self.net.channel)

    def disable(self, teardown=True):
        if teardown and self.teardown_function:
            self.teardown_function(self, self.device)
        self.mux.clear()
        self.device.disable_channel(self.net.channel)

    def __getattr__(self, attr):
        return getattr(self.device, attr)

def setup_vbus(net, device):
    print('setup vbus')

def teardown_vbus(net, device):
    print('teardown vbus')

def main():
    vbus_net = Net('VBUS', type=NetType.Analog, setup_function=setup_vbus, teardown_function=teardown_vbus)
    vbat_net = Net('VBAT', type=NetType.Battery)
    vbus_net.enable()
    vbus_net.trace_settings.set_volts_per_div(.5)
    vbus_net.trace_settings.set_volt_offset(-4)
    vbus_net.trace_settings.set_time_per_div(.00001)
    vbus_net.trigger_settings.set_mode_normal()
    vbus_net.trigger_settings.set_coupling_DC()
    vbus_net.trigger_settings.set_type(TriggerType.Edge)
    vbus_net.trigger_settings.edge.set_source_analog(1)
    vbus_net.trigger_settings.edge.set_slope_both()
    vbus_net.trigger_settings.edge.set_level(4.95)
    print(vbus_net.trigger_settings.edge.get_source())
    print(vbus_net.trigger_settings.edge.get_slope())
    print(vbus_net.trigger_settings.edge.get_level())

    vmax = vbus_net.measurement.voltage_max()
    print(f"Vmax: {vmax}")
    vmin = vbus_net.measurement.voltage_min()
    print(f"Vmin: {vmin}")
    time_base = vbus_net.trace_settings.get_time_per_div()
    print(f"Time Base: {time_base}")
    vbus_net.disable()
