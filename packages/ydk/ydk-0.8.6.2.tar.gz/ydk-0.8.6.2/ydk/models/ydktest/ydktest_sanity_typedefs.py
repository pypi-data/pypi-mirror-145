""" ydktest_sanity_typedefs 

This module contains 461 typedef statements copied from NXOS Device YANG Model 
The module created to test YDK with newer version of libyang library, 
which supports more than 255 typedef statements

"""
import sys
from collections import OrderedDict

from ydk.types import Entity as _Entity_
from ydk.types import EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.types import Entity, EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.filters import YFilter
from ydk.errors import YError, YModelError
from ydk.errors.error_handler import handle_type_error as _handle_type_error



class AaaAccountStatus(Enum):
    """
    AaaAccountStatus (Enum Class)

    .. data:: active = 0

    .. data:: inactive = 1

    """

    active = Enum.YLeaf(0, "active")

    inactive = Enum.YLeaf(1, "inactive")


class AaaAuthenticationProtocol(Enum):
    """
    AaaAuthenticationProtocol (Enum Class)

    .. data:: pap = 0

    .. data:: chap = 1

    .. data:: mschap = 2

    .. data:: mschapv2 = 3

    .. data:: ascii = 4

    """

    pap = Enum.YLeaf(0, "pap")

    chap = Enum.YLeaf(1, "chap")

    mschap = Enum.YLeaf(2, "mschap")

    mschapv2 = Enum.YLeaf(3, "mschapv2")

    ascii = Enum.YLeaf(4, "ascii")


class AaaBoolean(Enum):
    """
    AaaBoolean (Enum Class)

    .. data:: no = 0

    .. data:: yes = 1

    """

    no = Enum.YLeaf(0, "no")

    yes = Enum.YLeaf(1, "yes")


class AaaClear(Enum):
    """
    AaaClear (Enum Class)

    .. data:: no = 0

    .. data:: yes = 1

    """

    no = Enum.YLeaf(0, "no")

    yes = Enum.YLeaf(1, "yes")


class AaaCmdType(Enum):
    """
    AaaCmdType (Enum Class)

    .. data:: config = 0

    .. data:: exec_ = 1

    """

    config = Enum.YLeaf(0, "config")

    exec_ = Enum.YLeaf(1, "exec")


class AaaKeyEnc(Enum):
    """
    AaaKeyEnc (Enum Class)

    .. data:: Y_0 = 0

    .. data:: Y_6 = 6

    .. data:: Y_7 = 7

    """

    Y_0 = Enum.YLeaf(0, "0")

    Y_6 = Enum.YLeaf(6, "6")

    Y_7 = Enum.YLeaf(7, "7")


class AaaKeyEncUserPass(Enum):
    """
    AaaKeyEncUserPass (Enum Class)

    .. data:: unspecified = 255

    .. data:: clear = 0

    .. data:: Encrypt = 5

    """

    unspecified = Enum.YLeaf(255, "unspecified")

    clear = Enum.YLeaf(0, "clear")

    Encrypt = Enum.YLeaf(5, "Encrypt")


class AaaLdapSSLStrictnessLevel(Enum):
    """
    AaaLdapSSLStrictnessLevel (Enum Class)

    .. data:: strict = 0

    .. data:: permissive = 1

    """

    strict = Enum.YLeaf(0, "strict")

    permissive = Enum.YLeaf(1, "permissive")


class AaaLoggingLevel(Enum):
    """
    AaaLoggingLevel (Enum Class)

    .. data:: Emergency = 0

    .. data:: Alert = 1

    .. data:: Critical = 2

    .. data:: Error = 3

    .. data:: Warning = 4

    .. data:: Notif = 5

    .. data:: Inform = 6

    .. data:: Debug = 7

    """

    Emergency = Enum.YLeaf(0, "Emergency")

    Alert = Enum.YLeaf(1, "Alert")

    Critical = Enum.YLeaf(2, "Critical")

    Error = Enum.YLeaf(3, "Error")

    Warning = Enum.YLeaf(4, "Warning")

    Notif = Enum.YLeaf(5, "Notif")

    Inform = Enum.YLeaf(6, "Inform")

    Debug = Enum.YLeaf(7, "Debug")


class AaaMonitorServerType(Enum):
    """
    AaaMonitorServerType (Enum Class)

    .. data:: disabled = 0

    .. data:: enabled = 1

    """

    disabled = Enum.YLeaf(0, "disabled")

    enabled = Enum.YLeaf(1, "enabled")


class AaaNoRolePolicy(Enum):
    """
    AaaNoRolePolicy (Enum Class)

    .. data:: no_login = 0

    .. data:: assign_default_role = 1

    """

    no_login = Enum.YLeaf(0, "no-login")

    assign_default_role = Enum.YLeaf(1, "assign-default-role")


class AaaProviderGroupProtocol(Enum):
    """
    AaaProviderGroupProtocol (Enum Class)

    .. data:: tacacs = 0

    .. data:: radius = 1

    .. data:: ldap = 2

    """

    tacacs = Enum.YLeaf(0, "tacacs")

    radius = Enum.YLeaf(1, "radius")

    ldap = Enum.YLeaf(2, "ldap")


class AaaProviderState(Enum):
    """
    AaaProviderState (Enum Class)

    .. data:: unknown = 0

    .. data:: operable = 1

    .. data:: inoperable = 2

    """

    unknown = Enum.YLeaf(0, "unknown")

    operable = Enum.YLeaf(1, "operable")

    inoperable = Enum.YLeaf(2, "inoperable")


class AaaPwdPolicy(Enum):
    """
    AaaPwdPolicy (Enum Class)

    .. data:: enable = 0

    .. data:: disable = 1

    """

    enable = Enum.YLeaf(0, "enable")

    disable = Enum.YLeaf(1, "disable")


class AaaRadSrvUseType(Enum):
    """
    AaaRadSrvUseType (Enum Class)

    .. data:: Auth = 0

    .. data:: Author = 1

    .. data:: Acc = 2

    .. data:: All = 3

    """

    Auth = Enum.YLeaf(0, "Auth")

    Author = Enum.YLeaf(1, "Author")

    Acc = Enum.YLeaf(2, "Acc")

    All = Enum.YLeaf(3, "All")


class AaaRealm(Enum):
    """
    AaaRealm (Enum Class)

    .. data:: local = 0

    .. data:: radius = 1

    .. data:: tacacs = 2

    .. data:: ldap = 3

    """

    local = Enum.YLeaf(0, "local")

    radius = Enum.YLeaf(1, "radius")

    tacacs = Enum.YLeaf(2, "tacacs")

    ldap = Enum.YLeaf(3, "ldap")


class AaaRuleAccessType(Enum):
    """
    AaaRuleAccessType (Enum Class)

    .. data:: none = 0

    .. data:: read = 1

    .. data:: read_write = 2

    .. data:: command = 3

    """

    none = Enum.YLeaf(0, "none")

    read = Enum.YLeaf(1, "read")

    read_write = Enum.YLeaf(2, "read-write")

    command = Enum.YLeaf(3, "command")


class AaaRulePermissionType(Enum):
    """
    AaaRulePermissionType (Enum Class)

    .. data:: none = 0

    .. data:: permit = 1

    .. data:: deny = 2

    """

    none = Enum.YLeaf(0, "none")

    permit = Enum.YLeaf(1, "permit")

    deny = Enum.YLeaf(2, "deny")


class AaaRuleScopeType(Enum):
    """
    AaaRuleScopeType (Enum Class)

    .. data:: none = 0

    .. data:: feature = 2

    .. data:: feature_group = 3

    .. data:: oid = 21

    """

    none = Enum.YLeaf(0, "none")

    feature = Enum.YLeaf(2, "feature")

    feature_group = Enum.YLeaf(3, "feature-group")

    oid = Enum.YLeaf(21, "oid")


class AaaUserRolePrivType(Enum):
    """
    AaaUserRolePrivType (Enum Class)

    .. data:: noDataPriv = 0

    .. data:: readPriv = 1

    .. data:: writePriv = 2

    """

    noDataPriv = Enum.YLeaf(0, "noDataPriv")

    readPriv = Enum.YLeaf(1, "readPriv")

    writePriv = Enum.YLeaf(2, "writePriv")


class AcBankT(Enum):
    """
    AcBankT (Enum Class)

    .. data:: even = 1

    .. data:: Odd = 2

    """

    even = Enum.YLeaf(1, "even")

    Odd = Enum.YLeaf(2, "Odd")


class AcRuleOperSt(Enum):
    """
    AcRuleOperSt (Enum Class)

    .. data:: pending = 1

    .. data:: installed = 2

    .. data:: failed = 3

    """

    pending = Enum.YLeaf(1, "pending")

    installed = Enum.YLeaf(2, "installed")

    failed = Enum.YLeaf(3, "failed")


class AclActionType(Enum):
    """
    AclActionType (Enum Class)

    .. data:: invalid = 0

    .. data:: permit = 1

    .. data:: deny = 2

    .. data:: copy = 3

    .. data:: divert = 4

    .. data:: redirect = 5

    """

    invalid = Enum.YLeaf(0, "invalid")

    permit = Enum.YLeaf(1, "permit")

    deny = Enum.YLeaf(2, "deny")

    copy = Enum.YLeaf(3, "copy")

    divert = Enum.YLeaf(4, "divert")

    redirect = Enum.YLeaf(5, "redirect")


class AclHttpOptionType(Enum):
    """
    AclHttpOptionType (Enum Class)

    .. data:: get = 1

    .. data:: put = 2

    .. data:: head = 3

    .. data:: post = 4

    .. data:: delete = 5

    .. data:: trace = 6

    .. data:: connect = 7

    .. data:: invalid = 0

    """

    get = Enum.YLeaf(1, "get")

    put = Enum.YLeaf(2, "put")

    head = Enum.YLeaf(3, "head")

    post = Enum.YLeaf(4, "post")

    delete = Enum.YLeaf(5, "delete")

    trace = Enum.YLeaf(6, "trace")

    connect = Enum.YLeaf(7, "connect")

    invalid = Enum.YLeaf(0, "invalid")


