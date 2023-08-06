""" ydktest_sanity_types 

This module contains a collection of YANG definitions
for sanity package.

This module contains definitions
for the following management objects\:
    

Copyright (c) 2013\-2014 by Cisco Systems, Inc.
All rights reserved.

"""
import sys
from collections import OrderedDict

from ydk.types import Entity as _Entity_
from ydk.types import EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.types import Entity, EntityPath, Identity, Enum, YType, YLeaf, YLeafList, YList, LeafDataList, Bits, Empty, Decimal64
from ydk.filters import YFilter
from ydk.errors import YError, YModelError
from ydk.errors.error_handler import handle_type_error as _handle_type_error

from ydk.models.ydktest.ydktest_sanity import BaseIdentity



class YdktestType(BaseIdentity):
    """
    This identity is used as a base for all YDK types.
    
    

    """

    _prefix = 'ydkut-types'
    _revision = '2016-04-11'

    def __init__(self, ns="http://cisco.com/ns/yang/ydktest-sanity-types", pref="ydktest-sanity-types", tag="ydktest-sanity-types:ydktest-type"):
        if sys.version_info > (3,):
            super().__init__(ns, pref, tag)
        else:
            super(YdktestType, self).__init__(ns, pref, tag)



class Other(YdktestType):
    """
    
    
    

    """

    _prefix = 'ydkut-types'
    _revision = '2016-04-11'

    def __init__(self, ns="http://cisco.com/ns/yang/ydktest-sanity-types", pref="ydktest-sanity-types", tag="ydktest-sanity-types:other"):
        if sys.version_info > (3,):
            super().__init__(ns, pref, tag)
        else:
            super(Other, self).__init__(ns, pref, tag)



class AnotherOne(YdktestType):
    """
    
    
    

    """

    _prefix = 'ydkut-types'
    _revision = '2016-04-11'

    def __init__(self, ns="http://cisco.com/ns/yang/ydktest-sanity-types", pref="ydktest-sanity-types", tag="ydktest-sanity-types:another-one"):
        if sys.version_info > (3,):
            super().__init__(ns, pref, tag)
        else:
            super(AnotherOne, self).__init__(ns, pref, tag)



