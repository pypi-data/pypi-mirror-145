""" ietf_interfaces 

This module contains a collection of YANG definitions for
managing network interfaces.

Copyright (c) 2014 IETF Trust and the persons identified as
authors of the code.  All rights reserved.

Redistribution and use in source and binary forms, with or
without modification, is permitted pursuant to, and subject
to the license terms contained in, the Simplified BSD License
set forth in Section 4.c of the IETF Trust's Legal Provisions
Relating to IETF Documents
(http\://trustee.ietf.org/license\-info).

This version of this YANG module is part of RFC 7223; see
the RFC itself for full legal notices.

"""
import sys
from collections import OrderedDict

from ydk.types import Entity as _Entity_
from ydk.types import EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.types import Entity, EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.filters import YFilter
from ydk.errors import YError, YModelError
from ydk.errors.error_handler import handle_type_error as _handle_type_error




class InterfaceType(Identity):
    """
    Base identity from which specific interface types are
    derived.
    
    

    """

    _prefix = 'if'
    _revision = '2014-05-08'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:ietf-interfaces", pref="ietf-interfaces", tag="ietf-interfaces:interface-type"):
        if sys.version_info > (3,):
            super().__init__(ns, pref, tag)
        else:
            super(InterfaceType, self).__init__(ns, pref, tag)



