""" oc_pattern 

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




class OcA(_Entity_):
    """
    
    
    .. attribute:: a  (key)
    
    	blah
    	**type**\: str
    
    	**refers to**\:  :py:class:`b <ydk.models.ydktest.oc_pattern.OcA.B>`
    
    .. attribute:: b
    
    	
    	**type**\:  :py:class:`B <ydk.models.ydktest.oc_pattern.OcA.B>`
    
    

    """

    _prefix = 'oc'
    _revision = '2015-11-17'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(OcA, self).__init__()
        self._top_entity = None

        self.yang_name = "oc-A"
        self.yang_parent_name = "oc-pattern"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = ['a']
        self._child_classes = OrderedDict([("B", ("b", OcA.B))])
        self._leafs = OrderedDict([
            ('a', (YLeaf(YType.str, 'a'), ['str'])),
        ])
        self.a = None

        self.b = OcA.B()
        self.b.parent = self
        self._children_name_map["b"] = "B"
        self._segment_path = lambda: "oc-pattern:oc-A" + "[a='" + str(self.a) + "']"
        self._is_frozen = True

    def __setattr__(self, name, value):
        self._perform_setattr(OcA, ['a'], name, value)


    class B(_Entity_):
        """
        
        
        .. attribute:: b
        
        	
        	**type**\: str
        
        

        """

        _prefix = 'oc'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(OcA.B, self).__init__()

            self.yang_name = "B"
            self.yang_parent_name = "oc-A"
            self.is_top_level_class = False
            self.has_list_ancestor = True
            self.ylist_key_names = []
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('b', (YLeaf(YType.str, 'b'), ['str'])),
            ])
            self.b = None
            self._segment_path = lambda: "B"
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(OcA.B, ['b'], name, value)


    def clone_ptr(self):
        self._top_entity = OcA()
        return self._top_entity



