""" openconfig_interfaces 

Model for managing network interfaces and subinterfaces.  This
module also defines convenience types / groupings for other
models to create references to interfaces\:

 base\-interface\-ref (type) \-  reference to a base interface
 interface\-ref (grouping) \-  container for reference to a
   interface + subinterface
 interface\-ref\-state (grouping) \- container for read\-only
   (opstate) reference to interface + subinterface

This model reuses data items defined in the IETF YANG model for
interfaces described by RFC 7223 with an alternate structure
(particularly for operational state data) and and with
additional configuration items.

"""
import sys
from collections import OrderedDict

from ydk.types import Entity as _Entity_
from ydk.types import EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.types import Entity, EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.filters import YFilter
from ydk.errors import YError, YModelError
from ydk.errors.error_handler import handle_type_error as _handle_type_error




class Interfaces(_Entity_):
    """
    Top level container for interfaces, including configuration
    and state data.
    
    .. attribute:: interface
    
    	The list of named interfaces on the device
    	**type**\: list of  		 :py:class:`Interface <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface>`
    
    

    """

    _prefix = 'oc-if'
    _revision = '2016-05-26'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(Interfaces, self).__init__()
        self._top_entity = None

        self.yang_name = "interfaces"
        self.yang_parent_name = "openconfig-interfaces"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([("interface", ("interface", Interfaces.Interface))])
        self._leafs = OrderedDict()

        self.interface = YList(self)
        self._segment_path = lambda: "openconfig-interfaces:interfaces"
        self._is_frozen = True

    def __setattr__(self, name, value):
        self._perform_setattr(Interfaces, [], name, value)


    class Interface(_Entity_):
        """
        The list of named interfaces on the device.
        
        .. attribute:: name  (key)
        
        	References the configured name of the interface
        	**type**\: str
        
        	**refers to**\:  :py:class:`name <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.Config>`
        
        .. attribute:: config
        
        	Configurable items at the global, physical interface level
        	**type**\:  :py:class:`Config <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.Config>`
        
        .. attribute:: state
        
        	Operational state data at the global interface level
        	**type**\:  :py:class:`State <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.State>`
        
        	**config**\: False
        
        .. attribute:: hold_time
        
        	Top\-level container for hold\-time settings to enable dampening advertisements of interface transitions
        	**type**\:  :py:class:`HoldTime <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.HoldTime>`
        
        .. attribute:: subinterfaces
        
        	Enclosing container for the list of subinterfaces associated with a physical interface
        	**type**\:  :py:class:`Subinterfaces <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.Subinterfaces>`
        
        .. attribute:: ethernet
        
        	Top\-level container for ethernet configuration and state
        	**type**\:  :py:class:`Ethernet <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.Ethernet>`
        
        

        """

        _prefix = 'oc-if'
        _revision = '2016-05-26'

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
            self._child_classes = OrderedDict([("config", ("config", Interfaces.Interface.Config)), ("state", ("state", Interfaces.Interface.State)), ("hold-time", ("hold_time", Interfaces.Interface.HoldTime)), ("subinterfaces", ("subinterfaces", Interfaces.Interface.Subinterfaces)), ("openconfig-if-ethernet:ethernet", ("ethernet", Interfaces.Interface.Ethernet))])
            self._leafs = OrderedDict([
                ('name', (YLeaf(YType.str, 'name'), ['str'])),
            ])
            self.name = None

            self.config = Interfaces.Interface.Config()
            self.config.parent = self
            self._children_name_map["config"] = "config"

            self.state = Interfaces.Interface.State()
            self.state.parent = self
            self._children_name_map["state"] = "state"

            self.hold_time = Interfaces.Interface.HoldTime()
            self.hold_time.parent = self
            self._children_name_map["hold_time"] = "hold-time"

            self.subinterfaces = Interfaces.Interface.Subinterfaces()
            self.subinterfaces.parent = self
            self._children_name_map["subinterfaces"] = "subinterfaces"

            self.ethernet = Interfaces.Interface.Ethernet()
            self.ethernet.parent = self
            self._children_name_map["ethernet"] = "openconfig-if-ethernet:ethernet"
            self._segment_path = lambda: "interface" + "[name='" + str(self.name) + "']"
            self._absolute_path = lambda: "openconfig-interfaces:interfaces/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Interfaces.Interface, ['name'], name, value)


        class Config(_Entity_):
            """
            Configurable items at the global, physical interface
            level
            
            .. attribute:: type
            
            	[adapted from IETF interfaces model (RFC 7223)]  The type of the interface.  When an interface entry is created, a server MAY initialize the type leaf with a valid value, e.g., if it is possible to derive the type from the name of the interface.  If a client tries to set the type of an interface to a value that can never be used by the system, e.g., if the type is not supported or if the type does not match the name of the interface, the server MUST reject the request. A NETCONF server MUST reply with an rpc\-error with the error\-tag 'invalid\-value' in this case
            	**type**\:  :py:class:`InterfaceType <ydk.models.ydktest.ietf_interfaces.InterfaceType>`
            
            .. attribute:: mtu
            
            	Set the max transmission unit size in octets for the physical interface.  If this is not set, the mtu is set to the operational default \-\- e.g., 1514 bytes on an Ethernet interface
            	**type**\: int
            
            	**range:** 0..65535
            
            .. attribute:: name
            
            	[adapted from IETF interfaces model (RFC 7223)]  The name of the interface.  A device MAY restrict the allowed values for this leaf, possibly depending on the type of the interface. For system\-controlled interfaces, this leaf is the device\-specific name of the interface.  The 'config false' list interfaces/interface[name]/state contains the currently existing interfaces on the device.  If a client tries to create configuration for a system\-controlled interface that is not present in the corresponding state list, the server MAY reject the request if the implementation does not support pre\-provisioning of interfaces or if the name refers to an interface that can never exist in the system.  A NETCONF server MUST reply with an rpc\-error with the error\-tag 'invalid\-value' in this case.  The IETF model in RFC 7223 provides YANG features for the following (i.e., pre\-provisioning and arbitrary\-names), however they are omitted here\:   If the device supports pre\-provisioning of interface  configuration, the 'pre\-provisioning' feature is  advertised.   If the device allows arbitrarily named user\-controlled  interfaces, the 'arbitrary\-names' feature is advertised.  When a configured user\-controlled interface is created by the system, it is instantiated with the same name in the /interfaces/interface[name]/state list
            	**type**\: str
            
            .. attribute:: description
            
            	[adapted from IETF interfaces model (RFC 7223)]  A textual description of the interface.  A server implementation MAY map this leaf to the ifAlias MIB object.  Such an implementation needs to use some mechanism to handle the differences in size and characters allowed between this leaf and ifAlias.  The definition of such a mechanism is outside the scope of this document.  Since ifAlias is defined to be stored in non\-volatile storage, the MIB implementation MUST map ifAlias to the value of 'description' in the persistently stored datastore.  Specifically, if the device supports '\:startup', when ifAlias is read the device MUST return the value of 'description' in the 'startup' datastore, and when it is written, it MUST be written to the 'running' and 'startup' datastores.  Note that it is up to the implementation to  decide whether to modify this single leaf in 'startup' or perform an implicit copy\-config from 'running' to 'startup'.  If the device does not support '\:startup', ifAlias MUST be mapped to the 'description' leaf in the 'running' datastore
            	**type**\: str
            
            .. attribute:: enabled
            
            	[adapted from IETF interfaces model (RFC 7223)]  This leaf contains the configured, desired state of the interface.  Systems that implement the IF\-MIB use the value of this leaf in the 'running' datastore to set IF\-MIB.ifAdminStatus to 'up' or 'down' after an ifEntry has been initialized, as described in RFC 2863.  Changes in this leaf in the 'running' datastore are reflected in ifAdminStatus, but if ifAdminStatus is changed over SNMP, this leaf is not affected
            	**type**\: bool
            
            	**default value**\: true
            
            

            """

            _prefix = 'oc-if'
            _revision = '2016-05-26'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Interfaces.Interface.Config, self).__init__()

                self.yang_name = "config"
                self.yang_parent_name = "interface"
                self.is_top_level_class = False
                self.has_list_ancestor = True
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('type', (YLeaf(YType.identityref, 'type'), [('ydk.models.ydktest.ietf_interfaces', 'InterfaceType')])),
                    ('mtu', (YLeaf(YType.uint16, 'mtu'), ['int'])),
                    ('name', (YLeaf(YType.str, 'name'), ['str'])),
                    ('description', (YLeaf(YType.str, 'description'), ['str'])),
                    ('enabled', (YLeaf(YType.boolean, 'enabled'), ['bool'])),
                ])
                self.type = None
                self.mtu = None
                self.name = None
                self.description = None
                self.enabled = None
                self._segment_path = lambda: "config"
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Interfaces.Interface.Config, ['type', 'mtu', 'name', 'description', 'enabled'], name, value)



        class State(_Entity_):
            """
            Operational state data at the global interface level
            
            .. attribute:: type
            
            	[adapted from IETF interfaces model (RFC 7223)]  The type of the interface.  When an interface entry is created, a server MAY initialize the type leaf with a valid value, e.g., if it is possible to derive the type from the name of the interface.  If a client tries to set the type of an interface to a value that can never be used by the system, e.g., if the type is not supported or if the type does not match the name of the interface, the server MUST reject the request. A NETCONF server MUST reply with an rpc\-error with the error\-tag 'invalid\-value' in this case
            	**type**\:  :py:class:`InterfaceType <ydk.models.ydktest.ietf_interfaces.InterfaceType>`
            
            	**config**\: False
            
            .. attribute:: mtu
            
            	Set the max transmission unit size in octets for the physical interface.  If this is not set, the mtu is set to the operational default \-\- e.g., 1514 bytes on an Ethernet interface
            	**type**\: int
            
            	**range:** 0..65535
            
            	**config**\: False
            
            .. attribute:: name
            
            	[adapted from IETF interfaces model (RFC 7223)]  The name of the interface.  A device MAY restrict the allowed values for this leaf, possibly depending on the type of the interface. For system\-controlled interfaces, this leaf is the device\-specific name of the interface.  The 'config false' list interfaces/interface[name]/state contains the currently existing interfaces on the device.  If a client tries to create configuration for a system\-controlled interface that is not present in the corresponding state list, the server MAY reject the request if the implementation does not support pre\-provisioning of interfaces or if the name refers to an interface that can never exist in the system.  A NETCONF server MUST reply with an rpc\-error with the error\-tag 'invalid\-value' in this case.  The IETF model in RFC 7223 provides YANG features for the following (i.e., pre\-provisioning and arbitrary\-names), however they are omitted here\:   If the device supports pre\-provisioning of interface  configuration, the 'pre\-provisioning' feature is  advertised.   If the device allows arbitrarily named user\-controlled  interfaces, the 'arbitrary\-names' feature is advertised.  When a configured user\-controlled interface is created by the system, it is instantiated with the same name in the /interfaces/interface[name]/state list
            	**type**\: str
            
            	**config**\: False
            
            .. attribute:: description
            
            	[adapted from IETF interfaces model (RFC 7223)]  A textual description of the interface.  A server implementation MAY map this leaf to the ifAlias MIB object.  Such an implementation needs to use some mechanism to handle the differences in size and characters allowed between this leaf and ifAlias.  The definition of such a mechanism is outside the scope of this document.  Since ifAlias is defined to be stored in non\-volatile storage, the MIB implementation MUST map ifAlias to the value of 'description' in the persistently stored datastore.  Specifically, if the device supports '\:startup', when ifAlias is read the device MUST return the value of 'description' in the 'startup' datastore, and when it is written, it MUST be written to the 'running' and 'startup' datastores.  Note that it is up to the implementation to  decide whether to modify this single leaf in 'startup' or perform an implicit copy\-config from 'running' to 'startup'.  If the device does not support '\:startup', ifAlias MUST be mapped to the 'description' leaf in the 'running' datastore
            	**type**\: str
            
            	**config**\: False
            
            .. attribute:: enabled
            
            	[adapted from IETF interfaces model (RFC 7223)]  This leaf contains the configured, desired state of the interface.  Systems that implement the IF\-MIB use the value of this leaf in the 'running' datastore to set IF\-MIB.ifAdminStatus to 'up' or 'down' after an ifEntry has been initialized, as described in RFC 2863.  Changes in this leaf in the 'running' datastore are reflected in ifAdminStatus, but if ifAdminStatus is changed over SNMP, this leaf is not affected
            	**type**\: bool
            
            	**config**\: False
            
            	**default value**\: true
            
            .. attribute:: ifindex
            
            	System assigned number for each interface.  Corresponds to ifIndex object in SNMP Interface MIB
            	**type**\: int
            
            	**range:** 0..4294967295
            
            	**config**\: False
            
            .. attribute:: admin_status
            
            	[adapted from IETF interfaces model (RFC 7223)]  The desired state of the interface.  In RFC 7223 this leaf has the same read semantics as ifAdminStatus.  Here, it reflects the administrative state as set by enabling or disabling the interface
            	**type**\:  :py:class:`AdminStatus <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.State.AdminStatus>`
            
            	**config**\: False
            
            .. attribute:: oper_status
            
            	[adapted from IETF interfaces model (RFC 7223)]  The current operational state of the interface.  This leaf has the same semantics as ifOperStatus
            	**type**\:  :py:class:`OperStatus <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.State.OperStatus>`
            
            	**config**\: False
            
            .. attribute:: last_change
            
            	Date and time of the last state change of the interface (e.g., up\-to\-down transition).   This corresponds to the ifLastChange object in the standard interface MIB
            	**type**\: int
            
            	**range:** 0..4294967295
            
            	**config**\: False
            
            .. attribute:: counters
            
            	A collection of interface\-related statistics objects
            	**type**\:  :py:class:`Counters <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.State.Counters>`
            
            	**config**\: False
            
            .. attribute:: hardware_port
            
            	References the hardware port in the device inventory
            	**type**\: str
            
            	**refers to**\:  :py:class:`name <ydk.models.ydktest.openconfig_platform.Components.Component>`
            
            	**config**\: False
            
            

            """

            _prefix = 'oc-if'
            _revision = '2016-05-26'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Interfaces.Interface.State, self).__init__()

                self.yang_name = "state"
                self.yang_parent_name = "interface"
                self.is_top_level_class = False
                self.has_list_ancestor = True
                self.ylist_key_names = []
                self._child_classes = OrderedDict([("counters", ("counters", Interfaces.Interface.State.Counters))])
                self._leafs = OrderedDict([
                    ('type', (YLeaf(YType.identityref, 'type'), [('ydk.models.ydktest.ietf_interfaces', 'InterfaceType')])),
                    ('mtu', (YLeaf(YType.uint16, 'mtu'), ['int'])),
                    ('name', (YLeaf(YType.str, 'name'), ['str'])),
                    ('description', (YLeaf(YType.str, 'description'), ['str'])),
                    ('enabled', (YLeaf(YType.boolean, 'enabled'), ['bool'])),
                    ('ifindex', (YLeaf(YType.uint32, 'ifindex'), ['int'])),
                    ('admin_status', (YLeaf(YType.enumeration, 'admin-status'), [('ydk.models.ydktest.openconfig_interfaces', 'Interfaces', 'Interface.State.AdminStatus')])),
                    ('oper_status', (YLeaf(YType.enumeration, 'oper-status'), [('ydk.models.ydktest.openconfig_interfaces', 'Interfaces', 'Interface.State.OperStatus')])),
                    ('last_change', (YLeaf(YType.uint32, 'last-change'), ['int'])),
                    ('hardware_port', (YLeaf(YType.str, 'openconfig-platform:hardware-port'), ['str'])),
                ])
                self.type = None
                self.mtu = None
                self.name = None
                self.description = None
                self.enabled = None
                self.ifindex = None
                self.admin_status = None
                self.oper_status = None
                self.last_change = None
                self.hardware_port = None

                self.counters = Interfaces.Interface.State.Counters()
                self.counters.parent = self
                self._children_name_map["counters"] = "counters"
                self._segment_path = lambda: "state"
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Interfaces.Interface.State, ['type', 'mtu', 'name', 'description', 'enabled', 'ifindex', 'admin_status', 'oper_status', 'last_change', 'hardware_port'], name, value)

            class AdminStatus(Enum):
                """
                AdminStatus (Enum Class)

                [adapted from IETF interfaces model (RFC 7223)]

                The desired state of the interface.  In RFC 7223 this leaf

                has the same read semantics as ifAdminStatus.  Here, it

                reflects the administrative state as set by enabling or

                disabling the interface.

                .. data:: UP = 0

                	Ready to pass packets.

                .. data:: DOWN = 1

                	Not ready to pass packets and not in some test mode.

                .. data:: TESTING = 2

                	In some test mode.

                """

                UP = Enum.YLeaf(0, "UP")

                DOWN = Enum.YLeaf(1, "DOWN")

                TESTING = Enum.YLeaf(2, "TESTING")


            class OperStatus(Enum):
                """
                OperStatus (Enum Class)

                [adapted from IETF interfaces model (RFC 7223)]

                The current operational state of the interface.

                This leaf has the same semantics as ifOperStatus.

                .. data:: UP = 1

                	Ready to pass packets.

                .. data:: DOWN = 2

                	The interface does not pass any packets.

                .. data:: TESTING = 3

                	In some test mode.  No operational packets can

                	be passed.

                .. data:: UNKNOWN = 4

                	Status cannot be determined for some reason.

                .. data:: DORMANT = 5

                	Waiting for some external event.

                .. data:: NOT_PRESENT = 6

                	Some component (typically hardware) is missing.

                .. data:: LOWER_LAYER_DOWN = 7

                	Down due to state of lower-layer interface(s).

                """

                UP = Enum.YLeaf(1, "UP")

                DOWN = Enum.YLeaf(2, "DOWN")

                TESTING = Enum.YLeaf(3, "TESTING")

                UNKNOWN = Enum.YLeaf(4, "UNKNOWN")

                DORMANT = Enum.YLeaf(5, "DORMANT")

                NOT_PRESENT = Enum.YLeaf(6, "NOT_PRESENT")

                LOWER_LAYER_DOWN = Enum.YLeaf(7, "LOWER_LAYER_DOWN")



            class Counters(_Entity_):
                """
                A collection of interface\-related statistics objects.
                
                .. attribute:: in_octets
                
                	[adapted from IETF interfaces model (RFC 7223)]  The total number of octets received on the interface, including framing characters.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                	**type**\: int
                
                	**range:** 0..18446744073709551615
                
                	**config**\: False
                
                .. attribute:: in_unicast_pkts
                
                	[adapted from IETF interfaces model (RFC 7223)]  The number of packets, delivered by this sub\-layer to a higher (sub\-)layer, that were not addressed to a multicast or broadcast address at this sub\-layer.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                	**type**\: int
                
                	**range:** 0..18446744073709551615
                
                	**config**\: False
                
                .. attribute:: in_broadcast_pkts
                
                	[adapted from IETF interfaces model (RFC 7223)]  The number of packets, delivered by this sub\-layer to a higher (sub\-)layer, that were addressed to a broadcast address at this sub\-layer.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                	**type**\: int
                
                	**range:** 0..18446744073709551615
                
                	**config**\: False
                
                .. attribute:: in_multicast_pkts
                
                	[adapted from IETF interfaces model (RFC 7223)]   The number of packets, delivered by this sub\-layer to a higher (sub\-)layer, that were addressed to a multicast address at this sub\-layer.  For a MAC\-layer protocol, this includes both Group and Functional addresses.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                	**type**\: int
                
                	**range:** 0..18446744073709551615
                
                	**config**\: False
                
                .. attribute:: in_discards
                
                	[adapted from IETF interfaces model (RFC 7223)] Changed the counter type to counter64.  The number of inbound packets that were chosen to be discarded even though no errors had been detected to prevent their being deliverable to a higher\-layer protocol.  One possible reason for discarding such a packet could be to free up buffer space.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                	**type**\: int
                
                	**range:** 0..18446744073709551615
                
                	**config**\: False
                
                .. attribute:: in_errors
                
                	[adapted from IETF interfaces model (RFC 7223)] Changed the counter type to counter64.  For packet\-oriented interfaces, the number of inbound packets that contained errors preventing them from being deliverable to a higher\-layer protocol.  For character\- oriented or fixed\-length interfaces, the number of inbound transmission units that contained errors preventing them from being deliverable to a higher\-layer protocol.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                	**type**\: int
                
                	**range:** 0..18446744073709551615
                
                	**config**\: False
                
                .. attribute:: in_unknown_protos
                
                	[adapted from IETF interfaces model (RFC 7223)] Changed the counter type to counter64.  For packet\-oriented interfaces, the number of packets received via the interface that were discarded because of an unknown or unsupported protocol.  For character\-oriented or fixed\-length interfaces that support protocol multiplexing, the number of transmission units received via the interface that were discarded because of an unknown or unsupported protocol. For any interface that does not support protocol multiplexing, this counter is not present.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                	**type**\: int
                
                	**range:** 0..4294967295
                
                	**config**\: False
                
                .. attribute:: out_octets
                
                	[adapted from IETF interfaces model (RFC 7223)] Changed the counter type to counter64.  The total number of octets transmitted out of the interface, including framing characters.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                	**type**\: int
                
                	**range:** 0..18446744073709551615
                
                	**config**\: False
                
                .. attribute:: out_unicast_pkts
                
                	[adapted from IETF interfaces model (RFC 7223)]  The total number of packets that higher\-level protocols requested be transmitted, and that were not addressed to a multicast or broadcast address at this sub\-layer, including those that were discarded or not sent.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                	**type**\: int
                
                	**range:** 0..18446744073709551615
                
                	**config**\: False
                
                .. attribute:: out_broadcast_pkts
                
                	[adapted from IETF interfaces model (RFC 7223)]  The total number of packets that higher\-level protocols requested be transmitted, and that were addressed to a broadcast address at this sub\-layer, including those that were discarded or not sent.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                	**type**\: int
                
                	**range:** 0..18446744073709551615
                
                	**config**\: False
                
                .. attribute:: out_multicast_pkts
                
                	[adapted from IETF interfaces model (RFC 7223)] Changed the counter type to counter64.  The total number of packets that higher\-level protocols requested be transmitted, and that were addressed to a multicast address at this sub\-layer, including those that were discarded or not sent.  For a MAC\-layer protocol, this includes both Group and Functional addresses.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                	**type**\: int
                
                	**range:** 0..18446744073709551615
                
                	**config**\: False
                
                .. attribute:: out_discards
                
                	[adapted from IETF interfaces model (RFC 7223)] Changed the counter type to counter64.  The number of outbound packets that were chosen to be discarded even though no errors had been detected to prevent their being transmitted.  One possible reason for discarding such a packet could be to free up buffer space.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                	**type**\: int
                
                	**range:** 0..18446744073709551615
                
                	**config**\: False
                
                .. attribute:: out_errors
                
                	[adapted from IETF interfaces model (RFC 7223)] Changed the counter type to counter64.  For packet\-oriented interfaces, the number of outbound packets that could not be transmitted because of errors. For character\-oriented or fixed\-length interfaces, the number of outbound transmission units that could not be transmitted because of errors.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                	**type**\: int
                
                	**range:** 0..18446744073709551615
                
                	**config**\: False
                
                .. attribute:: last_clear
                
                	Indicates the last time the interface counters were cleared
                	**type**\: str
                
                	**pattern:** \\d{4}\-\\d{2}\-\\d{2}T\\d{2}\:\\d{2}\:\\d{2}(\\.\\d+)?(Z\|[\\+\\\-]\\d{2}\:\\d{2})
                
                	**config**\: False
                
                

                """

                _prefix = 'oc-if'
                _revision = '2016-05-26'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Interfaces.Interface.State.Counters, self).__init__()

                    self.yang_name = "counters"
                    self.yang_parent_name = "state"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('in_octets', (YLeaf(YType.uint64, 'in-octets'), ['int'])),
                        ('in_unicast_pkts', (YLeaf(YType.uint64, 'in-unicast-pkts'), ['int'])),
                        ('in_broadcast_pkts', (YLeaf(YType.uint64, 'in-broadcast-pkts'), ['int'])),
                        ('in_multicast_pkts', (YLeaf(YType.uint64, 'in-multicast-pkts'), ['int'])),
                        ('in_discards', (YLeaf(YType.uint64, 'in-discards'), ['int'])),
                        ('in_errors', (YLeaf(YType.uint64, 'in-errors'), ['int'])),
                        ('in_unknown_protos', (YLeaf(YType.uint32, 'in-unknown-protos'), ['int'])),
                        ('out_octets', (YLeaf(YType.uint64, 'out-octets'), ['int'])),
                        ('out_unicast_pkts', (YLeaf(YType.uint64, 'out-unicast-pkts'), ['int'])),
                        ('out_broadcast_pkts', (YLeaf(YType.uint64, 'out-broadcast-pkts'), ['int'])),
                        ('out_multicast_pkts', (YLeaf(YType.uint64, 'out-multicast-pkts'), ['int'])),
                        ('out_discards', (YLeaf(YType.uint64, 'out-discards'), ['int'])),
                        ('out_errors', (YLeaf(YType.uint64, 'out-errors'), ['int'])),
                        ('last_clear', (YLeaf(YType.str, 'last-clear'), ['str'])),
                    ])
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
                    self.last_clear = None
                    self._segment_path = lambda: "counters"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Interfaces.Interface.State.Counters, ['in_octets', 'in_unicast_pkts', 'in_broadcast_pkts', 'in_multicast_pkts', 'in_discards', 'in_errors', 'in_unknown_protos', 'out_octets', 'out_unicast_pkts', 'out_broadcast_pkts', 'out_multicast_pkts', 'out_discards', 'out_errors', 'last_clear'], name, value)




        class HoldTime(_Entity_):
            """
            Top\-level container for hold\-time settings to enable
            dampening advertisements of interface transitions.
            
            .. attribute:: config
            
            	Configuration data for interface hold\-time settings
            	**type**\:  :py:class:`Config <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.HoldTime.Config>`
            
            .. attribute:: state
            
            	Operational state data for interface hold\-time
            	**type**\:  :py:class:`State <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.HoldTime.State>`
            
            	**config**\: False
            
            

            """

            _prefix = 'oc-if'
            _revision = '2016-05-26'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Interfaces.Interface.HoldTime, self).__init__()

                self.yang_name = "hold-time"
                self.yang_parent_name = "interface"
                self.is_top_level_class = False
                self.has_list_ancestor = True
                self.ylist_key_names = []
                self._child_classes = OrderedDict([("config", ("config", Interfaces.Interface.HoldTime.Config)), ("state", ("state", Interfaces.Interface.HoldTime.State))])
                self._leafs = OrderedDict()

                self.config = Interfaces.Interface.HoldTime.Config()
                self.config.parent = self
                self._children_name_map["config"] = "config"

                self.state = Interfaces.Interface.HoldTime.State()
                self.state.parent = self
                self._children_name_map["state"] = "state"
                self._segment_path = lambda: "hold-time"
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Interfaces.Interface.HoldTime, [], name, value)


            class Config(_Entity_):
                """
                Configuration data for interface hold\-time settings.
                
                .. attribute:: up
                
                	Dampens advertisement when the interface transitions from down to up.  A zero value means dampening is turned off, i.e., immediate notification
                	**type**\: int
                
                	**range:** 0..4294967295
                
                	**units**\: milliseconds
                
                	**default value**\: 0
                
                .. attribute:: down
                
                	Dampens advertisement when the interface transitions from up to down.  A zero value means dampening is turned off, i.e., immediate notification
                	**type**\: int
                
                	**range:** 0..4294967295
                
                	**units**\: milliseconds
                
                	**default value**\: 0
                
                

                """

                _prefix = 'oc-if'
                _revision = '2016-05-26'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Interfaces.Interface.HoldTime.Config, self).__init__()

                    self.yang_name = "config"
                    self.yang_parent_name = "hold-time"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('up', (YLeaf(YType.uint32, 'up'), ['int'])),
                        ('down', (YLeaf(YType.uint32, 'down'), ['int'])),
                    ])
                    self.up = None
                    self.down = None
                    self._segment_path = lambda: "config"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Interfaces.Interface.HoldTime.Config, ['up', 'down'], name, value)



            class State(_Entity_):
                """
                Operational state data for interface hold\-time.
                
                .. attribute:: up
                
                	Dampens advertisement when the interface transitions from down to up.  A zero value means dampening is turned off, i.e., immediate notification
                	**type**\: int
                
                	**range:** 0..4294967295
                
                	**config**\: False
                
                	**units**\: milliseconds
                
                	**default value**\: 0
                
                .. attribute:: down
                
                	Dampens advertisement when the interface transitions from up to down.  A zero value means dampening is turned off, i.e., immediate notification
                	**type**\: int
                
                	**range:** 0..4294967295
                
                	**config**\: False
                
                	**units**\: milliseconds
                
                	**default value**\: 0
                
                

                """

                _prefix = 'oc-if'
                _revision = '2016-05-26'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Interfaces.Interface.HoldTime.State, self).__init__()

                    self.yang_name = "state"
                    self.yang_parent_name = "hold-time"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('up', (YLeaf(YType.uint32, 'up'), ['int'])),
                        ('down', (YLeaf(YType.uint32, 'down'), ['int'])),
                    ])
                    self.up = None
                    self.down = None
                    self._segment_path = lambda: "state"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Interfaces.Interface.HoldTime.State, ['up', 'down'], name, value)




        class Subinterfaces(_Entity_):
            """
            Enclosing container for the list of subinterfaces associated
            with a physical interface
            
            .. attribute:: subinterface
            
            	The list of subinterfaces (logical interfaces) associated with a physical interface
            	**type**\: list of  		 :py:class:`Subinterface <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.Subinterfaces.Subinterface>`
            
            

            """

            _prefix = 'oc-if'
            _revision = '2016-05-26'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Interfaces.Interface.Subinterfaces, self).__init__()

                self.yang_name = "subinterfaces"
                self.yang_parent_name = "interface"
                self.is_top_level_class = False
                self.has_list_ancestor = True
                self.ylist_key_names = []
                self._child_classes = OrderedDict([("subinterface", ("subinterface", Interfaces.Interface.Subinterfaces.Subinterface))])
                self._leafs = OrderedDict()

                self.subinterface = YList(self)
                self._segment_path = lambda: "subinterfaces"
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Interfaces.Interface.Subinterfaces, [], name, value)


            class Subinterface(_Entity_):
                """
                The list of subinterfaces (logical interfaces) associated
                with a physical interface
                
                .. attribute:: index  (key)
                
                	The index number of the subinterface \-\- used to address the logical interface
                	**type**\: int
                
                	**range:** 0..4294967295
                
                	**refers to**\:  :py:class:`index <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.Subinterfaces.Subinterface.Config>`
                
                .. attribute:: config
                
                	Configurable items at the subinterface level
                	**type**\:  :py:class:`Config <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.Subinterfaces.Subinterface.Config>`
                
                .. attribute:: state
                
                	Operational state data for logical interfaces
                	**type**\:  :py:class:`State <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.Subinterfaces.Subinterface.State>`
                
                	**config**\: False
                
                

                """

                _prefix = 'oc-if'
                _revision = '2016-05-26'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Interfaces.Interface.Subinterfaces.Subinterface, self).__init__()

                    self.yang_name = "subinterface"
                    self.yang_parent_name = "subinterfaces"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = ['index']
                    self._child_classes = OrderedDict([("config", ("config", Interfaces.Interface.Subinterfaces.Subinterface.Config)), ("state", ("state", Interfaces.Interface.Subinterfaces.Subinterface.State))])
                    self._leafs = OrderedDict([
                        ('index', (YLeaf(YType.str, 'index'), ['int'])),
                    ])
                    self.index = None

                    self.config = Interfaces.Interface.Subinterfaces.Subinterface.Config()
                    self.config.parent = self
                    self._children_name_map["config"] = "config"

                    self.state = Interfaces.Interface.Subinterfaces.Subinterface.State()
                    self.state.parent = self
                    self._children_name_map["state"] = "state"
                    self._segment_path = lambda: "subinterface" + "[index='" + str(self.index) + "']"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Interfaces.Interface.Subinterfaces.Subinterface, ['index'], name, value)


                class Config(_Entity_):
                    """
                    Configurable items at the subinterface level
                    
                    .. attribute:: index
                    
                    	The index of the subinterface, or logical interface number. On systems with no support for subinterfaces, or not using subinterfaces, this value should default to 0, i.e., the default subinterface
                    	**type**\: int
                    
                    	**range:** 0..4294967295
                    
                    	**default value**\: 0
                    
                    .. attribute:: name
                    
                    	[adapted from IETF interfaces model (RFC 7223)]  The name of the interface.  A device MAY restrict the allowed values for this leaf, possibly depending on the type of the interface. For system\-controlled interfaces, this leaf is the device\-specific name of the interface.  The 'config false' list interfaces/interface[name]/state contains the currently existing interfaces on the device.  If a client tries to create configuration for a system\-controlled interface that is not present in the corresponding state list, the server MAY reject the request if the implementation does not support pre\-provisioning of interfaces or if the name refers to an interface that can never exist in the system.  A NETCONF server MUST reply with an rpc\-error with the error\-tag 'invalid\-value' in this case.  The IETF model in RFC 7223 provides YANG features for the following (i.e., pre\-provisioning and arbitrary\-names), however they are omitted here\:   If the device supports pre\-provisioning of interface  configuration, the 'pre\-provisioning' feature is  advertised.   If the device allows arbitrarily named user\-controlled  interfaces, the 'arbitrary\-names' feature is advertised.  When a configured user\-controlled interface is created by the system, it is instantiated with the same name in the /interfaces/interface[name]/state list
                    	**type**\: str
                    
                    .. attribute:: description
                    
                    	[adapted from IETF interfaces model (RFC 7223)]  A textual description of the interface.  A server implementation MAY map this leaf to the ifAlias MIB object.  Such an implementation needs to use some mechanism to handle the differences in size and characters allowed between this leaf and ifAlias.  The definition of such a mechanism is outside the scope of this document.  Since ifAlias is defined to be stored in non\-volatile storage, the MIB implementation MUST map ifAlias to the value of 'description' in the persistently stored datastore.  Specifically, if the device supports '\:startup', when ifAlias is read the device MUST return the value of 'description' in the 'startup' datastore, and when it is written, it MUST be written to the 'running' and 'startup' datastores.  Note that it is up to the implementation to  decide whether to modify this single leaf in 'startup' or perform an implicit copy\-config from 'running' to 'startup'.  If the device does not support '\:startup', ifAlias MUST be mapped to the 'description' leaf in the 'running' datastore
                    	**type**\: str
                    
                    .. attribute:: enabled
                    
                    	[adapted from IETF interfaces model (RFC 7223)]  This leaf contains the configured, desired state of the interface.  Systems that implement the IF\-MIB use the value of this leaf in the 'running' datastore to set IF\-MIB.ifAdminStatus to 'up' or 'down' after an ifEntry has been initialized, as described in RFC 2863.  Changes in this leaf in the 'running' datastore are reflected in ifAdminStatus, but if ifAdminStatus is changed over SNMP, this leaf is not affected
                    	**type**\: bool
                    
                    	**default value**\: true
                    
                    

                    """

                    _prefix = 'oc-if'
                    _revision = '2016-05-26'

                    def __init__(self):
                        if sys.version_info > (3,):
                            super().__init__()
                        else:
                            super(Interfaces.Interface.Subinterfaces.Subinterface.Config, self).__init__()

                        self.yang_name = "config"
                        self.yang_parent_name = "subinterface"
                        self.is_top_level_class = False
                        self.has_list_ancestor = True
                        self.ylist_key_names = []
                        self._child_classes = OrderedDict([])
                        self._leafs = OrderedDict([
                            ('index', (YLeaf(YType.uint32, 'index'), ['int'])),
                            ('name', (YLeaf(YType.str, 'name'), ['str'])),
                            ('description', (YLeaf(YType.str, 'description'), ['str'])),
                            ('enabled', (YLeaf(YType.boolean, 'enabled'), ['bool'])),
                        ])
                        self.index = None
                        self.name = None
                        self.description = None
                        self.enabled = None
                        self._segment_path = lambda: "config"
                        self._is_frozen = True

                    def __setattr__(self, name, value):
                        self._perform_setattr(Interfaces.Interface.Subinterfaces.Subinterface.Config, ['index', 'name', 'description', 'enabled'], name, value)



                class State(_Entity_):
                    """
                    Operational state data for logical interfaces
                    
                    .. attribute:: index
                    
                    	The index of the subinterface, or logical interface number. On systems with no support for subinterfaces, or not using subinterfaces, this value should default to 0, i.e., the default subinterface
                    	**type**\: int
                    
                    	**range:** 0..4294967295
                    
                    	**config**\: False
                    
                    	**default value**\: 0
                    
                    .. attribute:: name
                    
                    	[adapted from IETF interfaces model (RFC 7223)]  The name of the interface.  A device MAY restrict the allowed values for this leaf, possibly depending on the type of the interface. For system\-controlled interfaces, this leaf is the device\-specific name of the interface.  The 'config false' list interfaces/interface[name]/state contains the currently existing interfaces on the device.  If a client tries to create configuration for a system\-controlled interface that is not present in the corresponding state list, the server MAY reject the request if the implementation does not support pre\-provisioning of interfaces or if the name refers to an interface that can never exist in the system.  A NETCONF server MUST reply with an rpc\-error with the error\-tag 'invalid\-value' in this case.  The IETF model in RFC 7223 provides YANG features for the following (i.e., pre\-provisioning and arbitrary\-names), however they are omitted here\:   If the device supports pre\-provisioning of interface  configuration, the 'pre\-provisioning' feature is  advertised.   If the device allows arbitrarily named user\-controlled  interfaces, the 'arbitrary\-names' feature is advertised.  When a configured user\-controlled interface is created by the system, it is instantiated with the same name in the /interfaces/interface[name]/state list
                    	**type**\: str
                    
                    	**config**\: False
                    
                    .. attribute:: description
                    
                    	[adapted from IETF interfaces model (RFC 7223)]  A textual description of the interface.  A server implementation MAY map this leaf to the ifAlias MIB object.  Such an implementation needs to use some mechanism to handle the differences in size and characters allowed between this leaf and ifAlias.  The definition of such a mechanism is outside the scope of this document.  Since ifAlias is defined to be stored in non\-volatile storage, the MIB implementation MUST map ifAlias to the value of 'description' in the persistently stored datastore.  Specifically, if the device supports '\:startup', when ifAlias is read the device MUST return the value of 'description' in the 'startup' datastore, and when it is written, it MUST be written to the 'running' and 'startup' datastores.  Note that it is up to the implementation to  decide whether to modify this single leaf in 'startup' or perform an implicit copy\-config from 'running' to 'startup'.  If the device does not support '\:startup', ifAlias MUST be mapped to the 'description' leaf in the 'running' datastore
                    	**type**\: str
                    
                    	**config**\: False
                    
                    .. attribute:: enabled
                    
                    	[adapted from IETF interfaces model (RFC 7223)]  This leaf contains the configured, desired state of the interface.  Systems that implement the IF\-MIB use the value of this leaf in the 'running' datastore to set IF\-MIB.ifAdminStatus to 'up' or 'down' after an ifEntry has been initialized, as described in RFC 2863.  Changes in this leaf in the 'running' datastore are reflected in ifAdminStatus, but if ifAdminStatus is changed over SNMP, this leaf is not affected
                    	**type**\: bool
                    
                    	**config**\: False
                    
                    	**default value**\: true
                    
                    .. attribute:: ifindex
                    
                    	System assigned number for each interface.  Corresponds to ifIndex object in SNMP Interface MIB
                    	**type**\: int
                    
                    	**range:** 0..4294967295
                    
                    	**config**\: False
                    
                    .. attribute:: admin_status
                    
                    	[adapted from IETF interfaces model (RFC 7223)]  The desired state of the interface.  In RFC 7223 this leaf has the same read semantics as ifAdminStatus.  Here, it reflects the administrative state as set by enabling or disabling the interface
                    	**type**\:  :py:class:`AdminStatus <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.Subinterfaces.Subinterface.State.AdminStatus>`
                    
                    	**config**\: False
                    
                    .. attribute:: oper_status
                    
                    	[adapted from IETF interfaces model (RFC 7223)]  The current operational state of the interface.  This leaf has the same semantics as ifOperStatus
                    	**type**\:  :py:class:`OperStatus <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.Subinterfaces.Subinterface.State.OperStatus>`
                    
                    	**config**\: False
                    
                    .. attribute:: last_change
                    
                    	Date and time of the last state change of the interface (e.g., up\-to\-down transition).   This corresponds to the ifLastChange object in the standard interface MIB
                    	**type**\: int
                    
                    	**range:** 0..4294967295
                    
                    	**config**\: False
                    
                    .. attribute:: counters
                    
                    	A collection of interface\-related statistics objects
                    	**type**\:  :py:class:`Counters <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.Subinterfaces.Subinterface.State.Counters>`
                    
                    	**config**\: False
                    
                    

                    """

                    _prefix = 'oc-if'
                    _revision = '2016-05-26'

                    def __init__(self):
                        if sys.version_info > (3,):
                            super().__init__()
                        else:
                            super(Interfaces.Interface.Subinterfaces.Subinterface.State, self).__init__()

                        self.yang_name = "state"
                        self.yang_parent_name = "subinterface"
                        self.is_top_level_class = False
                        self.has_list_ancestor = True
                        self.ylist_key_names = []
                        self._child_classes = OrderedDict([("counters", ("counters", Interfaces.Interface.Subinterfaces.Subinterface.State.Counters))])
                        self._leafs = OrderedDict([
                            ('index', (YLeaf(YType.uint32, 'index'), ['int'])),
                            ('name', (YLeaf(YType.str, 'name'), ['str'])),
                            ('description', (YLeaf(YType.str, 'description'), ['str'])),
                            ('enabled', (YLeaf(YType.boolean, 'enabled'), ['bool'])),
                            ('ifindex', (YLeaf(YType.uint32, 'ifindex'), ['int'])),
                            ('admin_status', (YLeaf(YType.enumeration, 'admin-status'), [('ydk.models.ydktest.openconfig_interfaces', 'Interfaces', 'Interface.Subinterfaces.Subinterface.State.AdminStatus')])),
                            ('oper_status', (YLeaf(YType.enumeration, 'oper-status'), [('ydk.models.ydktest.openconfig_interfaces', 'Interfaces', 'Interface.Subinterfaces.Subinterface.State.OperStatus')])),
                            ('last_change', (YLeaf(YType.uint32, 'last-change'), ['int'])),
                        ])
                        self.index = None
                        self.name = None
                        self.description = None
                        self.enabled = None
                        self.ifindex = None
                        self.admin_status = None
                        self.oper_status = None
                        self.last_change = None

                        self.counters = Interfaces.Interface.Subinterfaces.Subinterface.State.Counters()
                        self.counters.parent = self
                        self._children_name_map["counters"] = "counters"
                        self._segment_path = lambda: "state"
                        self._is_frozen = True

                    def __setattr__(self, name, value):
                        self._perform_setattr(Interfaces.Interface.Subinterfaces.Subinterface.State, ['index', 'name', 'description', 'enabled', 'ifindex', 'admin_status', 'oper_status', 'last_change'], name, value)

                    class AdminStatus(Enum):
                        """
                        AdminStatus (Enum Class)

                        [adapted from IETF interfaces model (RFC 7223)]

                        The desired state of the interface.  In RFC 7223 this leaf

                        has the same read semantics as ifAdminStatus.  Here, it

                        reflects the administrative state as set by enabling or

                        disabling the interface.

                        .. data:: UP = 0

                        	Ready to pass packets.

                        .. data:: DOWN = 1

                        	Not ready to pass packets and not in some test mode.

                        .. data:: TESTING = 2

                        	In some test mode.

                        """

                        UP = Enum.YLeaf(0, "UP")

                        DOWN = Enum.YLeaf(1, "DOWN")

                        TESTING = Enum.YLeaf(2, "TESTING")


                    class OperStatus(Enum):
                        """
                        OperStatus (Enum Class)

                        [adapted from IETF interfaces model (RFC 7223)]

                        The current operational state of the interface.

                        This leaf has the same semantics as ifOperStatus.

                        .. data:: UP = 1

                        	Ready to pass packets.

                        .. data:: DOWN = 2

                        	The interface does not pass any packets.

                        .. data:: TESTING = 3

                        	In some test mode.  No operational packets can

                        	be passed.

                        .. data:: UNKNOWN = 4

                        	Status cannot be determined for some reason.

                        .. data:: DORMANT = 5

                        	Waiting for some external event.

                        .. data:: NOT_PRESENT = 6

                        	Some component (typically hardware) is missing.

                        .. data:: LOWER_LAYER_DOWN = 7

                        	Down due to state of lower-layer interface(s).

                        """

                        UP = Enum.YLeaf(1, "UP")

                        DOWN = Enum.YLeaf(2, "DOWN")

                        TESTING = Enum.YLeaf(3, "TESTING")

                        UNKNOWN = Enum.YLeaf(4, "UNKNOWN")

                        DORMANT = Enum.YLeaf(5, "DORMANT")

                        NOT_PRESENT = Enum.YLeaf(6, "NOT_PRESENT")

                        LOWER_LAYER_DOWN = Enum.YLeaf(7, "LOWER_LAYER_DOWN")



                    class Counters(_Entity_):
                        """
                        A collection of interface\-related statistics objects.
                        
                        .. attribute:: in_octets
                        
                        	[adapted from IETF interfaces model (RFC 7223)]  The total number of octets received on the interface, including framing characters.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                        	**type**\: int
                        
                        	**range:** 0..18446744073709551615
                        
                        	**config**\: False
                        
                        .. attribute:: in_unicast_pkts
                        
                        	[adapted from IETF interfaces model (RFC 7223)]  The number of packets, delivered by this sub\-layer to a higher (sub\-)layer, that were not addressed to a multicast or broadcast address at this sub\-layer.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                        	**type**\: int
                        
                        	**range:** 0..18446744073709551615
                        
                        	**config**\: False
                        
                        .. attribute:: in_broadcast_pkts
                        
                        	[adapted from IETF interfaces model (RFC 7223)]  The number of packets, delivered by this sub\-layer to a higher (sub\-)layer, that were addressed to a broadcast address at this sub\-layer.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                        	**type**\: int
                        
                        	**range:** 0..18446744073709551615
                        
                        	**config**\: False
                        
                        .. attribute:: in_multicast_pkts
                        
                        	[adapted from IETF interfaces model (RFC 7223)]   The number of packets, delivered by this sub\-layer to a higher (sub\-)layer, that were addressed to a multicast address at this sub\-layer.  For a MAC\-layer protocol, this includes both Group and Functional addresses.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                        	**type**\: int
                        
                        	**range:** 0..18446744073709551615
                        
                        	**config**\: False
                        
                        .. attribute:: in_discards
                        
                        	[adapted from IETF interfaces model (RFC 7223)] Changed the counter type to counter64.  The number of inbound packets that were chosen to be discarded even though no errors had been detected to prevent their being deliverable to a higher\-layer protocol.  One possible reason for discarding such a packet could be to free up buffer space.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                        	**type**\: int
                        
                        	**range:** 0..18446744073709551615
                        
                        	**config**\: False
                        
                        .. attribute:: in_errors
                        
                        	[adapted from IETF interfaces model (RFC 7223)] Changed the counter type to counter64.  For packet\-oriented interfaces, the number of inbound packets that contained errors preventing them from being deliverable to a higher\-layer protocol.  For character\- oriented or fixed\-length interfaces, the number of inbound transmission units that contained errors preventing them from being deliverable to a higher\-layer protocol.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                        	**type**\: int
                        
                        	**range:** 0..18446744073709551615
                        
                        	**config**\: False
                        
                        .. attribute:: in_unknown_protos
                        
                        	[adapted from IETF interfaces model (RFC 7223)] Changed the counter type to counter64.  For packet\-oriented interfaces, the number of packets received via the interface that were discarded because of an unknown or unsupported protocol.  For character\-oriented or fixed\-length interfaces that support protocol multiplexing, the number of transmission units received via the interface that were discarded because of an unknown or unsupported protocol. For any interface that does not support protocol multiplexing, this counter is not present.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                        	**type**\: int
                        
                        	**range:** 0..4294967295
                        
                        	**config**\: False
                        
                        .. attribute:: out_octets
                        
                        	[adapted from IETF interfaces model (RFC 7223)] Changed the counter type to counter64.  The total number of octets transmitted out of the interface, including framing characters.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                        	**type**\: int
                        
                        	**range:** 0..18446744073709551615
                        
                        	**config**\: False
                        
                        .. attribute:: out_unicast_pkts
                        
                        	[adapted from IETF interfaces model (RFC 7223)]  The total number of packets that higher\-level protocols requested be transmitted, and that were not addressed to a multicast or broadcast address at this sub\-layer, including those that were discarded or not sent.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                        	**type**\: int
                        
                        	**range:** 0..18446744073709551615
                        
                        	**config**\: False
                        
                        .. attribute:: out_broadcast_pkts
                        
                        	[adapted from IETF interfaces model (RFC 7223)]  The total number of packets that higher\-level protocols requested be transmitted, and that were addressed to a broadcast address at this sub\-layer, including those that were discarded or not sent.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                        	**type**\: int
                        
                        	**range:** 0..18446744073709551615
                        
                        	**config**\: False
                        
                        .. attribute:: out_multicast_pkts
                        
                        	[adapted from IETF interfaces model (RFC 7223)] Changed the counter type to counter64.  The total number of packets that higher\-level protocols requested be transmitted, and that were addressed to a multicast address at this sub\-layer, including those that were discarded or not sent.  For a MAC\-layer protocol, this includes both Group and Functional addresses.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                        	**type**\: int
                        
                        	**range:** 0..18446744073709551615
                        
                        	**config**\: False
                        
                        .. attribute:: out_discards
                        
                        	[adapted from IETF interfaces model (RFC 7223)] Changed the counter type to counter64.  The number of outbound packets that were chosen to be discarded even though no errors had been detected to prevent their being transmitted.  One possible reason for discarding such a packet could be to free up buffer space.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                        	**type**\: int
                        
                        	**range:** 0..18446744073709551615
                        
                        	**config**\: False
                        
                        .. attribute:: out_errors
                        
                        	[adapted from IETF interfaces model (RFC 7223)] Changed the counter type to counter64.  For packet\-oriented interfaces, the number of outbound packets that could not be transmitted because of errors. For character\-oriented or fixed\-length interfaces, the number of outbound transmission units that could not be transmitted because of errors.  Discontinuities in the value of this counter can occur at re\-initialization of the management system, and at other times as indicated by the value of 'discontinuity\-time'
                        	**type**\: int
                        
                        	**range:** 0..18446744073709551615
                        
                        	**config**\: False
                        
                        .. attribute:: last_clear
                        
                        	Indicates the last time the interface counters were cleared
                        	**type**\: str
                        
                        	**pattern:** \\d{4}\-\\d{2}\-\\d{2}T\\d{2}\:\\d{2}\:\\d{2}(\\.\\d+)?(Z\|[\\+\\\-]\\d{2}\:\\d{2})
                        
                        	**config**\: False
                        
                        

                        """

                        _prefix = 'oc-if'
                        _revision = '2016-05-26'

                        def __init__(self):
                            if sys.version_info > (3,):
                                super().__init__()
                            else:
                                super(Interfaces.Interface.Subinterfaces.Subinterface.State.Counters, self).__init__()

                            self.yang_name = "counters"
                            self.yang_parent_name = "state"
                            self.is_top_level_class = False
                            self.has_list_ancestor = True
                            self.ylist_key_names = []
                            self._child_classes = OrderedDict([])
                            self._leafs = OrderedDict([
                                ('in_octets', (YLeaf(YType.uint64, 'in-octets'), ['int'])),
                                ('in_unicast_pkts', (YLeaf(YType.uint64, 'in-unicast-pkts'), ['int'])),
                                ('in_broadcast_pkts', (YLeaf(YType.uint64, 'in-broadcast-pkts'), ['int'])),
                                ('in_multicast_pkts', (YLeaf(YType.uint64, 'in-multicast-pkts'), ['int'])),
                                ('in_discards', (YLeaf(YType.uint64, 'in-discards'), ['int'])),
                                ('in_errors', (YLeaf(YType.uint64, 'in-errors'), ['int'])),
                                ('in_unknown_protos', (YLeaf(YType.uint32, 'in-unknown-protos'), ['int'])),
                                ('out_octets', (YLeaf(YType.uint64, 'out-octets'), ['int'])),
                                ('out_unicast_pkts', (YLeaf(YType.uint64, 'out-unicast-pkts'), ['int'])),
                                ('out_broadcast_pkts', (YLeaf(YType.uint64, 'out-broadcast-pkts'), ['int'])),
                                ('out_multicast_pkts', (YLeaf(YType.uint64, 'out-multicast-pkts'), ['int'])),
                                ('out_discards', (YLeaf(YType.uint64, 'out-discards'), ['int'])),
                                ('out_errors', (YLeaf(YType.uint64, 'out-errors'), ['int'])),
                                ('last_clear', (YLeaf(YType.str, 'last-clear'), ['str'])),
                            ])
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
                            self.last_clear = None
                            self._segment_path = lambda: "counters"
                            self._is_frozen = True

                        def __setattr__(self, name, value):
                            self._perform_setattr(Interfaces.Interface.Subinterfaces.Subinterface.State.Counters, ['in_octets', 'in_unicast_pkts', 'in_broadcast_pkts', 'in_multicast_pkts', 'in_discards', 'in_errors', 'in_unknown_protos', 'out_octets', 'out_unicast_pkts', 'out_broadcast_pkts', 'out_multicast_pkts', 'out_discards', 'out_errors', 'last_clear'], name, value)






        class Ethernet(_Entity_):
            """
            Top\-level container for ethernet configuration
            and state
            
            .. attribute:: config
            
            	Configuration data for ethernet interfaces
            	**type**\:  :py:class:`Config <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.Ethernet.Config>`
            
            .. attribute:: state
            
            	State variables for Ethernet interfaces
            	**type**\:  :py:class:`State <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.Ethernet.State>`
            
            	**config**\: False
            
            

            """

            _prefix = 'oc-eth'
            _revision = '2016-05-26'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Interfaces.Interface.Ethernet, self).__init__()

                self.yang_name = "ethernet"
                self.yang_parent_name = "interface"
                self.is_top_level_class = False
                self.has_list_ancestor = True
                self.ylist_key_names = []
                self._child_classes = OrderedDict([("config", ("config", Interfaces.Interface.Ethernet.Config)), ("state", ("state", Interfaces.Interface.Ethernet.State))])
                self._leafs = OrderedDict()

                self.config = Interfaces.Interface.Ethernet.Config()
                self.config.parent = self
                self._children_name_map["config"] = "config"

                self.state = Interfaces.Interface.Ethernet.State()
                self.state.parent = self
                self._children_name_map["state"] = "state"
                self._segment_path = lambda: "openconfig-if-ethernet:ethernet"
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Interfaces.Interface.Ethernet, [], name, value)


            class Config(_Entity_):
                """
                Configuration data for ethernet interfaces
                
                .. attribute:: mac_address
                
                	Assigns a MAC address to the Ethernet interface.  If not specified, the corresponding operational state leaf is expected to show the system\-assigned MAC address
                	**type**\: str
                
                	**pattern:** [0\-9a\-fA\-F]{2}(\:[0\-9a\-fA\-F]{2}){5}
                
                .. attribute:: auto_negotiate
                
                	Set to TRUE to request the interface to auto\-negotiate transmission parameters with its peer interface.  When set to FALSE, the transmission parameters are specified manually
                	**type**\: bool
                
                	**default value**\: true
                
                .. attribute:: duplex_mode
                
                	When auto\-negotiate is TRUE, this optionally sets the duplex mode that will be advertised to the peer.  If unspecified, the interface should negotiate the duplex mode directly (typically full\-duplex).  When auto\-negotiate is FALSE, this sets the duplex mode on the interface directly
                	**type**\:  :py:class:`DuplexMode <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.Ethernet.Config.DuplexMode>`
                
                .. attribute:: port_speed
                
                	When auto\-negotiate is TRUE, this optionally sets the port\-speed mode that will be advertised to the peer for negotiation.  If unspecified, it is expected that the interface will select the highest speed available based on negotiation.  When auto\-negotiate is set to FALSE, sets the link speed to a fixed value \-\- supported values are defined by ETHERNET\_SPEED identities
                	**type**\:  :py:class:`ETHERNETSPEED <ydk.models.ydktest.openconfig_if_ethernet.ETHERNETSPEED>`
                
                .. attribute:: enable_flow_control
                
                	Enable or disable flow control for this interface. Ethernet flow control is a mechanism by which a receiver may send PAUSE frames to a sender to stop transmission for a specified time.  This setting should override auto\-negotiated flow control settings.  If left unspecified, and auto\-negotiate is TRUE, flow control mode is negotiated with the peer interface
                	**type**\: bool
                
                	**default value**\: false
                
                

                """

                _prefix = 'oc-eth'
                _revision = '2016-05-26'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Interfaces.Interface.Ethernet.Config, self).__init__()

                    self.yang_name = "config"
                    self.yang_parent_name = "ethernet"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('mac_address', (YLeaf(YType.str, 'mac-address'), ['str'])),
                        ('auto_negotiate', (YLeaf(YType.boolean, 'auto-negotiate'), ['bool'])),
                        ('duplex_mode', (YLeaf(YType.enumeration, 'duplex-mode'), [('ydk.models.ydktest.openconfig_interfaces', 'Interfaces', 'Interface.Ethernet.Config.DuplexMode')])),
                        ('port_speed', (YLeaf(YType.identityref, 'port-speed'), [('ydk.models.ydktest.openconfig_if_ethernet', 'ETHERNETSPEED')])),
                        ('enable_flow_control', (YLeaf(YType.boolean, 'enable-flow-control'), ['bool'])),
                    ])
                    self.mac_address = None
                    self.auto_negotiate = None
                    self.duplex_mode = None
                    self.port_speed = None
                    self.enable_flow_control = None
                    self._segment_path = lambda: "config"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Interfaces.Interface.Ethernet.Config, ['mac_address', 'auto_negotiate', 'duplex_mode', 'port_speed', 'enable_flow_control'], name, value)

                class DuplexMode(Enum):
                    """
                    DuplexMode (Enum Class)

                    When auto\-negotiate is TRUE, this optionally sets the

                    duplex mode that will be advertised to the peer.  If

                    unspecified, the interface should negotiate the duplex mode

                    directly (typically full\-duplex).  When auto\-negotiate is

                    FALSE, this sets the duplex mode on the interface directly.

                    .. data:: FULL = 0

                    	Full duplex mode

                    .. data:: HALF = 1

                    	Half duplex mode

                    """

                    FULL = Enum.YLeaf(0, "FULL")

                    HALF = Enum.YLeaf(1, "HALF")




            class State(_Entity_):
                """
                State variables for Ethernet interfaces
                
                .. attribute:: mac_address
                
                	Assigns a MAC address to the Ethernet interface.  If not specified, the corresponding operational state leaf is expected to show the system\-assigned MAC address
                	**type**\: str
                
                	**pattern:** [0\-9a\-fA\-F]{2}(\:[0\-9a\-fA\-F]{2}){5}
                
                	**config**\: False
                
                .. attribute:: auto_negotiate
                
                	Set to TRUE to request the interface to auto\-negotiate transmission parameters with its peer interface.  When set to FALSE, the transmission parameters are specified manually
                	**type**\: bool
                
                	**config**\: False
                
                	**default value**\: true
                
                .. attribute:: duplex_mode
                
                	When auto\-negotiate is TRUE, this optionally sets the duplex mode that will be advertised to the peer.  If unspecified, the interface should negotiate the duplex mode directly (typically full\-duplex).  When auto\-negotiate is FALSE, this sets the duplex mode on the interface directly
                	**type**\:  :py:class:`DuplexMode <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.Ethernet.State.DuplexMode>`
                
                	**config**\: False
                
                .. attribute:: port_speed
                
                	When auto\-negotiate is TRUE, this optionally sets the port\-speed mode that will be advertised to the peer for negotiation.  If unspecified, it is expected that the interface will select the highest speed available based on negotiation.  When auto\-negotiate is set to FALSE, sets the link speed to a fixed value \-\- supported values are defined by ETHERNET\_SPEED identities
                	**type**\:  :py:class:`ETHERNETSPEED <ydk.models.ydktest.openconfig_if_ethernet.ETHERNETSPEED>`
                
                	**config**\: False
                
                .. attribute:: enable_flow_control
                
                	Enable or disable flow control for this interface. Ethernet flow control is a mechanism by which a receiver may send PAUSE frames to a sender to stop transmission for a specified time.  This setting should override auto\-negotiated flow control settings.  If left unspecified, and auto\-negotiate is TRUE, flow control mode is negotiated with the peer interface
                	**type**\: bool
                
                	**config**\: False
                
                	**default value**\: false
                
                .. attribute:: hw_mac_address
                
                	Represenets the 'burned\-in',  or system\-assigned, MAC address for the Ethernet interface
                	**type**\: str
                
                	**pattern:** [0\-9a\-fA\-F]{2}(\:[0\-9a\-fA\-F]{2}){5}
                
                	**config**\: False
                
                .. attribute:: effective_speed
                
                	Reports the effective speed of the interface, e.g., the negotiated speed if auto\-negotiate is enabled
                	**type**\: int
                
                	**range:** 0..4294967295
                
                	**config**\: False
                
                	**units**\: Mbps
                
                .. attribute:: counters
                
                	Ethernet interface counters
                	**type**\:  :py:class:`Counters <ydk.models.ydktest.openconfig_interfaces.Interfaces.Interface.Ethernet.State.Counters>`
                
                	**config**\: False
                
                

                """

                _prefix = 'oc-eth'
                _revision = '2016-05-26'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Interfaces.Interface.Ethernet.State, self).__init__()

                    self.yang_name = "state"
                    self.yang_parent_name = "ethernet"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([("counters", ("counters", Interfaces.Interface.Ethernet.State.Counters))])
                    self._leafs = OrderedDict([
                        ('mac_address', (YLeaf(YType.str, 'mac-address'), ['str'])),
                        ('auto_negotiate', (YLeaf(YType.boolean, 'auto-negotiate'), ['bool'])),
                        ('duplex_mode', (YLeaf(YType.enumeration, 'duplex-mode'), [('ydk.models.ydktest.openconfig_interfaces', 'Interfaces', 'Interface.Ethernet.State.DuplexMode')])),
                        ('port_speed', (YLeaf(YType.identityref, 'port-speed'), [('ydk.models.ydktest.openconfig_if_ethernet', 'ETHERNETSPEED')])),
                        ('enable_flow_control', (YLeaf(YType.boolean, 'enable-flow-control'), ['bool'])),
                        ('hw_mac_address', (YLeaf(YType.str, 'hw-mac-address'), ['str'])),
                        ('effective_speed', (YLeaf(YType.uint32, 'effective-speed'), ['int'])),
                    ])
                    self.mac_address = None
                    self.auto_negotiate = None
                    self.duplex_mode = None
                    self.port_speed = None
                    self.enable_flow_control = None
                    self.hw_mac_address = None
                    self.effective_speed = None

                    self.counters = Interfaces.Interface.Ethernet.State.Counters()
                    self.counters.parent = self
                    self._children_name_map["counters"] = "counters"
                    self._segment_path = lambda: "state"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Interfaces.Interface.Ethernet.State, ['mac_address', 'auto_negotiate', 'duplex_mode', 'port_speed', 'enable_flow_control', 'hw_mac_address', 'effective_speed'], name, value)

                class DuplexMode(Enum):
                    """
                    DuplexMode (Enum Class)

                    When auto\-negotiate is TRUE, this optionally sets the

                    duplex mode that will be advertised to the peer.  If

                    unspecified, the interface should negotiate the duplex mode

                    directly (typically full\-duplex).  When auto\-negotiate is

                    FALSE, this sets the duplex mode on the interface directly.

                    .. data:: FULL = 0

                    	Full duplex mode

                    .. data:: HALF = 1

                    	Half duplex mode

                    """

                    FULL = Enum.YLeaf(0, "FULL")

                    HALF = Enum.YLeaf(1, "HALF")



                class Counters(_Entity_):
                    """
                    Ethernet interface counters
                    
                    .. attribute:: in_mac_control_frames
                    
                    	MAC layer control frames received on the interface
                    	**type**\: int
                    
                    	**range:** 0..18446744073709551615
                    
                    	**config**\: False
                    
                    .. attribute:: in_mac_pause_frames
                    
                    	MAC layer PAUSE frames received on the interface
                    	**type**\: int
                    
                    	**range:** 0..18446744073709551615
                    
                    	**config**\: False
                    
                    .. attribute:: in_oversize_frames
                    
                    	Number of oversize frames received on the interface
                    	**type**\: int
                    
                    	**range:** 0..18446744073709551615
                    
                    	**config**\: False
                    
                    .. attribute:: in_jabber_frames
                    
                    	Number of jabber frames received on the interface.  Jabber frames are typically defined as oversize frames which also have a bad CRC.  Implementations may use slightly different definitions of what constitutes a jabber frame.  Often indicative of a NIC hardware problem
                    	**type**\: int
                    
                    	**range:** 0..18446744073709551615
                    
                    	**config**\: False
                    
                    .. attribute:: in_fragment_frames
                    
                    	Number of fragment frames received on the interface
                    	**type**\: int
                    
                    	**range:** 0..18446744073709551615
                    
                    	**config**\: False
                    
                    .. attribute:: in_8021q_frames
                    
                    	Number of 802.1q tagged frames received on the interface
                    	**type**\: int
                    
                    	**range:** 0..18446744073709551615
                    
                    	**config**\: False
                    
                    .. attribute:: in_crc_errors
                    
                    	Number of receive error events due to FCS/CRC check failure
                    	**type**\: int
                    
                    	**range:** 0..18446744073709551615
                    
                    	**config**\: False
                    
                    .. attribute:: out_mac_control_frames
                    
                    	MAC layer control frames sent on the interface
                    	**type**\: int
                    
                    	**range:** 0..18446744073709551615
                    
                    	**config**\: False
                    
                    .. attribute:: out_mac_pause_frames
                    
                    	MAC layer PAUSE frames sent on the interface
                    	**type**\: int
                    
                    	**range:** 0..18446744073709551615
                    
                    	**config**\: False
                    
                    .. attribute:: out_8021q_frames
                    
                    	Number of 802.1q tagged frames sent on the interface
                    	**type**\: int
                    
                    	**range:** 0..18446744073709551615
                    
                    	**config**\: False
                    
                    

                    """

                    _prefix = 'oc-eth'
                    _revision = '2016-05-26'

                    def __init__(self):
                        if sys.version_info > (3,):
                            super().__init__()
                        else:
                            super(Interfaces.Interface.Ethernet.State.Counters, self).__init__()

                        self.yang_name = "counters"
                        self.yang_parent_name = "state"
                        self.is_top_level_class = False
                        self.has_list_ancestor = True
                        self.ylist_key_names = []
                        self._child_classes = OrderedDict([])
                        self._leafs = OrderedDict([
                            ('in_mac_control_frames', (YLeaf(YType.uint64, 'in-mac-control-frames'), ['int'])),
                            ('in_mac_pause_frames', (YLeaf(YType.uint64, 'in-mac-pause-frames'), ['int'])),
                            ('in_oversize_frames', (YLeaf(YType.uint64, 'in-oversize-frames'), ['int'])),
                            ('in_jabber_frames', (YLeaf(YType.uint64, 'in-jabber-frames'), ['int'])),
                            ('in_fragment_frames', (YLeaf(YType.uint64, 'in-fragment-frames'), ['int'])),
                            ('in_8021q_frames', (YLeaf(YType.uint64, 'in-8021q-frames'), ['int'])),
                            ('in_crc_errors', (YLeaf(YType.uint64, 'in-crc-errors'), ['int'])),
                            ('out_mac_control_frames', (YLeaf(YType.uint64, 'out-mac-control-frames'), ['int'])),
                            ('out_mac_pause_frames', (YLeaf(YType.uint64, 'out-mac-pause-frames'), ['int'])),
                            ('out_8021q_frames', (YLeaf(YType.uint64, 'out-8021q-frames'), ['int'])),
                        ])
                        self.in_mac_control_frames = None
                        self.in_mac_pause_frames = None
                        self.in_oversize_frames = None
                        self.in_jabber_frames = None
                        self.in_fragment_frames = None
                        self.in_8021q_frames = None
                        self.in_crc_errors = None
                        self.out_mac_control_frames = None
                        self.out_mac_pause_frames = None
                        self.out_8021q_frames = None
                        self._segment_path = lambda: "counters"
                        self._is_frozen = True

                    def __setattr__(self, name, value):
                        self._perform_setattr(Interfaces.Interface.Ethernet.State.Counters, ['in_mac_control_frames', 'in_mac_pause_frames', 'in_oversize_frames', 'in_jabber_frames', 'in_fragment_frames', 'in_8021q_frames', 'in_crc_errors', 'out_mac_control_frames', 'out_mac_pause_frames', 'out_8021q_frames'], name, value)





    def clone_ptr(self):
        self._top_entity = Interfaces()
        return self._top_entity



