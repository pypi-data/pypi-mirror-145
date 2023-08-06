""" ietf_yang_library 

This module provides information about the YANG modules,
datastores, and datastore schemas used by a network
management server.
The key words 'MUST', 'MUST NOT', 'REQUIRED', 'SHALL', 'SHALL
NOT', 'SHOULD', 'SHOULD NOT', 'RECOMMENDED', 'NOT RECOMMENDED',
'MAY', and 'OPTIONAL' in this document are to be interpreted as
described in BCP 14 (RFC 2119) (RFC 8174) when, and only when,
they appear in all capitals, as shown here.

Copyright (c) 2019 IETF Trust and the persons identified as
authors of the code.  All rights reserved.

Redistribution and use in source and binary forms, with or
without modification, is permitted pursuant to, and subject
to the license terms contained in, the Simplified BSD License
set forth in Section 4.c of the IETF Trust's Legal Provisions
Relating to IETF Documents
(https\://trustee.ietf.org/license\-info).

This version of this YANG module is part of RFC 8525; see
the RFC itself for full legal notices.

"""
from collections import OrderedDict

from ydk.types import Entity as _Entity_
from ydk.types import EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.types import Entity, EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.filters import YFilter
from ydk.errors import YError, YModelError
from ydk.errors.error_handler import handle_type_error as _handle_type_error


