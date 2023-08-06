""" policy_types 

This module contains a collection of YANG groupings
in filter configurations for policy model.

"""
from collections import OrderedDict

from ydk.types import Entity as _Entity_
from ydk.types import EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.types import Entity, EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.filters import YFilter
from ydk.errors import YError, YModelError
from ydk.errors.error_handler import handle_type_error as _handle_type_error

from ydk.models.ietf.ietf_diffserv_classifier import FilterType


class Direction(Enum):
    """
    Direction (Enum Class)

    This typedef defines directional enums used in c3pl.

    inbound\:         Incoming direction.

    outbound\:        Outgoing direction.

    .. data:: inbound = 0

    .. data:: outbound = 1

    """

    inbound = Enum.YLeaf(0, "inbound")

    outbound = Enum.YLeaf(1, "outbound")


class Metric(Enum):
    """
    Metric (Enum Class)

    metric

    .. data:: none = 0

    .. data:: peta = 1

    .. data:: tera = 2

    .. data:: giga = 3

    .. data:: mega = 4

    .. data:: kilo = 5

    .. data:: milli = 6

    .. data:: nano = 7

    """

    none = Enum.YLeaf(0, "none")

    peta = Enum.YLeaf(1, "peta")

    tera = Enum.YLeaf(2, "tera")

    giga = Enum.YLeaf(3, "giga")

    mega = Enum.YLeaf(4, "mega")

    kilo = Enum.YLeaf(5, "kilo")

    milli = Enum.YLeaf(6, "milli")

    nano = Enum.YLeaf(7, "nano")


class RateUnit(Enum):
    """
    RateUnit (Enum Class)

    Unit for traffic rate\:

    pps\:     packets per sec

    cps\:     cells per sec

    bps\:     bits per sec

    perc\:    percentage

    ratio\:   ratio

    .. data:: pps = 0

    .. data:: cps = 1

    .. data:: bps = 2

    .. data:: perc = 3

    .. data:: ratio = 4

    """

    pps = Enum.YLeaf(0, "pps")

    cps = Enum.YLeaf(1, "cps")

    bps = Enum.YLeaf(2, "bps")

    perc = Enum.YLeaf(3, "perc")

    ratio = Enum.YLeaf(4, "ratio")


class PolicyType(Identity):
    """
    This is identity of base policy\-type
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:policy-type"):
        super().__init__(ns, pref, tag)


class ClassType(Identity):
    """
    This is identity of base class\-type
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:class-type"):
        super().__init__(ns, pref, tag)


class Cos(FilterType):
    """
    Filter\-type IEEE 802.1Q/ISL class of service/user
    priority values
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:cos"):
        super().__init__(ns, pref, tag)


class CosInner(FilterType):
    """
    ATM VC configured as Access VC
    class of service/user priority values
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:cos-inner"):
        super().__init__(ns, pref, tag)


class Ipv4AclName(FilterType):
    """
    IPV4 access group list
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:ipv4-acl-name"):
        super().__init__(ns, pref, tag)


class Ipv6AclName(FilterType):
    """
    IPV6 access group list
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:ipv6-acl-name"):
        super().__init__(ns, pref, tag)


class Ipv4Acl(FilterType):
    """
    IPV4 access group Index
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:ipv4-acl"):
        super().__init__(ns, pref, tag)


class Ipv6Acl(FilterType):
    """
    IPV6 access group Index
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:ipv6-acl"):
        super().__init__(ns, pref, tag)


class InputInterface(FilterType):
    """
    Input interface
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:input-interface"):
        super().__init__(ns, pref, tag)


class SrcMac(FilterType):
    """
    Source MAC address
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:src-mac"):
        super().__init__(ns, pref, tag)


class DstMac(FilterType):
    """
    Destination MAC address
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:dst-mac"):
        super().__init__(ns, pref, tag)


class MplsExpTop(FilterType):
    """
    Multi Protocol Label Switching experimental
    topmost specific values
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:mpls-exp-top"):
        super().__init__(ns, pref, tag)


class MplsExpImp(FilterType):
    """
    Multi Protocol Label Switching experimental
    imposition specific values
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:mpls-exp-imp"):
        super().__init__(ns, pref, tag)


class PacketLength(FilterType):
    """
    Layer 3 packet length
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:packet-length"):
        super().__init__(ns, pref, tag)


class Prec(FilterType):
    """
    IP precendence
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:prec"):
        super().__init__(ns, pref, tag)


class QosGroup(FilterType):
    """
    QOS group
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:qos-group"):
        super().__init__(ns, pref, tag)


