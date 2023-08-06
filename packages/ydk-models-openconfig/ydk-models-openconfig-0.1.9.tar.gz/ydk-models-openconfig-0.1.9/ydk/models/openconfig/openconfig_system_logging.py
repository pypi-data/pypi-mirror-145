""" openconfig_system_logging 

This module defines configuration and operational state data
for common logging facilities on network systems.

"""
from collections import OrderedDict

from ydk.types import Entity as _Entity_
from ydk.types import EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.types import Entity, EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.filters import YFilter
from ydk.errors import YError, YModelError
from ydk.errors.error_handler import handle_type_error as _handle_type_error


class SyslogSeverity(Enum):
    """
    SyslogSeverity (Enum Class)

    Syslog message severities

    .. data:: EMERGENCY = 0

        Emergency: system is unusable (0)

    .. data:: ALERT = 1

        Alert: action must be taken immediately (1)

    .. data:: CRITICAL = 2

        Critical: critical conditions (2)

    .. data:: ERROR = 3

        Error: error conditions (3)

    .. data:: WARNING = 4

        Warning: warning conditions (4)

    .. data:: NOTICE = 5

        Notice: normal but significant  condition(5)

    .. data:: INFORMATIONAL = 6

        Informational: informational messages (6)

    .. data:: DEBUG = 7

        Debug: debug-level messages (7)

    """

    EMERGENCY = Enum.YLeaf(0, "EMERGENCY")

    ALERT = Enum.YLeaf(1, "ALERT")

    CRITICAL = Enum.YLeaf(2, "CRITICAL")

    ERROR = Enum.YLeaf(3, "ERROR")

    WARNING = Enum.YLeaf(4, "WARNING")

    NOTICE = Enum.YLeaf(5, "NOTICE")

    INFORMATIONAL = Enum.YLeaf(6, "INFORMATIONAL")

    DEBUG = Enum.YLeaf(7, "DEBUG")


class SYSLOGFACILITY(Identity):
    """
    Base identity for Syslog message facilities.
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:SYSLOG_FACILITY"):
        super().__init__(ns, pref, tag)


class LOGDESTINATIONTYPE(Identity):
    """
    Base identity for destination for logging messages
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:LOG_DESTINATION_TYPE"):
        super().__init__(ns, pref, tag)


class ALL(SYSLOGFACILITY):
    """
    All supported facilities
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:ALL"):
        super().__init__(ns, pref, tag)


class KERNEL(SYSLOGFACILITY):
    """
    The facility for kernel messages
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:KERNEL"):
        super().__init__(ns, pref, tag)


class USER(SYSLOGFACILITY):
    """
    The facility for user\-level messages.
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:USER"):
        super().__init__(ns, pref, tag)


class MAIL(SYSLOGFACILITY):
    """
    The facility for the mail system.
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:MAIL"):
        super().__init__(ns, pref, tag)


class SYSTEMDAEMON(SYSLOGFACILITY):
    """
    The facility for the system daemons.
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:SYSTEM_DAEMON"):
        super().__init__(ns, pref, tag)


class AUTH(SYSLOGFACILITY):
    """
    The facility for security/authorization messages.
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:AUTH"):
        super().__init__(ns, pref, tag)


class SYSLOG(SYSLOGFACILITY):
    """
    The facility for messages generated internally by syslogd
    facility.
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:SYSLOG"):
        super().__init__(ns, pref, tag)


class AUTHPRIV(SYSLOGFACILITY):
    """
    The facility for privileged security/authorization messages.
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:AUTHPRIV"):
        super().__init__(ns, pref, tag)


class NTP(SYSLOGFACILITY):
    """
    The facility for the NTP subsystem.
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:NTP"):
        super().__init__(ns, pref, tag)


class AUDIT(SYSLOGFACILITY):
    """
    The facility for log audit messages.
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:AUDIT"):
        super().__init__(ns, pref, tag)


class CONSOLE(SYSLOGFACILITY):
    """
    The facility for log alert messages.
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:CONSOLE"):
        super().__init__(ns, pref, tag)


class LOCAL0(SYSLOGFACILITY):
    """
    The facility for local use 0 messages.
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:LOCAL0"):
        super().__init__(ns, pref, tag)


class LOCAL1(SYSLOGFACILITY):
    """
    The facility for local use 1 messages.
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:LOCAL1"):
        super().__init__(ns, pref, tag)


class LOCAL2(SYSLOGFACILITY):
    """
    The facility for local use 2 messages.
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:LOCAL2"):
        super().__init__(ns, pref, tag)


class LOCAL3(SYSLOGFACILITY):
    """
    The facility for local use 3 messages.
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:LOCAL3"):
        super().__init__(ns, pref, tag)


class LOCAL4(SYSLOGFACILITY):
    """
    The facility for local use 4 messages.
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:LOCAL4"):
        super().__init__(ns, pref, tag)


class LOCAL5(SYSLOGFACILITY):
    """
    The facility for local use 5 messages.
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:LOCAL5"):
        super().__init__(ns, pref, tag)


class LOCAL6(SYSLOGFACILITY):
    """
    The facility for local use 6 messages.
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:LOCAL6"):
        super().__init__(ns, pref, tag)


class LOCAL7(SYSLOGFACILITY):
    """
    The facility for local use 7 messages.
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:LOCAL7"):
        super().__init__(ns, pref, tag)


class DESTCONSOLE(LOGDESTINATIONTYPE):
    """
    Directs log messages to the console
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:DEST_CONSOLE"):
        super().__init__(ns, pref, tag)


class DESTBUFFER(LOGDESTINATIONTYPE):
    """
    Directs log messages to and in\-memory circular buffer
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:DEST_BUFFER"):
        super().__init__(ns, pref, tag)


class DESTFILE(LOGDESTINATIONTYPE):
    """
    Directs log messages to a local file
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:DEST_FILE"):
        super().__init__(ns, pref, tag)


class DESTREMOTE(LOGDESTINATIONTYPE):
    """
    Directs log messages to a remote syslog server
    
    """
    _prefix = 'oc-log'
    _revision = '2017-09-18'

    def __init__(self, ns="http://openconfig.net/yang/system/logging", pref="openconfig-system-logging", tag="openconfig-system-logging:DEST_REMOTE"):
        super().__init__(ns, pref, tag)



