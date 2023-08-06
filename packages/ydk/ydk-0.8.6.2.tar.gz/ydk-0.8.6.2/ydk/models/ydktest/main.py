""" main 

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




class A(_Entity_):
    """
    
    
    .. attribute:: one
    
    	blah
    	**type**\: int
    
    	**range:** \-2147483648..2147483647
    
    .. attribute:: c
    
    	
    	**type**\:  :py:class:`C <ydk.models.ydktest.main.A.C>`
    
    

    """

    _prefix = 'main'
    _revision = '2015-11-17'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(A, self).__init__()
        self._top_entity = None

        self.yang_name = "A"
        self.yang_parent_name = "main"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([("main-aug1:C", ("c", A.C))])
        self._leafs = OrderedDict([
            ('one', (YLeaf(YType.int32, 'one'), ['int'])),
        ])
        self.one = None

        self.c = A.C()
        self.c.parent = self
        self._children_name_map["c"] = "main-aug1:C"
        self._segment_path = lambda: "main:A"
        self._is_frozen = True

    def __setattr__(self, name, value):
        self._perform_setattr(A, ['one'], name, value)


    class C(_Entity_):
        """
        
        
        .. attribute:: two
        
        	blah
        	**type**\: str
        
        

        """

        _prefix = 'aug1'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(A.C, self).__init__()

            self.yang_name = "C"
            self.yang_parent_name = "A"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('two', (YLeaf(YType.str, 'two'), ['str'])),
            ])
            self.two = None
            self._segment_path = lambda: "main-aug1:C"
            self._absolute_path = lambda: "main:A/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(A.C, ['two'], name, value)


    def clone_ptr(self):
        self._top_entity = A()
        return self._top_entity