class AclVAclActionType(Enum):
    """
    AclVAclActionType (Enum Class)

    .. data:: invalid = 0

    .. data:: forward = 1

    .. data:: drop = 2

    .. data:: redirect = 3

    """

    invalid = Enum.YLeaf(0, "invalid")

    forward = Enum.YLeaf(1, "forward")

    drop = Enum.YLeaf(2, "drop")

    redirect = Enum.YLeaf(3, "redirect")


class ActionAdminSt(Enum):
    """
    ActionAdminSt (Enum Class)

    .. data:: unknown = 0

    .. data:: start = 1

    .. data:: stop = 2

    .. data:: suspend = 3

    """

    unknown = Enum.YLeaf(0, "unknown")

    start = Enum.YLeaf(1, "start")

    stop = Enum.YLeaf(2, "stop")

    suspend = Enum.YLeaf(3, "suspend")


class ActionOperSt(Enum):
    """
    ActionOperSt (Enum Class)

    .. data:: scheduled = 0

    .. data:: processing = 1

    .. data:: completed = 2

    .. data:: cancelled = 3

    .. data:: failed = 4

    .. data:: indeterminate = 5

    .. data:: suspended = 6

    .. data:: crashsuspect = 7

    """

    scheduled = Enum.YLeaf(0, "scheduled")

    processing = Enum.YLeaf(1, "processing")

    completed = Enum.YLeaf(2, "completed")

    cancelled = Enum.YLeaf(3, "cancelled")

    failed = Enum.YLeaf(4, "failed")

    indeterminate = Enum.YLeaf(5, "indeterminate")

    suspended = Enum.YLeaf(6, "suspended")

    crashsuspect = Enum.YLeaf(7, "crashsuspect")


class ActionType(Enum):
    """
    ActionType (Enum Class)

    .. data:: clear = 1

    .. data:: reset = 2

    .. data:: reload = 3

    .. data:: locate = 4

    .. data:: install = 5

    .. data:: test = 6

    .. data:: collect = 7

    .. data:: interface_in_service = 8

    """

    clear = Enum.YLeaf(1, "clear")

    reset = Enum.YLeaf(2, "reset")

    reload = Enum.YLeaf(3, "reload")

    locate = Enum.YLeaf(4, "locate")

    install = Enum.YLeaf(5, "install")

    test = Enum.YLeaf(6, "test")

    collect = Enum.YLeaf(7, "collect")

    interface_in_service = Enum.YLeaf(8, "interface-in-service")


class ActrlDirection(Enum):
    """
    ActrlDirection (Enum Class)

    .. data:: uni_dir = 1

    .. data:: bi_dir = 2

    """

    uni_dir = Enum.YLeaf(1, "uni-dir")

    bi_dir = Enum.YLeaf(2, "bi-dir")


class ActrlOperSt(Enum):
    """
    ActrlOperSt (Enum Class)

    .. data:: enabled = 1

    .. data:: disabled = 2

    """

    enabled = Enum.YLeaf(1, "enabled")

    disabled = Enum.YLeaf(2, "disabled")


class ActrlRuleT(Enum):
    """
    ActrlRuleT (Enum Class)

    .. data:: tenant = 1

    .. data:: mgmt = 2

    .. data:: snmp = 3

    .. data:: bd_flood = 4

    .. data:: vrf_default = 5

    .. data:: infra = 6

    """

    tenant = Enum.YLeaf(1, "tenant")

    mgmt = Enum.YLeaf(2, "mgmt")

    snmp = Enum.YLeaf(3, "snmp")

    bd_flood = Enum.YLeaf(4, "bd_flood")

    vrf_default = Enum.YLeaf(5, "vrf_default")

    infra = Enum.YLeaf(6, "infra")


class ActrlcapSubj(Enum):
    """
    ActrlcapSubj (Enum Class)

    .. data:: unknown = 0

    .. data:: rule_namespace = 1

    .. data:: scope_namespace = 2

    """

    unknown = Enum.YLeaf(0, "unknown")

    rule_namespace = Enum.YLeaf(1, "rule-namespace")

    scope_namespace = Enum.YLeaf(2, "scope-namespace")


class AdjacencyAdjOperSt(Enum):
    """
    AdjacencyAdjOperSt (Enum Class)

    .. data:: unspecified = 0

    .. data:: incomplete = 1

    .. data:: normal = 2

    """

    unspecified = Enum.YLeaf(0, "unspecified")

    incomplete = Enum.YLeaf(1, "incomplete")

    normal = Enum.YLeaf(2, "normal")


class AdjacencyDbT(Enum):
    """
    AdjacencyDbT (Enum Class)

    .. data:: ip = 1

    .. data:: ipv6 = 2

    """

    ip = Enum.YLeaf(1, "ip")

    ipv6 = Enum.YLeaf(2, "ipv6")


class AggregateAdminState(Enum):
    """
    AggregateAdminState (Enum Class)

    .. data:: unknown = 0

    .. data:: up = 1

    .. data:: down = 2

    """

    unknown = Enum.YLeaf(0, "unknown")

    up = Enum.YLeaf(1, "up")

    down = Enum.YLeaf(2, "down")


class AggregateAfT(Enum):
    """
    AggregateAfT (Enum Class)

    .. data:: ipv4_ucast = 0

    .. data:: vpnv4_ucast = 1

    .. data:: ipv6_ucast = 2

    .. data:: vpnv6_ucast = 3

    .. data:: l2_evpn = 4

    """

    ipv4_ucast = Enum.YLeaf(0, "ipv4-ucast")

    vpnv4_ucast = Enum.YLeaf(1, "vpnv4-ucast")

    ipv6_ucast = Enum.YLeaf(2, "ipv6-ucast")

    vpnv6_ucast = Enum.YLeaf(3, "vpnv6-ucast")

    l2_evpn = Enum.YLeaf(4, "l2-evpn")


class AggregateBfdStatus(Enum):
    """
    AggregateBfdStatus (Enum Class)

    .. data:: unknown = 0

    .. data:: admin_down = 1

    .. data:: down = 2

    .. data:: init = 3

    .. data:: up = 4

    """

    unknown = Enum.YLeaf(0, "unknown")

    admin_down = Enum.YLeaf(1, "admin_down")

    down = Enum.YLeaf(2, "down")

    init = Enum.YLeaf(3, "init")

    up = Enum.YLeaf(4, "up")


class AggregateBooleanFlag(Enum):
    """
    AggregateBooleanFlag (Enum Class)

    .. data:: no = 0

    .. data:: yes = 1

    """

    no = Enum.YLeaf(0, "no")

    yes = Enum.YLeaf(1, "yes")


class AggregateConfTmplStatus(Enum):
    """
    AggregateConfTmplStatus (Enum Class)

    .. data:: inactive = 0

    .. data:: active = 1

    .. data:: failed = 2

    """

    inactive = Enum.YLeaf(0, "inactive")

    active = Enum.YLeaf(1, "active")

    failed = Enum.YLeaf(2, "failed")


class AggregateConfigMgmtStatus(Enum):
    """
    AggregateConfigMgmtStatus (Enum Class)

    .. data:: unknown = 0

    .. data:: configMgmtReady = 1

    .. data:: configMgmtNotReady = 2

    .. data:: configMgmtPurgeStart = 4

    """

    unknown = Enum.YLeaf(0, "unknown")

    configMgmtReady = Enum.YLeaf(1, "configMgmtReady")

    configMgmtNotReady = Enum.YLeaf(2, "configMgmtNotReady")

    configMgmtPurgeStart = Enum.YLeaf(4, "configMgmtPurgeStart")


class AggregateConfigSourceType(Enum):
    """
    AggregateConfigSourceType (Enum Class)

    .. data:: unknown = 0

    .. data:: cli = 1

    .. data:: controller = 2

    """

    unknown = Enum.YLeaf(0, "unknown")

    cli = Enum.YLeaf(1, "cli")

    controller = Enum.YLeaf(2, "controller")


class AggregateConfigStatus(Enum):
    """
    AggregateConfigStatus (Enum Class)

    .. data:: unknown = 0

    .. data:: configReady = 1

    .. data:: configNotReady = 2

    .. data:: configPurgeInProgress = 4

    """

    unknown = Enum.YLeaf(0, "unknown")

    configReady = Enum.YLeaf(1, "configReady")

    configNotReady = Enum.YLeaf(2, "configNotReady")

    configPurgeInProgress = Enum.YLeaf(4, "configPurgeInProgress")


class AggregateCtrlrType(Enum):
    """
    AggregateCtrlrType (Enum Class)

    .. data:: unknown = 0

    .. data:: l2_vxlan = 1

    .. data:: vxlan = 2

    """

    unknown = Enum.YLeaf(0, "unknown")

    l2_vxlan = Enum.YLeaf(1, "l2-vxlan")

    vxlan = Enum.YLeaf(2, "vxlan")


class AggregateFabFwdMode(Enum):
    """
    AggregateFabFwdMode (Enum Class)

    .. data:: standard = 0

    .. data:: anycastgw = 1

    .. data:: proxygw = 2

    """

    standard = Enum.YLeaf(0, "standard")

    anycastgw = Enum.YLeaf(1, "anycastgw")

    proxygw = Enum.YLeaf(2, "proxygw")


class AggregateHostReachabilityMode(Enum):
    """
    AggregateHostReachabilityMode (Enum Class)

    .. data:: unknown = 0

    .. data:: floodAndLearn = 1

    .. data:: controller = 2

    .. data:: bgp = 3

    """

    unknown = Enum.YLeaf(0, "unknown")

    floodAndLearn = Enum.YLeaf(1, "floodAndLearn")

    controller = Enum.YLeaf(2, "controller")

    bgp = Enum.YLeaf(3, "bgp")


