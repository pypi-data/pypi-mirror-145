""" iana_if_type 

This YANG module defines YANG identities for IANA\-registered
interface types.

This YANG module is maintained by IANA and reflects the
'ifType definitions' registry.

The latest revision of this YANG module can be obtained from
the IANA web site.

Requests for new values should be made to IANA via
email (iana@iana.org).

Copyright (c) 2014 IETF Trust and the persons identified as
authors of the code.  All rights reserved.

Redistribution and use in source and binary forms, with or
without modification, is permitted pursuant to, and subject
to the license terms contained in, the Simplified BSD License
set forth in Section 4.c of the IETF Trust's Legal Provisions
Relating to IETF Documents
(http\://trustee.ietf.org/license\-info).

The initial version of this YANG module is part of RFC 7224;
see the RFC itself for full legal notices.

"""
from collections import OrderedDict

from ydk.types import Entity as _Entity_
from ydk.types import EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.types import Entity, EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.filters import YFilter
from ydk.errors import YError, YModelError
from ydk.errors.error_handler import handle_type_error as _handle_type_error

from ydk.models.ietf.ietf_interfaces import InterfaceType


class IanaInterfaceType(InterfaceType):
    """
    This identity is used as a base for all interface types
    defined in the 'ifType definitions' registry.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:iana-interface-type"):
        super().__init__(ns, pref, tag)


class Other(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:other"):
        super().__init__(ns, pref, tag)


class Regular1822(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:regular1822"):
        super().__init__(ns, pref, tag)


class Hdh1822(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:hdh1822"):
        super().__init__(ns, pref, tag)


class DdnX25(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ddnX25"):
        super().__init__(ns, pref, tag)


class Rfc877x25(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:rfc877x25"):
        super().__init__(ns, pref, tag)


class EthernetCsmacd(IanaInterfaceType):
    """
    For all Ethernet\-like interfaces, regardless of speed,
    as per RFC 3635.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ethernetCsmacd"):
        super().__init__(ns, pref, tag)


class Iso88023Csmacd(IanaInterfaceType):
    """
    Deprecated via RFC 3635.
    Use ethernetCsmacd(6) instead.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:iso88023Csmacd"):
        super().__init__(ns, pref, tag)


class Iso88024TokenBus(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:iso88024TokenBus"):
        super().__init__(ns, pref, tag)


class Iso88025TokenRing(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:iso88025TokenRing"):
        super().__init__(ns, pref, tag)


class Iso88026Man(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:iso88026Man"):
        super().__init__(ns, pref, tag)


class StarLan(IanaInterfaceType):
    """
    Deprecated via RFC 3635.
    Use ethernetCsmacd(6) instead.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:starLan"):
        super().__init__(ns, pref, tag)


