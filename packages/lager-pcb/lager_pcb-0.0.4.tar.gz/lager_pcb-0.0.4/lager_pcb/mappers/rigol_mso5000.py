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

    def voltage_max(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            vmax = float(self.get_measure_item(MeasurementItem.VMax, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return vmax


    def voltage_min(self, display=False):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            vmin = float(self.get_measure_item(MeasurementItem.VMin, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return vmin

    def voltage_peak_to_peak(self, display=False):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            vpp = float(self.get_measure_item(MeasurementItem.VPP, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return vpp

    def voltage_flat_top(self, display=False):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            vtop = float(self.get_measure_item(MeasurementItem.VTop, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return vtop

    def voltage_flat_base(self, display=False):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            vbase = float(self.get_measure_item(MeasurementItem.VBase, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return vbase

    def voltage_flat_amplitude(self, display=False):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            vamp = float(self.get_measure_item(MeasurementItem.VAmp, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return vamp

    def voltage_average(self, display=False):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            vavg = float(self.get_measure_item(MeasurementItem.VAvg, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return vavg

    def voltage_rms(self, display=False):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            vrms = float(self.get_measure_item(MeasurementItem.VRMS, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return vrms

    def voltage_overshoot(self, display=False):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            overshoot = float(self.get_measure_item(MeasurementItem.Overshoot, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return overshoot

    def voltage_preshoot(self, display=False):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            preshoot = float(self.get_measure_item(MeasurementItem.Preshoot, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return preshoot

    def waveform_area(self, display=False):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            marea = float(self.get_measure_item(MeasurementItem.MArea, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return marea

    def waveform_period_area(self, display=False):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            mparea = float(self.get_measure_item(MeasurementItem.MPArea, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return mparea

    def period(self, display=False):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            period = float(self.get_measure_item(MeasurementItem.Period, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return period

    def frequency(self, display=False):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            freq = float(self.get_measure_item(MeasurementItem.Frequency, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return freq

    def rise_time(self, display=False):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            rtime = float(self.get_measure_item(MeasurementItem.RTime, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return rtime

    def fall_time(self, display=False):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            ftime = float(self.get_measure_item(MeasurementItem.FTime, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return ftime

    def pulse_width_positive(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            pwidth = float(self.get_measure_item(MeasurementItem.PWidth, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return pwidth

    def pulse_width_negative(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            nwidth = float(self.get_measure_item(MeasurementItem.NWidth, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return nwidth

    def duty_cycle_positive(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            pduty = float(self.get_measure_item(MeasurementItem.PDuty, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return pduty

    def duty_cycle_negative(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            nduty = float(self.get_measure_item(MeasurementItem.NDuty, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return nduty

    def time_at_voltage_max(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            tvmax = float(self.get_measure_item(MeasurementItem.TVMax, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return tvmax

    def time_at_voltage_min(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            tvmin = float(self.get_measure_item(MeasurementItem.TVMin, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return tvmin

    def positive_slew_rate(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            pos_slew_rate = float(self.get_measure_item(MeasurementItem.PSlewrate, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return pos_slew_rate

    def negative_slew_rate(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            neg_slew_rate = float(self.get_measure_item(MeasurementItem.NSlewrate, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return neg_slew_rate

    def voltage_threshold_upper(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            volt_upper = float(self.get_measure_item(MeasurementItem.VUpper, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return volt_upper

    def voltage_threshold_lower(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            volt_lower = float(self.get_measure_item(MeasurementItem.VLower, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return volt_lower

    def voltage_threshold_mid(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            volt_mid = float(self.get_measure_item(MeasurementItem.VMid, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return volt_mid

    def variance(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            variance = float(self.get_measure_item(MeasurementItem.Variance, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return variance

    def pvoltage_rms(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            pvrms = float(self.get_measure_item(MeasurementItem.PVRMS, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return pvrms

    def positve_pulse_count(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            pos_pulses = float(self.get_measure_item(MeasurementItem.PPulses, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return pos_pulses

    def negative_pulse_count(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            neg_pulses = float(self.get_measure_item(MeasurementItem.NPulses, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return neg_pulses

    def positive_edge_count(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            pos_edges = float(self.get_measure_item(MeasurementItem.PEdges, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return pos_edges

    def negative_edge_count(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            neg_edges = float(self.get_measure_item(MeasurementItem.NEdges, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return neg_edges

    def delay_rising_rising_edge(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            return float(self.get_measure_item(MeasurementItem.RRDelay, chan))
        except:
            return None
        finally:
            self.clear_measurement(MeasurementClear.All)

    def delay_rising_falling_edge(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            return float(self.get_measure_item(MeasurementItem.RFDelay, chan))
        except:
            return None
        finally:
            self.clear_measurement(MeasurementClear.All)

    def delay_falling_rising_edge(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            return float(self.get_measure_item(MeasurementItem.FRDelay, chan))
        except:
            return None
        finally:
            self.clear_measurement(MeasurementClear.All)

    def delay_falling_falling_edge(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            return float(self.get_measure_item(MeasurementItem.FFDelay, chan))
        except:
            return None
        finally:
            self.clear_measurement(MeasurementClear.All)

    def phase_rising_rising_edge(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            return float(self.get_measure_item(MeasurementItem.RRPhase, chan))
        except:
            return None
        finally:
            self.clear_measurement(MeasurementClear.All)

    def phase_rising_falling_edge(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            rise_fall_phase = float(self.get_measure_item(MeasurementItem.RFPhase, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return rise_fall_phase

    def phase_falling_rising_edge(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            fall_rise_phase = float(self.get_measure_item(MeasurementItem.FRPhase, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return fall_rise_phase

    def phase_falling_falling_edge(self):
        chan = map_mux_channel_to_scope(self.net.channel)
        try:
            fall_fall_phase = float(self.get_measure_item(MeasurementItem.FFPhase, chan))
        except:
            return None
        self.clear_measurement(MeasurementClear.All)
        return fall_fall_phase

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