class AggregateIngressRepProtocolType(Enum):
    """
    AggregateIngressRepProtocolType (Enum Class)

    .. data:: unknown = 0

    .. data:: static = 1

    .. data:: bgp = 2

    """

    unknown = Enum.YLeaf(0, "unknown")

    static = Enum.YLeaf(1, "static")

    bgp = Enum.YLeaf(2, "bgp")


class AggregateIntfAssignMode(Enum):
    """
    AggregateIntfAssignMode (Enum Class)

    .. data:: dedicated = 0

    .. data:: shared = 1

    """

    dedicated = Enum.YLeaf(0, "dedicated")

    shared = Enum.YLeaf(1, "shared")


class AggregateIntfType(Enum):
    """
    AggregateIntfType (Enum Class)

    .. data:: unknown = 0

    .. data:: port = 1

    .. data:: port_channel = 2

    .. data:: tunnel = 3

    .. data:: loopback = 4

    .. data:: svi = 5

    """

    unknown = Enum.YLeaf(0, "unknown")

    port = Enum.YLeaf(1, "port")

    port_channel = Enum.YLeaf(2, "port-channel")

    tunnel = Enum.YLeaf(3, "tunnel")

    loopback = Enum.YLeaf(4, "loopback")

    svi = Enum.YLeaf(5, "svi")


class AggregateMacType(Enum):
    """
    AggregateMacType (Enum Class)

    .. data:: unknown = 0

    .. data:: unicast = 1

    .. data:: multicast = 2

    """

    unknown = Enum.YLeaf(0, "unknown")

    unicast = Enum.YLeaf(1, "unicast")

    multicast = Enum.YLeaf(2, "multicast")


class AggregateOperState(Enum):
    """
    AggregateOperState (Enum Class)

    .. data:: unknown = 0

    .. data:: up = 1

    .. data:: down = 2

    """

    unknown = Enum.YLeaf(0, "unknown")

    up = Enum.YLeaf(1, "up")

    down = Enum.YLeaf(2, "down")


class AggregateReplicationModeType(Enum):
    """
    AggregateReplicationModeType (Enum Class)

    .. data:: unknown = 0

    .. data:: replicationServer = 1

    .. data:: ingressReplication = 2

    .. data:: ipMulticast = 3

    """

    unknown = Enum.YLeaf(0, "unknown")

    replicationServer = Enum.YLeaf(1, "replicationServer")

    ingressReplication = Enum.YLeaf(2, "ingressReplication")

    ipMulticast = Enum.YLeaf(3, "ipMulticast")


class AggregateResourceStatus(Enum):
    """
    AggregateResourceStatus (Enum Class)

    .. data:: unknown = 0

    .. data:: vlanCreated = 1

    .. data:: vlanFailed = 2

    .. data:: vnidCreated = 3

    .. data:: vnidFailed = 4

    .. data:: vlansCarved = 5

    .. data:: vlansNotCarved = 6

    .. data:: vnidCreationReceived = 7

    .. data:: myTEPIPPublished = 101

    .. data:: controllerIntfNotCarved = 201

    .. data:: controllerIntfCarved = 202

    """

    unknown = Enum.YLeaf(0, "unknown")

    vlanCreated = Enum.YLeaf(1, "vlanCreated")

    vlanFailed = Enum.YLeaf(2, "vlanFailed")

    vnidCreated = Enum.YLeaf(3, "vnidCreated")

    vnidFailed = Enum.YLeaf(4, "vnidFailed")

    vlansCarved = Enum.YLeaf(5, "vlansCarved")

    vlansNotCarved = Enum.YLeaf(6, "vlansNotCarved")

    vnidCreationReceived = Enum.YLeaf(7, "vnidCreationReceived")

    myTEPIPPublished = Enum.YLeaf(101, "myTEPIPPublished")

    controllerIntfNotCarved = Enum.YLeaf(201, "controllerIntfNotCarved")

    controllerIntfCarved = Enum.YLeaf(202, "controllerIntfCarved")


class AggregateRttPType(Enum):
    """
    AggregateRttPType (Enum Class)

    .. data:: import_ = 1

    .. data:: export = 2

    """

    import_ = Enum.YLeaf(1, "import")

    export = Enum.YLeaf(2, "export")


class AggregateTunnelType(Enum):
    """
    AggregateTunnelType (Enum Class)

    .. data:: unknown = 0

    .. data:: vxlanipv4 = 1

    .. data:: vxlanipv6 = 2

    .. data:: nvgre = 3

    """

    unknown = Enum.YLeaf(0, "unknown")

    vxlanipv4 = Enum.YLeaf(1, "vxlanipv4")

    vxlanipv6 = Enum.YLeaf(2, "vxlanipv6")

    nvgre = Enum.YLeaf(3, "nvgre")


class AggregateVpcKeepaliveStatus(Enum):
    """
    AggregateVpcKeepaliveStatus (Enum Class)

    .. data:: VpcOobUnknown = 0

    .. data:: VpcOobDisabled = 1

    .. data:: VpcOobPeerAlive = 2

    .. data:: VpcOobPeerNotAlive = 3

    .. data:: VpcOobPeerAliveDomainMismatch = 4

    .. data:: VpcOobSuspended = 5

    .. data:: VpcOobNotOperational = 6

    .. data:: VpcOobSuspendedVrf = 7

    .. data:: VpcOobMisconfig = 8

    """

    VpcOobUnknown = Enum.YLeaf(0, "VpcOobUnknown")

    VpcOobDisabled = Enum.YLeaf(1, "VpcOobDisabled")

    VpcOobPeerAlive = Enum.YLeaf(2, "VpcOobPeerAlive")

    VpcOobPeerNotAlive = Enum.YLeaf(3, "VpcOobPeerNotAlive")

    VpcOobPeerAliveDomainMismatch = Enum.YLeaf(4, "VpcOobPeerAliveDomainMismatch")

    VpcOobSuspended = Enum.YLeaf(5, "VpcOobSuspended")

    VpcOobNotOperational = Enum.YLeaf(6, "VpcOobNotOperational")

    VpcOobSuspendedVrf = Enum.YLeaf(7, "VpcOobSuspendedVrf")

    VpcOobMisconfig = Enum.YLeaf(8, "VpcOobMisconfig")


class AggregateVpcOperStatus(Enum):
    """
    AggregateVpcOperStatus (Enum Class)

    .. data:: down = 0

    .. data:: up = 1

    """

    down = Enum.YLeaf(0, "down")

    up = Enum.YLeaf(1, "up")


class AggregateVpcPeerLinkStatus(Enum):
    """
    AggregateVpcPeerLinkStatus (Enum Class)

    .. data:: VpcPeerNolink = 0

    .. data:: VpcPeerLinkDown = 1

    .. data:: VpcPeerOk = 2

    .. data:: VpcPeerNotfound = 3

    """

    VpcPeerNolink = Enum.YLeaf(0, "VpcPeerNolink")

    VpcPeerLinkDown = Enum.YLeaf(1, "VpcPeerLinkDown")

    VpcPeerOk = Enum.YLeaf(2, "VpcPeerOk")

    VpcPeerNotfound = Enum.YLeaf(3, "VpcPeerNotfound")


class AibDbT(Enum):
    """
    AibDbT (Enum Class)

    .. data:: adj = 1

    """

    adj = Enum.YLeaf(1, "adj")


class AnalyticsCModeT(Enum):
    """
    AnalyticsCModeT (Enum Class)

    .. data:: aci = 0

    .. data:: standalone = 1

    """

    aci = Enum.YLeaf(0, "aci")

    standalone = Enum.YLeaf(1, "standalone")


class AnalyticsCollVersion(Enum):
    """
    AnalyticsCollVersion (Enum Class)

    .. data:: v5 = 1

    .. data:: v9 = 2

    .. data:: cisco_v1 = 3

    """

    v5 = Enum.YLeaf(1, "v5")

    v9 = Enum.YLeaf(2, "v9")

    cisco_v1 = Enum.YLeaf(3, "cisco-v1")


class AnalyticsDefPolicyT(Enum):
    """
    AnalyticsDefPolicyT (Enum Class)

    .. data:: permit = 0

    .. data:: deny = 1

    """

    permit = Enum.YLeaf(0, "permit")

    deny = Enum.YLeaf(1, "deny")


class AnalyticsDirectionT(Enum):
    """
    AnalyticsDirectionT (Enum Class)

    .. data:: in_ = 1

    .. data:: out = 2

    .. data:: both = 3

    """

    in_ = Enum.YLeaf(1, "in")

    out = Enum.YLeaf(2, "out")

    both = Enum.YLeaf(3, "both")


class AnalyticsFltType(Enum):
    """
    AnalyticsFltType (Enum Class)

    .. data:: ipv4 = 1

    .. data:: ipv6 = 2

    .. data:: ce = 3

    """

    ipv4 = Enum.YLeaf(1, "ipv4")

    ipv6 = Enum.YLeaf(2, "ipv6")

    ce = Enum.YLeaf(3, "ce")


class AnalyticsModeT(Enum):
    """
    AnalyticsModeT (Enum Class)

    .. data:: analytics = 0

    .. data:: netflow = 1

    """

    analytics = Enum.YLeaf(0, "analytics")

    netflow = Enum.YLeaf(1, "netflow")


class AnalyticsOperSt(Enum):
    """
    AnalyticsOperSt (Enum Class)

    .. data:: enabled = 1

    .. data:: disabled = 2

    """

    enabled = Enum.YLeaf(1, "enabled")

    disabled = Enum.YLeaf(2, "disabled")


class AnalyticsSamplerMode(Enum):
    """
    AnalyticsSamplerMode (Enum Class)

    .. data:: flow = 1

    .. data:: pkts = 2

    """

    flow = Enum.YLeaf(1, "flow")

    pkts = Enum.YLeaf(2, "pkts")