class Proteon10Mbit(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:proteon10Mbit"):
        super().__init__(ns, pref, tag)


class Proteon80Mbit(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:proteon80Mbit"):
        super().__init__(ns, pref, tag)


class Hyperchannel(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:hyperchannel"):
        super().__init__(ns, pref, tag)


class Fddi(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:fddi"):
        super().__init__(ns, pref, tag)


class Lapb(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:lapb"):
        super().__init__(ns, pref, tag)


class Sdlc(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:sdlc"):
        super().__init__(ns, pref, tag)


class Ds1(IanaInterfaceType):
    """
    DS1\-MIB.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ds1"):
        super().__init__(ns, pref, tag)


class E1(IanaInterfaceType):
    """
    Obsolete; see DS1\-MIB.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:e1"):
        super().__init__(ns, pref, tag)


class BasicISDN(IanaInterfaceType):
    """
    No longer used.  See also RFC 2127.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:basicISDN"):
        super().__init__(ns, pref, tag)


class PrimaryISDN(IanaInterfaceType):
    """
    No longer used.  See also RFC 2127.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:primaryISDN"):
        super().__init__(ns, pref, tag)


class PropPointToPointSerial(IanaInterfaceType):
    """
    Proprietary serial.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:propPointToPointSerial"):
        super().__init__(ns, pref, tag)


class Ppp(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ppp"):
        super().__init__(ns, pref, tag)


class SoftwareLoopback(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:softwareLoopback"):
        super().__init__(ns, pref, tag)


class Eon(IanaInterfaceType):
    """
    CLNP over IP.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:eon"):
        super().__init__(ns, pref, tag)


class Ethernet3Mbit(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ethernet3Mbit"):
        super().__init__(ns, pref, tag)


class Nsip(IanaInterfaceType):
    """
    XNS over IP.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:nsip"):
        super().__init__(ns, pref, tag)


class Slip(IanaInterfaceType):
    """
    Generic SLIP.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:slip"):
        super().__init__(ns, pref, tag)


class Ultra(IanaInterfaceType):
    """
    Ultra Technologies.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ultra"):
        super().__init__(ns, pref, tag)


class Ds3(IanaInterfaceType):
    """
    DS3\-MIB.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ds3"):
        super().__init__(ns, pref, tag)


class Sip(IanaInterfaceType):
    """
    SMDS, coffee.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:sip"):
        super().__init__(ns, pref, tag)


class FrameRelay(IanaInterfaceType):
    """
    DTE only.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:frameRelay"):
        super().__init__(ns, pref, tag)


class Rs232(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:rs232"):
        super().__init__(ns, pref, tag)


class Para(IanaInterfaceType):
    """
    Parallel\-port.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:para"):
        super().__init__(ns, pref, tag)


class Arcnet(IanaInterfaceType):
    """
    ARCnet.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:arcnet"):
        super().__init__(ns, pref, tag)


class ArcnetPlus(IanaInterfaceType):
    """
    ARCnet Plus.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:arcnetPlus"):
        super().__init__(ns, pref, tag)


class Atm(IanaInterfaceType):
    """
    ATM cells.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:atm"):
        super().__init__(ns, pref, tag)


class Miox25(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:miox25"):
        super().__init__(ns, pref, tag)


class Sonet(IanaInterfaceType):
    """
    SONET or SDH.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:sonet"):
        super().__init__(ns, pref, tag)


class X25ple(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:x25ple"):
        super().__init__(ns, pref, tag)


class Iso88022llc(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:iso88022llc"):
        super().__init__(ns, pref, tag)


class LocalTalk(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:localTalk"):
        super().__init__(ns, pref, tag)


class SmdsDxi(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:smdsDxi"):
        super().__init__(ns, pref, tag)


class FrameRelayService(IanaInterfaceType):
    """
    FRNETSERV\-MIB.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:frameRelayService"):
        super().__init__(ns, pref, tag)


class V35(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:v35"):
        super().__init__(ns, pref, tag)


class Hssi(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:hssi"):
        super().__init__(ns, pref, tag)


class Hippi(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:hippi"):
        super().__init__(ns, pref, tag)


class Modem(IanaInterfaceType):
    """
    Generic modem.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:modem"):
        super().__init__(ns, pref, tag)


class Aal5(IanaInterfaceType):
    """
    AAL5 over ATM.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:aal5"):
        super().__init__(ns, pref, tag)


class SonetPath(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:sonetPath"):
        super().__init__(ns, pref, tag)


class SonetVT(IanaInterfaceType):
    """
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:sonetVT"):
        super().__init__(ns, pref, tag)


class SmdsIcip(IanaInterfaceType):
    """
    SMDS InterCarrier Interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:smdsIcip"):
        super().__init__(ns, pref, tag)


class PropVirtual(IanaInterfaceType):
    """
    Proprietary virtual/internal.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:propVirtual"):
        super().__init__(ns, pref, tag)


class PropMultiplexor(IanaInterfaceType):
    """
    Proprietary multiplexing.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:propMultiplexor"):
        super().__init__(ns, pref, tag)


class Ieee80212(IanaInterfaceType):
    """
    100BaseVG.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ieee80212"):
        super().__init__(ns, pref, tag)


class FibreChannel(IanaInterfaceType):
    """
    Fibre Channel.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:fibreChannel"):
        super().__init__(ns, pref, tag)


class HippiInterface(IanaInterfaceType):
    """
    HIPPI interfaces.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:hippiInterface"):
        super().__init__(ns, pref, tag)


class FrameRelayInterconnect(IanaInterfaceType):
    """
    Obsolete; use either
    frameRelay(32) or frameRelayService(44).
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:frameRelayInterconnect"):
        super().__init__(ns, pref, tag)


class Aflane8023(IanaInterfaceType):
    """
    ATM Emulated LAN for 802.3.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:aflane8023"):
        super().__init__(ns, pref, tag)


class Aflane8025(IanaInterfaceType):
    """
    ATM Emulated LAN for 802.5.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:aflane8025"):
        super().__init__(ns, pref, tag)


class CctEmul(IanaInterfaceType):
    """
    ATM Emulated circuit.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:cctEmul"):
        super().__init__(ns, pref, tag)


class FastEther(IanaInterfaceType):
    """
    Obsoleted via RFC 3635.
    ethernetCsmacd(6) should be used instead.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:fastEther"):
        super().__init__(ns, pref, tag)


class Isdn(IanaInterfaceType):
    """
    ISDN and X.25.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:isdn"):
        super().__init__(ns, pref, tag)


class V11(IanaInterfaceType):
    """
    CCITT V.11/X.21.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:v11"):
        super().__init__(ns, pref, tag)


class V36(IanaInterfaceType):
    """
    CCITT V.36.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:v36"):
        super().__init__(ns, pref, tag)


class G703at64k(IanaInterfaceType):
    """
    CCITT G703 at 64Kbps.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:g703at64k"):
        super().__init__(ns, pref, tag)


class G703at2mb(IanaInterfaceType):
    """
    Obsolete; see DS1\-MIB.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:g703at2mb"):
        super().__init__(ns, pref, tag)


class Qllc(IanaInterfaceType):
    """
    SNA QLLC.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:qllc"):
        super().__init__(ns, pref, tag)


class FastEtherFX(IanaInterfaceType):
    """
    Obsoleted via RFC 3635.
    ethernetCsmacd(6) should be used instead.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:fastEtherFX"):
        super().__init__(ns, pref, tag)


class Channel(IanaInterfaceType):
    """
    Channel.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:channel"):
        super().__init__(ns, pref, tag)


class Ieee80211(IanaInterfaceType):
    """
    Radio spread spectrum.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ieee80211"):
        super().__init__(ns, pref, tag)


class Ibm370parChan(IanaInterfaceType):
    """
    IBM System 360/370 OEMI Channel.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ibm370parChan"):
        super().__init__(ns, pref, tag)


class Escon(IanaInterfaceType):
    """
    IBM Enterprise Systems Connection.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:escon"):
        super().__init__(ns, pref, tag)


class Dlsw(IanaInterfaceType):
    """
    Data Link Switching.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:dlsw"):
        super().__init__(ns, pref, tag)


class Isdns(IanaInterfaceType):
    """
    ISDN S/T interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:isdns"):
        super().__init__(ns, pref, tag)


class Isdnu(IanaInterfaceType):
    """
    ISDN U interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:isdnu"):
        super().__init__(ns, pref, tag)


class Lapd(IanaInterfaceType):
    """
    Link Access Protocol D.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:lapd"):
        super().__init__(ns, pref, tag)


class IpSwitch(IanaInterfaceType):
    """
    IP Switching Objects.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ipSwitch"):
        super().__init__(ns, pref, tag)


class Rsrb(IanaInterfaceType):
    """
    Remote Source Route Bridging.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:rsrb"):
        super().__init__(ns, pref, tag)


class AtmLogical(IanaInterfaceType):
    """
    ATM Logical Port.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:atmLogical"):
        super().__init__(ns, pref, tag)


class Ds0(IanaInterfaceType):
    """
    Digital Signal Level 0.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ds0"):
        super().__init__(ns, pref, tag)


class Ds0Bundle(IanaInterfaceType):
    """
    Group of ds0s on the same ds1.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ds0Bundle"):
        super().__init__(ns, pref, tag)


class Bsc(IanaInterfaceType):
    """
    Bisynchronous Protocol.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:bsc"):
        super().__init__(ns, pref, tag)


class Async(IanaInterfaceType):
    """
    Asynchronous Protocol.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:async"):
        super().__init__(ns, pref, tag)


class Cnr(IanaInterfaceType):
    """
    Combat Net Radio.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:cnr"):
        super().__init__(ns, pref, tag)


class Iso88025Dtr(IanaInterfaceType):
    """
    ISO 802.5r DTR.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:iso88025Dtr"):
        super().__init__(ns, pref, tag)


class Eplrs(IanaInterfaceType):
    """
    Ext Pos Loc Report Sys.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:eplrs"):
        super().__init__(ns, pref, tag)


class Arap(IanaInterfaceType):
    """
    Appletalk Remote Access Protocol.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:arap"):
        super().__init__(ns, pref, tag)


class PropCnls(IanaInterfaceType):
    """
    Proprietary Connectionless Protocol.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:propCnls"):
        super().__init__(ns, pref, tag)


class HostPad(IanaInterfaceType):
    """
    CCITT\-ITU X.29 PAD Protocol.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:hostPad"):
        super().__init__(ns, pref, tag)


class TermPad(IanaInterfaceType):
    """
    CCITT\-ITU X.3 PAD Facility.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:termPad"):
        super().__init__(ns, pref, tag)


class FrameRelayMPI(IanaInterfaceType):
    """
    Multiproto Interconnect over FR.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:frameRelayMPI"):
        super().__init__(ns, pref, tag)


class X213(IanaInterfaceType):
    """
    CCITT\-ITU X213.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:x213"):
        super().__init__(ns, pref, tag)


class Adsl(IanaInterfaceType):
    """
    Asymmetric Digital Subscriber Loop.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:adsl"):
        super().__init__(ns, pref, tag)


class Radsl(IanaInterfaceType):
    """
    Rate\-Adapt. Digital Subscriber Loop.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:radsl"):
        super().__init__(ns, pref, tag)


class Sdsl(IanaInterfaceType):
    """
    Symmetric Digital Subscriber Loop.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:sdsl"):
        super().__init__(ns, pref, tag)


class Vdsl(IanaInterfaceType):
    """
    Very H\-Speed Digital Subscrib. Loop.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:vdsl"):
        super().__init__(ns, pref, tag)


class Iso88025CRFPInt(IanaInterfaceType):
    """
    ISO 802.5 CRFP.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:iso88025CRFPInt"):
        super().__init__(ns, pref, tag)


class Myrinet(IanaInterfaceType):
    """
    Myricom Myrinet.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:myrinet"):
        super().__init__(ns, pref, tag)


class VoiceEM(IanaInterfaceType):
    """
    Voice recEive and transMit.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:voiceEM"):
        super().__init__(ns, pref, tag)


class VoiceFXO(IanaInterfaceType):
    """
    Voice Foreign Exchange Office.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:voiceFXO"):
        super().__init__(ns, pref, tag)


class VoiceFXS(IanaInterfaceType):
    """
    Voice Foreign Exchange Station.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:voiceFXS"):
        super().__init__(ns, pref, tag)


class VoiceEncap(IanaInterfaceType):
    """
    Voice encapsulation.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:voiceEncap"):
        super().__init__(ns, pref, tag)


class VoiceOverIp(IanaInterfaceType):
    """
    Voice over IP encapsulation.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:voiceOverIp"):
        super().__init__(ns, pref, tag)


class AtmDxi(IanaInterfaceType):
    """
    ATM DXI.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:atmDxi"):
        super().__init__(ns, pref, tag)


class AtmFuni(IanaInterfaceType):
    """
    ATM FUNI.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:atmFuni"):
        super().__init__(ns, pref, tag)


class AtmIma(IanaInterfaceType):
    """
    ATM IMA.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:atmIma"):
        super().__init__(ns, pref, tag)


class PppMultilinkBundle(IanaInterfaceType):
    """
    PPP Multilink Bundle.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:pppMultilinkBundle"):
        super().__init__(ns, pref, tag)


class IpOverCdlc(IanaInterfaceType):
    """
    IBM ipOverCdlc.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ipOverCdlc"):
        super().__init__(ns, pref, tag)


class IpOverClaw(IanaInterfaceType):
    """
    IBM Common Link Access to Workstn.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ipOverClaw"):
        super().__init__(ns, pref, tag)


class StackToStack(IanaInterfaceType):
    """
    IBM stackToStack.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:stackToStack"):
        super().__init__(ns, pref, tag)


class VirtualIpAddress(IanaInterfaceType):
    """
    IBM VIPA.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:virtualIpAddress"):
        super().__init__(ns, pref, tag)


class Mpc(IanaInterfaceType):
    """
    IBM multi\-protocol channel support.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:mpc"):
        super().__init__(ns, pref, tag)


class IpOverAtm(IanaInterfaceType):
    """
    IBM ipOverAtm.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ipOverAtm"):
        super().__init__(ns, pref, tag)


class Iso88025Fiber(IanaInterfaceType):
    """
    ISO 802.5j Fiber Token Ring.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:iso88025Fiber"):
        super().__init__(ns, pref, tag)


class Tdlc(IanaInterfaceType):
    """
    IBM twinaxial data link control.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:tdlc"):
        super().__init__(ns, pref, tag)


class GigabitEthernet(IanaInterfaceType):
    """
    Obsoleted via RFC 3635.
    ethernetCsmacd(6) should be used instead.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:gigabitEthernet"):
        super().__init__(ns, pref, tag)


class Hdlc(IanaInterfaceType):
    """
    HDLC.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:hdlc"):
        super().__init__(ns, pref, tag)


class Lapf(IanaInterfaceType):
    """
    LAP F.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:lapf"):
        super().__init__(ns, pref, tag)


class V37(IanaInterfaceType):
    """
    V.37.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:v37"):
        super().__init__(ns, pref, tag)


class X25mlp(IanaInterfaceType):
    """
    Multi\-Link Protocol.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:x25mlp"):
        super().__init__(ns, pref, tag)


class X25huntGroup(IanaInterfaceType):
    """
    X25 Hunt Group.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:x25huntGroup"):
        super().__init__(ns, pref, tag)


class TranspHdlc(IanaInterfaceType):
    """
    Transp HDLC.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:transpHdlc"):
        super().__init__(ns, pref, tag)


class Interleave(IanaInterfaceType):
    """
    Interleave channel.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:interleave"):
        super().__init__(ns, pref, tag)


class Fast(IanaInterfaceType):
    """
    Fast channel.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:fast"):
        super().__init__(ns, pref, tag)


class Ip(IanaInterfaceType):
    """
    IP (for APPN HPR in IP networks).
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ip"):
        super().__init__(ns, pref, tag)


class DocsCableMaclayer(IanaInterfaceType):
    """
    CATV Mac Layer.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:docsCableMaclayer"):
        super().__init__(ns, pref, tag)


class DocsCableDownstream(IanaInterfaceType):
    """
    CATV Downstream interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:docsCableDownstream"):
        super().__init__(ns, pref, tag)


class DocsCableUpstream(IanaInterfaceType):
    """
    CATV Upstream interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:docsCableUpstream"):
        super().__init__(ns, pref, tag)


class A12MppSwitch(IanaInterfaceType):
    """
    Avalon Parallel Processor.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:a12MppSwitch"):
        super().__init__(ns, pref, tag)


class Tunnel(IanaInterfaceType):
    """
    Encapsulation interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:tunnel"):
        super().__init__(ns, pref, tag)


class Coffee(IanaInterfaceType):
    """
    Coffee pot.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:coffee"):
        super().__init__(ns, pref, tag)


class Ces(IanaInterfaceType):
    """
    Circuit Emulation Service.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ces"):
        super().__init__(ns, pref, tag)


class AtmSubInterface(IanaInterfaceType):
    """
    ATM Sub Interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:atmSubInterface"):
        super().__init__(ns, pref, tag)


class L2vlan(IanaInterfaceType):
    """
    Layer 2 Virtual LAN using 802.1Q.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:l2vlan"):
        super().__init__(ns, pref, tag)


class L3ipvlan(IanaInterfaceType):
    """
    Layer 3 Virtual LAN using IP.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:l3ipvlan"):
        super().__init__(ns, pref, tag)


class L3ipxvlan(IanaInterfaceType):
    """
    Layer 3 Virtual LAN using IPX.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:l3ipxvlan"):
        super().__init__(ns, pref, tag)


class DigitalPowerline(IanaInterfaceType):
    """
    IP over Power Lines.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:digitalPowerline"):
        super().__init__(ns, pref, tag)


class MediaMailOverIp(IanaInterfaceType):
    """
    Multimedia Mail over IP.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:mediaMailOverIp"):
        super().__init__(ns, pref, tag)


class Dtm(IanaInterfaceType):
    """
    Dynamic synchronous Transfer Mode.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:dtm"):
        super().__init__(ns, pref, tag)


class Dcn(IanaInterfaceType):
    """
    Data Communications Network.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:dcn"):
        super().__init__(ns, pref, tag)


class IpForward(IanaInterfaceType):
    """
    IP Forwarding Interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ipForward"):
        super().__init__(ns, pref, tag)


class Msdsl(IanaInterfaceType):
    """
    Multi\-rate Symmetric DSL.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:msdsl"):
        super().__init__(ns, pref, tag)


class Ieee1394(IanaInterfaceType):
    """
    IEEE1394 High Performance Serial Bus.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ieee1394"):
        super().__init__(ns, pref, tag)


class IfGsn(IanaInterfaceType):
    """
    HIPPI\-6400.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:if-gsn"):
        super().__init__(ns, pref, tag)


class DvbRccMacLayer(IanaInterfaceType):
    """
    DVB\-RCC MAC Layer.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:dvbRccMacLayer"):
        super().__init__(ns, pref, tag)


class DvbRccDownstream(IanaInterfaceType):
    """
    DVB\-RCC Downstream Channel.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:dvbRccDownstream"):
        super().__init__(ns, pref, tag)


class DvbRccUpstream(IanaInterfaceType):
    """
    DVB\-RCC Upstream Channel.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:dvbRccUpstream"):
        super().__init__(ns, pref, tag)


class AtmVirtual(IanaInterfaceType):
    """
    ATM Virtual Interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:atmVirtual"):
        super().__init__(ns, pref, tag)


class MplsTunnel(IanaInterfaceType):
    """
    MPLS Tunnel Virtual Interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:mplsTunnel"):
        super().__init__(ns, pref, tag)


class Srp(IanaInterfaceType):
    """
    Spatial Reuse Protocol.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:srp"):
        super().__init__(ns, pref, tag)


class VoiceOverAtm(IanaInterfaceType):
    """
    Voice over ATM.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:voiceOverAtm"):
        super().__init__(ns, pref, tag)


class VoiceOverFrameRelay(IanaInterfaceType):
    """
    Voice Over Frame Relay.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:voiceOverFrameRelay"):
        super().__init__(ns, pref, tag)


class Idsl(IanaInterfaceType):
    """
    Digital Subscriber Loop over ISDN.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:idsl"):
        super().__init__(ns, pref, tag)


class CompositeLink(IanaInterfaceType):
    """
    Avici Composite Link Interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:compositeLink"):
        super().__init__(ns, pref, tag)


class Ss7SigLink(IanaInterfaceType):
    """
    SS7 Signaling Link.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ss7SigLink"):
        super().__init__(ns, pref, tag)


class PropWirelessP2P(IanaInterfaceType):
    """
    Prop. P2P wireless interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:propWirelessP2P"):
        super().__init__(ns, pref, tag)


class FrForward(IanaInterfaceType):
    """
    Frame Forward Interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:frForward"):
        super().__init__(ns, pref, tag)


class Rfc1483(IanaInterfaceType):
    """
    Multiprotocol over ATM AAL5.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:rfc1483"):
        super().__init__(ns, pref, tag)


class Usb(IanaInterfaceType):
    """
    USB Interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:usb"):
        super().__init__(ns, pref, tag)


class Ieee8023adLag(IanaInterfaceType):
    """
    IEEE 802.3ad Link Aggregate.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ieee8023adLag"):
        super().__init__(ns, pref, tag)


class Bgppolicyaccounting(IanaInterfaceType):
    """
    BGP Policy Accounting.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:bgppolicyaccounting"):
        super().__init__(ns, pref, tag)


class Frf16MfrBundle(IanaInterfaceType):
    """
    FRF.16 Multilink Frame Relay.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:frf16MfrBundle"):
        super().__init__(ns, pref, tag)


class H323Gatekeeper(IanaInterfaceType):
    """
    H323 Gatekeeper.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:h323Gatekeeper"):
        super().__init__(ns, pref, tag)


class H323Proxy(IanaInterfaceType):
    """
    H323 Voice and Video Proxy.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:h323Proxy"):
        super().__init__(ns, pref, tag)


class Mpls(IanaInterfaceType):
    """
    MPLS.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:mpls"):
        super().__init__(ns, pref, tag)


class MfSigLink(IanaInterfaceType):
    """
    Multi\-frequency signaling link.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:mfSigLink"):
        super().__init__(ns, pref, tag)


class Hdsl2(IanaInterfaceType):
    """
    High Bit\-Rate DSL \- 2nd generation.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:hdsl2"):
        super().__init__(ns, pref, tag)


class Shdsl(IanaInterfaceType):
    """
    Multirate HDSL2.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:shdsl"):
        super().__init__(ns, pref, tag)


class Ds1FDL(IanaInterfaceType):
    """
    Facility Data Link (4Kbps) on a DS1.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ds1FDL"):
        super().__init__(ns, pref, tag)


class Pos(IanaInterfaceType):
    """
    Packet over SONET/SDH Interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:pos"):
        super().__init__(ns, pref, tag)


class DvbAsiIn(IanaInterfaceType):
    """
    DVB\-ASI Input.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:dvbAsiIn"):
        super().__init__(ns, pref, tag)


class DvbAsiOut(IanaInterfaceType):
    """
    DVB\-ASI Output.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:dvbAsiOut"):
        super().__init__(ns, pref, tag)


class Plc(IanaInterfaceType):
    """
    Power Line Communications.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:plc"):
        super().__init__(ns, pref, tag)


class Nfas(IanaInterfaceType):
    """
    Non\-Facility Associated Signaling.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:nfas"):
        super().__init__(ns, pref, tag)


class Tr008(IanaInterfaceType):
    """
    TR008.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:tr008"):
        super().__init__(ns, pref, tag)


class Gr303RDT(IanaInterfaceType):
    """
    Remote Digital Terminal.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:gr303RDT"):
        super().__init__(ns, pref, tag)


class Gr303IDT(IanaInterfaceType):
    """
    Integrated Digital Terminal.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:gr303IDT"):
        super().__init__(ns, pref, tag)


class Isup(IanaInterfaceType):
    """
    ISUP.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:isup"):
        super().__init__(ns, pref, tag)


class PropDocsWirelessMaclayer(IanaInterfaceType):
    """
    Cisco proprietary Maclayer.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:propDocsWirelessMaclayer"):
        super().__init__(ns, pref, tag)


class PropDocsWirelessDownstream(IanaInterfaceType):
    """
    Cisco proprietary Downstream.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:propDocsWirelessDownstream"):
        super().__init__(ns, pref, tag)


class PropDocsWirelessUpstream(IanaInterfaceType):
    """
    Cisco proprietary Upstream.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:propDocsWirelessUpstream"):
        super().__init__(ns, pref, tag)


class Hiperlan2(IanaInterfaceType):
    """
    HIPERLAN Type 2 Radio Interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:hiperlan2"):
        super().__init__(ns, pref, tag)


class PropBWAp2Mp(IanaInterfaceType):
    """
    PropBroadbandWirelessAccesspt2Multipt (use of this value
    for IEEE 802.16 WMAN interfaces as per IEEE Std 802.16f
    is deprecated, and ieee80216WMAN(237) should be used
    instead).
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:propBWAp2Mp"):
        super().__init__(ns, pref, tag)


class SonetOverheadChannel(IanaInterfaceType):
    """
    SONET Overhead Channel.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:sonetOverheadChannel"):
        super().__init__(ns, pref, tag)


class DigitalWrapperOverheadChannel(IanaInterfaceType):
    """
    Digital Wrapper.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:digitalWrapperOverheadChannel"):
        super().__init__(ns, pref, tag)


class Aal2(IanaInterfaceType):
    """
    ATM adaptation layer 2.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:aal2"):
        super().__init__(ns, pref, tag)


class RadioMAC(IanaInterfaceType):
    """
    MAC layer over radio links.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:radioMAC"):
        super().__init__(ns, pref, tag)


class AtmRadio(IanaInterfaceType):
    """
    ATM over radio links.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:atmRadio"):
        super().__init__(ns, pref, tag)


class Imt(IanaInterfaceType):
    """
    Inter\-Machine Trunks.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:imt"):
        super().__init__(ns, pref, tag)


class Mvl(IanaInterfaceType):
    """
    Multiple Virtual Lines DSL.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:mvl"):
        super().__init__(ns, pref, tag)


class ReachDSL(IanaInterfaceType):
    """
    Long Reach DSL.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:reachDSL"):
        super().__init__(ns, pref, tag)


class FrDlciEndPt(IanaInterfaceType):
    """
    Frame Relay DLCI End Point.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:frDlciEndPt"):
        super().__init__(ns, pref, tag)


class AtmVciEndPt(IanaInterfaceType):
    """
    ATM VCI End Point.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:atmVciEndPt"):
        super().__init__(ns, pref, tag)


class OpticalChannel(IanaInterfaceType):
    """
    Optical Channel.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:opticalChannel"):
        super().__init__(ns, pref, tag)


class OpticalTransport(IanaInterfaceType):
    """
    Optical Transport.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:opticalTransport"):
        super().__init__(ns, pref, tag)


class PropAtm(IanaInterfaceType):
    """
    Proprietary ATM.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:propAtm"):
        super().__init__(ns, pref, tag)


class VoiceOverCable(IanaInterfaceType):
    """
    Voice Over Cable Interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:voiceOverCable"):
        super().__init__(ns, pref, tag)


class Infiniband(IanaInterfaceType):
    """
    Infiniband.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:infiniband"):
        super().__init__(ns, pref, tag)


class TeLink(IanaInterfaceType):
    """
    TE Link.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:teLink"):
        super().__init__(ns, pref, tag)


class Q2931(IanaInterfaceType):
    """
    Q.2931.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:q2931"):
        super().__init__(ns, pref, tag)


class VirtualTg(IanaInterfaceType):
    """
    Virtual Trunk Group.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:virtualTg"):
        super().__init__(ns, pref, tag)


class SipTg(IanaInterfaceType):
    """
    SIP Trunk Group.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:sipTg"):
        super().__init__(ns, pref, tag)


class SipSig(IanaInterfaceType):
    """
    SIP Signaling.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:sipSig"):
        super().__init__(ns, pref, tag)


class DocsCableUpstreamChannel(IanaInterfaceType):
    """
    CATV Upstream Channel.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:docsCableUpstreamChannel"):
        super().__init__(ns, pref, tag)


class Econet(IanaInterfaceType):
    """
    Acorn Econet.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:econet"):
        super().__init__(ns, pref, tag)


class Pon155(IanaInterfaceType):
    """
    FSAN 155Mb Symetrical PON interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:pon155"):
        super().__init__(ns, pref, tag)


class Pon622(IanaInterfaceType):
    """
    FSAN 622Mb Symetrical PON interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:pon622"):
        super().__init__(ns, pref, tag)


class Bridge(IanaInterfaceType):
    """
    Transparent bridge interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:bridge"):
        super().__init__(ns, pref, tag)


class Linegroup(IanaInterfaceType):
    """
    Interface common to multiple lines.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:linegroup"):
        super().__init__(ns, pref, tag)


class VoiceEMFGD(IanaInterfaceType):
    """
    Voice E&M Feature Group D.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:voiceEMFGD"):
        super().__init__(ns, pref, tag)


class VoiceFGDEANA(IanaInterfaceType):
    """
    Voice FGD Exchange Access North American.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:voiceFGDEANA"):
        super().__init__(ns, pref, tag)


class VoiceDID(IanaInterfaceType):
    """
    Voice Direct Inward Dialing.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:voiceDID"):
        super().__init__(ns, pref, tag)


class MpegTransport(IanaInterfaceType):
    """
    MPEG transport interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:mpegTransport"):
        super().__init__(ns, pref, tag)


class SixToFour(IanaInterfaceType):
    """
    6to4 interface (DEPRECATED).
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:sixToFour"):
        super().__init__(ns, pref, tag)


class Gtp(IanaInterfaceType):
    """
    GTP (GPRS Tunneling Protocol).
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:gtp"):
        super().__init__(ns, pref, tag)


class PdnEtherLoop1(IanaInterfaceType):
    """
    Paradyne EtherLoop 1.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:pdnEtherLoop1"):
        super().__init__(ns, pref, tag)


class PdnEtherLoop2(IanaInterfaceType):
    """
    Paradyne EtherLoop 2.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:pdnEtherLoop2"):
        super().__init__(ns, pref, tag)


class OpticalChannelGroup(IanaInterfaceType):
    """
    Optical Channel Group.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:opticalChannelGroup"):
        super().__init__(ns, pref, tag)


class Homepna(IanaInterfaceType):
    """
    HomePNA ITU\-T G.989.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:homepna"):
        super().__init__(ns, pref, tag)


class Gfp(IanaInterfaceType):
    """
    Generic Framing Procedure (GFP).
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:gfp"):
        super().__init__(ns, pref, tag)


class CiscoISLvlan(IanaInterfaceType):
    """
    Layer 2 Virtual LAN using Cisco ISL.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ciscoISLvlan"):
        super().__init__(ns, pref, tag)


class ActelisMetaLOOP(IanaInterfaceType):
    """
    Acteleis proprietary MetaLOOP High Speed Link.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:actelisMetaLOOP"):
        super().__init__(ns, pref, tag)


class FcipLink(IanaInterfaceType):
    """
    FCIP Link.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:fcipLink"):
        super().__init__(ns, pref, tag)


class Rpr(IanaInterfaceType):
    """
    Resilient Packet Ring Interface Type.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:rpr"):
        super().__init__(ns, pref, tag)


class Qam(IanaInterfaceType):
    """
    RF Qam Interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:qam"):
        super().__init__(ns, pref, tag)


class Lmp(IanaInterfaceType):
    """
    Link Management Protocol.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:lmp"):
        super().__init__(ns, pref, tag)


class CblVectaStar(IanaInterfaceType):
    """
    Cambridge Broadband Networks Limited VectaStar.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:cblVectaStar"):
        super().__init__(ns, pref, tag)


class DocsCableMCmtsDownstream(IanaInterfaceType):
    """
    CATV Modular CMTS Downstream Interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:docsCableMCmtsDownstream"):
        super().__init__(ns, pref, tag)


class Adsl2(IanaInterfaceType):
    """
    Asymmetric Digital Subscriber Loop Version 2
    (DEPRECATED/OBSOLETED \- please use adsl2plus(238)
    instead).
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:adsl2"):
        super().__init__(ns, pref, tag)


class MacSecControlledIF(IanaInterfaceType):
    """
    MACSecControlled.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:macSecControlledIF"):
        super().__init__(ns, pref, tag)


class MacSecUncontrolledIF(IanaInterfaceType):
    """
    MACSecUncontrolled.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:macSecUncontrolledIF"):
        super().__init__(ns, pref, tag)


class AviciOpticalEther(IanaInterfaceType):
    """
    Avici Optical Ethernet Aggregate.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:aviciOpticalEther"):
        super().__init__(ns, pref, tag)


class Atmbond(IanaInterfaceType):
    """
    atmbond.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:atmbond"):
        super().__init__(ns, pref, tag)


class VoiceFGDOS(IanaInterfaceType):
    """
    Voice FGD Operator Services.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:voiceFGDOS"):
        super().__init__(ns, pref, tag)


class MocaVersion1(IanaInterfaceType):
    """
    MultiMedia over Coax Alliance (MoCA) Interface
    as documented in information provided privately to IANA.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:mocaVersion1"):
        super().__init__(ns, pref, tag)


class Ieee80216WMAN(IanaInterfaceType):
    """
    IEEE 802.16 WMAN interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ieee80216WMAN"):
        super().__init__(ns, pref, tag)


class Adsl2plus(IanaInterfaceType):
    """
    Asymmetric Digital Subscriber Loop Version 2 \-
    Version 2 Plus and all variants.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:adsl2plus"):
        super().__init__(ns, pref, tag)


class DvbRcsMacLayer(IanaInterfaceType):
    """
    DVB\-RCS MAC Layer.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:dvbRcsMacLayer"):
        super().__init__(ns, pref, tag)


class DvbTdm(IanaInterfaceType):
    """
    DVB Satellite TDM.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:dvbTdm"):
        super().__init__(ns, pref, tag)


class DvbRcsTdma(IanaInterfaceType):
    """
    DVB\-RCS TDMA.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:dvbRcsTdma"):
        super().__init__(ns, pref, tag)


class X86Laps(IanaInterfaceType):
    """
    LAPS based on ITU\-T X.86/Y.1323.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:x86Laps"):
        super().__init__(ns, pref, tag)


class WwanPP(IanaInterfaceType):
    """
    3GPP WWAN.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:wwanPP"):
        super().__init__(ns, pref, tag)


class WwanPP2(IanaInterfaceType):
    """
    3GPP2 WWAN.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:wwanPP2"):
        super().__init__(ns, pref, tag)


class VoiceEBS(IanaInterfaceType):
    """
    Voice P\-phone EBS physical interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:voiceEBS"):
        super().__init__(ns, pref, tag)


class IfPwType(IanaInterfaceType):
    """
    Pseudowire interface type.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ifPwType"):
        super().__init__(ns, pref, tag)


class Ilan(IanaInterfaceType):
    """
    Internal LAN on a bridge per IEEE 802.1ap.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ilan"):
        super().__init__(ns, pref, tag)


class Pip(IanaInterfaceType):
    """
    Provider Instance Port on a bridge per IEEE 802.1ah PBB.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:pip"):
        super().__init__(ns, pref, tag)


class AluELP(IanaInterfaceType):
    """
    Alcatel\-Lucent Ethernet Link Protection.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:aluELP"):
        super().__init__(ns, pref, tag)


class Gpon(IanaInterfaceType):
    """
    Gigabit\-capable passive optical networks (G\-PON) as per
    ITU\-T G.948.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:gpon"):
        super().__init__(ns, pref, tag)


class Vdsl2(IanaInterfaceType):
    """
    Very high speed digital subscriber line Version 2
    (as per ITU\-T Recommendation G.993.2).
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:vdsl2"):
        super().__init__(ns, pref, tag)


class CapwapDot11Profile(IanaInterfaceType):
    """
    WLAN Profile Interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:capwapDot11Profile"):
        super().__init__(ns, pref, tag)


class CapwapDot11Bss(IanaInterfaceType):
    """
    WLAN BSS Interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:capwapDot11Bss"):
        super().__init__(ns, pref, tag)


class CapwapWtpVirtualRadio(IanaInterfaceType):
    """
    WTP Virtual Radio Interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:capwapWtpVirtualRadio"):
        super().__init__(ns, pref, tag)


class Bits(IanaInterfaceType):
    """
    bitsport.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:bits"):
        super().__init__(ns, pref, tag)


class DocsCableUpstreamRfPort(IanaInterfaceType):
    """
    DOCSIS CATV Upstream RF Port.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:docsCableUpstreamRfPort"):
        super().__init__(ns, pref, tag)


class CableDownstreamRfPort(IanaInterfaceType):
    """
    CATV downstream RF Port.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:cableDownstreamRfPort"):
        super().__init__(ns, pref, tag)


class VmwareVirtualNic(IanaInterfaceType):
    """
    VMware Virtual Network Interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:vmwareVirtualNic"):
        super().__init__(ns, pref, tag)


class Ieee802154(IanaInterfaceType):
    """
    IEEE 802.15.4 WPAN interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ieee802154"):
        super().__init__(ns, pref, tag)


class OtnOdu(IanaInterfaceType):
    """
    OTN Optical Data Unit.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:otnOdu"):
        super().__init__(ns, pref, tag)


class OtnOtu(IanaInterfaceType):
    """
    OTN Optical channel Transport Unit.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:otnOtu"):
        super().__init__(ns, pref, tag)


class IfVfiType(IanaInterfaceType):
    """
    VPLS Forwarding Instance Interface Type.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:ifVfiType"):
        super().__init__(ns, pref, tag)


class G9981(IanaInterfaceType):
    """
    G.998.1 bonded interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:g9981"):
        super().__init__(ns, pref, tag)


class G9982(IanaInterfaceType):
    """
    G.998.2 bonded interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:g9982"):
        super().__init__(ns, pref, tag)


class G9983(IanaInterfaceType):
    """
    G.998.3 bonded interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:g9983"):
        super().__init__(ns, pref, tag)


class AluEpon(IanaInterfaceType):
    """
    Ethernet Passive Optical Networks (E\-PON).
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:aluEpon"):
        super().__init__(ns, pref, tag)


class AluEponOnu(IanaInterfaceType):
    """
    EPON Optical Network Unit.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:aluEponOnu"):
        super().__init__(ns, pref, tag)


class AluEponPhysicalUni(IanaInterfaceType):
    """
    EPON physical User to Network interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:aluEponPhysicalUni"):
        super().__init__(ns, pref, tag)


class AluEponLogicalLink(IanaInterfaceType):
    """
    The emulation of a point\-to\-point link over the EPON
    layer.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:aluEponLogicalLink"):
        super().__init__(ns, pref, tag)


class AluGponOnu(IanaInterfaceType):
    """
    GPON Optical Network Unit.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:aluGponOnu"):
        super().__init__(ns, pref, tag)


class AluGponPhysicalUni(IanaInterfaceType):
    """
    GPON physical User to Network interface.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:aluGponPhysicalUni"):
        super().__init__(ns, pref, tag)


class VmwareNicTeam(IanaInterfaceType):
    """
    VMware NIC Team.
    
    """
    _prefix = 'ianaift'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:iana-if-type", pref="iana-if-type", tag="iana-if-type:vmwareNicTeam"):
        super().__init__(ns, pref, tag)



