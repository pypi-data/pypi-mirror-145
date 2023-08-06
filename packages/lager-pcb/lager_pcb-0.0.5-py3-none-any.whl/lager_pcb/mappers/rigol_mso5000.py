from ..defines import (
    MeasurementSource,
    RigolTriggerEdgeSource,
    MeasurementItem,
    TriggerType_TO_Rigol,
    RigolTriggerMode,
    RigolTriggerCoupling,
    Rigol_TO_TriggerType,
    RigolTriggerEdgeSlope,
    Rigol_TO_TriggerEdgeSource,
    MeasurementClear,
    TriggerType,
    Rigol_TO_TriggerEdgeSlope,
)

def map_mux_channel_to_scope(mux_ch):
    chan = None
    if mux_ch == 1:
        chan = MeasurementSource.Channel1
    elif mux_ch == 2:
        chan = MeasurementSource.Channel2
    elif mux_ch == 3:
        chan = MeasurementSource.Channel3
    elif mux_ch == 4:
        chan = MeasurementSource.Channel4
    else:
        raise ValueError("Math channel must be in the range 1-4")
    return chan

def map_analog_source_to_trigger_edge_source(analog_source):
    if analog_source == 1:
        return RigolTriggerEdgeSource.Channel1
    elif analog_source == 2:
        return RigolTriggerEdgeSource.Channel2
    elif analog_source == 3:
        return RigolTriggerEdgeSource.Channel3
    elif analog_source == 4:
        return RigolTriggerEdgeSource.Channel4
    else:
        raise ValueError("Analog channel must be in the range 1-4")

def map_digital_source_to_trigger_edge_source(digital_source):
    if digital_source == 0:
        return RigolTriggerEdgeSource.D0
    elif digital_source == 1:
        return RigolTriggerEdgeSource.D1
    elif digital_source == 2:
        return RigolTriggerEdgeSource.D2
    elif digital_source == 3:
        return RigolTriggerEdgeSource.D3
    elif digital_source == 4:
        return RigolTriggerEdgeSource.D4
    elif digital_source == 5:
        return RigolTriggerEdgeSource.D5
    elif digital_source == 6:
        return RigolTriggerEdgeSource.D6
    elif digital_source == 7:
        return RigolTriggerEdgeSource.D7
    elif digital_source == 8:
        return RigolTriggerEdgeSource.D8
    elif digital_source == 9:
        return RigolTriggerEdgeSource.D9
    elif digital_source == 10:
        return RigolTriggerEdgeSource.D10
    elif digital_source == 11:
        return RigolTriggerEdgeSource.D11
    elif digital_source == 12:
        return RigolTriggerEdgeSource.D12
    elif digital_source == 13:
        return RigolTriggerEdgeSource.D13
    elif digital_source == 14:
        return RigolTriggerEdgeSource.D14
    elif digital_source == 15:
        return RigolTriggerEdgeSource.D15
    else:
        raise ValueError("Digital channel must be in the range 0-15")

class TraceSettings_RigolMSO5000FunctionMapper:
    def __init__(self, net, device):
        self.net = net
        self.device = device

    def set_volt_offset(self, offset):
        self.set_channel_offset(self.net.channel, offset)

    def get_volt_offset(self):
        return float(self.get_channel_offset(self.net.channel))

    def set_volts_per_div(self, volts):
        self.set_channel_scale(self.net.channel, volts)

    def get_volts_per_div(self):
        return float(self.get_channel_scale(self.net.channel))

    def set_time_per_div(self, time):
        self.set_timebase_scale(time)

    def get_time_per_div(self):
        return float(self.get_timebase_scale())

    def __getattr__(self, attr):
        return getattr(self.device, attr)