class ArpAdjOperSt(Enum):
    """
    ArpAdjOperSt (Enum Class)

    .. data:: unspecified = 0

    .. data:: incomplete = 1

    .. data:: normal = 2

    """

    unspecified = Enum.YLeaf(0, "unspecified")

    incomplete = Enum.YLeaf(1, "incomplete")

    normal = Enum.YLeaf(2, "normal")


class ArpDbT(Enum):
    """
    ArpDbT (Enum Class)

    .. data:: ip = 1

    .. data:: supcache = 2

    """

    ip = Enum.YLeaf(1, "ip")

    supcache = Enum.YLeaf(2, "supcache")


class ArpEventLogSize(Enum):
    """
    ArpEventLogSize (Enum Class)

    .. data:: disabled = 0

    .. data:: small = 1

    .. data:: medium = 2

    .. data:: large = 3

    """

    disabled = Enum.YLeaf(0, "disabled")

    small = Enum.YLeaf(1, "small")

    medium = Enum.YLeaf(2, "medium")

    large = Enum.YLeaf(3, "large")


class ArpEventType(Enum):
    """
    ArpEventType (Enum Class)

    .. data:: cli = 0

    .. data:: client_events = 1

    .. data:: client_errors = 2

    .. data:: control_events = 3

    .. data:: internal_events = 4

    .. data:: internal_errors = 5

    .. data:: high_availability = 6

    .. data:: ip_sync = 7

    .. data:: local_cache_events = 8

    .. data:: local_cache_errors = 9

    .. data:: pkt_messages = 10

    .. data:: snmp = 11

    .. data:: suppress_events = 12

    .. data:: suppress_errors = 13

    .. data:: sync = 14

    .. data:: arp_controller_errors = 15

    .. data:: arp_dme_event = 16

    .. data:: adjacency_control = 101

    .. data:: adjacency_errors = 102

    .. data:: adjacency_ipc_events = 103

    .. data:: adjacency_stats = 104

    .. data:: adjacency_high_availability = 105

    .. data:: adjacency_cli = 106

    .. data:: adjacency_sdb = 107

    .. data:: adjacency_snmp = 108

    .. data:: adjacency_netbroker = 109

    .. data:: am_dme_event = 110

    .. data:: am_event = 111

    """

    cli = Enum.YLeaf(0, "cli")

    client_events = Enum.YLeaf(1, "client-events")

    client_errors = Enum.YLeaf(2, "client-errors")

    control_events = Enum.YLeaf(3, "control-events")

    internal_events = Enum.YLeaf(4, "internal-events")

    internal_errors = Enum.YLeaf(5, "internal-errors")

    high_availability = Enum.YLeaf(6, "high-availability")

    ip_sync = Enum.YLeaf(7, "ip-sync")

    local_cache_events = Enum.YLeaf(8, "local-cache-events")

    local_cache_errors = Enum.YLeaf(9, "local-cache-errors")

    pkt_messages = Enum.YLeaf(10, "pkt-messages")

    snmp = Enum.YLeaf(11, "snmp")

    suppress_events = Enum.YLeaf(12, "suppress-events")

    suppress_errors = Enum.YLeaf(13, "suppress-errors")

    sync = Enum.YLeaf(14, "sync")

    arp_controller_errors = Enum.YLeaf(15, "arp-controller-errors")

    arp_dme_event = Enum.YLeaf(16, "arp-dme-event")

    adjacency_control = Enum.YLeaf(101, "adjacency-control")

    adjacency_errors = Enum.YLeaf(102, "adjacency-errors")

    adjacency_ipc_events = Enum.YLeaf(103, "adjacency-ipc-events")

    adjacency_stats = Enum.YLeaf(104, "adjacency-stats")

    adjacency_high_availability = Enum.YLeaf(105, "adjacency-high-availability")

    adjacency_cli = Enum.YLeaf(106, "adjacency-cli")

    adjacency_sdb = Enum.YLeaf(107, "adjacency-sdb")

    adjacency_snmp = Enum.YLeaf(108, "adjacency-snmp")

    adjacency_netbroker = Enum.YLeaf(109, "adjacency-netbroker")

    am_dme_event = Enum.YLeaf(110, "am-dme-event")

    am_event = Enum.YLeaf(111, "am-event")


class ArpLoggingLevel(Enum):
    """
    ArpLoggingLevel (Enum Class)

    .. data:: emergency = 0

    .. data:: alert = 1

    .. data:: critical = 2

    .. data:: error = 3

    .. data:: warning = 4

    .. data:: notification = 5

    .. data:: informational = 6

    .. data:: debug = 7

    """

    emergency = Enum.YLeaf(0, "emergency")

    alert = Enum.YLeaf(1, "alert")

    critical = Enum.YLeaf(2, "critical")

    error = Enum.YLeaf(3, "error")

    warning = Enum.YLeaf(4, "warning")

    notification = Enum.YLeaf(5, "notification")

    informational = Enum.YLeaf(6, "informational")

    debug = Enum.YLeaf(7, "debug")


class ArpOpcode(Enum):
    """
    ArpOpcode (Enum Class)

    .. data:: unspecified = 0

    .. data:: req = 1

    .. data:: reply = 2

    """

    unspecified = Enum.YLeaf(0, "unspecified")

    req = Enum.YLeaf(1, "req")

    reply = Enum.YLeaf(2, "reply")


class ArpStAdjOperSt(Enum):
    """
    ArpStAdjOperSt (Enum Class)

    .. data:: down = 0

    .. data:: up = 1

    .. data:: unspecified = 10

    """

    down = Enum.YLeaf(0, "down")

    up = Enum.YLeaf(1, "up")

    unspecified = Enum.YLeaf(10, "unspecified")


class ArpStAdjOperStQual(Enum):
    """
    ArpStAdjOperStQual (Enum Class)

    .. data:: unspecified = 0

    .. data:: subnet_mismatch = 1

    .. data:: invalid_mac = 2

    .. data:: invalid_ip = 3

    .. data:: invalid_vrf = 4

    .. data:: own_mac = 5

    .. data:: if_down = 6

    .. data:: up = 7

    .. data:: invalid_if = 8

    .. data:: invalid_clidata = 9

    .. data:: no_memory = 10

    """

    unspecified = Enum.YLeaf(0, "unspecified")

    subnet_mismatch = Enum.YLeaf(1, "subnet-mismatch")

    invalid_mac = Enum.YLeaf(2, "invalid-mac")

    invalid_ip = Enum.YLeaf(3, "invalid-ip")

    invalid_vrf = Enum.YLeaf(4, "invalid-vrf")

    own_mac = Enum.YLeaf(5, "own-mac")

    if_down = Enum.YLeaf(6, "if-down")

    up = Enum.YLeaf(7, "up")

    invalid_if = Enum.YLeaf(8, "invalid-if")

    invalid_clidata = Enum.YLeaf(9, "invalid-clidata")

    no_memory = Enum.YLeaf(10, "no-memory")


class ArpSuppressArpMode(Enum):
    """
    ArpSuppressArpMode (Enum Class)

    .. data:: disabled = 0

    .. data:: l2suppressarp = 1

    .. data:: l2l3suppressarp = 2

    .. data:: invalid = 3

    """

    disabled = Enum.YLeaf(0, "disabled")

    l2suppressarp = Enum.YLeaf(1, "l2suppressarp")

    l2l3suppressarp = Enum.YLeaf(2, "l2l3suppressarp")

    invalid = Enum.YLeaf(3, "invalid")


class BdDefaultSVIAutoState(Enum):
    """
    BdDefaultSVIAutoState (Enum Class)

    .. data:: disable = 0

    .. data:: enable = 1

    """

    disable = Enum.YLeaf(0, "disable")

    enable = Enum.YLeaf(1, "enable")


class BfdAfT(Enum):
    """
    BfdAfT (Enum Class)

    .. data:: ipv4 = 1

    .. data:: ipv6 = 2

    """

    ipv4 = Enum.YLeaf(1, "ipv4")

    ipv6 = Enum.YLeaf(2, "ipv6")


class BfdAuthT(Enum):
    """
    BfdAuthT (Enum Class)

    .. data:: none = 0

    .. data:: sha1 = 4

    .. data:: met_sha1 = 5

    """

    none = Enum.YLeaf(0, "none")

    sha1 = Enum.YLeaf(4, "sha1")

    met_sha1 = Enum.YLeaf(5, "met-sha1")


class BfdDiagCode(Enum):
    """
    BfdDiagCode (Enum Class)

    .. data:: none = 0

    .. data:: detect_timeout = 1

    .. data:: echo_fail = 2

    .. data:: nbr_signal_down = 3

    .. data:: fwd_plane_reset = 4

    .. data:: path_down = 5

    .. data:: concat_path_down = 6

    .. data:: admin_down = 7

    .. data:: rev_concat_path_down = 8

    """

    none = Enum.YLeaf(0, "none")

    detect_timeout = Enum.YLeaf(1, "detect-timeout")

    echo_fail = Enum.YLeaf(2, "echo-fail")

    nbr_signal_down = Enum.YLeaf(3, "nbr-signal-down")

    fwd_plane_reset = Enum.YLeaf(4, "fwd-plane-reset")

    path_down = Enum.YLeaf(5, "path-down")

    concat_path_down = Enum.YLeaf(6, "concat-path-down")

    admin_down = Enum.YLeaf(7, "admin-down")

    rev_concat_path_down = Enum.YLeaf(8, "rev-concat-path-down")


class BfdOperSt(Enum):
    """
    BfdOperSt (Enum Class)

    .. data:: admin_down = 0

    .. data:: down = 1

    .. data:: init = 2

    .. data:: up = 3

    """

    admin_down = Enum.YLeaf(0, "admin-down")

    down = Enum.YLeaf(1, "down")

    init = Enum.YLeaf(2, "init")

    up = Enum.YLeaf(3, "up")


