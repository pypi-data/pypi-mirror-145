""" ydktest_aug_ietf_5 

This module contains augmentation for ietf\-netconf module,
for testing purpose.

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




class AugIdentity(Identity):
    """
    aug\-identity
    
    

    """

    _prefix = 'yaug-five'
    _revision = '2017-07-26'

    def __init__(self, ns="http://cisco.com/ns/yang/yaug-five", pref="ydktest-aug-ietf-5", tag="ydktest-aug-ietf-5:aug-identity"):
        if sys.version_info > (3,):
            super().__init__(ns, pref, tag)
        else:
            super(AugIdentity, self).__init__(ns, pref, tag)



class DerivedAugIdentity(AugIdentity):
    """
    derived aug\-identity
    
    

    """

    _prefix = 'yaug-five'
    _revision = '2017-07-26'

    def __init__(self, ns="http://cisco.com/ns/yang/yaug-five", pref="ydktest-aug-ietf-5", tag="ydktest-aug-ietf-5:derived-aug-identity"):
        if sys.version_info > (3,):
            super().__init__(ns, pref, tag)
        else:
            super(DerivedAugIdentity, self).__init__(ns, pref, tag)