class TriggerSettings_RigolMSO5000FunctionMapper:
    def __init__(self, net, device):
        self.net = net
        self.device = device
        self.edge = TriggerSettingsEdge_RigolMSO5000FunctionMapper(self.net, self.device)

    def get_trigger_status(self):
        return self.get_trigger_status()

    def set_mode_auto(self):
        self.set_trigger_mode(RigolTriggerMode.Auto)

    def set_mode_normal(self):
        self.set_trigger_mode(RigolTriggerMode.Normal)

    def set_mode_single(self):
        self.set_trigger_mode(RigolTriggerMode.Single)

    def get_trigger_mode(self):
        return self.get_trigger_mode()

    def set_coupling_AC(self):
        self.set_trigger_coupling(RigolTriggerCoupling.AC)

    def set_coupling_DC(self):
        self.set_trigger_coupling(RigolTriggerCoupling.DC)

    def set_coupling_low_freq_reject(self):
        self.set_trigger_coupling(RigolTriggerCoupling.LF_Reject)

    def set_coupling_high_freq_reject(self):
        self.set_trigger_coupling(RigolTriggerCoupling.HF_Reject)

    def get_coupling(self):
        return self.get_trigger_coupling()

    def set_type(self, trigger_type):
        self.set_trigger_type(TriggerType_TO_Rigol[trigger_type])
        #self.set_trigger_type(RigolTriggerType.Edge)

    def get_trigger_type(self):
        return(Rigol_TO_TriggerType[self.get_trigger_type()])

    def __getattr__(self, attr):
        return getattr(self.device, attr)

class TriggerSettingsEdge_RigolMSO5000FunctionMapper:
    def __init__(self, net, device):
        self.net = net
        self.device = device

    def set_source_analog(self, analog_source=None):
        if analog_source is None:
            raise ValueError("Please specify an analog channel between 1 and 4")
        self.set_trigger_edge_source(map_analog_source_to_trigger_edge_source(analog_source))

    def set_source_digital(self, digital_source=None):
        if digital_source is None:
            raise ValueError("Please specify a digital channel between 0 and 15.")
        self.set_trigger_edge_source(map_digital_source_to_trigger_edge_source(digital_source))

    def get_source(self):
        return(Rigol_TO_TriggerEdgeSource[self.get_trigger_edge_source()])

    def set_slope_rising(self):
        self.set_trigger_edge_slope(RigolTriggerEdgeSlope.Positive)

    def set_slope_falling(self):
        self.set_trigger_edge_slope(RigolTriggerEdgeSlope.Negative)

    def set_slope_both(self):
        self.set_trigger_edge_slope(RigolTriggerEdgeSlope.Either)

    def get_slope(self):
        return(Rigol_TO_TriggerEdgeSlope[self.get_trigger_edge_slope()])

    def set_level(self,level):
        self.set_trigger_edge_level(level)

    def get_level(self):
        try:
            return float(self.get_trigger_edge_level())
        except:
            return None


    def __getattr__(self, attr):
        return getattr(self.device, attr)