class BfdTrkMbrLnk(Enum):
    """
    BfdTrkMbrLnk (Enum Class)

    .. data:: enable = 1

    .. data:: disable = 0

    """

    enable = Enum.YLeaf(1, "enable")

    disable = Enum.YLeaf(0, "disable")


class BgpAdminSt(Enum):
    """
    BgpAdminSt (Enum Class)

    .. data:: enabled = 1

    .. data:: disabled = 2

    """

    enabled = Enum.YLeaf(1, "enabled")

    disabled = Enum.YLeaf(2, "disabled")


class BgpAdvertL2vpnEvpn(Enum):
    """
    BgpAdvertL2vpnEvpn (Enum Class)

    .. data:: enabled = 1

    .. data:: disabled = 0

    """

    enabled = Enum.YLeaf(1, "enabled")

    disabled = Enum.YLeaf(0, "disabled")


class BgpAdvtMapCondition(Enum):
    """
    BgpAdvtMapCondition (Enum Class)

    .. data:: none = 0

    .. data:: exist = 1

    .. data:: non_exist = 2

    """

    none = Enum.YLeaf(0, "none")

    exist = Enum.YLeaf(1, "exist")

    non_exist = Enum.YLeaf(2, "non-exist")


class BgpAfT(Enum):
    """
    BgpAfT (Enum Class)

    .. data:: ipv4_ucast = 1

    .. data:: ipv4_mcast = 2

    .. data:: vpnv4_ucast = 3

    .. data:: ipv6_ucast = 5

    .. data:: ipv6_mcast = 6

    .. data:: vpnv6_ucast = 7

    .. data:: l2vpn_evpn = 9

    .. data:: ipv4_lucast = 10

    .. data:: ipv6_lucast = 11

    .. data:: lnkstate = 12

    .. data:: ipv4_mvpn = 13

    .. data:: ipv6_mvpn = 14

    .. data:: l2vpn_vpls = 15

    .. data:: ipv4_mdt = 16

    """

    ipv4_ucast = Enum.YLeaf(1, "ipv4-ucast")

    ipv4_mcast = Enum.YLeaf(2, "ipv4-mcast")

    vpnv4_ucast = Enum.YLeaf(3, "vpnv4-ucast")

    ipv6_ucast = Enum.YLeaf(5, "ipv6-ucast")

    ipv6_mcast = Enum.YLeaf(6, "ipv6-mcast")

    vpnv6_ucast = Enum.YLeaf(7, "vpnv6-ucast")

    l2vpn_evpn = Enum.YLeaf(9, "l2vpn-evpn")

    ipv4_lucast = Enum.YLeaf(10, "ipv4-lucast")

    ipv6_lucast = Enum.YLeaf(11, "ipv6-lucast")

    lnkstate = Enum.YLeaf(12, "lnkstate")

    ipv4_mvpn = Enum.YLeaf(13, "ipv4-mvpn")

    ipv6_mvpn = Enum.YLeaf(14, "ipv6-mvpn")

    l2vpn_vpls = Enum.YLeaf(15, "l2vpn-vpls")

    ipv4_mdt = Enum.YLeaf(16, "ipv4-mdt")


class BgpAsSegT(Enum):
    """
    BgpAsSegT (Enum Class)

    .. data:: sequence = 1

    .. data:: set = 2

    """

    sequence = Enum.YLeaf(1, "sequence")

    set = Enum.YLeaf(2, "set")


class BgpAsSet(Enum):
    """
    BgpAsSet (Enum Class)

    .. data:: enabled = 1

    .. data:: disabled = 0

    """

    enabled = Enum.YLeaf(1, "enabled")

    disabled = Enum.YLeaf(0, "disabled")


class BgpAsnPropagation(Enum):
    """
    BgpAsnPropagation (Enum Class)

    .. data:: none = 0

    .. data:: no_prepend = 1

    .. data:: replace_as = 2

    .. data:: dual_as = 3

    """

    none = Enum.YLeaf(0, "none")

    no_prepend = Enum.YLeaf(1, "no-prepend")

    replace_as = Enum.YLeaf(2, "replace-as")

    dual_as = Enum.YLeaf(3, "dual-as")


class BgpBmpSt(Enum):
    """
    BgpBmpSt (Enum Class)

    .. data:: enabled = 0

    .. data:: disabled = 1

    """

    enabled = Enum.YLeaf(0, "enabled")

    disabled = Enum.YLeaf(1, "disabled")


class BgpDomOperSt(Enum):
    """
    BgpDomOperSt (Enum Class)

    .. data:: unknown = 0

    .. data:: up = 1

    .. data:: down = 2

    """

    unknown = Enum.YLeaf(0, "unknown")

    up = Enum.YLeaf(1, "up")

    down = Enum.YLeaf(2, "down")


class BgpEgressPeerEng(Enum):
    """
    BgpEgressPeerEng (Enum Class)

    .. data:: none = 0

    .. data:: enabled = 1

    .. data:: enabled_adj_sid = 2

    """

    none = Enum.YLeaf(0, "none")

    enabled = Enum.YLeaf(1, "enabled")

    enabled_adj_sid = Enum.YLeaf(2, "enabled-adj-sid")


class BgpEhType(Enum):
    """
    BgpEhType (Enum Class)

    .. data:: none = 0

    .. data:: cli = 1

    .. data:: events = 2

    .. data:: periodic = 3

    .. data:: detail = 4

    .. data:: errors = 5

    .. data:: objstore = 6

    """

    none = Enum.YLeaf(0, "none")

    cli = Enum.YLeaf(1, "cli")

    events = Enum.YLeaf(2, "events")

    periodic = Enum.YLeaf(3, "periodic")

    detail = Enum.YLeaf(4, "detail")

    errors = Enum.YLeaf(5, "errors")

    objstore = Enum.YLeaf(6, "objstore")


class BgpEvpnRtType(Enum):
    """
    BgpEvpnRtType (Enum Class)

    .. data:: none = 0

    .. data:: a_d = 1

    .. data:: mac_ip = 2

    .. data:: imet = 3

    .. data:: eth_seg = 4

    .. data:: ip_pfx = 5

    """

    none = Enum.YLeaf(0, "none")

    a_d = Enum.YLeaf(1, "a-d")

    mac_ip = Enum.YLeaf(2, "mac-ip")

    imet = Enum.YLeaf(3, "imet")

    eth_seg = Enum.YLeaf(4, "eth-seg")

    ip_pfx = Enum.YLeaf(5, "ip-pfx")


class BgpLogNbrSt(Enum):
    """
    BgpLogNbrSt (Enum Class)

    .. data:: none = 0

    .. data:: enable = 1

    .. data:: disable = 2

    """

    none = Enum.YLeaf(0, "none")

    enable = Enum.YLeaf(1, "enable")

    disable = Enum.YLeaf(2, "disable")


class BgpLsAdminSt(Enum):
    """
    BgpLsAdminSt (Enum Class)

    .. data:: inactive = 0

    .. data:: active = 1

    """

    inactive = Enum.YLeaf(0, "inactive")

    active = Enum.YLeaf(1, "active")


class BgpLsAttrEntryType(Enum):
    """
    BgpLsAttrEntryType (Enum Class)

    .. data:: none = 0

    .. data:: peer_node_sid = 1101

    .. data:: peer_adj_sid = 1102

    .. data:: peer_set_sid = 1103

    """

    none = Enum.YLeaf(0, "none")

    peer_node_sid = Enum.YLeaf(1101, "peer-node-sid")

    peer_adj_sid = Enum.YLeaf(1102, "peer-adj-sid")

    peer_set_sid = Enum.YLeaf(1103, "peer-set-sid")


class BgpLsNlriType(Enum):
    """
    BgpLsNlriType (Enum Class)

    .. data:: none = 0

    .. data:: node = 1

    .. data:: link = 2

    .. data:: ipv4_topo = 3

    .. data:: ipv6_topo = 4

    """

    none = Enum.YLeaf(0, "none")

    node = Enum.YLeaf(1, "node")

    link = Enum.YLeaf(2, "link")

    ipv4_topo = Enum.YLeaf(3, "ipv4-topo")

    ipv6_topo = Enum.YLeaf(4, "ipv6-topo")


class BgpLsProtoId(Enum):
    """
    BgpLsProtoId (Enum Class)

    .. data:: none = 0

    .. data:: isis_l1 = 1

    .. data:: isis_l2 = 2

    .. data:: ospf_v2 = 3

    .. data:: direct = 4

    .. data:: static = 5

    .. data:: ospf_v3 = 6

    .. data:: epe = 7

    """

    none = Enum.YLeaf(0, "none")

    isis_l1 = Enum.YLeaf(1, "isis-l1")

    isis_l2 = Enum.YLeaf(2, "isis-l2")

    ospf_v2 = Enum.YLeaf(3, "ospf-v2")

    direct = Enum.YLeaf(4, "direct")

    static = Enum.YLeaf(5, "static")

    ospf_v3 = Enum.YLeaf(6, "ospf-v3")

    epe = Enum.YLeaf(7, "epe")


