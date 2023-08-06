from enum import Enum, auto
from lager.lager_pcb.lager_pcb import rigol_mso5000_defines

RigolTriggerType = rigol_mso5000_defines.TriggerType
RigolTriggerMode = rigol_mso5000_defines.TriggerMode
RigolTriggerCoupling = rigol_mso5000_defines.TriggerCoupling

RigolTriggerEdgeSource = rigol_mso5000_defines.TriggerEdgeSource
RigolTriggerEdgeSlope = rigol_mso5000_defines.TriggerEdgeSlope

MeasurementItem = rigol_mso5000_defines.MeasurementItem
MeasurementSource = rigol_mso5000_defines.MeasurementSource
MeasurementClear = rigol_mso5000_defines.MeasurementClear

class TriggerType(Enum):
    Edge = auto()
    Pulse = auto()
    Slope = auto()
    Video = auto()
    Pattern = auto()
    Duration = auto()
    Timeout = auto()
    Runt = auto()
    Window = auto()
    Delay = auto()
    Setup = auto()
    NEdge = auto()
    RS232 = auto()
    IIC = auto()
    SPI = auto()
    CAN = auto()
    Flexray = auto()
    LIN = auto()
    IIS = auto()
    M1553 = auto()

TriggerType_TO_Rigol = {
    TriggerType.Edge: RigolTriggerType.Edge,
    TriggerType.Pulse: RigolTriggerType.Pulse,
    TriggerType.Slope: RigolTriggerType.Slope,
    TriggerType.Video: RigolTriggerType.Video,
    TriggerType.Pattern: RigolTriggerType.Pattern,
    TriggerType.Duration: RigolTriggerType.Duration,
    TriggerType.Timeout: RigolTriggerType.Timeout,
    TriggerType.Runt: RigolTriggerType.Runt,
    TriggerType.Window: RigolTriggerType.Window,
    TriggerType.Delay: RigolTriggerType.Delay,
    TriggerType.Setup: RigolTriggerType.Setup,
    TriggerType.NEdge: RigolTriggerType.NEdge,
    TriggerType.RS232: RigolTriggerType.RS232,
    TriggerType.IIC: RigolTriggerType.IIC,
    TriggerType.SPI: RigolTriggerType.SPI,
    TriggerType.CAN: RigolTriggerType.CAN,
    TriggerType.Flexray: RigolTriggerType.Flexray,
    TriggerType.LIN: RigolTriggerType.LIN,
    TriggerType.IIS: RigolTriggerType.IIS,
    TriggerType.M1553: RigolTriggerType.M1553,
}

Rigol_TO_TriggerType = {v: k for k, v in TriggerType_TO_Rigol.items()}

class TriggerEdgeSource(Enum):
    D0 = auto()
    D1 = auto()
    D2 = auto()
    D3 = auto()
    D4 = auto()
    D5 = auto()
    D6 = auto()
    D7 = auto()
    D8 = auto()
    D9 = auto()
    D10 = auto()
    D11 = auto()
    D12 = auto()
    D13 = auto()
    D14 = auto()
    D15 = auto()
    Channel1 = auto()
    Channel2 = auto()
    Channel3 = auto()
    Channel4 = auto()
    AC_Line = auto()

TriggerEdgeSource_TO_Rigol = {
    TriggerEdgeSource.D0 : RigolTriggerEdgeSource.D0,
    TriggerEdgeSource.D1 : RigolTriggerEdgeSource.D1,
    TriggerEdgeSource.D2 : RigolTriggerEdgeSource.D2,
    TriggerEdgeSource.D3 : RigolTriggerEdgeSource.D3,
    TriggerEdgeSource.D4 : RigolTriggerEdgeSource.D4,
    TriggerEdgeSource.D5 : RigolTriggerEdgeSource.D5,
    TriggerEdgeSource.D6 : RigolTriggerEdgeSource.D6,
    TriggerEdgeSource.D7 : RigolTriggerEdgeSource.D7,
    TriggerEdgeSource.D8 : RigolTriggerEdgeSource.D8,
    TriggerEdgeSource.D9 : RigolTriggerEdgeSource.D9,
    TriggerEdgeSource.D10 : RigolTriggerEdgeSource.D10,
    TriggerEdgeSource.D11 : RigolTriggerEdgeSource.D11,
    TriggerEdgeSource.D12 : RigolTriggerEdgeSource.D12,
    TriggerEdgeSource.D13 : RigolTriggerEdgeSource.D13,
    TriggerEdgeSource.D14 : RigolTriggerEdgeSource.D14,
    TriggerEdgeSource.D15 : RigolTriggerEdgeSource.D15,
    TriggerEdgeSource.Channel1 : RigolTriggerEdgeSource.Channel1,
    TriggerEdgeSource.Channel2 : RigolTriggerEdgeSource.Channel2,
    TriggerEdgeSource.Channel3 : RigolTriggerEdgeSource.Channel3,
    TriggerEdgeSource.Channel4 : RigolTriggerEdgeSource.Channel4,
    TriggerEdgeSource.AC_Line : RigolTriggerEdgeSource.AC_Line,
}
Rigol_TO_TriggerEdgeSource = {v: k for k, v in TriggerEdgeSource_TO_Rigol.items()}


class TriggerEdgeSlope(Enum):
    Rising = auto()
    Falling = auto()
    Both = auto()

TriggerEdgeSlope_TO_Rigol = {
    TriggerEdgeSlope.Rising : RigolTriggerEdgeSlope.Positive,
    TriggerEdgeSlope.Falling : RigolTriggerEdgeSlope.Negative,
    TriggerEdgeSlope.Both : RigolTriggerEdgeSlope.Either,
}
Rigol_TO_TriggerEdgeSlope = {v: k for k, v in TriggerEdgeSlope_TO_Rigol.items()}
