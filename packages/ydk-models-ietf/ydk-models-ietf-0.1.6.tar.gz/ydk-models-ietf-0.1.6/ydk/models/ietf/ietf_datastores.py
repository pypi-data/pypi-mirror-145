""" ietf_datastores 

This YANG module defines a set of identities for identifying
datastores.

Copyright (c) 2018 IETF Trust and the persons identified as
authors of the code.  All rights reserved.

Redistribution and use in source and binary forms, with or
without modification, is permitted pursuant to, and subject to
the license terms contained in, the Simplified BSD License set
forth in Section 4.c of the IETF Trust's Legal Provisions
Relating to IETF Documents
(https\://trustee.ietf.org/license\-info).

This version of this YANG module is part of RFC 8342
(https\://www.rfc\-editor.org/info/rfc8342); see the RFC itself
for full legal notices.

"""
from collections import OrderedDict

from ydk.types import Entity as _Entity_
from ydk.types import EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.types import Entity, EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.filters import YFilter
from ydk.errors import YError, YModelError
from ydk.errors.error_handler import handle_type_error as _handle_type_error


class Datastore(Identity):
    """
    Abstract base identity for datastore identities.
    
    """
    _prefix = 'ds'
    _revision = '2018-02-14'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:ietf-datastores", pref="ietf-datastores", tag="ietf-datastores:datastore"):
        super().__init__(ns, pref, tag)


class Conventional(Datastore):
    """
    Abstract base identity for conventional configuration
    datastores.
    
    """
    _prefix = 'ds'
    _revision = '2018-02-14'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:ietf-datastores", pref="ietf-datastores", tag="ietf-datastores:conventional"):
        super().__init__(ns, pref, tag)


class Running(Conventional):
    """
    The running configuration datastore.
    
    """
    _prefix = 'ds'
    _revision = '2018-02-14'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:ietf-datastores", pref="ietf-datastores", tag="ietf-datastores:running"):
        super().__init__(ns, pref, tag)


class Candidate(Conventional):
    """
    The candidate configuration datastore.
    
    """
    _prefix = 'ds'
    _revision = '2018-02-14'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:ietf-datastores", pref="ietf-datastores", tag="ietf-datastores:candidate"):
        super().__init__(ns, pref, tag)


class Startup(Conventional):
    """
    The startup configuration datastore.
    
    """
    _prefix = 'ds'
    _revision = '2018-02-14'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:ietf-datastores", pref="ietf-datastores", tag="ietf-datastores:startup"):
        super().__init__(ns, pref, tag)


class Intended(Conventional):
    """
    The intended configuration datastore.
    
    """
    _prefix = 'ds'
    _revision = '2018-02-14'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:ietf-datastores", pref="ietf-datastores", tag="ietf-datastores:intended"):
        super().__init__(ns, pref, tag)


class Dynamic(Datastore):
    """
    Abstract base identity for dynamic configuration datastores.
    
    """
    _prefix = 'ds'
    _revision = '2018-02-14'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:ietf-datastores", pref="ietf-datastores", tag="ietf-datastores:dynamic"):
        super().__init__(ns, pref, tag)


class Operational(Datastore):
    """
    The operational state datastore.
    
    """
    _prefix = 'ds'
    _revision = '2018-02-14'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:ietf-datastores", pref="ietf-datastores", tag="ietf-datastores:operational"):
        super().__init__(ns, pref, tag)



