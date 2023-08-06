""" ydktest_types 

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




class YDKIDENTITY(Identity):
    """
    YDK identity
    
    

    """

    _prefix = 'types'
    _revision = '2016-05-23'

    def __init__(self, ns="http://cisco.com/ns/yang/ydktest-types", pref="ydktest-types", tag="ydktest-types:YDK_IDENTITY"):
        if sys.version_info > (3,):
            super().__init__(ns, pref, tag)
        else:
            super(YDKIDENTITY, self).__init__(ns, pref, tag)