class YangLibrary(_Entity_):
    """
    Container holding the entire YANG library of this server.
    
    .. attribute:: module_set
    
        A set of modules that may be used by one or more schemas.  A module set does not have to be referentially complete, i.e., it may define modules that contain import statements for other modules not included in the module set
    
        **type**: list of    :py:class:`ModuleSet<ydk.models.ietf.ietf_yang_library.YangLibrary.ModuleSet>`
    
        **config**: False
    
    .. attribute:: schema
    
        A datastore schema that may be used by one or more datastores.  The schema must be valid and referentially complete, i.e., it must contain modules to satisfy all used import statements for all modules specified in the schema
    
        **type**: list of    :py:class:`Schema<ydk.models.ietf.ietf_yang_library.YangLibrary.Schema>`
    
        **config**: False
    
    .. attribute:: datastore
    
        A datastore supported by this server.  Each datastore indicates which schema it supports.  The server MUST instantiate one entry in this list per specific datastore it supports. Each datastore entry with the same datastore schema SHOULD reference the same schema
    
        **type**: list of    :py:class:`Datastore<ydk.models.ietf.ietf_yang_library.YangLibrary.Datastore>`
    
        **config**: False
    
    .. attribute:: content_id
    
        A server\-generated identifier of the contents of the '/yang\-library' tree.  The server MUST change the value of this leaf if the information represented by the '/yang\-library' tree, except '/yang\-library/content\-id', has changed
    
        **type**: str
    
        **mandatory**: True
    
        **config**: False
    
    """
    _prefix = 'yanglib'
    _revision = '2019-01-04'

    def __init__(self):
        super().__init__()
        self._top_entity = None

        self.yang_name = "yang-library"
        self.yang_parent_name = "ietf-yang-library"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([("module-set", ("module_set", YangLibrary.ModuleSet)), ("schema", ("schema", YangLibrary.Schema)), ("datastore", ("datastore", YangLibrary.Datastore))])
        self._leafs = OrderedDict([
            ('content_id', (YLeaf(YType.str, 'content-id'), ['str'])),
        ])
        self.content_id = None

        self.module_set = YList(self)
        self.schema = YList(self)
        self.datastore = YList(self)
        self._segment_path = lambda: "ietf-yang-library:yang-library"
        self._is_frozen = True

    def __setattr__(self, name, value):
        self._perform_setattr(YangLibrary, ['content_id'], name, value)

    class ModuleSet(_Entity_):
        """
        A set of modules that may be used by one or more schemas.
        
        A module set does not have to be referentially complete,
        i.e., it may define modules that contain import statements
        for other modules not included in the module set.
        
        .. attribute:: name  (key)
        
            An arbitrary name of the module set
        
            **type**: str
        
            **config**: False
        
        .. attribute:: module
        
            An entry in this list represents a module implemented by the server, as per Section 5.6.5 of RFC 7950, with a particular set of supported features and deviations
        
            **type**: list of    :py:class:`Module<ydk.models.ietf.ietf_yang_library.YangLibrary.ModuleSet.Module>`
        
            **config**: False
        
        .. attribute:: import_only_module
        
            An entry in this list indicates that the server imports reusable definitions from the specified revision of the module but does not implement any protocol\-accessible objects from this revision.  Multiple entries for the same module name MAY exist.  This can occur if multiple modules import the same module but specify different revision dates in the import statements
        
            **type**: list of    :py:class:`ImportOnlyModule<ydk.models.ietf.ietf_yang_library.YangLibrary.ModuleSet.ImportOnlyModule>`
        
            **config**: False
        
        """
        _prefix = 'yanglib'
        _revision = '2019-01-04'

        def __init__(self):
            super().__init__()

            self.yang_name = "module-set"
            self.yang_parent_name = "yang-library"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = ['name']
            self._child_classes = OrderedDict([("module", ("module", YangLibrary.ModuleSet.Module)), ("import-only-module", ("import_only_module", YangLibrary.ModuleSet.ImportOnlyModule))])
            self._leafs = OrderedDict([
                ('name', (YLeaf(YType.str, 'name'), ['str'])),
            ])
            self.name = None

            self.module = YList(self)
            self.import_only_module = YList(self)
            self._segment_path = lambda: "module-set" + "[name='" + str(self.name) + "']"
            self._absolute_path = lambda: "ietf-yang-library:yang-library/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(YangLibrary.ModuleSet, ['name'], name, value)

        class Module(_Entity_):
            """
            An entry in this list represents a module implemented by the
            server, as per Section 5.6.5 of RFC 7950, with a particular
            set of supported features and deviations.
            
            .. attribute:: name  (key)
            
                The YANG module or submodule name
            
                **type**: str
            
                    **pattern:** [a\-zA\-Z\_][a\-zA\-Z0\-9\\\-\_.]\*
            
                **mandatory**: True
            
                **config**: False
            
            .. attribute:: revision
            
                The YANG module or submodule revision date.  If no revision statement is present in the YANG module or submodule, this leaf is not instantiated
            
                **type**: str
            
                    **pattern:** \\d{4}\-\\d{2}\-\\d{2}
            
                **config**: False
            
            .. attribute:: namespace
            
                The XML namespace identifier for this module
            
                **type**: str
            
                **mandatory**: True
            
                **config**: False
            
            .. attribute:: location
            
                Contains a URL that represents the YANG schema resource for this module or submodule.  This leaf will only be present if there is a URL available for retrieval of the schema for this entry
            
                **type**: list of str
            
                **config**: False
            
            .. attribute:: submodule
            
                Each entry represents one submodule within the parent module
            
                **type**: list of    :py:class:`Submodule<ydk.models.ietf.ietf_yang_library.YangLibrary.ModuleSet.Module.Submodule>`
            
                **config**: False
            
            .. attribute:: feature
            
                List of all YANG feature names from this module that are supported by the server, regardless whether they are defined in the module or any included submodule
            
                **type**: list of str
            
                    **pattern:** [a\-zA\-Z\_][a\-zA\-Z0\-9\\\-\_.]\*
            
                **config**: False
            
            .. attribute:: deviation
            
                List of all YANG deviation modules used by this server to modify the conformance of the module associated with this entry.  Note that the same module can be used for deviations for multiple modules, so the same entry MAY appear within multiple 'module' entries.  This reference MUST NOT (directly or indirectly) refer to the module being deviated.  Robust clients may want to make sure that they handle a situation where a module deviates itself (directly or indirectly) gracefully
            
                **type**: list of str
            
                    **pattern:** [a\-zA\-Z\_][a\-zA\-Z0\-9\\\-\_.]\*
            
                **refers to**:  :py:class:`name<ydk.models.ietf.ietf_yang_library.YangLibrary.ModuleSet.Module>`
            
                **config**: False
            
            """
            _prefix = 'yanglib'
            _revision = '2019-01-04'

            def __init__(self):
                super().__init__()

                self.yang_name = "module"
                self.yang_parent_name = "module-set"
                self.is_top_level_class = False
                self.has_list_ancestor = True
                self.ylist_key_names = ['name']
                self._child_classes = OrderedDict([("submodule", ("submodule", YangLibrary.ModuleSet.Module.Submodule))])
                self._leafs = OrderedDict([
                    ('name', (YLeaf(YType.str, 'name'), ['str'])),
                    ('revision', (YLeaf(YType.str, 'revision'), ['str'])),
                    ('namespace', (YLeaf(YType.str, 'namespace'), ['str'])),
                    ('location', (YLeafList(YType.str, 'location'), ['str'])),
                    ('feature', (YLeafList(YType.str, 'feature'), ['str'])),
                    ('deviation', (YLeafList(YType.str, 'deviation'), ['str'])),
                ])
                self.name = None
                self.revision = None
                self.namespace = None
                self.location = []
                self.feature = []
                self.deviation = []

                self.submodule = YList(self)
                self._segment_path = lambda: "module" + "[name='" + str(self.name) + "']"
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(YangLibrary.ModuleSet.Module, ['name', 'revision', 'namespace', 'location', 'feature', 'deviation'], name, value)

            class Submodule(_Entity_):
                """
                Each entry represents one submodule within the
                parent module.
                
                .. attribute:: name  (key)
                
                    The YANG module or submodule name
                
                    **type**: str
                
                        **pattern:** [a\-zA\-Z\_][a\-zA\-Z0\-9\\\-\_.]\*
                
                    **mandatory**: True
                
                    **config**: False
                
                .. attribute:: revision
                
                    The YANG module or submodule revision date.  If no revision statement is present in the YANG module or submodule, this leaf is not instantiated
                
                    **type**: str
                
                        **pattern:** \\d{4}\-\\d{2}\-\\d{2}
                
                    **config**: False
                
                .. attribute:: location
                
                    Contains a URL that represents the YANG schema resource for this module or submodule.  This leaf will only be present if there is a URL available for retrieval of the schema for this entry
                
                    **type**: list of str
                
                    **config**: False
                
                """
                _prefix = 'yanglib'
                _revision = '2019-01-04'

                def __init__(self):
                    super().__init__()

                    self.yang_name = "submodule"
                    self.yang_parent_name = "module"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = ['name']
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('name', (YLeaf(YType.str, 'name'), ['str'])),
                        ('revision', (YLeaf(YType.str, 'revision'), ['str'])),
                        ('location', (YLeafList(YType.str, 'location'), ['str'])),
                    ])
                    self.name = None
                    self.revision = None
                    self.location = []
                    self._segment_path = lambda: "submodule" + "[name='" + str(self.name) + "']"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(YangLibrary.ModuleSet.Module.Submodule, ['name', 'revision', 'location'], name, value)



        class ImportOnlyModule(_Entity_):
            """
            An entry in this list indicates that the server imports
            reusable definitions from the specified revision of the
            module but does not implement any protocol\-accessible
            objects from this revision.
            
            Multiple entries for the same module name MAY exist.  This
            can occur if multiple modules import the same module but
            specify different revision dates in the import statements.
            
            .. attribute:: name  (key)
            
                The YANG module name
            
                **type**: str
            
                    **pattern:** [a\-zA\-Z\_][a\-zA\-Z0\-9\\\-\_.]\*
            
                **config**: False
            
            .. attribute:: revision  (key)
            
                The YANG module revision date. A zero\-length string is used if no revision statement is present in the YANG module
            
                **type**: union of the below types:
            
                    **type**: str
            
                        **pattern:** \\d{4}\-\\d{2}\-\\d{2}
            
                    **type**: str
            
                        **length:** 0..0
            
                **config**: False
            
            .. attribute:: namespace
            
                The XML namespace identifier for this module
            
                **type**: str
            
                **mandatory**: True
            
                **config**: False
            
            .. attribute:: location
            
                Contains a URL that represents the YANG schema resource for this module or submodule.  This leaf will only be present if there is a URL available for retrieval of the schema for this entry
            
                **type**: list of str
            
                **config**: False
            
            .. attribute:: submodule
            
                Each entry represents one submodule within the parent module
            
                **type**: list of    :py:class:`Submodule<ydk.models.ietf.ietf_yang_library.YangLibrary.ModuleSet.ImportOnlyModule.Submodule>`
            
                **config**: False
            
            """
            _prefix = 'yanglib'
            _revision = '2019-01-04'

            def __init__(self):
                super().__init__()

                self.yang_name = "import-only-module"
                self.yang_parent_name = "module-set"
                self.is_top_level_class = False
                self.has_list_ancestor = True
                self.ylist_key_names = ['name','revision']
                self._child_classes = OrderedDict([("submodule", ("submodule", YangLibrary.ModuleSet.ImportOnlyModule.Submodule))])
                self._leafs = OrderedDict([
                    ('name', (YLeaf(YType.str, 'name'), ['str'])),
                    ('revision', (YLeaf(YType.str, 'revision'), ['str','str'])),
                    ('namespace', (YLeaf(YType.str, 'namespace'), ['str'])),
                    ('location', (YLeafList(YType.str, 'location'), ['str'])),
                ])
                self.name = None
                self.revision = None
                self.namespace = None
                self.location = []

                self.submodule = YList(self)
                self._segment_path = lambda: "import-only-module" + "[name='" + str(self.name) + "']" + "[revision='" + str(self.revision) + "']"
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(YangLibrary.ModuleSet.ImportOnlyModule, ['name', 'revision', 'namespace', 'location'], name, value)

            class Submodule(_Entity_):
                """
                Each entry represents one submodule within the
                parent module.
                
                .. attribute:: name  (key)
                
                    The YANG module or submodule name
                
                    **type**: str
                
                        **pattern:** [a\-zA\-Z\_][a\-zA\-Z0\-9\\\-\_.]\*
                
                    **mandatory**: True
                
                    **config**: False
                
                .. attribute:: revision
                
                    The YANG module or submodule revision date.  If no revision statement is present in the YANG module or submodule, this leaf is not instantiated
                
                    **type**: str
                
                        **pattern:** \\d{4}\-\\d{2}\-\\d{2}
                
                    **config**: False
                
                .. attribute:: location
                
                    Contains a URL that represents the YANG schema resource for this module or submodule.  This leaf will only be present if there is a URL available for retrieval of the schema for this entry
                
                    **type**: list of str
                
                    **config**: False
                
                """
                _prefix = 'yanglib'
                _revision = '2019-01-04'

                def __init__(self):
                    super().__init__()

                    self.yang_name = "submodule"
                    self.yang_parent_name = "import-only-module"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = ['name']
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('name', (YLeaf(YType.str, 'name'), ['str'])),
                        ('revision', (YLeaf(YType.str, 'revision'), ['str'])),
                        ('location', (YLeafList(YType.str, 'location'), ['str'])),
                    ])
                    self.name = None
                    self.revision = None
                    self.location = []
                    self._segment_path = lambda: "submodule" + "[name='" + str(self.name) + "']"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(YangLibrary.ModuleSet.ImportOnlyModule.Submodule, ['name', 'revision', 'location'], name, value)




    class Schema(_Entity_):
        """
        A datastore schema that may be used by one or more
        datastores.
        
        The schema must be valid and referentially complete, i.e.,
        it must contain modules to satisfy all used import
        statements for all modules specified in the schema.
        
        .. attribute:: name  (key)
        
            An arbitrary name of the schema
        
            **type**: str
        
            **config**: False
        
        .. attribute:: module_set
        
            A set of module\-sets that are included in this schema. If a non\-import\-only module appears in multiple module sets, then the module revision and the associated features and deviations must be identical
        
            **type**: list of str
        
            **refers to**:  :py:class:`name<ydk.models.ietf.ietf_yang_library.YangLibrary.ModuleSet>`
        
            **config**: False
        
        """
        _prefix = 'yanglib'
        _revision = '2019-01-04'

        def __init__(self):
            super().__init__()

            self.yang_name = "schema"
            self.yang_parent_name = "yang-library"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = ['name']
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('name', (YLeaf(YType.str, 'name'), ['str'])),
                ('module_set', (YLeafList(YType.str, 'module-set'), ['str'])),
            ])
            self.name = None
            self.module_set = []
            self._segment_path = lambda: "schema" + "[name='" + str(self.name) + "']"
            self._absolute_path = lambda: "ietf-yang-library:yang-library/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(YangLibrary.Schema, ['name', 'module_set'], name, value)


    class Datastore(_Entity_):
        """
        A datastore supported by this server.
        
        Each datastore indicates which schema it supports.
        
        The server MUST instantiate one entry in this list per
        specific datastore it supports.
        Each datastore entry with the same datastore schema SHOULD
        reference the same schema.
        
        .. attribute:: name  (key)
        
            The identity of the datastore
        
            **type**:  :py:class:`Datastore<ydk.models.ietf.ietf_datastores.Datastore>`
        
            **config**: False
        
        .. attribute:: schema
        
            A reference to the schema supported by this datastore. All non\-import\-only modules of the schema are implemented with their associated features and deviations
        
            **type**: str
        
            **refers to**:  :py:class:`name<ydk.models.ietf.ietf_yang_library.YangLibrary.Schema>`
        
            **mandatory**: True
        
            **config**: False
        
        """
        _prefix = 'yanglib'
        _revision = '2019-01-04'

        def __init__(self):
            super().__init__()

            self.yang_name = "datastore"
            self.yang_parent_name = "yang-library"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = ['name']
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('name', (YLeaf(YType.identityref, 'name'), [('ydk.models.ietf.ietf_datastores', 'Datastore')])),
                ('schema', (YLeaf(YType.str, 'schema'), ['str'])),
            ])
            self.name = None
            self.schema = None
            self._segment_path = lambda: "datastore" + "[name='" + str(self.name) + "']"
            self._absolute_path = lambda: "ietf-yang-library:yang-library/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(YangLibrary.Datastore, ['name', 'schema'], name, value)


    def clone_ptr(self):
        self._top_entity = YangLibrary()
        return self._top_entity