class BgpMajNotifErr(Enum):
    """
    BgpMajNotifErr (Enum Class)

    .. data:: none = 0

    .. data:: hdr_err = 1

    .. data:: open_msg_err = 2

    .. data:: upd_msg_err = 3

    .. data:: hold_timer_exp = 4

    .. data:: fsm_err = 5

    .. data:: cease_err = 6

    .. data:: cap_msg_err = 7

    .. data:: process_restart_err = 101

    .. data:: fd_read_err = 102

    .. data:: fd_ioctl_err = 103

    .. data:: peer_close_sess_err = 104

    .. data:: rcvd_notif_err = 105

    .. data:: rcvd_dup_conn_req = 106

    .. data:: dyn_cap_no_buf = 107

    """

    none = Enum.YLeaf(0, "none")

    hdr_err = Enum.YLeaf(1, "hdr-err")

    open_msg_err = Enum.YLeaf(2, "open-msg-err")

    upd_msg_err = Enum.YLeaf(3, "upd-msg-err")

    hold_timer_exp = Enum.YLeaf(4, "hold-timer-exp")

    fsm_err = Enum.YLeaf(5, "fsm-err")

    cease_err = Enum.YLeaf(6, "cease-err")

    cap_msg_err = Enum.YLeaf(7, "cap-msg-err")

    process_restart_err = Enum.YLeaf(101, "process-restart-err")

    fd_read_err = Enum.YLeaf(102, "fd-read-err")

    fd_ioctl_err = Enum.YLeaf(103, "fd-ioctl-err")

    peer_close_sess_err = Enum.YLeaf(104, "peer-close-sess-err")

    rcvd_notif_err = Enum.YLeaf(105, "rcvd-notif-err")

    rcvd_dup_conn_req = Enum.YLeaf(106, "rcvd-dup-conn-req")

    dyn_cap_no_buf = Enum.YLeaf(107, "dyn-cap-no-buf")


class BgpMaxPfxAct(Enum):
    """
    BgpMaxPfxAct (Enum Class)

    .. data:: log = 1

    .. data:: shut = 2

    .. data:: restart = 3

    """

    log = Enum.YLeaf(1, "log")

    shut = Enum.YLeaf(2, "shut")

    restart = Enum.YLeaf(3, "restart")


class BgpMinNotifErr(Enum):
    """
    BgpMinNotifErr (Enum Class)

    .. data:: none = 0

    .. data:: unspecified_msg_hdr_err = 1

    .. data:: conn_not_synced = 2

    .. data:: bad_msg_len = 3

    .. data:: bad_msg_type = 4

    .. data:: unknown_msg_hdr_err = 5

    .. data:: unspecified_open_err = 6

    .. data:: unsupp_version = 7

    .. data:: bad_peer_as = 8

    .. data:: bad_peer_rtrid = 9

    .. data:: unsupp_opt_param = 10

    .. data:: auth_err = 11

    .. data:: bad_holdtime = 12

    .. data:: unsupp_cap = 13

    .. data:: unknown_open_hdr_err = 14

    .. data:: unspecified_update_err = 15

    .. data:: malformed_attr_list = 16

    .. data:: unrecognized_wellknown_attr = 17

    .. data:: missing_wellknown_attr = 18

    .. data:: attr_flags_err = 19

    .. data:: attr_len_err = 20

    .. data:: invalid_origin_attr = 21

    .. data:: as_loop_err = 22

    .. data:: invalid_nh_attr = 23

    .. data:: opt_attr_err = 24

    .. data:: invalid_nw_field = 25

    .. data:: bad_as_path = 26

    .. data:: unknown_update_hdr_err = 27

    .. data:: unspecified_cease_err = 28

    .. data:: max_pfx_count_err = 29

    .. data:: admin_shut = 30

    .. data:: peer_decfg = 31

    .. data:: session_cleared = 32

    .. data:: conn_rej = 33

    .. data:: other_cfg_chg = 34

    .. data:: conn_coll_resolution = 35

    .. data:: out_of_rsrc = 36

    .. data:: dyn_cap_cfg_chg = 37

    .. data:: ttl_cfg_chg = 38

    .. data:: ttl_security_cfg_chg = 39

    .. data:: passive_neighbor_cfg_chg = 40

    .. data:: af_cfg_chg = 41

    .. data:: rr_cfg_chg = 42

    .. data:: rtrid_cfg_chg = 43

    .. data:: confed_id_chg = 44

    .. data:: confed_membership_change = 45

    .. data:: gr_cfg_chg = 46

    .. data:: soft_recfg_chg = 47

    .. data:: updatesrc_if_chg = 48

    .. data:: localas_chg = 49

    .. data:: unknown_cease_err = 50

    .. data:: unspecified_cap_msg_err = 51

    .. data:: unknown_seq_num = 52

    .. data:: invalid_cap_len = 53

    .. data:: bad_cap_val = 54

    .. data:: unsupp_cap_code = 55

    .. data:: unknown_cap_err = 56

    """

    none = Enum.YLeaf(0, "none")

    unspecified_msg_hdr_err = Enum.YLeaf(1, "unspecified-msg-hdr-err")

    conn_not_synced = Enum.YLeaf(2, "conn-not-synced")

    bad_msg_len = Enum.YLeaf(3, "bad-msg-len")

    bad_msg_type = Enum.YLeaf(4, "bad-msg-type")

    unknown_msg_hdr_err = Enum.YLeaf(5, "unknown-msg-hdr-err")

    unspecified_open_err = Enum.YLeaf(6, "unspecified-open-err")

    unsupp_version = Enum.YLeaf(7, "unsupp-version")

    bad_peer_as = Enum.YLeaf(8, "bad-peer-as")

    bad_peer_rtrid = Enum.YLeaf(9, "bad-peer-rtrid")

    unsupp_opt_param = Enum.YLeaf(10, "unsupp-opt-param")

    auth_err = Enum.YLeaf(11, "auth-err")

    bad_holdtime = Enum.YLeaf(12, "bad-holdtime")

    unsupp_cap = Enum.YLeaf(13, "unsupp-cap")

    unknown_open_hdr_err = Enum.YLeaf(14, "unknown-open-hdr-err")

    unspecified_update_err = Enum.YLeaf(15, "unspecified-update-err")

    malformed_attr_list = Enum.YLeaf(16, "malformed-attr-list")

    unrecognized_wellknown_attr = Enum.YLeaf(17, "unrecognized-wellknown-attr")

    missing_wellknown_attr = Enum.YLeaf(18, "missing-wellknown-attr")

    attr_flags_err = Enum.YLeaf(19, "attr-flags-err")

    attr_len_err = Enum.YLeaf(20, "attr-len-err")

    invalid_origin_attr = Enum.YLeaf(21, "invalid-origin-attr")

    as_loop_err = Enum.YLeaf(22, "as-loop-err")

    invalid_nh_attr = Enum.YLeaf(23, "invalid-nh-attr")

    opt_attr_err = Enum.YLeaf(24, "opt-attr-err")

    invalid_nw_field = Enum.YLeaf(25, "invalid-nw-field")

    bad_as_path = Enum.YLeaf(26, "bad-as-path")

    unknown_update_hdr_err = Enum.YLeaf(27, "unknown-update-hdr-err")

    unspecified_cease_err = Enum.YLeaf(28, "unspecified-cease-err")

    max_pfx_count_err = Enum.YLeaf(29, "max-pfx-count-err")

    admin_shut = Enum.YLeaf(30, "admin-shut")

    peer_decfg = Enum.YLeaf(31, "peer-decfg")

    session_cleared = Enum.YLeaf(32, "session-cleared")

    conn_rej = Enum.YLeaf(33, "conn-rej")

    other_cfg_chg = Enum.YLeaf(34, "other-cfg-chg")

    conn_coll_resolution = Enum.YLeaf(35, "conn-coll-resolution")

    out_of_rsrc = Enum.YLeaf(36, "out-of-rsrc")

    dyn_cap_cfg_chg = Enum.YLeaf(37, "dyn-cap-cfg-chg")

    ttl_cfg_chg = Enum.YLeaf(38, "ttl-cfg-chg")

    ttl_security_cfg_chg = Enum.YLeaf(39, "ttl-security-cfg-chg")

    passive_neighbor_cfg_chg = Enum.YLeaf(40, "passive-neighbor-cfg-chg")

    af_cfg_chg = Enum.YLeaf(41, "af-cfg-chg")

    rr_cfg_chg = Enum.YLeaf(42, "rr-cfg-chg")

    rtrid_cfg_chg = Enum.YLeaf(43, "rtrid-cfg-chg")

    confed_id_chg = Enum.YLeaf(44, "confed-id-chg")

    confed_membership_change = Enum.YLeaf(45, "confed-membership-change")

    gr_cfg_chg = Enum.YLeaf(46, "gr-cfg-chg")

    soft_recfg_chg = Enum.YLeaf(47, "soft-recfg-chg")

    updatesrc_if_chg = Enum.YLeaf(48, "updatesrc-if-chg")

    localas_chg = Enum.YLeaf(49, "localas-chg")

    unknown_cease_err = Enum.YLeaf(50, "unknown-cease-err")

    unspecified_cap_msg_err = Enum.YLeaf(51, "unspecified-cap-msg-err")

    unknown_seq_num = Enum.YLeaf(52, "unknown-seq-num")

    invalid_cap_len = Enum.YLeaf(53, "invalid-cap-len")

    bad_cap_val = Enum.YLeaf(54, "bad-cap-val")

    unsupp_cap_code = Enum.YLeaf(55, "unsupp-cap-code")

    unknown_cap_err = Enum.YLeaf(56, "unknown-cap-err")


class BgpMode(Enum):
    """
    BgpMode (Enum Class)

    .. data:: fabric = 1

    .. data:: external = 2

    """

    fabric = Enum.YLeaf(1, "fabric")

    external = Enum.YLeaf(2, "external")


class BgpMvpnRtType(Enum):
    """
    BgpMvpnRtType (Enum Class)

    .. data:: none = 0

    .. data:: interas_ipmsi_ad = 1

    .. data:: intraas_ipmsi_ad = 2

    .. data:: spmsi_ad = 3

    .. data:: leaf_ad = 4

    .. data:: sa_ad = 5

    .. data:: shared_c_mcast = 6

    .. data:: source_c_mcast = 7

    """

    none = Enum.YLeaf(0, "none")

    interas_ipmsi_ad = Enum.YLeaf(1, "interas-ipmsi-ad")

    intraas_ipmsi_ad = Enum.YLeaf(2, "intraas-ipmsi-ad")

    spmsi_ad = Enum.YLeaf(3, "spmsi-ad")

    leaf_ad = Enum.YLeaf(4, "leaf-ad")

    sa_ad = Enum.YLeaf(5, "sa-ad")

    shared_c_mcast = Enum.YLeaf(6, "shared-c-mcast")

    source_c_mcast = Enum.YLeaf(7, "source-c-mcast")


