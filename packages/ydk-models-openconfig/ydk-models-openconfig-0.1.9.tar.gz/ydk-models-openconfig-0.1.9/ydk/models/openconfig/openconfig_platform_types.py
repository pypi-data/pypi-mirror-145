""" openconfig_platform_types 

This module defines data types (e.g., YANG identities)
to support the OpenConfig component inventory model.

"""
from collections import OrderedDict

from ydk.types import Entity as _Entity_
from ydk.types import EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.types import Entity, EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.filters import YFilter
from ydk.errors import YError, YModelError
from ydk.errors.error_handler import handle_type_error as _handle_type_error


class ComponentPowerType(Enum):
    """
    ComponentPowerType (Enum Class)

    A generic type reflecting whether a hardware component

    is powered on or off

    .. data:: POWER_ENABLED = 0

        Enable power on the component

    .. data:: POWER_DISABLED = 1

        Disable power on the component

    """

    POWER_ENABLED = Enum.YLeaf(0, "POWER_ENABLED")

    POWER_DISABLED = Enum.YLeaf(1, "POWER_DISABLED")


class OPENCONFIGHARDWARECOMPONENT(Identity):
    """
    Base identity for hardware related components in a managed
    device.  Derived identities are partially based on contents
    of the IANA Entity MIB.
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:OPENCONFIG_HARDWARE_COMPONENT"):
        super().__init__(ns, pref, tag)


class OPENCONFIGSOFTWARECOMPONENT(Identity):
    """
    Base identity for software\-related components in a managed
    device
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:OPENCONFIG_SOFTWARE_COMPONENT"):
        super().__init__(ns, pref, tag)


class COMPONENTOPERSTATUS(Identity):
    """
    Current operational status of a platform component
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:COMPONENT_OPER_STATUS"):
        super().__init__(ns, pref, tag)


class FECMODETYPE(Identity):
    """
    Base identity for FEC operational modes.
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:FEC_MODE_TYPE"):
        super().__init__(ns, pref, tag)


class FECSTATUSTYPE(Identity):
    """
    Base identity for FEC operational statuses.
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:FEC_STATUS_TYPE"):
        super().__init__(ns, pref, tag)


class CHASSIS(OPENCONFIGHARDWARECOMPONENT):
    """
    Chassis component, typically with multiple slots / shelves
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:CHASSIS"):
        super().__init__(ns, pref, tag)


class BACKPLANE(OPENCONFIGHARDWARECOMPONENT):
    """
    Backplane component for aggregating traffic, typically
    contained in a chassis component
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:BACKPLANE"):
        super().__init__(ns, pref, tag)


class FABRIC(OPENCONFIGHARDWARECOMPONENT):
    """
    Interconnect between ingress and egress ports on the
    device (e.g., a crossbar switch).
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:FABRIC"):
        super().__init__(ns, pref, tag)


class POWERSUPPLY(OPENCONFIGHARDWARECOMPONENT):
    """
    Component that is supplying power to the device
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:POWER_SUPPLY"):
        super().__init__(ns, pref, tag)


class FAN(OPENCONFIGHARDWARECOMPONENT):
    """
    Cooling fan, or could be some other heat\-reduction component
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:FAN"):
        super().__init__(ns, pref, tag)


class SENSOR(OPENCONFIGHARDWARECOMPONENT):
    """
    Physical sensor, e.g., a temperature sensor in a chassis
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:SENSOR"):
        super().__init__(ns, pref, tag)


class FRU(OPENCONFIGHARDWARECOMPONENT):
    """
    Replaceable hardware component that does not have a more
    specific defined schema.
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:FRU"):
        super().__init__(ns, pref, tag)


class LINECARD(OPENCONFIGHARDWARECOMPONENT):
    """
    Linecard component, typically inserted into a chassis slot
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:LINECARD"):
        super().__init__(ns, pref, tag)


class CONTROLLERCARD(OPENCONFIGHARDWARECOMPONENT):
    """
    A type of linecard whose primary role is management or control
    rather than data forwarding.
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:CONTROLLER_CARD"):
        super().__init__(ns, pref, tag)


class PORT(OPENCONFIGHARDWARECOMPONENT):
    """
    Physical port, e.g., for attaching pluggables and networking
    cables
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:PORT"):
        super().__init__(ns, pref, tag)


class TRANSCEIVER(OPENCONFIGHARDWARECOMPONENT):
    """
    Pluggable module present in a port
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:TRANSCEIVER"):
        super().__init__(ns, pref, tag)


class CPU(OPENCONFIGHARDWARECOMPONENT):
    """
    Processing unit, e.g., a management processor
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:CPU"):
        super().__init__(ns, pref, tag)


class STORAGE(OPENCONFIGHARDWARECOMPONENT):
    """
    A storage subsystem on the device (disk, SSD, etc.)
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:STORAGE"):
        super().__init__(ns, pref, tag)


class INTEGRATEDCIRCUIT(OPENCONFIGHARDWARECOMPONENT):
    """
    A special purpose processing unit, typically for traffic
    switching/forwarding (e.g., switching ASIC, NPU, forwarding
    chip, etc.)
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:INTEGRATED_CIRCUIT"):
        super().__init__(ns, pref, tag)


class OPERATINGSYSTEM(OPENCONFIGSOFTWARECOMPONENT):
    """
    Operating system running on a component
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:OPERATING_SYSTEM"):
        super().__init__(ns, pref, tag)


class ACTIVE(COMPONENTOPERSTATUS):
    """
    Component is enabled and active (i.e., up)
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:ACTIVE"):
        super().__init__(ns, pref, tag)


class INACTIVE(COMPONENTOPERSTATUS):
    """
    Component is enabled but inactive (i.e., down)
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:INACTIVE"):
        super().__init__(ns, pref, tag)


class DISABLED(COMPONENTOPERSTATUS):
    """
    Component is administratively disabled.
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:DISABLED"):
        super().__init__(ns, pref, tag)


class FECENABLED(FECMODETYPE):
    """
    FEC is administratively enabled.
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:FEC_ENABLED"):
        super().__init__(ns, pref, tag)


class FECDISABLED(FECMODETYPE):
    """
    FEC is administratively disabled.
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:FEC_DISABLED"):
        super().__init__(ns, pref, tag)


class FECAUTO(FECMODETYPE):
    """
    System will determine whether to enable or disable
    FEC on a transceiver.
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:FEC_AUTO"):
        super().__init__(ns, pref, tag)


class FECSTATUSLOCKED(FECSTATUSTYPE):
    """
    FEC is operationally locked.
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:FEC_STATUS_LOCKED"):
        super().__init__(ns, pref, tag)


class FECSTATUSUNLOCKED(FECSTATUSTYPE):
    """
    FEC is operationally unlocked.
    
    """
    _prefix = 'oc-platform-types'
    _revision = '2018-11-21'

    def __init__(self, ns="http://openconfig.net/yang/platform-types", pref="openconfig-platform-types", tag="openconfig-platform-types:FEC_STATUS_UNLOCKED"):
        super().__init__(ns, pref, tag)



