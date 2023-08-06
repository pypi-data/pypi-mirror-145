""" ydktest_filterread 

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
    
    
    .. attribute:: a1
    
    	
    	**type**\: str
    
    .. attribute:: a2
    
    	
    	**type**\: str
    
    .. attribute:: a3
    
    	
    	**type**\: str
    
    .. attribute:: b
    
    	
    	**type**\:  :py:class:`B <ydk.models.ydktest.ydktest_filterread.A.B>`
    
    .. attribute:: lst
    
    	
    	**type**\: list of  		 :py:class:`Lst <ydk.models.ydktest.ydktest_filterread.A.Lst>`
    
    

    """

    _prefix = 'ydkflt'
    _revision = '2015-11-17'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(A, self).__init__()
        self._top_entity = None

        self.yang_name = "a"
        self.yang_parent_name = "ydktest-filterread"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([("b", ("b", A.B)), ("lst", ("lst", A.Lst))])
        self._leafs = OrderedDict([
            ('a1', (YLeaf(YType.str, 'a1'), ['str'])),
            ('a2', (YLeaf(YType.str, 'a2'), ['str'])),
            ('a3', (YLeaf(YType.str, 'a3'), ['str'])),
        ])
        self.a1 = None
        self.a2 = None
        self.a3 = None

        self.b = A.B()
        self.b.parent = self
        self._children_name_map["b"] = "b"

        self.lst = YList(self)
        self._segment_path = lambda: "ydktest-filterread:a"
        self._is_frozen = True

    def __setattr__(self, name, value):
        self._perform_setattr(A, ['a1', 'a2', 'a3'], name, value)


    class B(_Entity_):
        """
        
        
        .. attribute:: b1
        
        	
        	**type**\: str
        
        .. attribute:: b2
        
        	
        	**type**\: str
        
        .. attribute:: b3
        
        	
        	**type**\: str
        
        .. attribute:: c
        
        	
        	**type**\:  :py:class:`C <ydk.models.ydktest.ydktest_filterread.A.B.C>`
        
        	**presence node**\: True
        
        .. attribute:: d
        
        	
        	**type**\:  :py:class:`D <ydk.models.ydktest.ydktest_filterread.A.B.D>`
        
        .. attribute:: f
        
        	
        	**type**\:  :py:class:`F <ydk.models.ydktest.ydktest_filterread.A.B.F>`
        
        	**presence node**\: True
        
        

        """

        _prefix = 'ydkflt'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(A.B, self).__init__()

            self.yang_name = "b"
            self.yang_parent_name = "a"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("c", ("c", A.B.C)), ("d", ("d", A.B.D)), ("f", ("f", A.B.F))])
            self._leafs = OrderedDict([
                ('b1', (YLeaf(YType.str, 'b1'), ['str'])),
                ('b2', (YLeaf(YType.str, 'b2'), ['str'])),
                ('b3', (YLeaf(YType.str, 'b3'), ['str'])),
            ])
            self.b1 = None
            self.b2 = None
            self.b3 = None

            self.c = None
            self._children_name_map["c"] = "c"

            self.d = A.B.D()
            self.d.parent = self
            self._children_name_map["d"] = "d"

            self.f = None
            self._children_name_map["f"] = "f"
            self._segment_path = lambda: "b"
            self._absolute_path = lambda: "ydktest-filterread:a/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(A.B, ['b1', 'b2', 'b3'], name, value)


        class C(_Entity_):
            """
            
            
            

            This class is a :ref:`presence class<presence-class>`

            """

            _prefix = 'ydkflt'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(A.B.C, self).__init__()

                self.yang_name = "c"
                self.yang_parent_name = "b"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self.is_presence_container = True
                self._leafs = OrderedDict()
                self._segment_path = lambda: "c"
                self._absolute_path = lambda: "ydktest-filterread:a/b/%s" % self._segment_path()
                self._is_frozen = True



        class D(_Entity_):
            """
            
            
            .. attribute:: d1
            
            	
            	**type**\: str
            
            .. attribute:: d2
            
            	
            	**type**\: str
            
            .. attribute:: d3
            
            	
            	**type**\: str
            
            .. attribute:: e
            
            	
            	**type**\:  :py:class:`E <ydk.models.ydktest.ydktest_filterread.A.B.D.E>`
            
            

            """

            _prefix = 'ydkflt'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(A.B.D, self).__init__()

                self.yang_name = "d"
                self.yang_parent_name = "b"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([("e", ("e", A.B.D.E))])
                self._leafs = OrderedDict([
                    ('d1', (YLeaf(YType.str, 'd1'), ['str'])),
                    ('d2', (YLeaf(YType.str, 'd2'), ['str'])),
                    ('d3', (YLeaf(YType.str, 'd3'), ['str'])),
                ])
                self.d1 = None
                self.d2 = None
                self.d3 = None

                self.e = A.B.D.E()
                self.e.parent = self
                self._children_name_map["e"] = "e"
                self._segment_path = lambda: "d"
                self._absolute_path = lambda: "ydktest-filterread:a/b/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(A.B.D, ['d1', 'd2', 'd3'], name, value)


            class E(_Entity_):
                """
                
                
                .. attribute:: e1
                
                	
                	**type**\: str
                
                .. attribute:: e2
                
                	
                	**type**\: str
                
                

                """

                _prefix = 'ydkflt'
                _revision = '2015-11-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(A.B.D.E, self).__init__()

                    self.yang_name = "e"
                    self.yang_parent_name = "d"
                    self.is_top_level_class = False
                    self.has_list_ancestor = False
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('e1', (YLeaf(YType.str, 'e1'), ['str'])),
                        ('e2', (YLeaf(YType.str, 'e2'), ['str'])),
                    ])
                    self.e1 = None
                    self.e2 = None
                    self._segment_path = lambda: "e"
                    self._absolute_path = lambda: "ydktest-filterread:a/b/d/%s" % self._segment_path()
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(A.B.D.E, ['e1', 'e2'], name, value)




        class F(_Entity_):
            """
            
            
            .. attribute:: f1
            
            	
            	**type**\: str
            
            

            This class is a :ref:`presence class<presence-class>`

            """

            _prefix = 'ydkflt'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(A.B.F, self).__init__()

                self.yang_name = "f"
                self.yang_parent_name = "b"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self.is_presence_container = True
                self._leafs = OrderedDict([
                    ('f1', (YLeaf(YType.str, 'f1'), ['str'])),
                ])
                self.f1 = None
                self._segment_path = lambda: "f"
                self._absolute_path = lambda: "ydktest-filterread:a/b/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(A.B.F, ['f1'], name, value)




    class Lst(_Entity_):
        """
        
        
        .. attribute:: number  (key)
        
        	
        	**type**\: int
        
        	**range:** \-2147483648..2147483647
        
        .. attribute:: value
        
        	
        	**type**\: str
        
        

        """

        _prefix = 'ydkflt'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(A.Lst, self).__init__()

            self.yang_name = "lst"
            self.yang_parent_name = "a"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = ['number']
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                ('value', (YLeaf(YType.str, 'value'), ['str'])),
            ])
            self.number = None
            self.value = None
            self._segment_path = lambda: "lst" + "[number='" + str(self.number) + "']"
            self._absolute_path = lambda: "ydktest-filterread:a/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(A.Lst, ['number', 'value'], name, value)


    def clone_ptr(self):
        self._top_entity = A()
        return self._top_entity



