""" ietf_system 

This module contains a collection of YANG definitions for the
configuration and identification of some common system
properties within a device containing a NETCONF server.  This
includes data node definitions for system identification,
time\-of\-day management, user management, DNS resolver
configuration, and some protocol operations for system
management.

Copyright (c) 2014 IETF Trust and the persons identified as
authors of the code.  All rights reserved.

Redistribution and use in source and binary forms, with or
without modification, is permitted pursuant to, and subject
to the license terms contained in, the Simplified BSD License
set forth in Section 4.c of the IETF Trust's Legal Provisions
Relating to IETF Documents
(http\://trustee.ietf.org/license\-info).

This version of this YANG module is part of RFC 7317; see
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




class AuthenticationMethod(Identity):
    """
    Base identity for user authentication methods.
    
    

    """

    _prefix = 'sys'
    _revision = '2014-08-06'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:ietf-system", pref="ietf-system", tag="ietf-system:authentication-method"):
        if sys.version_info > (3,):
            super().__init__(ns, pref, tag)
        else:
            super(AuthenticationMethod, self).__init__(ns, pref, tag)



class RadiusAuthenticationType(Identity):
    """
    Base identity for RADIUS authentication types.
    
    

    """

    _prefix = 'sys'
    _revision = '2014-08-06'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:ietf-system", pref="ietf-system", tag="ietf-system:radius-authentication-type"):
        if sys.version_info > (3,):
            super().__init__(ns, pref, tag)
        else:
            super(RadiusAuthenticationType, self).__init__(ns, pref, tag)



class System(_Entity_):
    """
    System group configuration.
    
    .. attribute:: contact
    
    	The administrator contact information for the system.  A server implementation MAY map this leaf to the sysContact MIB object.  Such an implementation needs to use some mechanism to handle the differences in size and characters allowed between this leaf and sysContact.  The definition of such a mechanism is outside the scope of this document
    	**type**\: str
    
    .. attribute:: hostname
    
    	The name of the host.  This name can be a single domain label or the fully qualified domain name of the host
    	**type**\: str
    
    	**pattern:** ((([a\-zA\-Z0\-9\_]([a\-zA\-Z0\-9\\\-\_]){0,61})?[a\-zA\-Z0\-9]\\.)\*([a\-zA\-Z0\-9\_]([a\-zA\-Z0\-9\\\-\_]){0,61})?[a\-zA\-Z0\-9]\\.?)\|\\.
    
    .. attribute:: location
    
    	The system location.  A server implementation MAY map this leaf to the sysLocation MIB object.  Such an implementation needs to use some mechanism to handle the differences in size and characters allowed between this leaf and sysLocation.  The definition of such a mechanism is outside the scope of this document
    	**type**\: str
    
    .. attribute:: clock
    
    	Configuration of the system date and time properties
    	**type**\:  :py:class:`Clock <ydk.models.ydktest.ietf_system.System.Clock>`
    
    .. attribute:: ntp
    
    	Configuration of the NTP client
    	**type**\:  :py:class:`Ntp <ydk.models.ydktest.ietf_system.System.Ntp>`
    
    	**presence node**\: True
    
    .. attribute:: dns_resolver
    
    	Configuration of the DNS resolver
    	**type**\:  :py:class:`DnsResolver <ydk.models.ydktest.ietf_system.System.DnsResolver>`
    
    .. attribute:: radius
    
    	Configuration of the RADIUS client
    	**type**\:  :py:class:`Radius <ydk.models.ydktest.ietf_system.System.Radius>`
    
    .. attribute:: authentication
    
    	The authentication configuration subtree
    	**type**\:  :py:class:`Authentication <ydk.models.ydktest.ietf_system.System.Authentication>`
    
    

    """

    _prefix = 'sys'
    _revision = '2014-08-06'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(System, self).__init__()
        self._top_entity = None

        self.yang_name = "system"
        self.yang_parent_name = "ietf-system"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([("clock", ("clock", System.Clock)), ("ntp", ("ntp", System.Ntp)), ("dns-resolver", ("dns_resolver", System.DnsResolver)), ("radius", ("radius", System.Radius)), ("authentication", ("authentication", System.Authentication))])
        self._leafs = OrderedDict([
            ('contact', (YLeaf(YType.str, 'contact'), ['str'])),
            ('hostname', (YLeaf(YType.str, 'hostname'), ['str'])),
            ('location', (YLeaf(YType.str, 'location'), ['str'])),
        ])
        self.contact = None
        self.hostname = None
        self.location = None

        self.clock = System.Clock()
        self.clock.parent = self
        self._children_name_map["clock"] = "clock"

        self.ntp = None
        self._children_name_map["ntp"] = "ntp"

        self.dns_resolver = System.DnsResolver()
        self.dns_resolver.parent = self
        self._children_name_map["dns_resolver"] = "dns-resolver"

        self.radius = System.Radius()
        self.radius.parent = self
        self._children_name_map["radius"] = "radius"

        self.authentication = System.Authentication()
        self.authentication.parent = self
        self._children_name_map["authentication"] = "authentication"
        self._segment_path = lambda: "ietf-system:system"
        self._is_frozen = True

    def __setattr__(self, name, value):
        self._perform_setattr(System, ['contact', 'hostname', 'location'], name, value)


    class Clock(_Entity_):
        """
        Configuration of the system date and time properties.
        
        .. attribute:: timezone_name
        
        	The TZ database name to use for the system, such as 'Europe/Stockholm'
        	**type**\: str
        
        .. attribute:: timezone_utc_offset
        
        	The number of minutes to add to UTC time to identify the time zone for this system.  For example, 'UTC \- 8\:00 hours' would be represented as '\-480'. Note that automatic daylight saving time adjustment is not provided if this object is used
        	**type**\: int
        
        	**range:** \-1500..1500
        
        	**units**\: minutes
        
        

        """

        _prefix = 'sys'
        _revision = '2014-08-06'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(System.Clock, self).__init__()

            self.yang_name = "clock"
            self.yang_parent_name = "system"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('timezone_name', (YLeaf(YType.str, 'timezone-name'), ['str'])),
                ('timezone_utc_offset', (YLeaf(YType.int16, 'timezone-utc-offset'), ['int'])),
            ])
            self.timezone_name = None
            self.timezone_utc_offset = None
            self._segment_path = lambda: "clock"
            self._absolute_path = lambda: "ietf-system:system/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(System.Clock, ['timezone_name', 'timezone_utc_offset'], name, value)



    class Ntp(_Entity_):
        """
        Configuration of the NTP client.
        
        .. attribute:: enabled
        
        	Indicates that the system should attempt to synchronize the system clock with an NTP server from the 'ntp/server' list
        	**type**\: bool
        
        	**default value**\: true
        
        .. attribute:: server
        
        	List of NTP servers to use for system clock synchronization.  If '/system/ntp/enabled' is 'true', then the system will attempt to contact and utilize the specified NTP servers
        	**type**\: list of  		 :py:class:`Server <ydk.models.ydktest.ietf_system.System.Ntp.Server>`
        
        

        This class is a :ref:`presence class<presence-class>`

        """

        _prefix = 'sys'
        _revision = '2014-08-06'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(System.Ntp, self).__init__()

            self.yang_name = "ntp"
            self.yang_parent_name = "system"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("server", ("server", System.Ntp.Server))])
            self.is_presence_container = True
            self._leafs = OrderedDict([
                ('enabled', (YLeaf(YType.boolean, 'enabled'), ['bool'])),
            ])
            self.enabled = None

            self.server = YList(self)
            self._segment_path = lambda: "ntp"
            self._absolute_path = lambda: "ietf-system:system/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(System.Ntp, ['enabled'], name, value)


        class Server(_Entity_):
            """
            List of NTP servers to use for system clock
            synchronization.  If '/system/ntp/enabled'
            is 'true', then the system will attempt to
            contact and utilize the specified NTP servers.
            
            .. attribute:: name  (key)
            
            	An arbitrary name for the NTP server
            	**type**\: str
            
            .. attribute:: udp
            
            	Contains UDP\-specific configuration parameters for NTP
            	**type**\:  :py:class:`Udp <ydk.models.ydktest.ietf_system.System.Ntp.Server.Udp>`
            
            .. attribute:: association_type
            
            	The desired association type for this NTP server
            	**type**\:  :py:class:`AssociationType <ydk.models.ydktest.ietf_system.System.Ntp.Server.AssociationType>`
            
            	**default value**\: server
            
            .. attribute:: iburst
            
            	Indicates whether this server should enable burst synchronization or not
            	**type**\: bool
            
            	**default value**\: false
            
            .. attribute:: prefer
            
            	Indicates whether this server should be preferred or not
            	**type**\: bool
            
            	**default value**\: false
            
            

            """

            _prefix = 'sys'
            _revision = '2014-08-06'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(System.Ntp.Server, self).__init__()

                self.yang_name = "server"
                self.yang_parent_name = "ntp"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = ['name']
                self._child_classes = OrderedDict([("udp", ("udp", System.Ntp.Server.Udp))])
                self._leafs = OrderedDict([
                    ('name', (YLeaf(YType.str, 'name'), ['str'])),
                    ('association_type', (YLeaf(YType.enumeration, 'association-type'), [('ydk.models.ydktest.ietf_system', 'System', 'Ntp.Server.AssociationType')])),
                    ('iburst', (YLeaf(YType.boolean, 'iburst'), ['bool'])),
                    ('prefer', (YLeaf(YType.boolean, 'prefer'), ['bool'])),
                ])
                self.name = None
                self.association_type = None
                self.iburst = None
                self.prefer = None

                self.udp = System.Ntp.Server.Udp()
                self.udp.parent = self
                self._children_name_map["udp"] = "udp"
                self._segment_path = lambda: "server" + "[name='" + str(self.name) + "']"
                self._absolute_path = lambda: "ietf-system:system/ntp/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(System.Ntp.Server, ['name', 'association_type', 'iburst', 'prefer'], name, value)

            class AssociationType(Enum):
                """
                AssociationType (Enum Class)

                The desired association type for this NTP server.

                .. data:: server = 0

                	Use client association mode.  This device

                	will not provide synchronization to the

                	configured NTP server.

                .. data:: peer = 1

                	Use symmetric active association mode.

                	This device may provide synchronization

                	to the configured NTP server.

                .. data:: pool = 2

                	Use client association mode with one or

                	more of the NTP servers found by DNS

                	resolution of the domain name given by

                	the 'address' leaf.  This device will not

                	provide synchronization to the servers.

                """

                server = Enum.YLeaf(0, "server")

                peer = Enum.YLeaf(1, "peer")

                pool = Enum.YLeaf(2, "pool")



            class Udp(_Entity_):
                """
                Contains UDP\-specific configuration parameters
                for NTP.
                
                .. attribute:: address
                
                	The address of the NTP server
                	**type**\: union of the below types:
                
                		**type**\: str
                
                			**pattern:** (([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])\\.){3}([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])(%[\\p{N}\\p{L}]+)?
                
                		**type**\: str
                
                			**pattern:** ((\:\|[0\-9a\-fA\-F]{0,4})\:)([0\-9a\-fA\-F]{0,4}\:){0,5}((([0\-9a\-fA\-F]{0,4}\:)?(\:\|[0\-9a\-fA\-F]{0,4}))\|(((25[0\-5]\|2[0\-4][0\-9]\|[01]?[0\-9]?[0\-9])\\.){3}(25[0\-5]\|2[0\-4][0\-9]\|[01]?[0\-9]?[0\-9])))(%[\\p{N}\\p{L}]+)?
                
                		**type**\: str
                
                			**pattern:** ((([a\-zA\-Z0\-9\_]([a\-zA\-Z0\-9\\\-\_]){0,61})?[a\-zA\-Z0\-9]\\.)\*([a\-zA\-Z0\-9\_]([a\-zA\-Z0\-9\\\-\_]){0,61})?[a\-zA\-Z0\-9]\\.?)\|\\.
                
                	**mandatory**\: True
                
                .. attribute:: port
                
                	The port number of the NTP server
                	**type**\: int
                
                	**range:** 0..65535
                
                	**default value**\: 123
                
                

                """

                _prefix = 'sys'
                _revision = '2014-08-06'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(System.Ntp.Server.Udp, self).__init__()

                    self.yang_name = "udp"
                    self.yang_parent_name = "server"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('address', (YLeaf(YType.str, 'address'), ['str','str','str'])),
                        ('port', (YLeaf(YType.uint16, 'port'), ['int'])),
                    ])
                    self.address = None
                    self.port = None
                    self._segment_path = lambda: "udp"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(System.Ntp.Server.Udp, ['address', 'port'], name, value)





    class DnsResolver(_Entity_):
        """
        Configuration of the DNS resolver.
        
        .. attribute:: search
        
        	An ordered list of domains to search when resolving a host name
        	**type**\: list of str
        
        	**pattern:** ((([a\-zA\-Z0\-9\_]([a\-zA\-Z0\-9\\\-\_]){0,61})?[a\-zA\-Z0\-9]\\.)\*([a\-zA\-Z0\-9\_]([a\-zA\-Z0\-9\\\-\_]){0,61})?[a\-zA\-Z0\-9]\\.?)\|\\.
        
        .. attribute:: server
        
        	List of the DNS servers that the resolver should query.  When the resolver is invoked by a calling application, it sends the query to the first name server in this list.  If no response has been received within 'timeout' seconds, the resolver continues with the next server in the list. If no response is received from any server, the resolver continues with the first server again.  When the resolver has traversed the list 'attempts' times without receiving any response, it gives up and returns an error to the calling application.  Implementations MAY limit the number of entries in this list
        	**type**\: list of  		 :py:class:`Server <ydk.models.ydktest.ietf_system.System.DnsResolver.Server>`
        
        .. attribute:: options
        
        	Resolver options.  The set of available options has been limited to those that are generally available across different resolver implementations and generally useful
        	**type**\:  :py:class:`Options <ydk.models.ydktest.ietf_system.System.DnsResolver.Options>`
        
        

        """

        _prefix = 'sys'
        _revision = '2014-08-06'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(System.DnsResolver, self).__init__()

            self.yang_name = "dns-resolver"
            self.yang_parent_name = "system"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("server", ("server", System.DnsResolver.Server)), ("options", ("options", System.DnsResolver.Options))])
            self._leafs = OrderedDict([
                ('search', (YLeafList(YType.str, 'search'), ['str'])),
            ])
            self.search = []

            self.options = System.DnsResolver.Options()
            self.options.parent = self
            self._children_name_map["options"] = "options"

            self.server = YList(self)
            self._segment_path = lambda: "dns-resolver"
            self._absolute_path = lambda: "ietf-system:system/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(System.DnsResolver, ['search'], name, value)


        class Server(_Entity_):
            """
            List of the DNS servers that the resolver should query.
            
            When the resolver is invoked by a calling application, it
            sends the query to the first name server in this list.  If
            no response has been received within 'timeout' seconds,
            the resolver continues with the next server in the list.
            If no response is received from any server, the resolver
            continues with the first server again.  When the resolver
            has traversed the list 'attempts' times without receiving
            any response, it gives up and returns an error to the
            calling application.
            
            Implementations MAY limit the number of entries in this
            list.
            
            .. attribute:: name  (key)
            
            	An arbitrary name for the DNS server
            	**type**\: str
            
            .. attribute:: udp_and_tcp
            
            	Contains UDP\- and TCP\-specific configuration parameters for DNS
            	**type**\:  :py:class:`UdpAndTcp <ydk.models.ydktest.ietf_system.System.DnsResolver.Server.UdpAndTcp>`
            
            

            """

            _prefix = 'sys'
            _revision = '2014-08-06'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(System.DnsResolver.Server, self).__init__()

                self.yang_name = "server"
                self.yang_parent_name = "dns-resolver"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = ['name']
                self._child_classes = OrderedDict([("udp-and-tcp", ("udp_and_tcp", System.DnsResolver.Server.UdpAndTcp))])
                self._leafs = OrderedDict([
                    ('name', (YLeaf(YType.str, 'name'), ['str'])),
                ])
                self.name = None

                self.udp_and_tcp = System.DnsResolver.Server.UdpAndTcp()
                self.udp_and_tcp.parent = self
                self._children_name_map["udp_and_tcp"] = "udp-and-tcp"
                self._segment_path = lambda: "server" + "[name='" + str(self.name) + "']"
                self._absolute_path = lambda: "ietf-system:system/dns-resolver/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(System.DnsResolver.Server, ['name'], name, value)


            class UdpAndTcp(_Entity_):
                """
                Contains UDP\- and TCP\-specific configuration
                parameters for DNS.
                
                .. attribute:: address
                
                	The address of the DNS server
                	**type**\: union of the below types:
                
                		**type**\: str
                
                			**pattern:** (([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])\\.){3}([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])(%[\\p{N}\\p{L}]+)?
                
                		**type**\: str
                
                			**pattern:** ((\:\|[0\-9a\-fA\-F]{0,4})\:)([0\-9a\-fA\-F]{0,4}\:){0,5}((([0\-9a\-fA\-F]{0,4}\:)?(\:\|[0\-9a\-fA\-F]{0,4}))\|(((25[0\-5]\|2[0\-4][0\-9]\|[01]?[0\-9]?[0\-9])\\.){3}(25[0\-5]\|2[0\-4][0\-9]\|[01]?[0\-9]?[0\-9])))(%[\\p{N}\\p{L}]+)?
                
                	**mandatory**\: True
                
                .. attribute:: port
                
                	The UDP and TCP port number of the DNS server
                	**type**\: int
                
                	**range:** 0..65535
                
                	**default value**\: 53
                
                

                """

                _prefix = 'sys'
                _revision = '2014-08-06'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(System.DnsResolver.Server.UdpAndTcp, self).__init__()

                    self.yang_name = "udp-and-tcp"
                    self.yang_parent_name = "server"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('address', (YLeaf(YType.str, 'address'), ['str','str'])),
                        ('port', (YLeaf(YType.uint16, 'port'), ['int'])),
                    ])
                    self.address = None
                    self.port = None
                    self._segment_path = lambda: "udp-and-tcp"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(System.DnsResolver.Server.UdpAndTcp, ['address', 'port'], name, value)




        class Options(_Entity_):
            """
            Resolver options.  The set of available options has been
            limited to those that are generally available across
            different resolver implementations and generally useful.
            
            .. attribute:: timeout
            
            	The amount of time the resolver will wait for a response from each remote name server before retrying the query via a different name server
            	**type**\: int
            
            	**range:** 1..255
            
            	**units**\: seconds
            
            	**default value**\: 5
            
            .. attribute:: attempts
            
            	The number of times the resolver will send a query to all of its name servers before giving up and returning an error to the calling application
            	**type**\: int
            
            	**range:** 1..255
            
            	**default value**\: 2
            
            

            """

            _prefix = 'sys'
            _revision = '2014-08-06'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(System.DnsResolver.Options, self).__init__()

                self.yang_name = "options"
                self.yang_parent_name = "dns-resolver"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('timeout', (YLeaf(YType.uint8, 'timeout'), ['int'])),
                    ('attempts', (YLeaf(YType.uint8, 'attempts'), ['int'])),
                ])
                self.timeout = None
                self.attempts = None
                self._segment_path = lambda: "options"
                self._absolute_path = lambda: "ietf-system:system/dns-resolver/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(System.DnsResolver.Options, ['timeout', 'attempts'], name, value)




    class Radius(_Entity_):
        """
        Configuration of the RADIUS client.
        
        .. attribute:: server
        
        	List of RADIUS servers used by the device.  When the RADIUS client is invoked by a calling application, it sends the query to the first server in this list.  If no response has been received within 'timeout' seconds, the client continues with the next server in the list.  If no response is received from any server, the client continues with the first server again. When the client has traversed the list 'attempts' times without receiving any response, it gives up and returns an error to the calling application
        	**type**\: list of  		 :py:class:`Server <ydk.models.ydktest.ietf_system.System.Radius.Server>`
        
        .. attribute:: options
        
        	RADIUS client options
        	**type**\:  :py:class:`Options <ydk.models.ydktest.ietf_system.System.Radius.Options>`
        
        

        """

        _prefix = 'sys'
        _revision = '2014-08-06'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(System.Radius, self).__init__()

            self.yang_name = "radius"
            self.yang_parent_name = "system"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("server", ("server", System.Radius.Server)), ("options", ("options", System.Radius.Options))])
            self._leafs = OrderedDict()

            self.options = System.Radius.Options()
            self.options.parent = self
            self._children_name_map["options"] = "options"

            self.server = YList(self)
            self._segment_path = lambda: "radius"
            self._absolute_path = lambda: "ietf-system:system/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(System.Radius, [], name, value)


        class Server(_Entity_):
            """
            List of RADIUS servers used by the device.
            
            When the RADIUS client is invoked by a calling
            application, it sends the query to the first server in
            this list.  If no response has been received within
            'timeout' seconds, the client continues with the next
            server in the list.  If no response is received from any
            server, the client continues with the first server again.
            When the client has traversed the list 'attempts' times
            without receiving any response, it gives up and returns an
            error to the calling application.
            
            .. attribute:: name  (key)
            
            	An arbitrary name for the RADIUS server
            	**type**\: str
            
            .. attribute:: udp
            
            	Contains UDP\-specific configuration parameters for RADIUS
            	**type**\:  :py:class:`Udp <ydk.models.ydktest.ietf_system.System.Radius.Server.Udp>`
            
            .. attribute:: authentication_type
            
            	The authentication type requested from the RADIUS server
            	**type**\:  :py:class:`RadiusAuthenticationType <ydk.models.ydktest.ietf_system.RadiusAuthenticationType>`
            
            	**default value**\: radius-pap
            
            

            """

            _prefix = 'sys'
            _revision = '2014-08-06'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(System.Radius.Server, self).__init__()

                self.yang_name = "server"
                self.yang_parent_name = "radius"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = ['name']
                self._child_classes = OrderedDict([("udp", ("udp", System.Radius.Server.Udp))])
                self._leafs = OrderedDict([
                    ('name', (YLeaf(YType.str, 'name'), ['str'])),
                    ('authentication_type', (YLeaf(YType.identityref, 'authentication-type'), [('ydk.models.ydktest.ietf_system', 'RadiusAuthenticationType')])),
                ])
                self.name = None
                self.authentication_type = None

                self.udp = System.Radius.Server.Udp()
                self.udp.parent = self
                self._children_name_map["udp"] = "udp"
                self._segment_path = lambda: "server" + "[name='" + str(self.name) + "']"
                self._absolute_path = lambda: "ietf-system:system/radius/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(System.Radius.Server, ['name', 'authentication_type'], name, value)


            class Udp(_Entity_):
                """
                Contains UDP\-specific configuration parameters
                for RADIUS.
                
                .. attribute:: address
                
                	The address of the RADIUS server
                	**type**\: union of the below types:
                
                		**type**\: str
                
                			**pattern:** (([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])\\.){3}([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])(%[\\p{N}\\p{L}]+)?
                
                		**type**\: str
                
                			**pattern:** ((\:\|[0\-9a\-fA\-F]{0,4})\:)([0\-9a\-fA\-F]{0,4}\:){0,5}((([0\-9a\-fA\-F]{0,4}\:)?(\:\|[0\-9a\-fA\-F]{0,4}))\|(((25[0\-5]\|2[0\-4][0\-9]\|[01]?[0\-9]?[0\-9])\\.){3}(25[0\-5]\|2[0\-4][0\-9]\|[01]?[0\-9]?[0\-9])))(%[\\p{N}\\p{L}]+)?
                
                		**type**\: str
                
                			**pattern:** ((([a\-zA\-Z0\-9\_]([a\-zA\-Z0\-9\\\-\_]){0,61})?[a\-zA\-Z0\-9]\\.)\*([a\-zA\-Z0\-9\_]([a\-zA\-Z0\-9\\\-\_]){0,61})?[a\-zA\-Z0\-9]\\.?)\|\\.
                
                	**mandatory**\: True
                
                .. attribute:: authentication_port
                
                	The port number of the RADIUS server
                	**type**\: int
                
                	**range:** 0..65535
                
                	**default value**\: 1812
                
                .. attribute:: shared_secret
                
                	The shared secret, which is known to both the RADIUS client and server
                	**type**\: str
                
                	**mandatory**\: True
                
                

                """

                _prefix = 'sys'
                _revision = '2014-08-06'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(System.Radius.Server.Udp, self).__init__()

                    self.yang_name = "udp"
                    self.yang_parent_name = "server"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('address', (YLeaf(YType.str, 'address'), ['str','str','str'])),
                        ('authentication_port', (YLeaf(YType.uint16, 'authentication-port'), ['int'])),
                        ('shared_secret', (YLeaf(YType.str, 'shared-secret'), ['str'])),
                    ])
                    self.address = None
                    self.authentication_port = None
                    self.shared_secret = None
                    self._segment_path = lambda: "udp"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(System.Radius.Server.Udp, ['address', 'authentication_port', 'shared_secret'], name, value)




        class Options(_Entity_):
            """
            RADIUS client options.
            
            .. attribute:: timeout
            
            	The number of seconds the device will wait for a response from each RADIUS server before trying with a different server
            	**type**\: int
            
            	**range:** 1..255
            
            	**units**\: seconds
            
            	**default value**\: 5
            
            .. attribute:: attempts
            
            	The number of times the device will send a query to all of its RADIUS servers before giving up
            	**type**\: int
            
            	**range:** 1..255
            
            	**default value**\: 2
            
            

            """

            _prefix = 'sys'
            _revision = '2014-08-06'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(System.Radius.Options, self).__init__()

                self.yang_name = "options"
                self.yang_parent_name = "radius"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('timeout', (YLeaf(YType.uint8, 'timeout'), ['int'])),
                    ('attempts', (YLeaf(YType.uint8, 'attempts'), ['int'])),
                ])
                self.timeout = None
                self.attempts = None
                self._segment_path = lambda: "options"
                self._absolute_path = lambda: "ietf-system:system/radius/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(System.Radius.Options, ['timeout', 'attempts'], name, value)




    class Authentication(_Entity_):
        """
        The authentication configuration subtree.
        
        .. attribute:: user_authentication_order
        
        	When the device authenticates a user with a password, it tries the authentication methods in this leaf\-list in order.  If authentication with one method fails, the next method is used.  If no method succeeds, the user is denied access.  An empty user\-authentication\-order leaf\-list still allows authentication of users using mechanisms that do not involve a password.  If the 'radius\-authentication' feature is advertised by the NETCONF server, the 'radius' identity can be added to this list.  If the 'local\-users' feature is advertised by the NETCONF server, the 'local\-users' identity can be added to this list
        	**type**\: list of   :py:class:`AuthenticationMethod <ydk.models.ydktest.ietf_system.AuthenticationMethod>`
        
        .. attribute:: user
        
        	The list of local users configured on this device
        	**type**\: list of  		 :py:class:`User <ydk.models.ydktest.ietf_system.System.Authentication.User>`
        
        

        """

        _prefix = 'sys'
        _revision = '2014-08-06'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(System.Authentication, self).__init__()

            self.yang_name = "authentication"
            self.yang_parent_name = "system"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("user", ("user", System.Authentication.User))])
            self._leafs = OrderedDict([
                ('user_authentication_order', (YLeafList(YType.identityref, 'user-authentication-order'), [('ydk.models.ydktest.ietf_system', 'AuthenticationMethod')])),
            ])
            self.user_authentication_order = []

            self.user = YList(self)
            self._segment_path = lambda: "authentication"
            self._absolute_path = lambda: "ietf-system:system/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(System.Authentication, ['user_authentication_order'], name, value)


        class User(_Entity_):
            """
            The list of local users configured on this device.
            
            .. attribute:: name  (key)
            
            	The user name string identifying this entry
            	**type**\: str
            
            .. attribute:: password
            
            	The password for this entry
            	**type**\: str
            
            	**pattern:** $0$.\*\|$1$[a\-zA\-Z0\-9./]{1,8}$[a\-zA\-Z0\-9./]{22}\|$5$(rounds=\\d+$)?[a\-zA\-Z0\-9./]{1,16}$[a\-zA\-Z0\-9./]{43}\|$6$(rounds=\\d+$)?[a\-zA\-Z0\-9./]{1,16}$[a\-zA\-Z0\-9./]{86}
            
            .. attribute:: authorized_key
            
            	A list of public SSH keys for this user.  These keys are allowed for SSH authentication, as described in RFC 4253
            	**type**\: list of  		 :py:class:`AuthorizedKey <ydk.models.ydktest.ietf_system.System.Authentication.User.AuthorizedKey>`
            
            

            """

            _prefix = 'sys'
            _revision = '2014-08-06'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(System.Authentication.User, self).__init__()

                self.yang_name = "user"
                self.yang_parent_name = "authentication"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = ['name']
                self._child_classes = OrderedDict([("authorized-key", ("authorized_key", System.Authentication.User.AuthorizedKey))])
                self._leafs = OrderedDict([
                    ('name', (YLeaf(YType.str, 'name'), ['str'])),
                    ('password', (YLeaf(YType.str, 'password'), ['str'])),
                ])
                self.name = None
                self.password = None

                self.authorized_key = YList(self)
                self._segment_path = lambda: "user" + "[name='" + str(self.name) + "']"
                self._absolute_path = lambda: "ietf-system:system/authentication/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(System.Authentication.User, ['name', 'password'], name, value)


            class AuthorizedKey(_Entity_):
                """
                A list of public SSH keys for this user.  These keys
                are allowed for SSH authentication, as described in
                RFC 4253.
                
                .. attribute:: name  (key)
                
                	An arbitrary name for the SSH key
                	**type**\: str
                
                .. attribute:: algorithm
                
                	The public key algorithm name for this SSH key.  Valid values are the values in the IANA 'Secure Shell (SSH) Protocol Parameters' registry, Public Key Algorithm Names
                	**type**\: str
                
                	**mandatory**\: True
                
                .. attribute:: key_data
                
                	The binary public key data for this SSH key, as specified by RFC 4253, Section 6.6, i.e.\:    string    certificate or public key format             identifier   byte[n]   key/certificate data
                	**type**\: str
                
                	**mandatory**\: True
                
                

                """

                _prefix = 'sys'
                _revision = '2014-08-06'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(System.Authentication.User.AuthorizedKey, self).__init__()

                    self.yang_name = "authorized-key"
                    self.yang_parent_name = "user"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = ['name']
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('name', (YLeaf(YType.str, 'name'), ['str'])),
                        ('algorithm', (YLeaf(YType.str, 'algorithm'), ['str'])),
                        ('key_data', (YLeaf(YType.str, 'key-data'), ['str'])),
                    ])
                    self.name = None
                    self.algorithm = None
                    self.key_data = None
                    self._segment_path = lambda: "authorized-key" + "[name='" + str(self.name) + "']"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(System.Authentication.User.AuthorizedKey, ['name', 'algorithm', 'key_data'], name, value)




    def clone_ptr(self):
        self._top_entity = System()
        return self._top_entity



class SystemState(_Entity_):
    """
    System group operational state.
    
    .. attribute:: platform
    
    	Contains vendor\-specific information for identifying the system platform and operating system
    	**type**\:  :py:class:`Platform <ydk.models.ydktest.ietf_system.SystemState.Platform>`
    
    	**config**\: False
    
    .. attribute:: clock
    
    	Monitoring of the system date and time properties
    	**type**\:  :py:class:`Clock <ydk.models.ydktest.ietf_system.SystemState.Clock>`
    
    	**config**\: False
    
    

    """

    _prefix = 'sys'
    _revision = '2014-08-06'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(SystemState, self).__init__()
        self._top_entity = None

        self.yang_name = "system-state"
        self.yang_parent_name = "ietf-system"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([("platform", ("platform", SystemState.Platform)), ("clock", ("clock", SystemState.Clock))])
        self._leafs = OrderedDict()

        self.platform = SystemState.Platform()
        self.platform.parent = self
        self._children_name_map["platform"] = "platform"

        self.clock = SystemState.Clock()
        self.clock.parent = self
        self._children_name_map["clock"] = "clock"
        self._segment_path = lambda: "ietf-system:system-state"
        self._is_frozen = True

    def __setattr__(self, name, value):
        self._perform_setattr(SystemState, [], name, value)


    class Platform(_Entity_):
        """
        Contains vendor\-specific information for
        identifying the system platform and operating system.
        
        .. attribute:: os_name
        
        	The name of the operating system in use \- for example, 'Linux'
        	**type**\: str
        
        	**config**\: False
        
        .. attribute:: os_release
        
        	The current release level of the operating system in use.  This string MAY indicate the OS source code revision
        	**type**\: str
        
        	**config**\: False
        
        .. attribute:: os_version
        
        	The current version level of the operating system in use.  This string MAY indicate the specific OS build date and target variant information
        	**type**\: str
        
        	**config**\: False
        
        .. attribute:: machine
        
        	A vendor\-specific identifier string representing the hardware in use
        	**type**\: str
        
        	**config**\: False
        
        

        """

        _prefix = 'sys'
        _revision = '2014-08-06'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(SystemState.Platform, self).__init__()

            self.yang_name = "platform"
            self.yang_parent_name = "system-state"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('os_name', (YLeaf(YType.str, 'os-name'), ['str'])),
                ('os_release', (YLeaf(YType.str, 'os-release'), ['str'])),
                ('os_version', (YLeaf(YType.str, 'os-version'), ['str'])),
                ('machine', (YLeaf(YType.str, 'machine'), ['str'])),
            ])
            self.os_name = None
            self.os_release = None
            self.os_version = None
            self.machine = None
            self._segment_path = lambda: "platform"
            self._absolute_path = lambda: "ietf-system:system-state/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(SystemState.Platform, ['os_name', 'os_release', 'os_version', 'machine'], name, value)



    class Clock(_Entity_):
        """
        Monitoring of the system date and time properties.
        
        .. attribute:: current_datetime
        
        	The current system date and time
        	**type**\: str
        
        	**pattern:** \\d{4}\-\\d{2}\-\\d{2}T\\d{2}\:\\d{2}\:\\d{2}(\\.\\d+)?(Z\|[\\+\\\-]\\d{2}\:\\d{2})
        
        	**config**\: False
        
        .. attribute:: boot_datetime
        
        	The system date and time when the system last restarted
        	**type**\: str
        
        	**pattern:** \\d{4}\-\\d{2}\-\\d{2}T\\d{2}\:\\d{2}\:\\d{2}(\\.\\d+)?(Z\|[\\+\\\-]\\d{2}\:\\d{2})
        
        	**config**\: False
        
        

        """

        _prefix = 'sys'
        _revision = '2014-08-06'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(SystemState.Clock, self).__init__()

            self.yang_name = "clock"
            self.yang_parent_name = "system-state"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('current_datetime', (YLeaf(YType.str, 'current-datetime'), ['str'])),
                ('boot_datetime', (YLeaf(YType.str, 'boot-datetime'), ['str'])),
            ])
            self.current_datetime = None
            self.boot_datetime = None
            self._segment_path = lambda: "clock"
            self._absolute_path = lambda: "ietf-system:system-state/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(SystemState.Clock, ['current_datetime', 'boot_datetime'], name, value)


    def clone_ptr(self):
        self._top_entity = SystemState()
        return self._top_entity



class SetCurrentDatetime(_Entity_):
    """
    Set the /system\-state/clock/current\-datetime leaf
    to the specified value.
    
    If the system is using NTP (i.e., /system/ntp/enabled
    is set to 'true'), then this operation will fail with
    error\-tag 'operation\-failed' and error\-app\-tag value of
    'ntp\-active'.
    
    .. attribute:: input
    
    	
    	**type**\:  :py:class:`Input <ydk.models.ydktest.ietf_system.SetCurrentDatetime.Input>`
    
    

    """

    _prefix = 'sys'
    _revision = '2014-08-06'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(SetCurrentDatetime, self).__init__()
        self._top_entity = None

        self.yang_name = "set-current-datetime"
        self.yang_parent_name = "ietf-system"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([])
        self._leafs = OrderedDict()

        self.input = SetCurrentDatetime.Input()
        self.input.parent = self
        self._children_name_map["input"] = "input"
        self._segment_path = lambda: "ietf-system:set-current-datetime"
        self._is_frozen = True


    class Input(_Entity_):
        """
        
        
        .. attribute:: current_datetime
        
        	The current system date and time
        	**type**\: str
        
        	**pattern:** \\d{4}\-\\d{2}\-\\d{2}T\\d{2}\:\\d{2}\:\\d{2}(\\.\\d+)?(Z\|[\\+\\\-]\\d{2}\:\\d{2})
        
        	**mandatory**\: True
        
        

        """

        _prefix = 'sys'
        _revision = '2014-08-06'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(SetCurrentDatetime.Input, self).__init__()

            self.yang_name = "input"
            self.yang_parent_name = "set-current-datetime"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('current_datetime', (YLeaf(YType.str, 'current-datetime'), ['str'])),
            ])
            self.current_datetime = None
            self._segment_path = lambda: "input"
            self._absolute_path = lambda: "ietf-system:set-current-datetime/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(SetCurrentDatetime.Input, ['current_datetime'], name, value)


    def clone_ptr(self):
        self._top_entity = SetCurrentDatetime()
        return self._top_entity



class SystemRestart(_Entity_):
    """
    Request that the entire system be restarted immediately.
    A server SHOULD send an rpc reply to the client before
    restarting the system.
    
    

    """

    _prefix = 'sys'
    _revision = '2014-08-06'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(SystemRestart, self).__init__()
        self._top_entity = None

        self.yang_name = "system-restart"
        self.yang_parent_name = "ietf-system"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([])
        self._leafs = OrderedDict()
        self._segment_path = lambda: "ietf-system:system-restart"
        self._is_frozen = True

    def clone_ptr(self):
        self._top_entity = SystemRestart()
        return self._top_entity



class SystemShutdown(_Entity_):
    """
    Request that the entire system be shut down immediately.
    A server SHOULD send an rpc reply to the client before
    shutting down the system.
    
    

    """

    _prefix = 'sys'
    _revision = '2014-08-06'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(SystemShutdown, self).__init__()
        self._top_entity = None

        self.yang_name = "system-shutdown"
        self.yang_parent_name = "ietf-system"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([])
        self._leafs = OrderedDict()
        self._segment_path = lambda: "ietf-system:system-shutdown"
        self._is_frozen = True

    def clone_ptr(self):
        self._top_entity = SystemShutdown()
        return self._top_entity



class Radius(AuthenticationMethod):
    """
    Indicates user authentication using RADIUS.
    
    

    """

    _prefix = 'sys'
    _revision = '2014-08-06'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:ietf-system", pref="ietf-system", tag="ietf-system:radius"):
        if sys.version_info > (3,):
            super().__init__(ns, pref, tag)
        else:
            super(Radius, self).__init__(ns, pref, tag)



class LocalUsers(AuthenticationMethod):
    """
    Indicates password\-based authentication of locally
    configured users.
    
    

    """

    _prefix = 'sys'
    _revision = '2014-08-06'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:ietf-system", pref="ietf-system", tag="ietf-system:local-users"):
        if sys.version_info > (3,):
            super().__init__(ns, pref, tag)
        else:
            super(LocalUsers, self).__init__(ns, pref, tag)



class RadiusPap(RadiusAuthenticationType):
    """
    The device requests Password Authentication Protocol (PAP)
    authentication from the RADIUS server.
    
    

    """

    _prefix = 'sys'
    _revision = '2014-08-06'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:ietf-system", pref="ietf-system", tag="ietf-system:radius-pap"):
        if sys.version_info > (3,):
            super().__init__(ns, pref, tag)
        else:
            super(RadiusPap, self).__init__(ns, pref, tag)



class RadiusChap(RadiusAuthenticationType):
    """
    The device requests Challenge Handshake Authentication
    Protocol (CHAP) authentication from the RADIUS server.
    
    

    """

    _prefix = 'sys'
    _revision = '2014-08-06'

    def __init__(self, ns="urn:ietf:params:xml:ns:yang:ietf-system", pref="ietf-system", tag="ietf-system:radius-chap"):
        if sys.version_info > (3,):
            super().__init__(ns, pref, tag)
        else:
            super(RadiusChap, self).__init__(ns, pref, tag)