class Measurement_RigolMSO5000FunctionMapper:
    def __init__(self, net, device):
        self.net = net
        self.device = device

    def _get_measurement_extra(self, item):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            return float(self.get_measure_item(item, chan))
        except:
            return None
        finally:
            self.clear_measurement(MeasurementClear.All)

    def voltage_max(self):
        return self._get_measurement_extra(MeasurementItem.VMax)

    def voltage_min(self, display=False):
        return self._get_measurement_extra(MeasurementItem.VMin)

    def voltage_peak_to_peak(self, display=False):
        return self._get_measurement_extra(MeasurementItem.VPP)

    def voltage_flat_top(self, display=False):
        return self._get_measurement_extra(MeasurementItem.VTop)

    def voltage_flat_base(self, display=False):
        return self._get_measurement_extra(MeasurementItem.VBase)

    def voltage_flat_amplitude(self, display=False):
        return self._get_measurement_extra(MeasurementItem.VAmp)

    def voltage_average(self, display=False):
        return self._get_measurement_extra(MeasurementItem.VAvg)

    def voltage_rms(self, display=False):
        return self._get_measurement_extra(MeasurementItem.VRMS)

    def voltage_overshoot(self, display=False):
        return self._get_measurement_extra(MeasurementItem.Overshoot)

    def voltage_preshoot(self, display=False):
        return self._get_measurement_extra(MeasurementItem.Preshoot)

    def waveform_area(self, display=False):
        return self._get_measurement_extra(MeasurementItem.MArea)

    def waveform_period_area(self, display=False):
        return self._get_measurement_extra(MeasurementItem.MPArea)

    def period(self, display=False):
        return self._get_measurement_extra(MeasurementItem.Period)

    def frequency(self, display=False):
        return self._get_measurement_extra(MeasurementItem.Frequency)

    def rise_time(self, display=False):
        return self._get_measurement_extra(MeasurementItem.RTime)

    def fall_time(self, display=False):
        return self._get_measurement_extra(MeasurementItem.FTime)

    def pulse_width_positive(self):
        return self._get_measurement_extra(MeasurementItem.PWidth)

    def pulse_width_negative(self):
        return self._get_measurement_extra(MeasurementItem.NWidth)

    def duty_cycle_positive(self):
        return self._get_measurement_extra(MeasurementItem.PDuty)

    def duty_cycle_negative(self):
        return self._get_measurement_extra(MeasurementItem.NDuty)

    def time_at_voltage_max(self):
        return self._get_measurement_extra(MeasurementItem.TVMax)

    def time_at_voltage_min(self):
        return self._get_measurement_extra(MeasurementItem.TVMin)

    def positive_slew_rate(self):
        return self._get_measurement_extra(MeasurementItem.PSlewrate)

    def negative_slew_rate(self):
        return self._get_measurement_extra(MeasurementItem.NSlewrate)

    def voltage_threshold_upper(self):
        return self._get_measurement_extra(MeasurementItem.VUpper)

    def voltage_threshold_lower(self):
        return self._get_measurement_extra(MeasurementItem.VLower)

    def voltage_threshold_mid(self):
        return self._get_measurement_extra(MeasurementItem.VMid)

    def variance(self):
        return self._get_measurement_extra(MeasurementItem.Variance)

    def pvoltage_rms(self):
        return self._get_measurement_extra(MeasurementItem.PVRMS)

    def positve_pulse_count(self):
        return self._get_measurement_extra(MeasurementItem.PPulses)

    def negative_pulse_count(self):
        return self._get_measurement_extra(MeasurementItem.NPulses)

    def positive_edge_count(self):
        return self._get_measurement_extra(MeasurementItem.PEdges)

    def negative_edge_count(self):
        return self._get_measurement_extra(MeasurementItem.NEdges)

    def delay_rising_rising_edge(self):
        return self._get_measurement_extra(MeasurementItem.RRDelay)

    def delay_rising_falling_edge(self):
        return self._get_measurement_extra(MeasurementItem.RFDelay)

    def delay_falling_rising_edge(self):
        return self._get_measurement_extra(MeasurementItem.FRDelay)

    def delay_falling_falling_edge(self):
        return self._get_measurement_extra(MeasurementItem.FFDelay)

    def phase_rising_rising_edge(self):
        return self._get_measurement_extra(MeasurementItem.RRPhase)

    def phase_rising_falling_edge(self):
        return self._get_measurement_extra(MeasurementItem.RFPhase)

    def phase_falling_rising_edge(self):
        return self._get_measurement_extra(MeasurementItem.FRPhase)

    def phase_falling_falling_edge(self):
        return self._get_measurement_extra(MeasurementItem.FFPhase)

    def __getattr__(self, attr):
        return getattr(self.device, attr)

class RigolMSO5000FunctionMapper:
    def __init__(self, net, device):
        self.net = net
        self.device = device
        self.measurement = Measurement_RigolMSO5000FunctionMapper(self.net, self.device)
        self.trigger_settings = TriggerSettings_RigolMSO5000FunctionMapper(self.net, self.device)
        self.trace_settings = TraceSettings_RigolMSO5000FunctionMapper(self.net, self.device)

    def autoscale(self):
        self.autoscale()

    def start(self):
        self.run()

    def stop(self):
        self.stop()

    def start_single(self):
        self.single()

    def trigger_force(self):
        self.trigger_force()

    def __getattr__(self, attr):
        return getattr(self.device, attr)

