""" ietf_aug_base_1 

This module is the augmentation base model for ydktest package.

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




class Cpython(_Entity_):
    """
    
    
    .. attribute:: doc
    
    	
    	**type**\:  :py:class:`Doc <ydk.models.ydktest.ietf_aug_base_1.Cpython.Doc>`
    
    .. attribute:: lib
    
    	
    	**type**\:  :py:class:`Lib <ydk.models.ydktest.ietf_aug_base_1.Cpython.Lib>`
    
    

    """

    _prefix = 'ietf-aug-base-1'
    _revision = '2016-07-01'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(Cpython, self).__init__()
        self._top_entity = None

        self.yang_name = "cpython"
        self.yang_parent_name = "ietf-aug-base-1"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([("doc", ("doc", Cpython.Doc)), ("lib", ("lib", Cpython.Lib))])
        self._leafs = OrderedDict()

        self.doc = Cpython.Doc()
        self.doc.parent = self
        self._children_name_map["doc"] = "doc"

        self.lib = Cpython.Lib()
        self.lib.parent = self
        self._children_name_map["lib"] = "lib"
        self._segment_path = lambda: "ietf-aug-base-1:cpython"
        self._is_frozen = True

    def __setattr__(self, name, value):
        self._perform_setattr(Cpython, [], name, value)


    class Doc(_Entity_):
        """
        
        
        .. attribute:: c_api
        
        	
        	**type**\:  :py:class:`CApi <ydk.models.ydktest.ietf_aug_base_1.Cpython.Doc.CApi>`
        
        .. attribute:: disutils
        
        	
        	**type**\:  :py:class:`Disutils <ydk.models.ydktest.ietf_aug_base_1.Cpython.Doc.Disutils>`
        
        .. attribute:: ydktest_aug_4
        
        	
        	**type**\:  :py:class:`YdktestAug4 <ydk.models.ydktest.ietf_aug_base_1.Cpython.Doc.YdktestAug4>`
        
        .. attribute:: aug_5_identityref
        
        	aug identityref
        	**type**\:  :py:class:`AugIdentity <ydk.models.ydktest.ydktest_aug_ietf_5.AugIdentity>`
        
        .. attribute:: ydktest_aug_2
        
        	
        	**type**\:  :py:class:`YdktestAug2 <ydk.models.ydktest.ietf_aug_base_1.Cpython.Doc.YdktestAug2>`
        
        .. attribute:: ydktest_aug_1
        
        	
        	**type**\:  :py:class:`YdktestAug1 <ydk.models.ydktest.ietf_aug_base_1.Cpython.Doc.YdktestAug1>`
        
        

        """

        _prefix = 'ietf-aug-base-1'
        _revision = '2016-07-01'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Cpython.Doc, self).__init__()

            self.yang_name = "doc"
            self.yang_parent_name = "cpython"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("c-api", ("c_api", Cpython.Doc.CApi)), ("disutils", ("disutils", Cpython.Doc.Disutils)), ("ydktest-aug-ietf-4:ydktest-aug-4", ("ydktest_aug_4", Cpython.Doc.YdktestAug4)), ("ydktest-aug-ietf-2:ydktest-aug-2", ("ydktest_aug_2", Cpython.Doc.YdktestAug2)), ("ydktest-aug-ietf-1:ydktest-aug-1", ("ydktest_aug_1", Cpython.Doc.YdktestAug1))])
            self._leafs = OrderedDict([
                ('aug_5_identityref', (YLeaf(YType.identityref, 'ydktest-aug-ietf-5:aug-5-identityref'), [('ydk.models.ydktest.ydktest_aug_ietf_5', 'AugIdentity')])),
            ])
            self.aug_5_identityref = None

            self.c_api = Cpython.Doc.CApi()
            self.c_api.parent = self
            self._children_name_map["c_api"] = "c-api"

            self.disutils = Cpython.Doc.Disutils()
            self.disutils.parent = self
            self._children_name_map["disutils"] = "disutils"

            self.ydktest_aug_4 = Cpython.Doc.YdktestAug4()
            self.ydktest_aug_4.parent = self
            self._children_name_map["ydktest_aug_4"] = "ydktest-aug-ietf-4:ydktest-aug-4"

            self.ydktest_aug_2 = Cpython.Doc.YdktestAug2()
            self.ydktest_aug_2.parent = self
            self._children_name_map["ydktest_aug_2"] = "ydktest-aug-ietf-2:ydktest-aug-2"

            self.ydktest_aug_1 = Cpython.Doc.YdktestAug1()
            self.ydktest_aug_1.parent = self
            self._children_name_map["ydktest_aug_1"] = "ydktest-aug-ietf-1:ydktest-aug-1"
            self._segment_path = lambda: "doc"
            self._absolute_path = lambda: "ietf-aug-base-1:cpython/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Cpython.Doc, ['aug_5_identityref'], name, value)


        class CApi(_Entity_):
            """
            
            
            .. attribute:: abstract
            
            	
            	**type**\: str
            
            

            """

            _prefix = 'ietf-aug-base-1'
            _revision = '2016-07-01'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Cpython.Doc.CApi, self).__init__()

                self.yang_name = "c-api"
                self.yang_parent_name = "doc"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('abstract', (YLeaf(YType.str, 'abstract'), ['str'])),
                ])
                self.abstract = None
                self._segment_path = lambda: "c-api"
                self._absolute_path = lambda: "ietf-aug-base-1:cpython/doc/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Cpython.Doc.CApi, ['abstract'], name, value)



        class Disutils(_Entity_):
            """
            
            
            .. attribute:: apiref
            
            	
            	**type**\: str
            
            .. attribute:: four_aug_list
            
            	config for four\_aug\_list data
            	**type**\:  :py:class:`FourAugList <ydk.models.ydktest.ietf_aug_base_1.Cpython.Doc.Disutils.FourAugList>`
            
            

            """

            _prefix = 'ietf-aug-base-1'
            _revision = '2016-07-01'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Cpython.Doc.Disutils, self).__init__()

                self.yang_name = "disutils"
                self.yang_parent_name = "doc"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([("ydktest-aug-ietf-4:four-aug-list", ("four_aug_list", Cpython.Doc.Disutils.FourAugList))])
                self._leafs = OrderedDict([
                    ('apiref', (YLeaf(YType.str, 'apiref'), ['str'])),
                ])
                self.apiref = None

                self.four_aug_list = Cpython.Doc.Disutils.FourAugList()
                self.four_aug_list.parent = self
                self._children_name_map["four_aug_list"] = "ydktest-aug-ietf-4:four-aug-list"
                self._segment_path = lambda: "disutils"
                self._absolute_path = lambda: "ietf-aug-base-1:cpython/doc/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Cpython.Doc.Disutils, ['apiref'], name, value)


            class FourAugList(_Entity_):
                """
                config for four\_aug\_list data
                
                .. attribute:: ldata
                
                	four aug list data
                	**type**\: list of  		 :py:class:`Ldata <ydk.models.ydktest.ietf_aug_base_1.Cpython.Doc.Disutils.FourAugList.Ldata>`
                
                .. attribute:: enabled
                
                	integer value type
                	**type**\: bool
                
                

                """

                _prefix = 'yaug-four'
                _revision = '2016-06-27'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Cpython.Doc.Disutils.FourAugList, self).__init__()

                    self.yang_name = "four-aug-list"
                    self.yang_parent_name = "disutils"
                    self.is_top_level_class = False
                    self.has_list_ancestor = False
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([("ldata", ("ldata", Cpython.Doc.Disutils.FourAugList.Ldata))])
                    self._leafs = OrderedDict([
                        ('enabled', (YLeaf(YType.boolean, 'enabled'), ['bool'])),
                    ])
                    self.enabled = None

                    self.ldata = YList(self)
                    self._segment_path = lambda: "ydktest-aug-ietf-4:four-aug-list"
                    self._absolute_path = lambda: "ietf-aug-base-1:cpython/doc/disutils/%s" % self._segment_path()
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Cpython.Doc.Disutils.FourAugList, ['enabled'], name, value)


                class Ldata(_Entity_):
                    """
                    four aug list data
                    
                    .. attribute:: number  (key)
                    
                    	integer value type
                    	**type**\: int
                    
                    	**range:** \-2147483648..2147483647
                    
                    .. attribute:: name
                    
                    	this is string value
                    	**type**\: str
                    
                    

                    """

                    _prefix = 'yaug-four'
                    _revision = '2016-06-27'

                    def __init__(self):
                        if sys.version_info > (3,):
                            super().__init__()
                        else:
                            super(Cpython.Doc.Disutils.FourAugList.Ldata, self).__init__()

                        self.yang_name = "ldata"
                        self.yang_parent_name = "four-aug-list"
                        self.is_top_level_class = False
                        self.has_list_ancestor = False
                        self.ylist_key_names = ['number']
                        self._child_classes = OrderedDict([])
                        self._leafs = OrderedDict([
                            ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                            ('name', (YLeaf(YType.str, 'name'), ['str'])),
                        ])
                        self.number = None
                        self.name = None
                        self._segment_path = lambda: "ldata" + "[number='" + str(self.number) + "']"
                        self._absolute_path = lambda: "ietf-aug-base-1:cpython/doc/disutils/ydktest-aug-ietf-4:four-aug-list/%s" % self._segment_path()
                        self._is_frozen = True

                    def __setattr__(self, name, value):
                        self._perform_setattr(Cpython.Doc.Disutils.FourAugList.Ldata, ['number', 'name'], name, value)





        class YdktestAug4(_Entity_):
            """
            
            
            .. attribute:: aug_four
            
            	ydktest augmentation four
            	**type**\: str
            
            

            """

            _prefix = 'yaug-four'
            _revision = '2016-06-27'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Cpython.Doc.YdktestAug4, self).__init__()

                self.yang_name = "ydktest-aug-4"
                self.yang_parent_name = "doc"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('aug_four', (YLeaf(YType.str, 'aug-four'), ['str'])),
                ])
                self.aug_four = None
                self._segment_path = lambda: "ydktest-aug-ietf-4:ydktest-aug-4"
                self._absolute_path = lambda: "ietf-aug-base-1:cpython/doc/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Cpython.Doc.YdktestAug4, ['aug_four'], name, value)



        class YdktestAug2(_Entity_):
            """
            
            
            .. attribute:: aug_two
            
            	ydktest augmentation two
            	**type**\: str
            
            

            """

            _prefix = 'yaug-two'
            _revision = '2016-06-22'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Cpython.Doc.YdktestAug2, self).__init__()

                self.yang_name = "ydktest-aug-2"
                self.yang_parent_name = "doc"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('aug_two', (YLeaf(YType.str, 'aug-two'), ['str'])),
                ])
                self.aug_two = None
                self._segment_path = lambda: "ydktest-aug-ietf-2:ydktest-aug-2"
                self._absolute_path = lambda: "ietf-aug-base-1:cpython/doc/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Cpython.Doc.YdktestAug2, ['aug_two'], name, value)



        class YdktestAug1(_Entity_):
            """
            
            
            .. attribute:: aug_one
            
            	ydktest augmentation one
            	**type**\: str
            
            

            """

            _prefix = 'yaug-one'
            _revision = '2016-06-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Cpython.Doc.YdktestAug1, self).__init__()

                self.yang_name = "ydktest-aug-1"
                self.yang_parent_name = "doc"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('aug_one', (YLeaf(YType.str, 'aug-one'), ['str'])),
                ])
                self.aug_one = None
                self._segment_path = lambda: "ydktest-aug-ietf-1:ydktest-aug-1"
                self._absolute_path = lambda: "ietf-aug-base-1:cpython/doc/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Cpython.Doc.YdktestAug1, ['aug_one'], name, value)




    class Lib(_Entity_):
        """
        
        
        .. attribute:: asyncio
        
        	
        	**type**\:  :py:class:`Asyncio <ydk.models.ydktest.ietf_aug_base_1.Cpython.Lib.Asyncio>`
        
        .. attribute:: collections
        
        	
        	**type**\:  :py:class:`Collections <ydk.models.ydktest.ietf_aug_base_1.Cpython.Lib.Collections>`
        
        .. attribute:: ydktest_aug_4
        
        	
        	**type**\:  :py:class:`YdktestAug4 <ydk.models.ydktest.ietf_aug_base_1.Cpython.Lib.YdktestAug4>`
        
        .. attribute:: ydktest_aug_2
        
        	
        	**type**\:  :py:class:`YdktestAug2 <ydk.models.ydktest.ietf_aug_base_1.Cpython.Lib.YdktestAug2>`
        
        .. attribute:: ydktest_aug_1
        
        	
        	**type**\:  :py:class:`YdktestAug1 <ydk.models.ydktest.ietf_aug_base_1.Cpython.Lib.YdktestAug1>`
        
        

        """

        _prefix = 'ietf-aug-base-1'
        _revision = '2016-07-01'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Cpython.Lib, self).__init__()

            self.yang_name = "lib"
            self.yang_parent_name = "cpython"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("asyncio", ("asyncio", Cpython.Lib.Asyncio)), ("collections", ("collections", Cpython.Lib.Collections)), ("ydktest-aug-ietf-4:ydktest-aug-4", ("ydktest_aug_4", Cpython.Lib.YdktestAug4)), ("ydktest-aug-ietf-2:ydktest-aug-2", ("ydktest_aug_2", Cpython.Lib.YdktestAug2)), ("ydktest-aug-ietf-1:ydktest-aug-1", ("ydktest_aug_1", Cpython.Lib.YdktestAug1))])
            self._leafs = OrderedDict()

            self.asyncio = Cpython.Lib.Asyncio()
            self.asyncio.parent = self
            self._children_name_map["asyncio"] = "asyncio"

            self.collections = Cpython.Lib.Collections()
            self.collections.parent = self
            self._children_name_map["collections"] = "collections"

            self.ydktest_aug_4 = Cpython.Lib.YdktestAug4()
            self.ydktest_aug_4.parent = self
            self._children_name_map["ydktest_aug_4"] = "ydktest-aug-ietf-4:ydktest-aug-4"

            self.ydktest_aug_2 = Cpython.Lib.YdktestAug2()
            self.ydktest_aug_2.parent = self
            self._children_name_map["ydktest_aug_2"] = "ydktest-aug-ietf-2:ydktest-aug-2"

            self.ydktest_aug_1 = Cpython.Lib.YdktestAug1()
            self.ydktest_aug_1.parent = self
            self._children_name_map["ydktest_aug_1"] = "ydktest-aug-ietf-1:ydktest-aug-1"
            self._segment_path = lambda: "lib"
            self._absolute_path = lambda: "ietf-aug-base-1:cpython/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Cpython.Lib, [], name, value)


        class Asyncio(_Entity_):
            """
            
            
            .. attribute:: base_events
            
            	
            	**type**\: str
            
            

            """

            _prefix = 'ietf-aug-base-1'
            _revision = '2016-07-01'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Cpython.Lib.Asyncio, self).__init__()

                self.yang_name = "asyncio"
                self.yang_parent_name = "lib"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('base_events', (YLeaf(YType.str, 'base-events'), ['str'])),
                ])
                self.base_events = None
                self._segment_path = lambda: "asyncio"
                self._absolute_path = lambda: "ietf-aug-base-1:cpython/lib/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Cpython.Lib.Asyncio, ['base_events'], name, value)



        class Collections(_Entity_):
            """
            
            
            .. attribute:: abc
            
            	
            	**type**\: str
            
            

            """

            _prefix = 'ietf-aug-base-1'
            _revision = '2016-07-01'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Cpython.Lib.Collections, self).__init__()

                self.yang_name = "collections"
                self.yang_parent_name = "lib"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('abc', (YLeaf(YType.str, 'abc'), ['str'])),
                ])
                self.abc = None
                self._segment_path = lambda: "collections"
                self._absolute_path = lambda: "ietf-aug-base-1:cpython/lib/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Cpython.Lib.Collections, ['abc'], name, value)



        class YdktestAug4(_Entity_):
            """
            
            
            .. attribute:: ydktest_aug_nested_4
            
            	
            	**type**\:  :py:class:`YdktestAugNested4 <ydk.models.ydktest.ietf_aug_base_1.Cpython.Lib.YdktestAug4.YdktestAugNested4>`
            
            

            """

            _prefix = 'yaug-four'
            _revision = '2016-06-27'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Cpython.Lib.YdktestAug4, self).__init__()

                self.yang_name = "ydktest-aug-4"
                self.yang_parent_name = "lib"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([("ydktest-aug-nested-4", ("ydktest_aug_nested_4", Cpython.Lib.YdktestAug4.YdktestAugNested4))])
                self._leafs = OrderedDict()

                self.ydktest_aug_nested_4 = Cpython.Lib.YdktestAug4.YdktestAugNested4()
                self.ydktest_aug_nested_4.parent = self
                self._children_name_map["ydktest_aug_nested_4"] = "ydktest-aug-nested-4"
                self._segment_path = lambda: "ydktest-aug-ietf-4:ydktest-aug-4"
                self._absolute_path = lambda: "ietf-aug-base-1:cpython/lib/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Cpython.Lib.YdktestAug4, [], name, value)


            class YdktestAugNested4(_Entity_):
                """
                
                
                .. attribute:: aug_four
                
                	ydktest augmentation four
                	**type**\: str
                
                

                """

                _prefix = 'yaug-four'
                _revision = '2016-06-27'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Cpython.Lib.YdktestAug4.YdktestAugNested4, self).__init__()

                    self.yang_name = "ydktest-aug-nested-4"
                    self.yang_parent_name = "ydktest-aug-4"
                    self.is_top_level_class = False
                    self.has_list_ancestor = False
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('aug_four', (YLeaf(YType.str, 'aug-four'), ['str'])),
                    ])
                    self.aug_four = None
                    self._segment_path = lambda: "ydktest-aug-nested-4"
                    self._absolute_path = lambda: "ietf-aug-base-1:cpython/lib/ydktest-aug-ietf-4:ydktest-aug-4/%s" % self._segment_path()
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Cpython.Lib.YdktestAug4.YdktestAugNested4, ['aug_four'], name, value)




        class YdktestAug2(_Entity_):
            """
            
            
            .. attribute:: ydktest_aug_nested_2
            
            	
            	**type**\:  :py:class:`YdktestAugNested2 <ydk.models.ydktest.ietf_aug_base_1.Cpython.Lib.YdktestAug2.YdktestAugNested2>`
            
            

            """

            _prefix = 'yaug-two'
            _revision = '2016-06-22'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Cpython.Lib.YdktestAug2, self).__init__()

                self.yang_name = "ydktest-aug-2"
                self.yang_parent_name = "lib"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([("ydktest-aug-nested-2", ("ydktest_aug_nested_2", Cpython.Lib.YdktestAug2.YdktestAugNested2))])
                self._leafs = OrderedDict()

                self.ydktest_aug_nested_2 = Cpython.Lib.YdktestAug2.YdktestAugNested2()
                self.ydktest_aug_nested_2.parent = self
                self._children_name_map["ydktest_aug_nested_2"] = "ydktest-aug-nested-2"
                self._segment_path = lambda: "ydktest-aug-ietf-2:ydktest-aug-2"
                self._absolute_path = lambda: "ietf-aug-base-1:cpython/lib/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Cpython.Lib.YdktestAug2, [], name, value)


            class YdktestAugNested2(_Entity_):
                """
                
                
                .. attribute:: aug_two
                
                	ydktest augmentation two
                	**type**\: str
                
                

                """

                _prefix = 'yaug-two'
                _revision = '2016-06-22'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Cpython.Lib.YdktestAug2.YdktestAugNested2, self).__init__()

                    self.yang_name = "ydktest-aug-nested-2"
                    self.yang_parent_name = "ydktest-aug-2"
                    self.is_top_level_class = False
                    self.has_list_ancestor = False
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('aug_two', (YLeaf(YType.str, 'aug-two'), ['str'])),
                    ])
                    self.aug_two = None
                    self._segment_path = lambda: "ydktest-aug-nested-2"
                    self._absolute_path = lambda: "ietf-aug-base-1:cpython/lib/ydktest-aug-ietf-2:ydktest-aug-2/%s" % self._segment_path()
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Cpython.Lib.YdktestAug2.YdktestAugNested2, ['aug_two'], name, value)




        class YdktestAug1(_Entity_):
            """
            
            
            .. attribute:: ydktest_aug_nested_1
            
            	
            	**type**\:  :py:class:`YdktestAugNested1 <ydk.models.ydktest.ietf_aug_base_1.Cpython.Lib.YdktestAug1.YdktestAugNested1>`
            
            

            """

            _prefix = 'yaug-one'
            _revision = '2016-06-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Cpython.Lib.YdktestAug1, self).__init__()

                self.yang_name = "ydktest-aug-1"
                self.yang_parent_name = "lib"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([("ydktest-aug-nested-1", ("ydktest_aug_nested_1", Cpython.Lib.YdktestAug1.YdktestAugNested1))])
                self._leafs = OrderedDict()

                self.ydktest_aug_nested_1 = Cpython.Lib.YdktestAug1.YdktestAugNested1()
                self.ydktest_aug_nested_1.parent = self
                self._children_name_map["ydktest_aug_nested_1"] = "ydktest-aug-nested-1"
                self._segment_path = lambda: "ydktest-aug-ietf-1:ydktest-aug-1"
                self._absolute_path = lambda: "ietf-aug-base-1:cpython/lib/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Cpython.Lib.YdktestAug1, [], name, value)


            class YdktestAugNested1(_Entity_):
                """
                
                
                .. attribute:: aug_one
                
                	ydktest augmentation one
                	**type**\: str
                
                

                """

                _prefix = 'yaug-one'
                _revision = '2016-06-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Cpython.Lib.YdktestAug1.YdktestAugNested1, self).__init__()

                    self.yang_name = "ydktest-aug-nested-1"
                    self.yang_parent_name = "ydktest-aug-1"
                    self.is_top_level_class = False
                    self.has_list_ancestor = False
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('aug_one', (YLeaf(YType.str, 'aug-one'), ['str'])),
                    ])
                    self.aug_one = None
                    self._segment_path = lambda: "ydktest-aug-nested-1"
                    self._absolute_path = lambda: "ietf-aug-base-1:cpython/lib/ydktest-aug-ietf-1:ydktest-aug-1/%s" % self._segment_path()
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Cpython.Lib.YdktestAug1.YdktestAugNested1, ['aug_one'], name, value)




    def clone_ptr(self):
        self._top_entity = Cpython()
        return self._top_entity