class Vlan(FilterType):
    """
    Vlan
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:vlan"):
        super().__init__(ns, pref, tag)


class VlanInner(FilterType):
    """
    Vlan\-inner
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:vlan-inner"):
        super().__init__(ns, pref, tag)


class AtmClp(FilterType):
    """
    ATM CLP bit
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:atm-clp"):
        super().__init__(ns, pref, tag)


class AtmVci(FilterType):
    """
    ATM VCI number
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:atm-vci"):
        super().__init__(ns, pref, tag)


class Dei(FilterType):
    """
    Frame\-relay DE bit
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:dei"):
        super().__init__(ns, pref, tag)


class DeiInner(FilterType):
    """
    Frame\-relay inner DE bit
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:dei-inner"):
        super().__init__(ns, pref, tag)


class FlowIp(FilterType):
    """
    Flow IP
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:flow-ip"):
        super().__init__(ns, pref, tag)


class FlowRecord(FilterType):
    """
    FLow record
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:flow-record"):
        super().__init__(ns, pref, tag)


class FlowDe(FilterType):
    """
    Flow DE
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:flow-de"):
        super().__init__(ns, pref, tag)


class FlowDlci(FilterType):
    """
    Frame\-relay DLCI
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:flow-dlci"):
        super().__init__(ns, pref, tag)


class WlanUserPriority(FilterType):
    """
    WLAN user priority
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:wlan-user-priority"):
        super().__init__(ns, pref, tag)


class DiscardClass(FilterType):
    """
    Discard behavior identifier
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:discard-class"):
        super().__init__(ns, pref, tag)


class ClassMap(FilterType):
    """
    class\-map
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:class-map"):
        super().__init__(ns, pref, tag)


class Metadata(FilterType):
    """
    metadata
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:metadata"):
        super().__init__(ns, pref, tag)


class Application(FilterType):
    """
    application
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:application"):
        super().__init__(ns, pref, tag)


class SecurityGroupName(FilterType):
    """
    security group name
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:security-group-name"):
        super().__init__(ns, pref, tag)


class SecurityGroupTag(FilterType):
    """
    security group tag
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:security-group-tag"):
        super().__init__(ns, pref, tag)


class IpRtp(FilterType):
    """
    IP RTP port
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:ip-rtp"):
        super().__init__(ns, pref, tag)


class Vpls(FilterType):
    """
    VPLS
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:vpls"):
        super().__init__(ns, pref, tag)


class Qos(PolicyType):
    """
    Policy\-type QOS (quality of service)
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:qos"):
        super().__init__(ns, pref, tag)


class Pbr(PolicyType):
    """
    Policy\-type PBR (policy based routing)
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:pbr"):
        super().__init__(ns, pref, tag)


class PerfMon(PolicyType):
    """
    Policy\-type PERF\-MON (performance monitoring)
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:perf-mon"):
        super().__init__(ns, pref, tag)


class AccessControl(PolicyType):
    """
    Policy\-type access\-control specific policy\-map
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:access-control"):
        super().__init__(ns, pref, tag)


class Appnav(PolicyType):
    """
    Policy\-type APPNAV Policy Map
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:appnav"):
        super().__init__(ns, pref, tag)


class Control(PolicyType):
    """
    Policy\-type control policy\-map
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:control"):
        super().__init__(ns, pref, tag)


class Inspect(PolicyType):
    """
    Policy\-type Firewall Policy Map
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:inspect"):
        super().__init__(ns, pref, tag)


class PacketService(PolicyType):
    """
    Policy\-type Packet Service Policy Map
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:packet-service"):
        super().__init__(ns, pref, tag)


class Service(PolicyType):
    """
    Policy\-type policymap service configuration
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:service"):
        super().__init__(ns, pref, tag)


class QosClass(ClassType):
    """
    QOS class\-map
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:qos-class"):
        super().__init__(ns, pref, tag)


class AccessControlClass(ClassType):
    """
    Access\-control specific class\-map
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:access-control-class"):
        super().__init__(ns, pref, tag)


class AppnavClass(ClassType):
    """
    APPNAV Class Map
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:appnav-class"):
        super().__init__(ns, pref, tag)


class ControlClass(ClassType):
    """
    Control policy class\-map
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:control-class"):
        super().__init__(ns, pref, tag)


class InspectClass(ClassType):
    """
    Firewall Class Map
    
    """
    _prefix = 'policy-types'
    _revision = '2013-10-07'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:c3pl-types", pref="policy-types", tag="policy-types:inspect-class"):
        super().__init__(ns, pref, tag)