class BgpOrigin(Enum):
    """
    BgpOrigin (Enum Class)

    .. data:: igp = 1

    .. data:: egp = 2

    .. data:: incomplete = 3

    """

    igp = Enum.YLeaf(1, "igp")

    egp = Enum.YLeaf(2, "egp")

    incomplete = Enum.YLeaf(3, "incomplete")


class BgpPasswdSet(Enum):
    """
    BgpPasswdSet (Enum Class)

    .. data:: enabled = 1

    .. data:: disabled = 0

    """

    enabled = Enum.YLeaf(1, "enabled")

    disabled = Enum.YLeaf(0, "disabled")


class BgpPathSt(Enum):
    """
    BgpPathSt (Enum Class)

    .. data:: deleted = 0

    .. data:: staled = 1

    .. data:: valid = 2

    .. data:: invalid = 3

    .. data:: history = 4

    .. data:: suppressed = 5

    .. data:: dampened = 6

    """

    deleted = Enum.YLeaf(0, "deleted")

    staled = Enum.YLeaf(1, "staled")

    valid = Enum.YLeaf(2, "valid")

    invalid = Enum.YLeaf(3, "invalid")

    history = Enum.YLeaf(4, "history")

    suppressed = Enum.YLeaf(5, "suppressed")

    dampened = Enum.YLeaf(6, "dampened")


class BgpPathT(Enum):
    """
    BgpPathT (Enum Class)

    .. data:: internal = 1

    .. data:: external = 2

    .. data:: confederation = 3

    .. data:: local = 4

    .. data:: aggregate = 5

    .. data:: redistribute = 6

    .. data:: injected = 7

    """

    internal = Enum.YLeaf(1, "internal")

    external = Enum.YLeaf(2, "external")

    confederation = Enum.YLeaf(3, "confederation")

    local = Enum.YLeaf(4, "local")

    aggregate = Enum.YLeaf(5, "aggregate")

    redistribute = Enum.YLeaf(6, "redistribute")

    injected = Enum.YLeaf(7, "injected")


class BgpPeerFabType(Enum):
    """
    BgpPeerFabType (Enum Class)

    .. data:: fabric_internal = 0

    .. data:: fabric_external = 1

    .. data:: fabric_border_leaf = 2

    """

    fabric_internal = Enum.YLeaf(0, "fabric-internal")

    fabric_external = Enum.YLeaf(1, "fabric-external")

    fabric_border_leaf = Enum.YLeaf(2, "fabric-border-leaf")


class BgpPeerGrSt(Enum):
    """
    BgpPeerGrSt (Enum Class)

    .. data:: na = 1

    .. data:: reset = 2

    .. data:: up = 3

    """

    na = Enum.YLeaf(1, "na")

    reset = Enum.YLeaf(2, "reset")

    up = Enum.YLeaf(3, "up")


class BgpPeerOperSt(Enum):
    """
    BgpPeerOperSt (Enum Class)

    .. data:: unspecified = 0

    .. data:: illegal = 1

    .. data:: shut = 2

    .. data:: idle = 3

    .. data:: connect = 4

    .. data:: active = 5

    .. data:: open_sent = 6

    .. data:: open_confirm = 7

    .. data:: established = 8

    .. data:: closing = 9

    .. data:: error = 10

    .. data:: unknown = 11

    """

    unspecified = Enum.YLeaf(0, "unspecified")

    illegal = Enum.YLeaf(1, "illegal")

    shut = Enum.YLeaf(2, "shut")

    idle = Enum.YLeaf(3, "idle")

    connect = Enum.YLeaf(4, "connect")

    active = Enum.YLeaf(5, "active")

    open_sent = Enum.YLeaf(6, "open-sent")

    open_confirm = Enum.YLeaf(7, "open-confirm")

    established = Enum.YLeaf(8, "established")

    closing = Enum.YLeaf(9, "closing")

    error = Enum.YLeaf(10, "error")

    unknown = Enum.YLeaf(11, "unknown")


class BgpPeerType(Enum):
    """
    BgpPeerType (Enum Class)

    .. data:: ibgp = 1

    .. data:: ebgp = 2

    """

    ibgp = Enum.YLeaf(1, "ibgp")

    ebgp = Enum.YLeaf(2, "ebgp")


class BgpPfxSidAttrEntryType(Enum):
    """
    BgpPfxSidAttrEntryType (Enum Class)

    .. data:: none = 0

    .. data:: label_index = 1

    .. data:: ipv6_sid = 2

    .. data:: origin_srgb = 3

    """

    none = Enum.YLeaf(0, "none")

    label_index = Enum.YLeaf(1, "label-index")

    ipv6_sid = Enum.YLeaf(2, "ipv6-sid")

    origin_srgb = Enum.YLeaf(3, "origin-srgb")


class BgpPmsiTunType(Enum):
    """
    BgpPmsiTunType (Enum Class)

    .. data:: none = 0

    .. data:: ingress_repl = 1

    """

    none = Enum.YLeaf(0, "none")

    ingress_repl = Enum.YLeaf(1, "ingress-repl")


class BgpPrivateASControl(Enum):
    """
    BgpPrivateASControl (Enum Class)

    .. data:: none = 0

    .. data:: remove_exclusive = 1

    .. data:: remove_all = 2

    .. data:: replace_as = 3

    """

    none = Enum.YLeaf(0, "none")

    remove_exclusive = Enum.YLeaf(1, "remove-exclusive")

    remove_all = Enum.YLeaf(2, "remove-all")

    replace_as = Enum.YLeaf(3, "replace-as")


class BgpRtCtrlDir(Enum):
    """
    BgpRtCtrlDir (Enum Class)

    .. data:: in_ = 1

    .. data:: out = 2

    """

    in_ = Enum.YLeaf(1, "in")

    out = Enum.YLeaf(2, "out")


class BgpRtCtrlOperSt(Enum):
    """
    BgpRtCtrlOperSt (Enum Class)

    .. data:: unresolved = 1

    .. data:: resolved = 2

    """

    unresolved = Enum.YLeaf(1, "unresolved")

    resolved = Enum.YLeaf(2, "resolved")


class BgpRttPType(Enum):
    """
    BgpRttPType (Enum Class)

    .. data:: import_ = 1

    .. data:: export = 2

    """

    import_ = Enum.YLeaf(1, "import")

    export = Enum.YLeaf(2, "export")


class BgpShutStQual(Enum):
    """
    BgpShutStQual (Enum Class)

    .. data:: unspecified = 0

    .. data:: admin = 1

    .. data:: no_mem = 2

    .. data:: exceeded_pfxlimit = 3

    .. data:: admin_up = 4

    .. data:: no_affinity = 5

    """

    unspecified = Enum.YLeaf(0, "unspecified")

    admin = Enum.YLeaf(1, "admin")

    no_mem = Enum.YLeaf(2, "no-mem")

    exceeded_pfxlimit = Enum.YLeaf(3, "exceeded-pfxlimit")

    admin_up = Enum.YLeaf(4, "admin-up")

    no_affinity = Enum.YLeaf(5, "no-affinity")


class BgpSoftReconfigBackup(Enum):
    """
    BgpSoftReconfigBackup (Enum Class)

    .. data:: none = 0

    .. data:: inbound = 1

    .. data:: inbound_always = 2

    """

    none = Enum.YLeaf(0, "none")

    inbound = Enum.YLeaf(1, "inbound")

    inbound_always = Enum.YLeaf(2, "inbound-always")


class BgpStReason(Enum):
    """
    BgpStReason (Enum Class)

    .. data:: none = 0

    .. data:: no_mem = 1

    """

    none = Enum.YLeaf(0, "none")

    no_mem = Enum.YLeaf(1, "no-mem")


class BgpSummaryOnly(Enum):
    """
    BgpSummaryOnly (Enum Class)

    .. data:: enabled = 1

    .. data:: disabled = 0

    """

    enabled = Enum.YLeaf(1, "enabled")

    disabled = Enum.YLeaf(0, "disabled")


class BgpTblSt(Enum):
    """
    BgpTblSt (Enum Class)

    .. data:: unknown = 0

    .. data:: up = 1

    .. data:: down = 2

    """

    unknown = Enum.YLeaf(0, "unknown")

    up = Enum.YLeaf(1, "up")

    down = Enum.YLeaf(2, "down")


class BgpVer(Enum):
    """
    BgpVer (Enum Class)

    .. data:: v4 = 4

    """

    v4 = Enum.YLeaf(4, "v4")


class CapRaiseFaultState(Enum):
    """
    CapRaiseFaultState (Enum Class)

    .. data:: nominal = 0

    .. data:: ruleHasLess = 1

    .. data:: ruleHasMore = 2

    """

    nominal = Enum.YLeaf(0, "nominal")

    ruleHasLess = Enum.YLeaf(1, "ruleHasLess")

    ruleHasMore = Enum.YLeaf(2, "ruleHasMore")


class CapRuleT(Enum):
    """
    CapRuleT (Enum Class)

    .. data:: limit = 1

    """

    limit = Enum.YLeaf(1, "limit")


class CapScope(Enum):
    """
    CapScope (Enum Class)

    .. data:: node = 0

    .. data:: policy_domain = 1

    .. data:: fabric = 2

    """

    node = Enum.YLeaf(0, "node")

    policy_domain = Enum.YLeaf(1, "policy-domain")

    fabric = Enum.YLeaf(2, "fabric")


class CdpDevIdT(Enum):
    """
    CdpDevIdT (Enum Class)

    .. data:: mac = 1

    .. data:: serialNum = 2

    .. data:: sysName = 3

    .. data:: sysNameAndSerialNum = 4

    """

    mac = Enum.YLeaf(1, "mac")

    serialNum = Enum.YLeaf(2, "serialNum")

    sysName = Enum.YLeaf(3, "sysName")

    sysNameAndSerialNum = Enum.YLeaf(4, "sysNameAndSerialNum")