class ModulesState(_Entity_):
    """
    Contains YANG module monitoring information.
    
    .. attribute:: module_set_id
    
        Contains a server\-specific identifier representing the current set of modules and submodules.  The server MUST change the value of this leaf if the information represented by the 'module' list instances has changed
    
        **type**: str
    
        **mandatory**: True
    
        **config**: False
    
        **status**: deprecated
    
    .. attribute:: module
    
        Each entry represents one revision of one module currently supported by the server
    
        **type**: list of    :py:class:`Module<ydk.models.ietf.ietf_yang_library.ModulesState.Module>`
    
        **config**: False
    
        **status**: deprecated
    
    """
    _prefix = 'yanglib'
    _revision = '2019-01-04'

    def __init__(self):
        super().__init__()
        self._top_entity = None

        self.yang_name = "modules-state"
        self.yang_parent_name = "ietf-yang-library"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([("module", ("module", ModulesState.Module))])
        self._leafs = OrderedDict([
            ('module_set_id', (YLeaf(YType.str, 'module-set-id'), ['str'])),
        ])
        self.module_set_id = None

        self.module = YList(self)
        self._segment_path = lambda: "ietf-yang-library:modules-state"
        self._is_frozen = True

    def __setattr__(self, name, value):
        self._perform_setattr(ModulesState, ['module_set_id'], name, value)

    class Module(_Entity_):
        """
        Each entry represents one revision of one module
        currently supported by the server.
        
        .. attribute:: name  (key)
        
            The YANG module or submodule name
        
            **type**: str
        
                **pattern:** [a\-zA\-Z\_][a\-zA\-Z0\-9\\\-\_.]\*
        
            **config**: False
        
            **status**: deprecated
        
        .. attribute:: revision  (key)
        
            The YANG module or submodule revision date. A zero\-length string is used if no revision statement is present in the YANG module or submodule
        
            **type**: union of the below types:
        
                **type**: str
        
                    **pattern:** \\d{4}\-\\d{2}\-\\d{2}
        
                **type**: str
        
                    **length:** 0..0
        
            **config**: False
        
            **status**: deprecated
        
        .. attribute:: schema
        
            Contains a URL that represents the YANG schema resource for this module or submodule.  This leaf will only be present if there is a URL available for retrieval of the schema for this entry
        
            **type**: str
        
            **config**: False
        
        .. attribute:: namespace
        
            The XML namespace identifier for this module
        
            **type**: str
        
            **mandatory**: True
        
            **config**: False
        
            **status**: deprecated
        
        .. attribute:: feature
        
            List of YANG feature names from this module that are supported by the server, regardless of whether they are defined in the module or any included submodule
        
            **type**: list of str
        
                **pattern:** [a\-zA\-Z\_][a\-zA\-Z0\-9\\\-\_.]\*
        
            **config**: False
        
            **status**: deprecated
        
        .. attribute:: deviation
        
            List of YANG deviation module names and revisions used by this server to modify the conformance of the module associated with this entry.  Note that the same module can be used for deviations for multiple modules, so the same entry MAY appear within multiple 'module' entries.  The deviation module MUST be present in the 'module' list, with the same name and revision values. The 'conformance\-type' value will be 'implement' for the deviation module
        
            **type**: list of    :py:class:`Deviation<ydk.models.ietf.ietf_yang_library.ModulesState.Module.Deviation>`
        
            **config**: False
        
            **status**: deprecated
        
        .. attribute:: conformance_type
        
            Indicates the type of conformance the server is claiming for the YANG module identified by this entry
        
            **type**:  :py:class:`ConformanceType<ydk.models.ietf.ietf_yang_library.ModulesState.Module.ConformanceType>`
        
            **mandatory**: True
        
            **config**: False
        
            **status**: deprecated
        
        .. attribute:: submodule
        
            Each entry represents one submodule within the parent module
        
            **type**: list of    :py:class:`Submodule<ydk.models.ietf.ietf_yang_library.ModulesState.Module.Submodule>`
        
            **config**: False
        
            **status**: deprecated
        
        """
        _prefix = 'yanglib'
        _revision = '2019-01-04'

        def __init__(self):
            super().__init__()

            self.yang_name = "module"
            self.yang_parent_name = "modules-state"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = ['name','revision']
            self._child_classes = OrderedDict([("deviation", ("deviation", ModulesState.Module.Deviation)), ("submodule", ("submodule", ModulesState.Module.Submodule))])
            self._leafs = OrderedDict([
                ('name', (YLeaf(YType.str, 'name'), ['str'])),
                ('revision', (YLeaf(YType.str, 'revision'), ['str','str'])),
                ('schema', (YLeaf(YType.str, 'schema'), ['str'])),
                ('namespace', (YLeaf(YType.str, 'namespace'), ['str'])),
                ('feature', (YLeafList(YType.str, 'feature'), ['str'])),
                ('conformance_type', (YLeaf(YType.enumeration, 'conformance-type'), [('ydk.models.ietf.ietf_yang_library', 'ModulesState', 'Module.ConformanceType')])),
            ])
            self.name = None
            self.revision = None
            self.schema = None
            self.namespace = None
            self.feature = []
            self.conformance_type = None

            self.deviation = YList(self)
            self.submodule = YList(self)
            self._segment_path = lambda: "module" + "[name='" + str(self.name) + "']" + "[revision='" + str(self.revision) + "']"
            self._absolute_path = lambda: "ietf-yang-library:modules-state/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(ModulesState.Module, ['name', 'revision', 'schema', 'namespace', 'feature', 'conformance_type'], name, value)

        class ConformanceType(Enum):
            """
            ConformanceType (Enum Class)

            .. data:: implement = 0

                Indicates that the server implements one or more

                protocol-accessible objects defined in the YANG module

                identified in this entry.  This includes deviation

                statements defined in the module.

                For YANG version 1.1 modules, there is at most one

                'module' entry with conformance type 'implement' for a

                particular module name, since YANG 1.1 requires that

                at most one revision of a module is implemented.

                For YANG version 1 modules, there SHOULD NOT be more

                than one 'module' entry for a particular module

                name.

            .. data:: import_ = 1

                Indicates that the server imports reusable definitions

                from the specified revision of the module but does

                not implement any protocol-accessible objects from

                this revision.

                Multiple 'module' entries for the same module name MAY

                exist.  This can occur if multiple modules import the

                same module but specify different revision dates in

                the import statements.

            """

            implement = Enum.YLeaf(0, "implement")

            import_ = Enum.YLeaf(1, "import")


        class Deviation(_Entity_):
            """
            List of YANG deviation module names and revisions
            used by this server to modify the conformance of
            the module associated with this entry.  Note that
            the same module can be used for deviations for
            multiple modules, so the same entry MAY appear
            within multiple 'module' entries.
            
            The deviation module MUST be present in the 'module'
            list, with the same name and revision values.
            The 'conformance\-type' value will be 'implement' for
            the deviation module.
            
            .. attribute:: name  (key)
            
                The YANG module or submodule name
            
                **type**: str
            
                    **pattern:** [a\-zA\-Z\_][a\-zA\-Z0\-9\\\-\_.]\*
            
                **config**: False
            
                **status**: deprecated
            
            .. attribute:: revision  (key)
            
                The YANG module or submodule revision date. A zero\-length string is used if no revision statement is present in the YANG module or submodule
            
                **type**: union of the below types:
            
                    **type**: str
            
                        **pattern:** \\d{4}\-\\d{2}\-\\d{2}
            
                    **type**: str
            
                        **length:** 0..0
            
                **config**: False
            
                **status**: deprecated
            
            """
            _prefix = 'yanglib'
            _revision = '2019-01-04'

            def __init__(self):
                super().__init__()

                self.yang_name = "deviation"
                self.yang_parent_name = "module"
                self.is_top_level_class = False
                self.has_list_ancestor = True
                self.ylist_key_names = ['name','revision']
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('name', (YLeaf(YType.str, 'name'), ['str'])),
                    ('revision', (YLeaf(YType.str, 'revision'), ['str','str'])),
                ])
                self.name = None
                self.revision = None
                self._segment_path = lambda: "deviation" + "[name='" + str(self.name) + "']" + "[revision='" + str(self.revision) + "']"
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(ModulesState.Module.Deviation, ['name', 'revision'], name, value)


        class Submodule(_Entity_):
            """
            Each entry represents one submodule within the
            parent module.
            
            .. attribute:: name  (key)
            
                The YANG module or submodule name
            
                **type**: str
            
                    **pattern:** [a\-zA\-Z\_][a\-zA\-Z0\-9\\\-\_.]\*
            
                **config**: False
            
                **status**: deprecated
            
            .. attribute:: revision  (key)
            
                The YANG module or submodule revision date. A zero\-length string is used if no revision statement is present in the YANG module or submodule
            
                **type**: union of the below types:
            
                    **type**: str
            
                        **pattern:** \\d{4}\-\\d{2}\-\\d{2}
            
                    **type**: str
            
                        **length:** 0..0
            
                **config**: False
            
                **status**: deprecated
            
            .. attribute:: schema
            
                Contains a URL that represents the YANG schema resource for this module or submodule.  This leaf will only be present if there is a URL available for retrieval of the schema for this entry
            
                **type**: str
            
                **config**: False
            
            """
            _prefix = 'yanglib'
            _revision = '2019-01-04'

            def __init__(self):
                super().__init__()

                self.yang_name = "submodule"
                self.yang_parent_name = "module"
                self.is_top_level_class = False
                self.has_list_ancestor = True
                self.ylist_key_names = ['name','revision']
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('name', (YLeaf(YType.str, 'name'), ['str'])),
                    ('revision', (YLeaf(YType.str, 'revision'), ['str','str'])),
                    ('schema', (YLeaf(YType.str, 'schema'), ['str'])),
                ])
                self.name = None
                self.revision = None
                self.schema = None
                self._segment_path = lambda: "submodule" + "[name='" + str(self.name) + "']" + "[revision='" + str(self.revision) + "']"
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(ModulesState.Module.Submodule, ['name', 'revision', 'schema'], name, value)



    def clone_ptr(self):
        self._top_entity = ModulesState()
        return self._top_entity