class Interfaces(_Entity_):
    """
    Interface configuration parameters.
    
    .. attribute:: interface
    
    	The list of configured interfaces on the device.  The operational state of an interface is available in the /interfaces\-state/interface list.  If the configuration of a system\-controlled interface cannot be used by the system (e.g., the interface hardware present does not match the interface type), then the configuration is not applied to the system\-controlled interface shown in the /interfaces\-state/interface list.  If the configuration of a user\-controlled interface cannot be used by the system, the configured interface is not instantiated in the /interfaces\-state/interface list
    	**type**\: list of  		 :py:class:`Interface <ydk.models.ydktest.ietf_interfaces.Interfaces.Interface>`
    
    

    """

    _prefix = 'if'
    _revision = '2014-05-08'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(Interfaces, self).__init__()
        self._top_entity = None

        self.yang_name = "interfaces"
        self.yang_parent_name = "ietf-interfaces"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([("interface", ("interface", Interfaces.Interface))])
        self._leafs = OrderedDict()

        self.interface = YList(self)
        self._segment_path = lambda: "ietf-interfaces:interfaces"
        self._is_frozen = True

    def __setattr__(self, name, value):
        self._perform_setattr(Interfaces, [], name, value)


    class Interface(_Entity_):
        """
        The list of configured interfaces on the device.
        
        The operational state of an interface is available in the
        /interfaces\-state/interface list.  If the configuration of a
        system\-controlled interface cannot be used by the system
        (e.g., the interface hardware present does not match the
        interface type), then the configuration is not applied to
        the system\-controlled interface shown in the
        /interfaces\-state/interface list.  If the configuration
        of a user\-controlled interface cannot be used by the system,
        the configured interface is not instantiated in the
        /interfaces\-state/interface list.
        
        .. attribute:: name  (key)
        
        	The name of the interface.  A device MAY restrict the allowed values for this leaf, possibly depending on the type of the interface. For system\-controlled interfaces, this leaf is the device\-specific name of the interface.  The 'config false' list /interfaces\-state/interface contains the currently existing interfaces on the device.  If a client tries to create configuration for a system\-controlled interface that is not present in the /interfaces\-state/interface list, the server MAY reject the request if the implementation does not support pre\-provisioning of interfaces or if the name refers to an interface that can never exist in the system.  A NETCONF server MUST reply with an rpc\-error with the error\-tag 'invalid\-value' in this case.  If the device supports pre\-provisioning of interface configuration, the 'pre\-provisioning' feature is advertised.  If the device allows arbitrarily named user\-controlled interfaces, the 'arbitrary\-names' feature is advertised.  When a configured user\-controlled interface is created by the system, it is instantiated with the same name in the /interface\-state/interface list
        	**type**\: str
        
        .. attribute:: description
        
        	A textual description of the interface.  A server implementation MAY map this leaf to the ifAlias MIB object.  Such an implementation needs to use some mechanism to handle the differences in size and characters allowed between this leaf and ifAlias.  The definition of such a mechanism is outside the scope of this document.  Since ifAlias is defined to be stored in non\-volatile storage, the MIB implementation MUST map ifAlias to the value of 'description' in the persistently stored datastore.  Specifically, if the device supports '\:startup', when ifAlias is read the device MUST return the value of 'description' in the 'startup' datastore, and when it is written, it MUST be written to the 'running' and 'startup' datastores.  Note that it is up to the implementation to  decide whether to modify this single leaf in 'startup' or perform an implicit copy\-config from 'running' to 'startup'.  If the device does not support '\:startup', ifAlias MUST be mapped to the 'description' leaf in the 'running' datastore
        	**type**\: str
        
        .. attribute:: type
        
        	The type of the interface.  When an interface entry is created, a server MAY initialize the type leaf with a valid value, e.g., if it is possible to derive the type from the name of the interface.  If a client tries to set the type of an interface to a value that can never be used by the system, e.g., if the type is not supported or if the type does not match the name of the interface, the server MUST reject the request. A NETCONF server MUST reply with an rpc\-error with the error\-tag 'invalid\-value' in this case
        	**type**\:  :py:class:`InterfaceType <ydk.models.ydktest.ietf_interfaces.InterfaceType>`
        
        	**mandatory**\: True
        
        .. attribute:: enabled
        
        	This leaf contains the configured, desired state of the interface.  Systems that implement the IF\-MIB use the value of this leaf in the 'running' datastore to set IF\-MIB.ifAdminStatus to 'up' or 'down' after an ifEntry has been initialized, as described in RFC 2863.    Changes in this leaf in the 'running' datastore are reflected in ifAdminStatus, but if ifAdminStatus is changed over SNMP, this leaf is not affected
        	**type**\: bool
        
        	**default value**\: true
        
        .. attribute:: link_up_down_trap_enable
        
        	Controls whether linkUp/linkDown SNMP notifications should be generated for this interface.  If this node is not configured, the value 'enabled' is operationally used by the server for interfaces that do not operate on top of any other interface (i.e., there are no 'lower\-layer\-if' entries), and 'disabled' otherwise
        	**type**\:  :py:class:`LinkUpDownTrapEnable <ydk.models.ydktest.ietf_interfaces.Interfaces.Interface.LinkUpDownTrapEnable>`
        
        

        """

        _prefix = 'if'
        _revision = '2014-05-08'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Interfaces.Interface, self).__init__()

            self.yang_name = "interface"
            self.yang_parent_name = "interfaces"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = ['name']
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('name', (YLeaf(YType.str, 'name'), ['str'])),
                ('description', (YLeaf(YType.str, 'description'), ['str'])),
                ('type', (YLeaf(YType.identityref, 'type'), [('ydk.models.ydktest.ietf_interfaces', 'InterfaceType')])),
                ('enabled', (YLeaf(YType.boolean, 'enabled'), ['bool'])),
                ('link_up_down_trap_enable', (YLeaf(YType.enumeration, 'link-up-down-trap-enable'), [('ydk.models.ydktest.ietf_interfaces', 'Interfaces', 'Interface.LinkUpDownTrapEnable')])),
            ])
            self.name = None
            self.description = None
            self.type = None
            self.enabled = None
            self.link_up_down_trap_enable = None
            self._segment_path = lambda: "interface" + "[name='" + str(self.name) + "']"
            self._absolute_path = lambda: "ietf-interfaces:interfaces/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Interfaces.Interface, ['name', 'description', 'type', 'enabled', 'link_up_down_trap_enable'], name, value)

        class LinkUpDownTrapEnable(Enum):
            """
            LinkUpDownTrapEnable (Enum Class)

            Controls whether linkUp/linkDown SNMP notifications

            should be generated for this interface.

            If this node is not configured, the value 'enabled' is

            operationally used by the server for interfaces that do

            not operate on top of any other interface (i.e., there are

            no 'lower\-layer\-if' entries), and 'disabled' otherwise.

            .. data:: enabled = 1

            .. data:: disabled = 2

            """

            enabled = Enum.YLeaf(1, "enabled")

            disabled = Enum.YLeaf(2, "disabled")



    def clone_ptr(self):
        self._top_entity = Interfaces()
        return self._top_entity