class CdpDuplex(Enum):
    """
    CdpDuplex (Enum Class)

    .. data:: unknown = 0

    .. data:: half = 1

    .. data:: full = 2

    """

    unknown = Enum.YLeaf(0, "unknown")

    half = Enum.YLeaf(1, "half")

    full = Enum.YLeaf(2, "full")


class CdpOperSt(Enum):
    """
    CdpOperSt (Enum Class)

    .. data:: up = 1

    .. data:: down = 2

    """

    up = Enum.YLeaf(1, "up")

    down = Enum.YLeaf(2, "down")


class CdpOperStQual(Enum):
    """
    CdpOperStQual (Enum Class)

    .. data:: up = 1

    .. data:: admin_down = 2

    .. data:: if_down = 3

    .. data:: unsupported = 4

    """

    up = Enum.YLeaf(1, "up")

    admin_down = Enum.YLeaf(2, "admin-down")

    if_down = Enum.YLeaf(3, "if-down")

    unsupported = Enum.YLeaf(4, "unsupported")


class CdpVer(Enum):
    """
    CdpVer (Enum Class)

    .. data:: v1 = 1

    .. data:: v2 = 2

    """

    v1 = Enum.YLeaf(1, "v1")

    v2 = Enum.YLeaf(2, "v2")


class CompHostState(Enum):
    """
    CompHostState (Enum Class)

    .. data:: maintenance = 0

    .. data:: connected = 1

    .. data:: noresponse = 2

    .. data:: disconnected = 3

    .. data:: poweredOn = 4

    .. data:: poweredOff = 5

    .. data:: standBy = 6

    .. data:: suspended = 7

    .. data:: unknown = 8

    """

    maintenance = Enum.YLeaf(0, "maintenance")

    connected = Enum.YLeaf(1, "connected")

    noresponse = Enum.YLeaf(2, "noresponse")

    disconnected = Enum.YLeaf(3, "disconnected")

    poweredOn = Enum.YLeaf(4, "poweredOn")

    poweredOff = Enum.YLeaf(5, "poweredOff")

    standBy = Enum.YLeaf(6, "standBy")

    suspended = Enum.YLeaf(7, "suspended")

    unknown = Enum.YLeaf(8, "unknown")


class CompNicInstType(Enum):
    """
    CompNicInstType (Enum Class)

    .. data:: unknown = 0

    .. data:: phys = 1

    .. data:: virt = 2

    .. data:: hv = 3

    """

    unknown = Enum.YLeaf(0, "unknown")

    phys = Enum.YLeaf(1, "phys")

    virt = Enum.YLeaf(2, "virt")

    hv = Enum.YLeaf(3, "hv")


class CompNicState(Enum):
    """
    CompNicState (Enum Class)

    .. data:: down = 0

    .. data:: up = 1

    """

    down = Enum.YLeaf(0, "down")

    up = Enum.YLeaf(1, "up")


class CompVendor(Enum):
    """
    CompVendor (Enum Class)

    .. data:: VMware = 1

    .. data:: Microsoft = 2

    """

    VMware = Enum.YLeaf(1, "VMware")

    Microsoft = Enum.YLeaf(2, "Microsoft")


class CompatFilterStatus(Enum):
    """
    CompatFilterStatus (Enum Class)

    .. data:: failed = 0

    .. data:: passed = 1

    """

    failed = Enum.YLeaf(0, "failed")

    passed = Enum.YLeaf(1, "passed")


class ConftmplOperationType(Enum):
    """
    ConftmplOperationType (Enum Class)

    .. data:: create = 1

    .. data:: delete = 2

    """

    create = Enum.YLeaf(1, "create")

    delete = Enum.YLeaf(2, "delete")


class ConftmplTemplateType(Enum):
    """
    ConftmplTemplateType (Enum Class)

    .. data:: unknown = 0

    .. data:: vrf = 1

    .. data:: vlan = 2

    .. data:: intf = 3

    """

    unknown = Enum.YLeaf(0, "unknown")

    vrf = Enum.YLeaf(1, "vrf")

    vlan = Enum.YLeaf(2, "vlan")

    intf = Enum.YLeaf(3, "intf")


class CoopAdjOperSt(Enum):
    """
    CoopAdjOperSt (Enum Class)

    .. data:: down = 1

    .. data:: up = 2

    """

    down = Enum.YLeaf(1, "down")

    up = Enum.YLeaf(2, "up")


class CoopAdjOperStQual(Enum):
    """
    CoopAdjOperStQual (Enum Class)

    .. data:: unspecified = 0

    .. data:: route_unreachable = 1

    .. data:: tcp_down = 2

    .. data:: peer_inactive = 3

    .. data:: peer_congested = 4

    .. data:: up = 5

    """

    unspecified = Enum.YLeaf(0, "unspecified")

    route_unreachable = Enum.YLeaf(1, "route-unreachable")

    tcp_down = Enum.YLeaf(2, "tcp-down")

    peer_inactive = Enum.YLeaf(3, "peer-inactive")

    peer_congested = Enum.YLeaf(4, "peer-congested")

    up = Enum.YLeaf(5, "up")


class CoopDampAction(Enum):
    """
    CoopDampAction (Enum Class)

    .. data:: freeze = 1

    .. data:: withdraw = 2

    """

    freeze = Enum.YLeaf(1, "freeze")

    withdraw = Enum.YLeaf(2, "withdraw")


class CoopDomOperSt(Enum):
    """
    CoopDomOperSt (Enum Class)

    .. data:: down = 0

    .. data:: init = 1

    .. data:: up = 2

    """

    down = Enum.YLeaf(0, "down")

    init = Enum.YLeaf(1, "init")

    up = Enum.YLeaf(2, "up")


class CoopDomOperStQual(Enum):
    """
    CoopDomOperStQual (Enum Class)

    .. data:: unspecified = 0

    .. data:: config_unresolved = 1

    .. data:: time_not_synced = 2

    .. data:: infra_dom_down = 3

    .. data:: council_pending = 4

    .. data:: inconsistent_config = 5

    .. data:: admin_down = 6

    .. data:: up = 7

    """

    unspecified = Enum.YLeaf(0, "unspecified")

    config_unresolved = Enum.YLeaf(1, "config-unresolved")

    time_not_synced = Enum.YLeaf(2, "time-not-synced")

    infra_dom_down = Enum.YLeaf(3, "infra-dom-down")

    council_pending = Enum.YLeaf(4, "council-pending")

    inconsistent_config = Enum.YLeaf(5, "inconsistent-config")

    admin_down = Enum.YLeaf(6, "admin-down")

    up = Enum.YLeaf(7, "up")


class CoopRepT(Enum):
    """
    CoopRepT (Enum Class)

    .. data:: ep = 1

    .. data:: oracle = 2

    .. data:: leaf = 3

    .. data:: mgrpmbr = 4

    .. data:: mrouter = 5

    .. data:: svcnode = 6

    .. data:: anycast = 7

    .. data:: extrtr = 8

    .. data:: vpc = 9

    .. data:: vtep = 10

    .. data:: ctx = 11

    """

    ep = Enum.YLeaf(1, "ep")

    oracle = Enum.YLeaf(2, "oracle")

    leaf = Enum.YLeaf(3, "leaf")

    mgrpmbr = Enum.YLeaf(4, "mgrpmbr")

    mrouter = Enum.YLeaf(5, "mrouter")

    svcnode = Enum.YLeaf(6, "svcnode")

    anycast = Enum.YLeaf(7, "anycast")

    extrtr = Enum.YLeaf(8, "extrtr")

    vpc = Enum.YLeaf(9, "vpc")

    vtep = Enum.YLeaf(10, "vtep")

    ctx = Enum.YLeaf(11, "ctx")


class CoopRole(Enum):
    """
    CoopRole (Enum Class)

    .. data:: citizen = 1

    .. data:: oracle = 2

    """

    citizen = Enum.YLeaf(1, "citizen")

    oracle = Enum.YLeaf(2, "oracle")


class CoopSynthGen(Enum):
    """
    CoopSynthGen (Enum Class)

    .. data:: xxx = 1

    """

    xxx = Enum.YLeaf(1, "xxx")


class TopMode(Enum):
    """
    TopMode (Enum Class)

    .. data:: unspecified = 0

    .. data:: stand_alone = 1

    .. data:: cluster = 2

    """

    unspecified = Enum.YLeaf(0, "unspecified")

    stand_alone = Enum.YLeaf(1, "stand-alone")

    cluster = Enum.YLeaf(2, "cluster")



class System(_Entity_):
    """
    System
    
    .. attribute:: id
    
    	
    	**type**\: int
    
    	**range:** 0..4294967295
    
    .. attribute:: mode
    
    	System mode
    	**type**\:  :py:class:`TopMode <ydk.models.ydktest.ydktest_sanity_typedefs.TopMode>`
    
    

    """

    _prefix = 'top'
    _revision = '2018-01-30'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(System, self).__init__()
        self._top_entity = None

        self.yang_name = "System"
        self.yang_parent_name = "ydktest-sanity-typedefs"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([])
        self._leafs = OrderedDict([
            ('id', (YLeaf(YType.uint32, 'id'), ['int'])),
            ('mode', (YLeaf(YType.enumeration, 'mode'), [('ydk.models.ydktest.ydktest_sanity_typedefs', 'TopMode', '')])),
        ])
        self.id = None
        self.mode = None
        self._segment_path = lambda: "ydktest-sanity-typedefs:System"
        self._is_frozen = True

    def __setattr__(self, name, value):
        self._perform_setattr(System, ['id', 'mode'], name, value)

    def clone_ptr(self):
        self._top_entity = System()
        return self._top_entity