class InterfacesState(_Entity_):
    """
    Data nodes for the operational state of interfaces.
    
    .. attribute:: interface
    
    	The list of interfaces on the device.  System\-controlled interfaces created by the system are always present in this list, whether they are configured or not
    	**type**\: list of  		 :py:class:`Interface <ydk.models.ydktest.ietf_interfaces.InterfacesState.Interface>`
    
    	**config**\: False
    
    

    """

    _prefix = 'if'
    _revision = '2014-05-08'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(InterfacesState, self).__init__()
        self._top_entity = None

        self.yang_name = "interfaces-state"
        self.yang_parent_name = "ietf-interfaces"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([("interface", ("interface", InterfacesState.Interface))])
        self._leafs = OrderedDict()

        self.interface = YList(self)
        self._segment_path = lambda: "ietf-interfaces:interfaces-state"
        self._is_frozen = True

    def __setattr__(self, name, value):
        self._perform_setattr(InterfacesState, [], name, value)


    class Interface(_Entity_):
        """
        The list of interfaces on the device.
        
        System\-controlled interfaces created by the system are
        always present in this list, whether they are configured or
        not.
        
        .. attribute:: name  (key)
        
        	The name of the interface.  A server implementation MAY map this leaf to the ifName MIB object.  Such an implementation needs to use some mechanism to handle the differences in size and characters allowed between this leaf and ifName.  The definition of such a mechanism is outside the scope of this document
        	**type**\: str
        
        	**config**\: False
        
        .. attribute:: type
        
        	The type of the interface
        	**type**\:  :py:class:`InterfaceType <ydk.models.ydktest.ietf_interfaces.InterfaceType>`
        
        	**mandatory**\: True
        
        	**config**\: False
        
        .. attribute:: admin_status
        
        	The desired state of the interface.  This leaf has the same read semantics as ifAdminStatus
        	**type**\:  :py:class:`AdminStatus <ydk.models.ydktest.ietf_interfaces.InterfacesState.Interface.AdminStatus>`
        
        	**mandatory**\: True
        
        	**config**\: False
        
        .. attribute:: oper_status
        
        	The current operational state of the interface.  This leaf has the same semantics as ifOperStatus
        	**type**\:  :py:class:`OperStatus <ydk.models.ydktest.ietf_interfaces.InterfacesState.Interface.OperStatus>`
        
        	**mandatory**\: True
        
        	**config**\: False
        
        .. attribute:: last_change
        
        	The time the interface entered its current operational state.  If the current state was entered prior to the last re\-initialization of the local network management subsystem, then this node is not present
        	**type**\: str
        
        	**pattern:** \\d{4}\-\\d{2}\-\\d{2}T\\d{2}\:\\d{2}\:\\d{2}(\\.\\d+)?(Z\|[\\+\\\-]\\d{2}\:\\d{2})
        
        	**config**\: False
        
        .. attribute:: if_index
        
        	The ifIndex value for the ifEntry represented by this interface
        	**type**\: int
        
        	**range:** 1..2147483647
        
        	**mandatory**\: True
        
        	**config**\: False
        
        .. attribute:: phys_address
        
        	The interface's address at its protocol sub\-layer.  For example, for an 802.x interface, this object normally contains a Media Access Control (MAC) address.  The interface's media\-specific modules must define the bit   and byte ordering and the format of the value of this object.  For interfaces that do not have such an address (e.g., a serial line), this node is not present
        	**type**\: str
        
        	**pattern:** ([0\-9a\-fA\-F]{2}(\:[0\-9a\-fA\-F]{2})\*)?
        
        	**config**\: False
        
        .. attribute:: higher_layer_if
        
        	A list of references to interfaces layered on top of this interface
        	**type**\: list of str
        
        	**refers to**\:  :py:class:`name <ydk.models.ydktest.ietf_interfaces.InterfacesState.Interface>`
        
        	**config**\: False
        
        .. attribute:: lower_layer_if
        
        	A list of references to interfaces layered underneath this interface
        	**type**\: list of str
        
        	**refers to**\:  :py:class:`name <ydk.models.ydktest.ietf_interfaces.InterfacesState.Interface>`
        
        	**config**\: False
        
        .. attribute:: speed
        
        	An estimate of the interface's current bandwidth in bits per second.  For interfaces that do not vary in bandwidth or for those where no accurate estimation can be made, this node should contain the nominal bandwidth. For interfaces that have no concept of bandwidth, this node is not present
        	**type**\: int
        
        	**range:** 0..18446744073709551615
        
        	**config**\: False
        
        	**units**\: bits/second
        
        .. attribute:: statistics
        
        	A collection of interface\-related statistics objects
        	**type**\:  :py:class:`Statistics <ydk.models.ydktest.ietf_interfaces.InterfacesState.Interface.Statistics>`
        
        	**config**\: False
        
        

        """

        _prefix = 'if'
        _revision = '2014-05-08'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(InterfacesState.Interface, self).__init__()

            self.yang_name = "interface"
            self.yang_parent_name = "interfaces-state"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = ['name']
            self._child_classes = OrderedDict([("statistics", ("statistics", InterfacesState.Interface.Statistics))])
            self._leafs = OrderedDict([
                ('name', (YLeaf(YType.str, 'name'), ['str'])),
                ('type', (YLeaf(YType.identityref, 'type'), [('ydk.models.ydktest.ietf_interfaces', 'InterfaceType')])),
                ('admin_status', (YLeaf(YType.enumeration, 'admin-status'), [('ydk.models.ydktest.ietf_interfaces', 'InterfacesState', 'Interface.AdminStatus')])),
                ('oper_status', (YLeaf(YType.enumeration, 'oper-status'), [('ydk.models.ydktest.ietf_interfaces', 'InterfacesState', 'Interface.OperStatus')])),
                ('last_change', (YLeaf(YType.str, 'last-change'), ['str'])),
                ('if_index', (YLeaf(YType.int32, 'if-index'), ['int'])),
                ('phys_address', (YLeaf(YType.str, 'phys-address'), ['str'])),
                ('higher_layer_if', (YLeafList(YType.str, 'higher-layer-if'), ['str'])),
                ('lower_layer_if', (YLeafList(YType.str, 'lower-layer-if'), ['str'])),
                ('speed', (YLeaf(YType.uint64, 'speed'), ['int'])),
            ])
            self.name = None
            self.type = None
            self.admin_status = None
            self.oper_status = None
            self.last_change = None
            self.if_index = None
            self.phys_address = None
            self.higher_layer_if = []
            self.lower_layer_if = []
            self.speed = None

            self.statistics = InterfacesState.Interface.Statistics()
            self.statistics.parent = self
            self._children_name_map["statistics"] = "statistics"
            self._segment_path = lambda: "interface" + "[name='" + str(self.name) + "']"
            self._absolute_path = lambda: "ietf-interfaces:interfaces-state/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(InterfacesState.Interface, ['name', 'type', 'admin_status', 'oper_status', 'last_change', 'if_index', 'phys_address', 'higher_layer_if', 'lower_layer_if', 'speed'], name, value)

        class AdminStatus(Enum):
            """
            AdminStatus (Enum Class)

            The desired state of the interface.

            This leaf has the same read semantics as ifAdminStatus.

            .. data:: up = 1

            	Ready to pass packets.

            .. data:: down = 2

            	Not ready to pass packets and not in some test mode.

            .. data:: testing = 3

            	In some test mode.

            """

            up = Enum.YLeaf(1, "up")

            down = Enum.YLeaf(2, "down")

            testing = Enum.YLeaf(3, "testing")


        class OperStatus(Enum):
            """
            OperStatus (Enum Class)

            The current operational state of the interface.

            This leaf has the same semantics as ifOperStatus.

            .. data:: up = 1

            	Ready to pass packets.

            .. data:: down = 2

            	The interface does not pass any packets.

            .. data:: testing = 3

            	In some test mode.  No operational packets can

            	be passed.

            .. data:: unknown = 4

            	Status cannot be determined for some reason.

            .. data:: dormant = 5

            	Waiting for some external event.

            .. data:: not_present = 6

            	Some component (typically hardware) is missing.

            .. data:: lower_layer_down = 7

            	Down due to state of lower-layer interface(s).

            """

            up = Enum.YLeaf(1, "up")

            down = Enum.YLeaf(2, "down")

            testing = Enum.YLeaf(3, "testing")

            unknown = Enum.YLeaf(4, "unknown")

            dormant = Enum.YLeaf(5, "dormant")

            not_present = Enum.YLeaf(6, "not-present")

            lower_layer_down = Enum.YLeaf(7, "lower-layer-down")



        class Statistics(_Entity_):
            """
            A collection of interface\-related statistics objects.
            
            .. attribute:: discontinuity_time
            
            	The time on the most recent occasion at which any one or more of this interface's counters suffered a discontinuity.  If no such discontinuities have occurred since the last re\-initialization of the local management subsystem, then this node contains the time the local management subsystem re\-initialized itself
            	**type**\: str
            
            	**pattern:** \\d{4}\-\\d{2}\-\\d{2}T\\d{2}\:\\d{2}\:\\d{2}(\\.\\d+)?(Z\|[\\+\\\-]\\d{2}\:\\d{2})
            
            	**mandatory**\: True
            
            	**config**\: False
            
            .. attribute:: in_octets
            
            	The total number of octets received on the interface, including framing characters.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
            	**type**\: int
            
            	**range:** 0..18446744073709551615
            
            	**config**\: False
            
            .. attribute:: in_unicast_pkts
            
            	The number of packets, delivered by this sub\-layer to a higher (sub\-)layer, that were not addressed to a multicast or broadcast address at this sub\-layer.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
            	**type**\: int
            
            	**range:** 0..18446744073709551615
            
            	**config**\: False
            
            .. attribute:: in_broadcast_pkts
            
            	The number of packets, delivered by this sub\-layer to a higher (sub\-)layer, that were addressed to a broadcast address at this sub\-layer.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
            	**type**\: int
            
            	**range:** 0..18446744073709551615
            
            	**config**\: False
            
            .. attribute:: in_multicast_pkts
            
            	The number of packets, delivered by this sub\-layer to a higher (sub\-)layer, that were addressed to a multicast address at this sub\-layer.  For a MAC\-layer protocol, this includes both Group and Functional addresses.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
            	**type**\: int
            
            	**range:** 0..18446744073709551615
            
            	**config**\: False
            
            .. attribute:: in_discards
            
            	The number of inbound packets that were chosen to be discarded even though no errors had been detected to prevent their being deliverable to a higher\-layer protocol.  One possible reason for discarding such a packet could be to free up buffer space.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
            	**type**\: int
            
            	**range:** 0..4294967295
            
            	**config**\: False
            
            .. attribute:: in_errors
            
            	For packet\-oriented interfaces, the number of inbound packets that contained errors preventing them from being deliverable to a higher\-layer protocol.  For character\- oriented or fixed\-length interfaces, the number of inbound transmission units that contained errors preventing them from being deliverable to a higher\-layer protocol.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
            	**type**\: int
            
            	**range:** 0..4294967295
            
            	**config**\: False
            
            .. attribute:: in_unknown_protos
            
            	For packet\-oriented interfaces, the number of packets received via the interface that were discarded because of an unknown or unsupported protocol.  For character\-oriented or fixed\-length interfaces that support protocol multiplexing, the number of transmission units received via the interface that were discarded because of an unknown or unsupported protocol. For any interface that does not support protocol multiplexing, this counter is not present.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
            	**type**\: int
            
            	**range:** 0..4294967295
            
            	**config**\: False
            
            .. attribute:: out_octets
            
            	The total number of octets transmitted out of the interface, including framing characters.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
            	**type**\: int
            
            	**range:** 0..18446744073709551615
            
            	**config**\: False
            
            .. attribute:: out_unicast_pkts
            
            	The total number of packets that higher\-level protocols requested be transmitted, and that were not addressed to a multicast or broadcast address at this sub\-layer, including those that were discarded or not sent.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
            	**type**\: int
            
            	**range:** 0..18446744073709551615
            
            	**config**\: False
            
            .. attribute:: out_broadcast_pkts
            
            	The total number of packets that higher\-level protocols requested be transmitted, and that were addressed to a broadcast address at this sub\-layer, including those that were discarded or not sent.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
            	**type**\: int
            
            	**range:** 0..18446744073709551615
            
            	**config**\: False
            
            .. attribute:: out_multicast_pkts
            
            	The total number of packets that higher\-level protocols requested be transmitted, and that were addressed to a multicast address at this sub\-layer, including those that were discarded or not sent.  For a MAC\-layer protocol, this includes both Group and Functional addresses.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
            	**type**\: int
            
            	**range:** 0..18446744073709551615
            
            	**config**\: False
            
            .. attribute:: out_discards
            
            	The number of outbound packets that were chosen to be discarded even though no errors had been detected to prevent their being transmitted.  One possible reason for discarding such a packet could be to free up buffer space.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
            	**type**\: int
            
            	**range:** 0..4294967295
            
            	**config**\: False
            
            .. attribute:: out_errors
            
            	For packet\-oriented interfaces, the number of outbound packets that could not be transmitted because of errors. For character\-oriented or fixed\-length interfaces, the number of outbound transmission units that could not be transmitted because of errors.     Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
            	**type**\: int
            
            	**range:** 0..4294967295
            
            	**config**\: False
            
            

            """

            _prefix = 'if'
            _revision = '2014-05-08'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(InterfacesState.Interface.Statistics, self).__init__()

                self.yang_name = "statistics"
                self.yang_parent_name = "interface"
                self.is_top_level_class = False
                self.has_list_ancestor = True
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('discontinuity_time', (YLeaf(YType.str, 'discontinuity-time'), ['str'])),
                    ('in_octets', (YLeaf(YType.uint64, 'in-octets'), ['int'])),
                    ('in_unicast_pkts', (YLeaf(YType.uint64, 'in-unicast-pkts'), ['int'])),
                    ('in_broadcast_pkts', (YLeaf(YType.uint64, 'in-broadcast-pkts'), ['int'])),
                    ('in_multicast_pkts', (YLeaf(YType.uint64, 'in-multicast-pkts'), ['int'])),
                    ('in_discards', (YLeaf(YType.uint32, 'in-discards'), ['int'])),
                    ('in_errors', (YLeaf(YType.uint32, 'in-errors'), ['int'])),
                    ('in_unknown_protos', (YLeaf(YType.uint32, 'in-unknown-protos'), ['int'])),
                    ('out_octets', (YLeaf(YType.uint64, 'out-octets'), ['int'])),
                    ('out_unicast_pkts', (YLeaf(YType.uint64, 'out-unicast-pkts'), ['int'])),
                    ('out_broadcast_pkts', (YLeaf(YType.uint64, 'out-broadcast-pkts'), ['int'])),
                    ('out_multicast_pkts', (YLeaf(YType.uint64, 'out-multicast-pkts'), ['int'])),
                    ('out_discards', (YLeaf(YType.uint32, 'out-discards'), ['int'])),
                    ('out_errors', (YLeaf(YType.uint32, 'out-errors'), ['int'])),
                ])
                self.discontinuity_time = None
                self.in_octets = None
                self.in_unicast_pkts = None
                self.in_broadcast_pkts = None
                self.in_multicast_pkts = None
                self.in_discards = None
                self.in_errors = None
                self.in_unknown_protos = None
                self.out_octets = None
                self.out_unicast_pkts = None
                self.out_broadcast_pkts = None
                self.out_multicast_pkts = None
                self.out_discards = None
                self.out_errors = None
                self._segment_path = lambda: "statistics"
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(InterfacesState.Interface.Statistics, ['discontinuity_time', 'in_octets', 'in_unicast_pkts', 'in_broadcast_pkts', 'in_multicast_pkts', 'in_discards', 'in_errors', 'in_unknown_protos', 'out_octets', 'out_unicast_pkts', 'out_broadcast_pkts', 'out_multicast_pkts', 'out_discards', 'out_errors'], name, value)



    def clone_ptr(self):
        self._top_entity = InterfacesState()
        return self._top_entity



