""" ydktest_sanity 

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



class CompInstType(Enum):
    """
    CompInstType (Enum Class)

    .. data:: unknown = 0

    .. data:: phys = 1

    .. data:: virt = 2

    .. data:: hv = 3

    """

    unknown = Enum.YLeaf(0, "unknown")

    phys = Enum.YLeaf(1, "phys")

    virt = Enum.YLeaf(2, "virt")

    hv = Enum.YLeaf(3, "hv")


class CompInstType_(Enum):
    """
    CompInstType\_ (Enum Class)

    .. data:: unknown = 0

    .. data:: phys = 1

    .. data:: virt = 2

    .. data:: hv = 3

    """

    unknown = Enum.YLeaf(0, "unknown")

    phys = Enum.YLeaf(1, "phys")

    virt = Enum.YLeaf(2, "virt")

    hv = Enum.YLeaf(3, "hv")


class YdkEnumIntTest(Enum):
    """
    YdkEnumIntTest (Enum Class)

    Int or any

    .. data:: any = 4096

    	Any value

    """

    any = Enum.YLeaf(4096, "any")


class YdkEnumTest(Enum):
    """
    YdkEnumTest (Enum Class)

    YDK Enum test

    .. data:: not_set = 0

    	Not Set

    .. data:: none = 1

    	None

    .. data:: local = 2

    	Local

    .. data:: remote = 3

    	Remote

    """

    not_set = Enum.YLeaf(0, "not-set")

    none = Enum.YLeaf(1, "none")

    local = Enum.YLeaf(2, "local")

    remote = Enum.YLeaf(3, "remote")



class BaseIdentity(Identity):
    """
    
    
    

    """

    _prefix = 'ydkut'
    _revision = '2015-11-17'

    def __init__(self, ns="http://cisco.com/ns/yang/ydktest-sanity", pref="ydktest-sanity", tag="ydktest-sanity:base-identity"):
        if sys.version_info > (3,):
            super().__init__(ns, pref, tag)
        else:
            super(BaseIdentity, self).__init__(ns, pref, tag)



class SubTest(_Entity_):
    """
    
    
    .. attribute:: one_aug
    
    	config for one\_level data
    	**type**\:  :py:class:`OneAug <ydk.models.ydktest.ydktest_sanity.SubTest.OneAug>`
    
    

    """

    _prefix = 'ydkut'
    _revision = '2016-04-25'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(SubTest, self).__init__()
        self._top_entity = None

        self.yang_name = "sub-test"
        self.yang_parent_name = "ydktest-sanity"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([("one-aug", ("one_aug", SubTest.OneAug))])
        self._leafs = OrderedDict()

        self.one_aug = SubTest.OneAug()
        self.one_aug.parent = self
        self._children_name_map["one_aug"] = "one-aug"
        self._segment_path = lambda: "ydktest-sanity:sub-test"
        self._is_frozen = True

    def __setattr__(self, name, value):
        self._perform_setattr(SubTest, [], name, value)


    class OneAug(_Entity_):
        """
        config for one\_level data
        
        .. attribute:: number
        
        	integer value type
        	**type**\: int
        
        	**range:** \-2147483648..2147483647
        
        .. attribute:: name
        
        	this is string value
        	**type**\: str
        
        

        """

        _prefix = 'ydkut'
        _revision = '2016-04-25'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(SubTest.OneAug, self).__init__()

            self.yang_name = "one-aug"
            self.yang_parent_name = "sub-test"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                ('name', (YLeaf(YType.str, 'name'), ['str'])),
            ])
            self.number = None
            self.name = None
            self._segment_path = lambda: "one-aug"
            self._absolute_path = lambda: "ydktest-sanity:sub-test/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(SubTest.OneAug, ['number', 'name'], name, value)


    def clone_ptr(self):
        self._top_entity = SubTest()
        return self._top_entity



class Runner(_Entity_):
    """
    
    
    .. attribute:: one
    
    	config for one\_level data
    	**type**\:  :py:class:`One <ydk.models.ydktest.ydktest_sanity.Runner.One>`
    
    .. attribute:: two
    
    	config for one\_level data
    	**type**\:  :py:class:`Two <ydk.models.ydktest.ydktest_sanity.Runner.Two>`
    
    .. attribute:: three
    
    	config for one\_level data
    	**type**\:  :py:class:`Three <ydk.models.ydktest.ydktest_sanity.Runner.Three>`
    
    .. attribute:: ytypes
    
    	config for one\_level data types
    	**type**\:  :py:class:`Ytypes <ydk.models.ydktest.ydktest_sanity.Runner.Ytypes>`
    
    .. attribute:: one_list
    
    	config for one\_level list data
    	**type**\:  :py:class:`OneList <ydk.models.ydktest.ydktest_sanity.Runner.OneList>`
    
    .. attribute:: two_list
    
    	config for one\_level list data
    	**type**\:  :py:class:`TwoList <ydk.models.ydktest.ydktest_sanity.Runner.TwoList>`
    
    .. attribute:: three_list
    
    	config for one\_level list data
    	**type**\:  :py:class:`ThreeList <ydk.models.ydktest.ydktest_sanity.Runner.ThreeList>`
    
    .. attribute:: inbtw_list
    
    	config for one\_level list data
    	**type**\:  :py:class:`InbtwList <ydk.models.ydktest.ydktest_sanity.Runner.InbtwList>`
    
    .. attribute:: two_key_list
    
    	
    	**type**\: list of  		 :py:class:`TwoKeyList <ydk.models.ydktest.ydktest_sanity.Runner.TwoKeyList>`
    
    .. attribute:: identity_list
    
    	
    	**type**\: list of  		 :py:class:`IdentityList <ydk.models.ydktest.ydktest_sanity.Runner.IdentityList>`
    
    .. attribute:: enum_list
    
    	
    	**type**\: list of  		 :py:class:`EnumList <ydk.models.ydktest.ydktest_sanity.Runner.EnumList>`
    
    .. attribute:: leaf_ref
    
    	
    	**type**\:  :py:class:`LeafRef <ydk.models.ydktest.ydktest_sanity.Runner.LeafRef>`
    
    .. attribute:: not_supported_1
    
    	
    	**type**\:  :py:class:`NotSupported1 <ydk.models.ydktest.ydktest_sanity.Runner.NotSupported1>`
    
    .. attribute:: not_supported_2
    
    	
    	**type**\: list of  		 :py:class:`NotSupported2 <ydk.models.ydktest.ydktest_sanity.Runner.NotSupported2>`
    
    .. attribute:: one_read_only
    
    	one\_read\_only data
    	**type**\:  :py:class:`OneReadOnly <ydk.models.ydktest.ydktest_sanity.Runner.OneReadOnly>`
    
    	**config**\: False
    
    .. attribute:: mtus
    
    	
    	**type**\:  :py:class:`Mtus <ydk.models.ydktest.ydktest_sanity.Runner.Mtus>`
    
    .. attribute:: passive
    
    	
    	**type**\: list of  		 :py:class:`Passive <ydk.models.ydktest.ydktest_sanity.Runner.Passive>`
    
    .. attribute:: outer
    
    	
    	**type**\:  :py:class:`Outer <ydk.models.ydktest.ydktest_sanity.Runner.Outer>`
    
    .. attribute:: runner_2
    
    	
    	**type**\:  :py:class:`Runner2 <ydk.models.ydktest.ydktest_sanity.Runner.Runner2>`
    
    	**presence node**\: True
    
    .. attribute:: no_key_list
    
    	
    	**type**\: list of  		 :py:class:`NoKeyList <ydk.models.ydktest.ydktest_sanity.Runner.NoKeyList>`
    
    	**config**\: False
    
    .. attribute:: one_key_list
    
    	
    	**type**\: list of  		 :py:class:`OneKeyList <ydk.models.ydktest.ydktest_sanity.Runner.OneKeyList>`
    
    .. attribute:: mand_list
    
    	
    	**type**\: list of  		 :py:class:`MandList <ydk.models.ydktest.ydktest_sanity.Runner.MandList>`
    
    .. attribute:: ydktest_sanity_augm_one
    
    	config for one\_level data
    	**type**\:  :py:class:`YdktestSanityAugmOne <ydk.models.ydktest.ydktest_sanity.Runner.YdktestSanityAugmOne>`
    
    

    """

    _prefix = 'ydkut'
    _revision = '2015-11-17'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(Runner, self).__init__()
        self._top_entity = None

        self.yang_name = "runner"
        self.yang_parent_name = "ydktest-sanity"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([("one", ("one", Runner.One)), ("two", ("two", Runner.Two)), ("three", ("three", Runner.Three)), ("ytypes", ("ytypes", Runner.Ytypes)), ("one-list", ("one_list", Runner.OneList)), ("two-list", ("two_list", Runner.TwoList)), ("three-list", ("three_list", Runner.ThreeList)), ("inbtw-list", ("inbtw_list", Runner.InbtwList)), ("two-key-list", ("two_key_list", Runner.TwoKeyList)), ("identity-list", ("identity_list", Runner.IdentityList)), ("enum-list", ("enum_list", Runner.EnumList)), ("leaf-ref", ("leaf_ref", Runner.LeafRef)), ("not-supported-1", ("not_supported_1", Runner.NotSupported1)), ("not-supported-2", ("not_supported_2", Runner.NotSupported2)), ("one-read-only", ("one_read_only", Runner.OneReadOnly)), ("mtus", ("mtus", Runner.Mtus)), ("passive", ("passive", Runner.Passive)), ("outer", ("outer", Runner.Outer)), ("runner-2", ("runner_2", Runner.Runner2)), ("no-key-list", ("no_key_list", Runner.NoKeyList)), ("one-key-list", ("one_key_list", Runner.OneKeyList)), ("mand-list", ("mand_list", Runner.MandList)), ("ydktest-sanity-augm:one", ("ydktest_sanity_augm_one", Runner.YdktestSanityAugmOne))])
        self._leafs = OrderedDict()

        self.one = Runner.One()
        self.one.parent = self
        self._children_name_map["one"] = "one"

        self.two = Runner.Two()
        self.two.parent = self
        self._children_name_map["two"] = "two"

        self.three = Runner.Three()
        self.three.parent = self
        self._children_name_map["three"] = "three"

        self.ytypes = Runner.Ytypes()
        self.ytypes.parent = self
        self._children_name_map["ytypes"] = "ytypes"

        self.one_list = Runner.OneList()
        self.one_list.parent = self
        self._children_name_map["one_list"] = "one-list"

        self.two_list = Runner.TwoList()
        self.two_list.parent = self
        self._children_name_map["two_list"] = "two-list"

        self.three_list = Runner.ThreeList()
        self.three_list.parent = self
        self._children_name_map["three_list"] = "three-list"

        self.inbtw_list = Runner.InbtwList()
        self.inbtw_list.parent = self
        self._children_name_map["inbtw_list"] = "inbtw-list"

        self.leaf_ref = Runner.LeafRef()
        self.leaf_ref.parent = self
        self._children_name_map["leaf_ref"] = "leaf-ref"

        self.not_supported_1 = Runner.NotSupported1()
        self.not_supported_1.parent = self
        self._children_name_map["not_supported_1"] = "not-supported-1"

        self.one_read_only = Runner.OneReadOnly()
        self.one_read_only.parent = self
        self._children_name_map["one_read_only"] = "one-read-only"

        self.mtus = Runner.Mtus()
        self.mtus.parent = self
        self._children_name_map["mtus"] = "mtus"

        self.outer = Runner.Outer()
        self.outer.parent = self
        self._children_name_map["outer"] = "outer"

        self.runner_2 = None
        self._children_name_map["runner_2"] = "runner-2"

        self.ydktest_sanity_augm_one = Runner.YdktestSanityAugmOne()
        self.ydktest_sanity_augm_one.parent = self
        self._children_name_map["ydktest_sanity_augm_one"] = "ydktest-sanity-augm:one"

        self.two_key_list = YList(self)
        self.identity_list = YList(self)
        self.enum_list = YList(self)
        self.not_supported_2 = YList(self)
        self.passive = YList(self)
        self.no_key_list = YList(self)
        self.one_key_list = YList(self)
        self.mand_list = YList(self)
        self._segment_path = lambda: "ydktest-sanity:runner"
        self._is_frozen = True

    def __setattr__(self, name, value):
        self._perform_setattr(Runner, [], name, value)


    class One(_Entity_):
        """
        config for one\_level data
        
        .. attribute:: number
        
        	integer value type
        	**type**\: int
        
        	**range:** \-2147483648..2147483647
        
        .. attribute:: name
        
        	this is string value
        	**type**\: str
        
        .. attribute:: config
        
        	test
        	**type**\: anyxml
        
        .. attribute:: one_aug
        
        	config for one\_level data
        	**type**\:  :py:class:`OneAug <ydk.models.ydktest.ydktest_sanity.Runner.One.OneAug>`
        
        .. attribute:: augmented_leaf
        
        	
        	**type**\: str
        
        .. attribute:: ospf
        
        	Open Shortest Path First (OSPF)
        	**type**\: list of  		 :py:class:`Ospf <ydk.models.ydktest.ydktest_sanity.Runner.One.Ospf>`
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.One, self).__init__()

            self.yang_name = "one"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("ydktest-sanity-augm:one-aug", ("one_aug", Runner.One.OneAug)), ("ydktest-sanity-augm:ospf", ("ospf", Runner.One.Ospf))])
            self._leafs = OrderedDict([
                ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                ('name', (YLeaf(YType.str, 'name'), ['str'])),
                ('config', (YLeaf(YType.str, 'config'), ['str'])),
                ('augmented_leaf', (YLeaf(YType.str, 'ydktest-sanity-augm:augmented-leaf'), ['str'])),
            ])
            self.number = None
            self.name = None
            self.config = None
            self.augmented_leaf = None

            self.one_aug = Runner.One.OneAug()
            self.one_aug.parent = self
            self._children_name_map["one_aug"] = "ydktest-sanity-augm:one-aug"

            self.ospf = YList(self)
            self._segment_path = lambda: "one"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.One, ['number', 'name', 'config', 'augmented_leaf'], name, value)


        class OneAug(_Entity_):
            """
            config for one\_level data
            
            .. attribute:: number
            
            	integer value type
            	**type**\: int
            
            	**range:** \-2147483648..2147483647
            
            .. attribute:: name
            
            	this is string value
            	**type**\: str
            
            

            """

            _prefix = 'ysanity-augm'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.One.OneAug, self).__init__()

                self.yang_name = "one-aug"
                self.yang_parent_name = "one"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                    ('name', (YLeaf(YType.str, 'name'), ['str'])),
                ])
                self.number = None
                self.name = None
                self._segment_path = lambda: "ydktest-sanity-augm:one-aug"
                self._absolute_path = lambda: "ydktest-sanity:runner/one/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Runner.One.OneAug, ['number', 'name'], name, value)



        class Ospf(_Entity_):
            """
            Open Shortest Path First (OSPF)
            
            .. attribute:: id  (key)
            
            	
            	**type**\: int
            
            	**range:** 1..65535
            
            .. attribute:: passive_interface
            
            	Suppress routing updates on an interface
            	**type**\:  :py:class:`PassiveInterface <ydk.models.ydktest.ydktest_sanity.Runner.One.Ospf.PassiveInterface>`
            
            .. attribute:: test
            
            	
            	**type**\: list of  		 :py:class:`Test <ydk.models.ydktest.ydktest_sanity.Runner.One.Ospf.Test>`
            
            

            """

            _prefix = 'ysanity-augm'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.One.Ospf, self).__init__()

                self.yang_name = "ospf"
                self.yang_parent_name = "one"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = ['id']
                self._child_classes = OrderedDict([("passive-interface", ("passive_interface", Runner.One.Ospf.PassiveInterface)), ("test", ("test", Runner.One.Ospf.Test))])
                self._leafs = OrderedDict([
                    ('id', (YLeaf(YType.uint16, 'id'), ['int'])),
                ])
                self.id = None

                self.passive_interface = Runner.One.Ospf.PassiveInterface()
                self.passive_interface.parent = self
                self._children_name_map["passive_interface"] = "passive-interface"

                self.test = YList(self)
                self._segment_path = lambda: "ydktest-sanity-augm:ospf" + "[id='" + str(self.id) + "']"
                self._absolute_path = lambda: "ydktest-sanity:runner/one/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Runner.One.Ospf, ['id'], name, value)


            class PassiveInterface(_Entity_):
                """
                Suppress routing updates on an interface
                
                .. attribute:: interface
                
                	
                	**type**\: str
                
                

                """

                _prefix = 'ysanity-augm'
                _revision = '2015-11-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Runner.One.Ospf.PassiveInterface, self).__init__()

                    self.yang_name = "passive-interface"
                    self.yang_parent_name = "ospf"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('interface', (YLeaf(YType.str, 'interface'), ['str'])),
                    ])
                    self.interface = None
                    self._segment_path = lambda: "passive-interface"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Runner.One.Ospf.PassiveInterface, ['interface'], name, value)



            class Test(_Entity_):
                """
                
                
                .. attribute:: name  (key)
                
                	
                	**type**\: str
                
                

                """

                _prefix = 'ysanity-augm'
                _revision = '2015-11-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Runner.One.Ospf.Test, self).__init__()

                    self.yang_name = "test"
                    self.yang_parent_name = "ospf"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = ['name']
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('name', (YLeaf(YType.str, 'name'), ['str'])),
                    ])
                    self.name = None
                    self._segment_path = lambda: "test" + "[name='" + str(self.name) + "']"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Runner.One.Ospf.Test, ['name'], name, value)





    class Two(_Entity_):
        """
        config for one\_level data
        
        .. attribute:: number
        
        	integer value type
        	**type**\: int
        
        	**range:** \-2147483648..2147483647
        
        .. attribute:: name
        
        	this is string value
        	**type**\: str
        
        .. attribute:: sub1
        
        	subconfig1 for config container
        	**type**\:  :py:class:`Sub1 <ydk.models.ydktest.ydktest_sanity.Runner.Two.Sub1>`
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.Two, self).__init__()

            self.yang_name = "two"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("sub1", ("sub1", Runner.Two.Sub1))])
            self._leafs = OrderedDict([
                ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                ('name', (YLeaf(YType.str, 'name'), ['str'])),
            ])
            self.number = None
            self.name = None

            self.sub1 = Runner.Two.Sub1()
            self.sub1.parent = self
            self._children_name_map["sub1"] = "sub1"
            self._segment_path = lambda: "two"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.Two, ['number', 'name'], name, value)


        class Sub1(_Entity_):
            """
            subconfig1 for config container
            
            .. attribute:: number
            
            	integer value type
            	**type**\: int
            
            	**range:** \-2147483648..2147483647
            
            

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.Two.Sub1, self).__init__()

                self.yang_name = "sub1"
                self.yang_parent_name = "two"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                ])
                self.number = None
                self._segment_path = lambda: "sub1"
                self._absolute_path = lambda: "ydktest-sanity:runner/two/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Runner.Two.Sub1, ['number'], name, value)




    class Three(_Entity_):
        """
        config for one\_level data
        
        .. attribute:: number
        
        	integer value type
        	**type**\: int
        
        	**range:** \-2147483648..2147483647
        
        .. attribute:: name
        
        	this is string value
        	**type**\: str
        
        .. attribute:: sub1
        
        	subconfig1 for config container
        	**type**\:  :py:class:`Sub1 <ydk.models.ydktest.ydktest_sanity.Runner.Three.Sub1>`
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.Three, self).__init__()

            self.yang_name = "three"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("sub1", ("sub1", Runner.Three.Sub1))])
            self._leafs = OrderedDict([
                ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                ('name', (YLeaf(YType.str, 'name'), ['str'])),
            ])
            self.number = None
            self.name = None

            self.sub1 = Runner.Three.Sub1()
            self.sub1.parent = self
            self._children_name_map["sub1"] = "sub1"
            self._segment_path = lambda: "three"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.Three, ['number', 'name'], name, value)


        class Sub1(_Entity_):
            """
            subconfig1 for config container
            
            .. attribute:: number
            
            	integer value type
            	**type**\: int
            
            	**range:** \-2147483648..2147483647
            
            .. attribute:: sub2
            
            	subconfig2 for config container
            	**type**\:  :py:class:`Sub2 <ydk.models.ydktest.ydktest_sanity.Runner.Three.Sub1.Sub2>`
            
            

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.Three.Sub1, self).__init__()

                self.yang_name = "sub1"
                self.yang_parent_name = "three"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([("sub2", ("sub2", Runner.Three.Sub1.Sub2))])
                self._leafs = OrderedDict([
                    ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                ])
                self.number = None

                self.sub2 = Runner.Three.Sub1.Sub2()
                self.sub2.parent = self
                self._children_name_map["sub2"] = "sub2"
                self._segment_path = lambda: "sub1"
                self._absolute_path = lambda: "ydktest-sanity:runner/three/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Runner.Three.Sub1, ['number'], name, value)


            class Sub2(_Entity_):
                """
                subconfig2 for config container
                
                .. attribute:: number
                
                	integer value type
                	**type**\: int
                
                	**range:** \-2147483648..2147483647
                
                

                """

                _prefix = 'ydkut'
                _revision = '2015-11-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Runner.Three.Sub1.Sub2, self).__init__()

                    self.yang_name = "sub2"
                    self.yang_parent_name = "sub1"
                    self.is_top_level_class = False
                    self.has_list_ancestor = False
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                    ])
                    self.number = None
                    self._segment_path = lambda: "sub2"
                    self._absolute_path = lambda: "ydktest-sanity:runner/three/sub1/%s" % self._segment_path()
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Runner.Three.Sub1.Sub2, ['number'], name, value)





    class Ytypes(_Entity_):
        """
        config for one\_level data types
        
        .. attribute:: none
        
        	
        	**type**\:  :py:class:`Y_None <ydk.models.ydktest.ydktest_sanity.Runner.Ytypes.Y_None>`
        
        .. attribute:: enabled
        
        	
        	**type**\: :py:class:`Empty<ydk.types.Empty>`
        
        .. attribute:: built_in_t
        
        	config for built\-in types
        	**type**\:  :py:class:`BuiltInT <ydk.models.ydktest.ydktest_sanity.Runner.Ytypes.BuiltInT>`
        
        .. attribute:: derived_t
        
        	config for one\_level derived data types
        	**type**\:  :py:class:`DerivedT <ydk.models.ydktest.ydktest_sanity.Runner.Ytypes.DerivedT>`
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.Ytypes, self).__init__()

            self.yang_name = "ytypes"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("none", ("none", Runner.Ytypes.Y_None)), ("built-in-t", ("built_in_t", Runner.Ytypes.BuiltInT)), ("derived-t", ("derived_t", Runner.Ytypes.DerivedT))])
            self._leafs = OrderedDict([
                ('enabled', (YLeaf(YType.empty, 'enabled'), ['Empty'])),
            ])
            self.enabled = None

            self.none = Runner.Ytypes.Y_None()
            self.none.parent = self
            self._children_name_map["none"] = "none"

            self.built_in_t = Runner.Ytypes.BuiltInT()
            self.built_in_t.parent = self
            self._children_name_map["built_in_t"] = "built-in-t"

            self.derived_t = Runner.Ytypes.DerivedT()
            self.derived_t.parent = self
            self._children_name_map["derived_t"] = "derived-t"
            self._segment_path = lambda: "ytypes"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.Ytypes, ['enabled'], name, value)


        class Y_None(_Entity_):
            """
            
            
            .. attribute:: test
            
            	
            	**type**\: str
            
            

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.Ytypes.Y_None, self).__init__()

                self.yang_name = "none"
                self.yang_parent_name = "ytypes"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('test', (YLeaf(YType.str, 'test'), ['str'])),
                ])
                self.test = None
                self._segment_path = lambda: "none"
                self._absolute_path = lambda: "ydktest-sanity:runner/ytypes/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Runner.Ytypes.Y_None, ['test'], name, value)



        class BuiltInT(_Entity_):
            """
            config for built\-in types
            
            .. attribute:: number8
            
            	 8 bit integer value type
            	**type**\: int
            
            	**range:** \-128..127
            
            .. attribute:: number16
            
            	16 bit integer value type
            	**type**\: int
            
            	**range:** \-32768..32767
            
            .. attribute:: number32
            
            	integer value type
            	**type**\: int
            
            	**range:** \-2147483648..0 \| 10..10 \| 19..19 \| 1000..2147483647
            
            .. attribute:: number64
            
            	integer value type
            	**type**\: int
            
            	**range:** \-9223372036854775808..9223372036854775807
            
            .. attribute:: u_number8
            
            	 8 bit uinteger value type, must be >=0 & <= 255
            	**type**\: int
            
            	**range:** 0..255
            
            .. attribute:: u_number16
            
            	16 bit uinteger value type, must be >=0 & <= 65025
            	**type**\: int
            
            	**range:** 0..65535
            
            .. attribute:: u_number32
            
            	32 bit uinteger value type
            	**type**\: int
            
            	**range:** 0..4294967295
            
            .. attribute:: u_number64
            
            	64 bit uinteger value type
            	**type**\: int
            
            	**range:** 0..18446744073709551615
            
            .. attribute:: leaf_ref
            
            	leaf\-ref
            	**type**\: int
            
            	**range:** \-128..127
            
            	**refers to**\:  :py:class:`number8 <ydk.models.ydktest.ydktest_sanity.Runner.Ytypes.BuiltInT>`
            
            .. attribute:: deci64
            
            	this is decimal value
            	**type**\: Decimal64
            
            	**range:** 1..3.14 \| 10..10 \| 20..92233720368547758.07
            
            .. attribute:: name
            
            	this is string value
            	**type**\: str
            
            .. attribute:: emptee
            
            	this is empty value
            	**type**\: :py:class:`Empty<ydk.types.Empty>`
            
            .. attribute:: bool_value
            
            	this is boolean type value
            	**type**\: bool
            
            .. attribute:: embeded_enum
            
            	enum embeded in leaf
            	**type**\:  :py:class:`EmbededEnum <ydk.models.ydktest.ydktest_sanity.Runner.Ytypes.BuiltInT.EmbededEnum>`
            
            .. attribute:: enum_leafref
            
            	
            	**type**\:  :py:class:`EmbededEnum <ydk.models.ydktest.ydktest_sanity.Runner.Ytypes.BuiltInT.EmbededEnum>`
            
            .. attribute:: enum_value
            
            	this is enum type value
            	**type**\:  :py:class:`YdkEnumTest <ydk.models.ydktest.ydktest_sanity.YdkEnumTest>`
            
            .. attribute:: enum_int_value
            
            	enum int type
            	**type**\: union of the below types:
            
            		**type**\:  :py:class:`YdkEnumIntTest <ydk.models.ydktest.ydktest_sanity.YdkEnumIntTest>`
            
            		**type**\: int
            
            			**range:** 1..4096
            
            .. attribute:: identity_ref_value
            
            	
            	**type**\:  :py:class:`BaseIdentity <ydk.models.ydktest.ydktest_sanity.BaseIdentity>`
            
            .. attribute:: bincoded
            
            	this is binary value
            	**type**\: str
            
            .. attribute:: bits_value
            
            	this is bits type value
            	**type**\:  :py:class:`YdkBitsType <ydk.models.ydktest.ydktest_types.YdkBitsType>`
            
            	**default value**\: auto-sense-speed
            
            .. attribute:: younion
            
            	union test value
            	**type**\: union of the below types:
            
            		**type**\:  :py:class:`YdkEnumTest <ydk.models.ydktest.ydktest_sanity.YdkEnumTest>`
            
            		**type**\: int
            
            			**range:** 0..63
            
            .. attribute:: llstring
            
            	A list of string
            	**type**\: list of str
            
            .. attribute:: status
            
            	Whether cable is connected or not
            	**type**\:  :py:class:`Status <ydk.models.ydktest.ydktest_sanity.Runner.Ytypes.BuiltInT.Status>`
            
            .. attribute:: bits_llist
            
            	
            	**type**\: list of   :py:class:`BitsLlist <ydk.models.ydktest.ydktest_sanity.Runner.Ytypes.BuiltInT.BitsLlist>`
            
            .. attribute:: enum_llist
            
            	A leaf\-list of enum
            	**type**\: list of   :py:class:`YdkEnumTest <ydk.models.ydktest.ydktest_sanity.YdkEnumTest>`
            
            .. attribute:: identity_llist
            
            	A leaf\-list of identityref
            	**type**\: list of   :py:class:`BaseIdentity <ydk.models.ydktest.ydktest_sanity.BaseIdentity>`
            
            .. attribute:: llunion
            
            	A list of union
            	**type**\: union of the below types:
            
            		**type**\: list of int
            
            			**range:** \-32768..32767
            
            		**type**\: list of str
            
            .. attribute:: younion_recursive
            
            	Recursive union leaf
            	**type**\: union of the below types:
            
            		**type**\: int
            
            			**range:** 0..4294967295
            
            		**type**\: str
            
            		**type**\: int
            
            			**range:** \-128..127
            
            .. attribute:: younion_list
            
            	members of the younion
            	**type**\: union of the below types:
            
            		**type**\: list of int
            
            			**range:** 0..4294967295
            
            		**type**\: list of str
            
            		**type**\: list of str
            
            		**type**\: list of str
            
            

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.Ytypes.BuiltInT, self).__init__()

                self.yang_name = "built-in-t"
                self.yang_parent_name = "ytypes"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('number8', (YLeaf(YType.int8, 'number8'), ['int'])),
                    ('number16', (YLeaf(YType.int16, 'number16'), ['int'])),
                    ('number32', (YLeaf(YType.int32, 'number32'), ['int'])),
                    ('number64', (YLeaf(YType.int64, 'number64'), ['int'])),
                    ('u_number8', (YLeaf(YType.uint8, 'u_number8'), ['int'])),
                    ('u_number16', (YLeaf(YType.uint16, 'u_number16'), ['int'])),
                    ('u_number32', (YLeaf(YType.uint32, 'u_number32'), ['int'])),
                    ('u_number64', (YLeaf(YType.uint64, 'u_number64'), ['int'])),
                    ('leaf_ref', (YLeaf(YType.str, 'leaf-ref'), ['int'])),
                    ('deci64', (YLeaf(YType.str, 'deci64'), ['Decimal64'])),
                    ('name', (YLeaf(YType.str, 'name'), ['str'])),
                    ('emptee', (YLeaf(YType.empty, 'emptee'), ['Empty'])),
                    ('bool_value', (YLeaf(YType.boolean, 'bool-value'), ['bool'])),
                    ('embeded_enum', (YLeaf(YType.enumeration, 'embeded-enum'), [('ydk.models.ydktest.ydktest_sanity', 'Runner', 'Ytypes.BuiltInT.EmbededEnum')])),
                    ('enum_leafref', (YLeaf(YType.enumeration, 'enum-leafref'), [('ydk.models.ydktest.ydktest_sanity', 'Runner', 'Ytypes.BuiltInT.EmbededEnum')])),
                    ('enum_value', (YLeaf(YType.enumeration, 'enum-value'), [('ydk.models.ydktest.ydktest_sanity', 'YdkEnumTest', '')])),
                    ('enum_int_value', (YLeaf(YType.str, 'enum-int-value'), [('ydk.models.ydktest.ydktest_sanity', 'YdkEnumIntTest', ''),'int'])),
                    ('identity_ref_value', (YLeaf(YType.identityref, 'identity-ref-value'), [('ydk.models.ydktest.ydktest_sanity', 'BaseIdentity')])),
                    ('bincoded', (YLeaf(YType.str, 'bincoded'), ['str'])),
                    ('bits_value', (YLeaf(YType.bits, 'bits-value'), ['Bits'])),
                    ('younion', (YLeaf(YType.str, 'younion'), [('ydk.models.ydktest.ydktest_sanity', 'YdkEnumTest', ''),'int'])),
                    ('llstring', (YLeafList(YType.str, 'llstring'), ['str'])),
                    ('status', (YLeaf(YType.enumeration, 'status'), [('ydk.models.ydktest.ydktest_sanity', 'Runner', 'Ytypes.BuiltInT.Status')])),
                    ('bits_llist', (YLeafList(YType.bits, 'bits-llist'), ['Bits'])),
                    ('enum_llist', (YLeafList(YType.enumeration, 'enum-llist'), [('ydk.models.ydktest.ydktest_sanity', 'YdkEnumTest', '')])),
                    ('identity_llist', (YLeafList(YType.identityref, 'identity-llist'), [('ydk.models.ydktest.ydktest_sanity', 'BaseIdentity')])),
                    ('llunion', (YLeafList(YType.str, 'llunion'), ['int','str'])),
                    ('younion_recursive', (YLeaf(YType.str, 'younion-recursive'), ['int','str','int'])),
                    ('younion_list', (YLeafList(YType.str, 'younion-list'), ['int','str','str','str'])),
                ])
                self.number8 = None
                self.number16 = None
                self.number32 = None
                self.number64 = None
                self.u_number8 = None
                self.u_number16 = None
                self.u_number32 = None
                self.u_number64 = None
                self.leaf_ref = None
                self.deci64 = None
                self.name = None
                self.emptee = None
                self.bool_value = None
                self.embeded_enum = None
                self.enum_leafref = None
                self.enum_value = None
                self.enum_int_value = None
                self.identity_ref_value = None
                self.bincoded = None
                self.bits_value = Bits()
                self.younion = None
                self.llstring = []
                self.status = None
                self.bits_llist = []
                self.enum_llist = []
                self.identity_llist = []
                self.llunion = []
                self.younion_recursive = None
                self.younion_list = []
                self._segment_path = lambda: "built-in-t"
                self._absolute_path = lambda: "ydktest-sanity:runner/ytypes/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Runner.Ytypes.BuiltInT, ['number8', 'number16', 'number32', 'number64', 'u_number8', 'u_number16', 'u_number32', 'u_number64', 'leaf_ref', 'deci64', 'name', 'emptee', 'bool_value', 'embeded_enum', 'enum_leafref', 'enum_value', 'enum_int_value', 'identity_ref_value', 'bincoded', 'bits_value', 'younion', 'llstring', 'status', 'bits_llist', 'enum_llist', 'identity_llist', 'llunion', 'younion_recursive', 'younion_list'], name, value)

            class EmbededEnum(Enum):
                """
                EmbededEnum (Enum Class)

                enum embeded in leaf

                .. data:: zero = 0

                .. data:: two = 1

                .. data:: seven = 7

                """

                zero = Enum.YLeaf(0, "zero")

                two = Enum.YLeaf(1, "two")

                seven = Enum.YLeaf(7, "seven")


            class Status(Enum):
                """
                Status (Enum Class)

                Whether cable is connected or not

                .. data:: good = 0

                .. data:: not_connected = 1

                """

                good = Enum.YLeaf(0, "good")

                not_connected = Enum.YLeaf(1, "not connected")




        class DerivedT(_Entity_):
            """
            config for one\_level derived data types
            
            

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.Ytypes.DerivedT, self).__init__()

                self.yang_name = "derived-t"
                self.yang_parent_name = "ytypes"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict()
                self._segment_path = lambda: "derived-t"
                self._absolute_path = lambda: "ydktest-sanity:runner/ytypes/%s" % self._segment_path()
                self._is_frozen = True




    class OneList(_Entity_):
        """
        config for one\_level list data
        
        .. attribute:: ldata
        
        	one list data
        	**type**\: list of  		 :py:class:`Ldata <ydk.models.ydktest.ydktest_sanity.Runner.OneList.Ldata>`
        
        .. attribute:: identity_list
        
        	one list data
        	**type**\: list of  		 :py:class:`IdentityList <ydk.models.ydktest.ydktest_sanity.Runner.OneList.IdentityList>`
        
        .. attribute:: one_aug_list
        
        	config for one\_level list data
        	**type**\:  :py:class:`OneAugList <ydk.models.ydktest.ydktest_sanity.Runner.OneList.OneAugList>`
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.OneList, self).__init__()

            self.yang_name = "one-list"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("ldata", ("ldata", Runner.OneList.Ldata)), ("identity-list", ("identity_list", Runner.OneList.IdentityList)), ("ydktest-sanity-augm:one-aug-list", ("one_aug_list", Runner.OneList.OneAugList))])
            self._leafs = OrderedDict()

            self.one_aug_list = Runner.OneList.OneAugList()
            self.one_aug_list.parent = self
            self._children_name_map["one_aug_list"] = "ydktest-sanity-augm:one-aug-list"

            self.ldata = YList(self)
            self.identity_list = YList(self)
            self._segment_path = lambda: "one-list"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.OneList, [], name, value)


        class Ldata(_Entity_):
            """
            one list data
            
            .. attribute:: number  (key)
            
            	integer value type
            	**type**\: int
            
            	**range:** \-2147483648..2147483647
            
            .. attribute:: name
            
            	this is string value
            	**type**\: str
            
            

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.OneList.Ldata, self).__init__()

                self.yang_name = "ldata"
                self.yang_parent_name = "one-list"
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
                self._absolute_path = lambda: "ydktest-sanity:runner/one-list/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Runner.OneList.Ldata, ['number', 'name'], name, value)



        class IdentityList(_Entity_):
            """
            one list data
            
            .. attribute:: id_ref  (key)
            
            	leafref key
            	**type**\:  :py:class:`BaseIdentity <ydk.models.ydktest.ydktest_sanity.BaseIdentity>`
            
            .. attribute:: config
            
            	
            	**type**\:  :py:class:`Config <ydk.models.ydktest.ydktest_sanity.Runner.OneList.IdentityList.Config>`
            
            

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.OneList.IdentityList, self).__init__()

                self.yang_name = "identity-list"
                self.yang_parent_name = "one-list"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = ['id_ref']
                self._child_classes = OrderedDict([("config", ("config", Runner.OneList.IdentityList.Config))])
                self._leafs = OrderedDict([
                    ('id_ref', (YLeaf(YType.identityref, 'id-ref'), [('ydk.models.ydktest.ydktest_sanity', 'BaseIdentity')])),
                ])
                self.id_ref = None

                self.config = Runner.OneList.IdentityList.Config()
                self.config.parent = self
                self._children_name_map["config"] = "config"
                self._segment_path = lambda: "identity-list" + "[id-ref='" + str(self.id_ref) + "']"
                self._absolute_path = lambda: "ydktest-sanity:runner/one-list/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Runner.OneList.IdentityList, ['id_ref'], name, value)


            class Config(_Entity_):
                """
                
                
                .. attribute:: id
                
                	base id id ref
                	**type**\:  :py:class:`BaseIdentity <ydk.models.ydktest.ydktest_sanity.BaseIdentity>`
                
                

                """

                _prefix = 'ydkut'
                _revision = '2015-11-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Runner.OneList.IdentityList.Config, self).__init__()

                    self.yang_name = "config"
                    self.yang_parent_name = "identity-list"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('id', (YLeaf(YType.identityref, 'id'), [('ydk.models.ydktest.ydktest_sanity', 'BaseIdentity')])),
                    ])
                    self.id = None
                    self._segment_path = lambda: "config"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Runner.OneList.IdentityList.Config, ['id'], name, value)




        class OneAugList(_Entity_):
            """
            config for one\_level list data
            
            .. attribute:: ldata
            
            	one list data
            	**type**\: list of  		 :py:class:`Ldata <ydk.models.ydktest.ydktest_sanity.Runner.OneList.OneAugList.Ldata>`
            
            .. attribute:: enabled
            
            	integer value type
            	**type**\: bool
            
            

            """

            _prefix = 'ysanity-augm'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.OneList.OneAugList, self).__init__()

                self.yang_name = "one-aug-list"
                self.yang_parent_name = "one-list"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([("ldata", ("ldata", Runner.OneList.OneAugList.Ldata))])
                self._leafs = OrderedDict([
                    ('enabled', (YLeaf(YType.boolean, 'enabled'), ['bool'])),
                ])
                self.enabled = None

                self.ldata = YList(self)
                self._segment_path = lambda: "ydktest-sanity-augm:one-aug-list"
                self._absolute_path = lambda: "ydktest-sanity:runner/one-list/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Runner.OneList.OneAugList, ['enabled'], name, value)


            class Ldata(_Entity_):
                """
                one list data
                
                .. attribute:: number  (key)
                
                	integer value type
                	**type**\: int
                
                	**range:** \-2147483648..2147483647
                
                .. attribute:: name
                
                	this is string value
                	**type**\: str
                
                

                """

                _prefix = 'ysanity-augm'
                _revision = '2015-11-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Runner.OneList.OneAugList.Ldata, self).__init__()

                    self.yang_name = "ldata"
                    self.yang_parent_name = "one-aug-list"
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
                    self._absolute_path = lambda: "ydktest-sanity:runner/one-list/ydktest-sanity-augm:one-aug-list/%s" % self._segment_path()
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Runner.OneList.OneAugList.Ldata, ['number', 'name'], name, value)





    class TwoList(_Entity_):
        """
        config for one\_level list data
        
        .. attribute:: ldata
        
        	one list data
        	**type**\: list of  		 :py:class:`Ldata <ydk.models.ydktest.ydktest_sanity.Runner.TwoList.Ldata>`
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.TwoList, self).__init__()

            self.yang_name = "two-list"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("ldata", ("ldata", Runner.TwoList.Ldata))])
            self._leafs = OrderedDict()

            self.ldata = YList(self)
            self._segment_path = lambda: "two-list"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.TwoList, [], name, value)


        class Ldata(_Entity_):
            """
            one list data
            
            .. attribute:: number  (key)
            
            	integer value type
            	**type**\: int
            
            	**range:** \-2147483648..2147483647
            
            .. attribute:: name
            
            	this is string value
            	**type**\: str
            
            .. attribute:: subl1
            
            	one list data
            	**type**\: list of  		 :py:class:`Subl1 <ydk.models.ydktest.ydktest_sanity.Runner.TwoList.Ldata.Subl1>`
            
            

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.TwoList.Ldata, self).__init__()

                self.yang_name = "ldata"
                self.yang_parent_name = "two-list"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = ['number']
                self._child_classes = OrderedDict([("subl1", ("subl1", Runner.TwoList.Ldata.Subl1))])
                self._leafs = OrderedDict([
                    ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                    ('name', (YLeaf(YType.str, 'name'), ['str'])),
                ])
                self.number = None
                self.name = None

                self.subl1 = YList(self)
                self._segment_path = lambda: "ldata" + "[number='" + str(self.number) + "']"
                self._absolute_path = lambda: "ydktest-sanity:runner/two-list/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Runner.TwoList.Ldata, ['number', 'name'], name, value)


            class Subl1(_Entity_):
                """
                one list data
                
                .. attribute:: number  (key)
                
                	integer value type
                	**type**\: int
                
                	**range:** \-2147483648..2147483647
                
                .. attribute:: name
                
                	this is string value
                	**type**\: str
                
                

                """

                _prefix = 'ydkut'
                _revision = '2015-11-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Runner.TwoList.Ldata.Subl1, self).__init__()

                    self.yang_name = "subl1"
                    self.yang_parent_name = "ldata"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = ['number']
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                        ('name', (YLeaf(YType.str, 'name'), ['str'])),
                    ])
                    self.number = None
                    self.name = None
                    self._segment_path = lambda: "subl1" + "[number='" + str(self.number) + "']"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Runner.TwoList.Ldata.Subl1, ['number', 'name'], name, value)





    class ThreeList(_Entity_):
        """
        config for one\_level list data
        
        .. attribute:: ldata
        
        	one list data
        	**type**\: list of  		 :py:class:`Ldata <ydk.models.ydktest.ydktest_sanity.Runner.ThreeList.Ldata>`
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.ThreeList, self).__init__()

            self.yang_name = "three-list"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("ldata", ("ldata", Runner.ThreeList.Ldata))])
            self._leafs = OrderedDict()

            self.ldata = YList(self)
            self._segment_path = lambda: "three-list"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.ThreeList, [], name, value)


        class Ldata(_Entity_):
            """
            one list data
            
            .. attribute:: number  (key)
            
            	integer value type
            	**type**\: int
            
            	**range:** \-2147483648..2147483647
            
            .. attribute:: name
            
            	this is string value
            	**type**\: str
            
            .. attribute:: subl1
            
            	one list data
            	**type**\: list of  		 :py:class:`Subl1 <ydk.models.ydktest.ydktest_sanity.Runner.ThreeList.Ldata.Subl1>`
            
            

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.ThreeList.Ldata, self).__init__()

                self.yang_name = "ldata"
                self.yang_parent_name = "three-list"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = ['number']
                self._child_classes = OrderedDict([("subl1", ("subl1", Runner.ThreeList.Ldata.Subl1))])
                self._leafs = OrderedDict([
                    ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                    ('name', (YLeaf(YType.str, 'name'), ['str'])),
                ])
                self.number = None
                self.name = None

                self.subl1 = YList(self)
                self._segment_path = lambda: "ldata" + "[number='" + str(self.number) + "']"
                self._absolute_path = lambda: "ydktest-sanity:runner/three-list/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Runner.ThreeList.Ldata, ['number', 'name'], name, value)


            class Subl1(_Entity_):
                """
                one list data
                
                .. attribute:: number  (key)
                
                	integer value type
                	**type**\: int
                
                	**range:** \-2147483648..2147483647
                
                .. attribute:: name
                
                	this is string value
                	**type**\: str
                
                .. attribute:: sub_subl1
                
                	one list data
                	**type**\: list of  		 :py:class:`SubSubl1 <ydk.models.ydktest.ydktest_sanity.Runner.ThreeList.Ldata.Subl1.SubSubl1>`
                
                

                """

                _prefix = 'ydkut'
                _revision = '2015-11-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Runner.ThreeList.Ldata.Subl1, self).__init__()

                    self.yang_name = "subl1"
                    self.yang_parent_name = "ldata"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = ['number']
                    self._child_classes = OrderedDict([("sub-subl1", ("sub_subl1", Runner.ThreeList.Ldata.Subl1.SubSubl1))])
                    self._leafs = OrderedDict([
                        ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                        ('name', (YLeaf(YType.str, 'name'), ['str'])),
                    ])
                    self.number = None
                    self.name = None

                    self.sub_subl1 = YList(self)
                    self._segment_path = lambda: "subl1" + "[number='" + str(self.number) + "']"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Runner.ThreeList.Ldata.Subl1, ['number', 'name'], name, value)


                class SubSubl1(_Entity_):
                    """
                    one list data
                    
                    .. attribute:: number  (key)
                    
                    	integer value type
                    	**type**\: int
                    
                    	**range:** \-2147483648..2147483647
                    
                    .. attribute:: name
                    
                    	this is string value
                    	**type**\: str
                    
                    

                    """

                    _prefix = 'ydkut'
                    _revision = '2015-11-17'

                    def __init__(self):
                        if sys.version_info > (3,):
                            super().__init__()
                        else:
                            super(Runner.ThreeList.Ldata.Subl1.SubSubl1, self).__init__()

                        self.yang_name = "sub-subl1"
                        self.yang_parent_name = "subl1"
                        self.is_top_level_class = False
                        self.has_list_ancestor = True
                        self.ylist_key_names = ['number']
                        self._child_classes = OrderedDict([])
                        self._leafs = OrderedDict([
                            ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                            ('name', (YLeaf(YType.str, 'name'), ['str'])),
                        ])
                        self.number = None
                        self.name = None
                        self._segment_path = lambda: "sub-subl1" + "[number='" + str(self.number) + "']"
                        self._is_frozen = True

                    def __setattr__(self, name, value):
                        self._perform_setattr(Runner.ThreeList.Ldata.Subl1.SubSubl1, ['number', 'name'], name, value)






    class InbtwList(_Entity_):
        """
        config for one\_level list data
        
        .. attribute:: ldata
        
        	one list data
        	**type**\: list of  		 :py:class:`Ldata <ydk.models.ydktest.ydktest_sanity.Runner.InbtwList.Ldata>`
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.InbtwList, self).__init__()

            self.yang_name = "inbtw-list"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("ldata", ("ldata", Runner.InbtwList.Ldata))])
            self._leafs = OrderedDict()

            self.ldata = YList(self)
            self._segment_path = lambda: "inbtw-list"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.InbtwList, [], name, value)


        class Ldata(_Entity_):
            """
            one list data
            
            .. attribute:: number  (key)
            
            	integer value type
            	**type**\: int
            
            	**range:** \-2147483648..2147483647
            
            .. attribute:: name
            
            	this is string value
            	**type**\: str
            
            .. attribute:: subc
            
            	one list subcontainer data
            	**type**\:  :py:class:`Subc <ydk.models.ydktest.ydktest_sanity.Runner.InbtwList.Ldata.Subc>`
            
            

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.InbtwList.Ldata, self).__init__()

                self.yang_name = "ldata"
                self.yang_parent_name = "inbtw-list"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = ['number']
                self._child_classes = OrderedDict([("subc", ("subc", Runner.InbtwList.Ldata.Subc))])
                self._leafs = OrderedDict([
                    ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                    ('name', (YLeaf(YType.str, 'name'), ['str'])),
                ])
                self.number = None
                self.name = None

                self.subc = Runner.InbtwList.Ldata.Subc()
                self.subc.parent = self
                self._children_name_map["subc"] = "subc"
                self._segment_path = lambda: "ldata" + "[number='" + str(self.number) + "']"
                self._absolute_path = lambda: "ydktest-sanity:runner/inbtw-list/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Runner.InbtwList.Ldata, ['number', 'name'], name, value)


            class Subc(_Entity_):
                """
                one list subcontainer data
                
                .. attribute:: number
                
                	integer value type
                	**type**\: int
                
                	**range:** \-2147483648..2147483647
                
                .. attribute:: name
                
                	this is string value
                	**type**\: str
                
                .. attribute:: subc_subl1
                
                	one list data
                	**type**\: list of  		 :py:class:`SubcSubl1 <ydk.models.ydktest.ydktest_sanity.Runner.InbtwList.Ldata.Subc.SubcSubl1>`
                
                

                """

                _prefix = 'ydkut'
                _revision = '2015-11-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Runner.InbtwList.Ldata.Subc, self).__init__()

                    self.yang_name = "subc"
                    self.yang_parent_name = "ldata"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([("subc-subl1", ("subc_subl1", Runner.InbtwList.Ldata.Subc.SubcSubl1))])
                    self._leafs = OrderedDict([
                        ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                        ('name', (YLeaf(YType.str, 'name'), ['str'])),
                    ])
                    self.number = None
                    self.name = None

                    self.subc_subl1 = YList(self)
                    self._segment_path = lambda: "subc"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Runner.InbtwList.Ldata.Subc, ['number', 'name'], name, value)


                class SubcSubl1(_Entity_):
                    """
                    one list data
                    
                    .. attribute:: number  (key)
                    
                    	integer value type
                    	**type**\: int
                    
                    	**range:** \-2147483648..2147483647
                    
                    .. attribute:: name
                    
                    	this is string value
                    	**type**\: str
                    
                    

                    """

                    _prefix = 'ydkut'
                    _revision = '2015-11-17'

                    def __init__(self):
                        if sys.version_info > (3,):
                            super().__init__()
                        else:
                            super(Runner.InbtwList.Ldata.Subc.SubcSubl1, self).__init__()

                        self.yang_name = "subc-subl1"
                        self.yang_parent_name = "subc"
                        self.is_top_level_class = False
                        self.has_list_ancestor = True
                        self.ylist_key_names = ['number']
                        self._child_classes = OrderedDict([])
                        self._leafs = OrderedDict([
                            ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                            ('name', (YLeaf(YType.str, 'name'), ['str'])),
                        ])
                        self.number = None
                        self.name = None
                        self._segment_path = lambda: "subc-subl1" + "[number='" + str(self.number) + "']"
                        self._is_frozen = True

                    def __setattr__(self, name, value):
                        self._perform_setattr(Runner.InbtwList.Ldata.Subc.SubcSubl1, ['number', 'name'], name, value)






    class TwoKeyList(_Entity_):
        """
        
        
        .. attribute:: first  (key)
        
        	
        	**type**\: str
        
        .. attribute:: second  (key)
        
        	
        	**type**\: int
        
        	**range:** 0..4294967295
        
        .. attribute:: property
        
        	
        	**type**\: str
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.TwoKeyList, self).__init__()

            self.yang_name = "two-key-list"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = ['first','second']
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('first', (YLeaf(YType.str, 'first'), ['str'])),
                ('second', (YLeaf(YType.uint32, 'second'), ['int'])),
                ('property', (YLeaf(YType.str, 'property'), ['str'])),
            ])
            self.first = None
            self.second = None
            self.property = None
            self._segment_path = lambda: "two-key-list" + "[first='" + str(self.first) + "']" + "[second='" + str(self.second) + "']"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.TwoKeyList, ['first', 'second', 'property'], name, value)



    class IdentityList(_Entity_):
        """
        
        
        .. attribute:: name  (key)
        
        	
        	**type**\:  :py:class:`BaseIdentity <ydk.models.ydktest.ydktest_sanity.BaseIdentity>`
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.IdentityList, self).__init__()

            self.yang_name = "identity-list"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = ['name']
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('name', (YLeaf(YType.identityref, 'name'), [('ydk.models.ydktest.ydktest_sanity', 'BaseIdentity')])),
            ])
            self.name = None
            self._segment_path = lambda: "identity-list" + "[name='" + str(self.name) + "']"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.IdentityList, ['name'], name, value)



    class EnumList(_Entity_):
        """
        
        
        .. attribute:: key_name  (key)
        
        	
        	**type**\:  :py:class:`YdkEnumTest <ydk.models.ydktest.ydktest_sanity.YdkEnumTest>`
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.EnumList, self).__init__()

            self.yang_name = "enum-list"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = ['key_name']
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('key_name', (YLeaf(YType.enumeration, 'key-name'), [('ydk.models.ydktest.ydktest_sanity', 'YdkEnumTest', '')])),
            ])
            self.key_name = None
            self._segment_path = lambda: "enum-list" + "[key-name='" + str(self.key_name) + "']"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.EnumList, ['key_name'], name, value)



    class LeafRef(_Entity_):
        """
        
        
        .. attribute:: ref_one_name
        
        	
        	**type**\: str
        
        	**refers to**\:  :py:class:`name <ydk.models.ydktest.ydktest_sanity.Runner.One>`
        
        .. attribute:: ref_two_sub1_number
        
        	
        	**type**\: int
        
        	**range:** \-2147483648..2147483647
        
        	**refers to**\:  :py:class:`number <ydk.models.ydktest.ydktest_sanity.Runner.Two.Sub1>`
        
        .. attribute:: ref_three_sub1_sub2_number
        
        	
        	**type**\: int
        
        	**range:** \-2147483648..2147483647
        
        	**refers to**\:  :py:class:`number <ydk.models.ydktest.ydktest_sanity.Runner.Three.Sub1.Sub2>`
        
        .. attribute:: ref_inbtw
        
        	
        	**type**\: str
        
        	**refers to**\:  :py:class:`name <ydk.models.ydktest.ydktest_sanity.Runner.InbtwList.Ldata.Subc.SubcSubl1>`
        
        .. attribute:: one
        
        	
        	**type**\:  :py:class:`One <ydk.models.ydktest.ydktest_sanity.Runner.LeafRef.One>`
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.LeafRef, self).__init__()

            self.yang_name = "leaf-ref"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("one", ("one", Runner.LeafRef.One))])
            self._leafs = OrderedDict([
                ('ref_one_name', (YLeaf(YType.str, 'ref-one-name'), ['str'])),
                ('ref_two_sub1_number', (YLeaf(YType.str, 'ref-two-sub1-number'), ['int'])),
                ('ref_three_sub1_sub2_number', (YLeaf(YType.str, 'ref-three-sub1-sub2-number'), ['int'])),
                ('ref_inbtw', (YLeaf(YType.str, 'ref-inbtw'), ['str'])),
            ])
            self.ref_one_name = None
            self.ref_two_sub1_number = None
            self.ref_three_sub1_sub2_number = None
            self.ref_inbtw = None

            self.one = Runner.LeafRef.One()
            self.one.parent = self
            self._children_name_map["one"] = "one"
            self._segment_path = lambda: "leaf-ref"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.LeafRef, ['ref_one_name', 'ref_two_sub1_number', 'ref_three_sub1_sub2_number', 'ref_inbtw'], name, value)


        class One(_Entity_):
            """
            
            
            .. attribute:: name_of_one
            
            	
            	**type**\: str
            
            	**pattern:** (([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])\\.){3}([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])(%[\\p{N}\\p{L}]+)?
            
            .. attribute:: two
            
            	
            	**type**\:  :py:class:`Two <ydk.models.ydktest.ydktest_sanity.Runner.LeafRef.One.Two>`
            
            

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.LeafRef.One, self).__init__()

                self.yang_name = "one"
                self.yang_parent_name = "leaf-ref"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([("two", ("two", Runner.LeafRef.One.Two))])
                self._leafs = OrderedDict([
                    ('name_of_one', (YLeaf(YType.str, 'name-of-one'), ['str'])),
                ])
                self.name_of_one = None

                self.two = Runner.LeafRef.One.Two()
                self.two.parent = self
                self._children_name_map["two"] = "two"
                self._segment_path = lambda: "one"
                self._absolute_path = lambda: "ydktest-sanity:runner/leaf-ref/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Runner.LeafRef.One, ['name_of_one'], name, value)


            class Two(_Entity_):
                """
                
                
                .. attribute:: self_ref_one_name
                
                	
                	**type**\: str
                
                	**refers to**\:  :py:class:`ref_one_name <ydk.models.ydktest.ydktest_sanity.Runner.LeafRef>`
                
                

                """

                _prefix = 'ydkut'
                _revision = '2015-11-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Runner.LeafRef.One.Two, self).__init__()

                    self.yang_name = "two"
                    self.yang_parent_name = "one"
                    self.is_top_level_class = False
                    self.has_list_ancestor = False
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('self_ref_one_name', (YLeaf(YType.str, 'self-ref-one-name'), ['str'])),
                    ])
                    self.self_ref_one_name = None
                    self._segment_path = lambda: "two"
                    self._absolute_path = lambda: "ydktest-sanity:runner/leaf-ref/one/%s" % self._segment_path()
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Runner.LeafRef.One.Two, ['self_ref_one_name'], name, value)





    class NotSupported1(_Entity_):
        """
        
        
        .. attribute:: not_supported_1_2
        
        	
        	**type**\:  :py:class:`NotSupported12 <ydk.models.ydktest.ydktest_sanity.Runner.NotSupported1.NotSupported12>`
        
        .. attribute:: not_supported_leaf
        
        	
        	**type**\: str
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.NotSupported1, self).__init__()

            self.yang_name = "not-supported-1"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("not-supported-1-2", ("not_supported_1_2", Runner.NotSupported1.NotSupported12))])
            self._leafs = OrderedDict([
                ('not_supported_leaf', (YLeaf(YType.str, 'not-supported-leaf'), ['str'])),
            ])
            self.not_supported_leaf = None

            self.not_supported_1_2 = Runner.NotSupported1.NotSupported12()
            self.not_supported_1_2.parent = self
            self._children_name_map["not_supported_1_2"] = "not-supported-1-2"
            self._segment_path = lambda: "not-supported-1"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.NotSupported1, ['not_supported_leaf'], name, value)


        class NotSupported12(_Entity_):
            """
            
            
            .. attribute:: some_leaf
            
            	
            	**type**\: str
            
            

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.NotSupported1.NotSupported12, self).__init__()

                self.yang_name = "not-supported-1-2"
                self.yang_parent_name = "not-supported-1"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('some_leaf', (YLeaf(YType.str, 'some-leaf'), ['str'])),
                ])
                self.some_leaf = None
                self._segment_path = lambda: "not-supported-1-2"
                self._absolute_path = lambda: "ydktest-sanity:runner/not-supported-1/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Runner.NotSupported1.NotSupported12, ['some_leaf'], name, value)




    class NotSupported2(_Entity_):
        """
        
        
        .. attribute:: number  (key)
        
        	Integer key for not supported list
        	**type**\: int
        
        	**range:** \-2147483648..2147483647
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.NotSupported2, self).__init__()

            self.yang_name = "not-supported-2"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = ['number']
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('number', (YLeaf(YType.int32, 'number'), ['int'])),
            ])
            self.number = None
            self._segment_path = lambda: "not-supported-2" + "[number='" + str(self.number) + "']"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.NotSupported2, ['number'], name, value)



    class OneReadOnly(_Entity_):
        """
        one\_read\_only data
        
        .. attribute:: number
        
        	integer value type
        	**type**\: int
        
        	**range:** \-2147483648..2147483647
        
        	**config**\: False
        
        .. attribute:: name
        
        	this is string value
        	**type**\: str
        
        	**config**\: False
        
        .. attribute:: config
        
        	test
        	**type**\: anyxml
        
        	**config**\: False
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.OneReadOnly, self).__init__()

            self.yang_name = "one-read-only"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('number', (YLeaf(YType.int32, 'number'), ['int'])),
                ('name', (YLeaf(YType.str, 'name'), ['str'])),
                ('config', (YLeaf(YType.str, 'config'), ['str'])),
            ])
            self.number = None
            self.name = None
            self.config = None
            self._segment_path = lambda: "one-read-only"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.OneReadOnly, ['number', 'name', 'config'], name, value)



    class Mtus(_Entity_):
        """
        
        
        .. attribute:: mtu
        
        	
        	**type**\: list of  		 :py:class:`Mtu <ydk.models.ydktest.ydktest_sanity.Runner.Mtus.Mtu>`
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.Mtus, self).__init__()

            self.yang_name = "mtus"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("mtu", ("mtu", Runner.Mtus.Mtu))])
            self._leafs = OrderedDict()

            self.mtu = YList(self)
            self._segment_path = lambda: "mtus"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.Mtus, [], name, value)


        class Mtu(_Entity_):
            """
            
            
            .. attribute:: owner  (key)
            
            	
            	**type**\: str
            
            .. attribute:: mtu
            
            	
            	**type**\: int
            
            	**range:** 10..8000
            
            	**mandatory**\: True
            
            

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.Mtus.Mtu, self).__init__()

                self.yang_name = "mtu"
                self.yang_parent_name = "mtus"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = ['owner']
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('owner', (YLeaf(YType.str, 'owner'), ['str'])),
                    ('mtu', (YLeaf(YType.int32, 'mtu'), ['int'])),
                ])
                self.owner = None
                self.mtu = None
                self._segment_path = lambda: "mtu" + "[owner='" + str(self.owner) + "']"
                self._absolute_path = lambda: "ydktest-sanity:runner/mtus/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Runner.Mtus.Mtu, ['owner', 'mtu'], name, value)




    class Passive(_Entity_):
        """
        
        
        .. attribute:: name  (key)
        
        	
        	**type**\: str
        
        .. attribute:: interfac
        
        	
        	**type**\: list of  		 :py:class:`Interfac <ydk.models.ydktest.ydktest_sanity.Runner.Passive.Interfac>`
        
        .. attribute:: testc
        
        	
        	**type**\:  :py:class:`Testc <ydk.models.ydktest.ydktest_sanity.Runner.Passive.Testc>`
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.Passive, self).__init__()

            self.yang_name = "passive"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = ['name']
            self._child_classes = OrderedDict([("interfac", ("interfac", Runner.Passive.Interfac)), ("ydktest-sanity-augm:testc", ("testc", Runner.Passive.Testc))])
            self._leafs = OrderedDict([
                ('name', (YLeaf(YType.str, 'name'), ['str'])),
            ])
            self.name = None

            self.testc = Runner.Passive.Testc()
            self.testc.parent = self
            self._children_name_map["testc"] = "ydktest-sanity-augm:testc"

            self.interfac = YList(self)
            self._segment_path = lambda: "passive" + "[name='" + str(self.name) + "']"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.Passive, ['name'], name, value)


        class Interfac(_Entity_):
            """
            
            
            .. attribute:: test  (key)
            
            	
            	**type**\: str
            
            

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.Passive.Interfac, self).__init__()

                self.yang_name = "interfac"
                self.yang_parent_name = "passive"
                self.is_top_level_class = False
                self.has_list_ancestor = True
                self.ylist_key_names = ['test']
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('test', (YLeaf(YType.str, 'test'), ['str'])),
                ])
                self.test = None
                self._segment_path = lambda: "interfac" + "[test='" + str(self.test) + "']"
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Runner.Passive.Interfac, ['test'], name, value)



        class Testc(_Entity_):
            """
            
            
            .. attribute:: xyz
            
            	
            	**type**\:  :py:class:`Xyz <ydk.models.ydktest.ydktest_sanity.Runner.Passive.Testc.Xyz>`
            
            	**presence node**\: True
            
            

            """

            _prefix = 'ysanity-augm'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.Passive.Testc, self).__init__()

                self.yang_name = "testc"
                self.yang_parent_name = "passive"
                self.is_top_level_class = False
                self.has_list_ancestor = True
                self.ylist_key_names = []
                self._child_classes = OrderedDict([("xyz", ("xyz", Runner.Passive.Testc.Xyz))])
                self._leafs = OrderedDict()

                self.xyz = None
                self._children_name_map["xyz"] = "xyz"
                self._segment_path = lambda: "ydktest-sanity-augm:testc"
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Runner.Passive.Testc, [], name, value)


            class Xyz(_Entity_):
                """
                
                
                .. attribute:: xyz
                
                	
                	**type**\: int
                
                	**range:** 0..4294967295
                
                

                This class is a :ref:`presence class<presence-class>`

                """

                _prefix = 'ysanity-augm'
                _revision = '2015-11-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Runner.Passive.Testc.Xyz, self).__init__()

                    self.yang_name = "xyz"
                    self.yang_parent_name = "testc"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([])
                    self.is_presence_container = True
                    self._leafs = OrderedDict([
                        ('xyz', (YLeaf(YType.uint32, 'xyz'), ['int'])),
                    ])
                    self.xyz = None
                    self._segment_path = lambda: "xyz"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Runner.Passive.Testc.Xyz, ['xyz'], name, value)





    class Outer(_Entity_):
        """
        
        
        .. attribute:: inner
        
        	
        	**type**\:  :py:class:`Inner <ydk.models.ydktest.ydktest_sanity.Runner.Outer.Inner>`
        
        	**presence node**\: True
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.Outer, self).__init__()

            self.yang_name = "outer"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("inner", ("inner", Runner.Outer.Inner))])
            self._leafs = OrderedDict()

            self.inner = None
            self._children_name_map["inner"] = "inner"
            self._segment_path = lambda: "outer"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.Outer, [], name, value)


        class Inner(_Entity_):
            """
            
            
            

            This class is a :ref:`presence class<presence-class>`

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.Outer.Inner, self).__init__()

                self.yang_name = "inner"
                self.yang_parent_name = "outer"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self.is_presence_container = True
                self._leafs = OrderedDict()
                self._segment_path = lambda: "inner"
                self._absolute_path = lambda: "ydktest-sanity:runner/outer/%s" % self._segment_path()
                self._is_frozen = True




    class Runner2(_Entity_):
        """
        
        
        .. attribute:: some_leaf
        
        	
        	**type**\: str
        
        

        This class is a :ref:`presence class<presence-class>`

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.Runner2, self).__init__()

            self.yang_name = "runner-2"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([])
            self.is_presence_container = True
            self._leafs = OrderedDict([
                ('some_leaf', (YLeaf(YType.str, 'some-leaf'), ['str'])),
            ])
            self.some_leaf = None
            self._segment_path = lambda: "runner-2"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.Runner2, ['some_leaf'], name, value)



    class NoKeyList(_Entity_):
        """
        
        
        .. attribute:: test
        
        	
        	**type**\: str
        
        	**config**\: False
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.NoKeyList, self).__init__()

            self.yang_name = "no-key-list"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('test', (YLeaf(YType.str, 'test'), ['str'])),
            ])
            self.test = None
            self._segment_path = lambda: "no-key-list"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.NoKeyList, ['test'], name, value)



    class OneKeyList(_Entity_):
        """
        
        
        .. attribute:: testy  (key)
        
        	
        	**type**\: str
        
        .. attribute:: test
        
        	
        	**type**\:  :py:class:`Test <ydk.models.ydktest.ydktest_sanity.Runner.OneKeyList.Test>`
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.OneKeyList, self).__init__()

            self.yang_name = "one-key-list"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = ['testy']
            self._child_classes = OrderedDict([("test", ("test", Runner.OneKeyList.Test))])
            self._leafs = OrderedDict([
                ('testy', (YLeaf(YType.str, 'testy'), ['str'])),
            ])
            self.testy = None

            self.test = Runner.OneKeyList.Test()
            self.test.parent = self
            self._children_name_map["test"] = "test"
            self._segment_path = lambda: "one-key-list" + "[testy='" + str(self.testy) + "']"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.OneKeyList, ['testy'], name, value)


        class Test(_Entity_):
            """
            
            
            .. attribute:: best
            
            	
            	**type**\:  :py:class:`Best <ydk.models.ydktest.ydktest_sanity.Runner.OneKeyList.Test.Best>`
            
            

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Runner.OneKeyList.Test, self).__init__()

                self.yang_name = "test"
                self.yang_parent_name = "one-key-list"
                self.is_top_level_class = False
                self.has_list_ancestor = True
                self.ylist_key_names = []
                self._child_classes = OrderedDict([("best", ("best", Runner.OneKeyList.Test.Best))])
                self._leafs = OrderedDict()

                self.best = Runner.OneKeyList.Test.Best()
                self.best.parent = self
                self._children_name_map["best"] = "best"
                self._segment_path = lambda: "test"
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Runner.OneKeyList.Test, [], name, value)


            class Best(_Entity_):
                """
                
                
                .. attribute:: gest
                
                	
                	**type**\: str
                
                

                """

                _prefix = 'ydkut'
                _revision = '2015-11-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Runner.OneKeyList.Test.Best, self).__init__()

                    self.yang_name = "best"
                    self.yang_parent_name = "test"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('gest', (YLeaf(YType.str, 'gest'), ['str'])),
                    ])
                    self.gest = None
                    self._segment_path = lambda: "best"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Runner.OneKeyList.Test.Best, ['gest'], name, value)





    class MandList(_Entity_):
        """
        
        
        .. attribute:: name  (key)
        
        	
        	**type**\: str
        
        .. attribute:: num
        
        	
        	**type**\: int
        
        	**range:** \-32768..32767
        
        	**mandatory**\: True
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.MandList, self).__init__()

            self.yang_name = "mand-list"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = ['name']
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('name', (YLeaf(YType.str, 'name'), ['str'])),
                ('num', (YLeaf(YType.int16, 'num'), ['int'])),
            ])
            self.name = None
            self.num = None
            self._segment_path = lambda: "mand-list" + "[name='" + str(self.name) + "']"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.MandList, ['name', 'num'], name, value)



    class YdktestSanityAugmOne(_Entity_):
        """
        config for one\_level data
        
        .. attribute:: twin_number
        
        	integer value type
        	**type**\: int
        
        	**range:** \-2147483648..2147483647
        
        

        """

        _prefix = 'ysanity-augm'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Runner.YdktestSanityAugmOne, self).__init__()

            self.yang_name = "one"
            self.yang_parent_name = "runner"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([])
            self._leafs = OrderedDict([
                ('twin_number', (YLeaf(YType.int32, 'twin-number'), ['int'])),
            ])
            self.twin_number = None
            self._segment_path = lambda: "ydktest-sanity-augm:one"
            self._absolute_path = lambda: "ydktest-sanity:runner/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Runner.YdktestSanityAugmOne, ['twin_number'], name, value)


    def clone_ptr(self):
        self._top_entity = Runner()
        return self._top_entity



class Native(_Entity_):
    """
    
    
    .. attribute:: version
    
    	Version
    	**type**\: str
    
    .. attribute:: hostname
    
    	Set system's network name
    	**type**\: str
    
    .. attribute:: interface
    
    	Configure Interfaces
    	**type**\:  :py:class:`Interface <ydk.models.ydktest.ydktest_sanity.Native.Interface>`
    
    

    """

    _prefix = 'ydkut'
    _revision = '2015-11-17'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(Native, self).__init__()
        self._top_entity = None

        self.yang_name = "native"
        self.yang_parent_name = "ydktest-sanity"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([("interface", ("interface", Native.Interface))])
        self._leafs = OrderedDict([
            ('version', (YLeaf(YType.str, 'version'), ['str'])),
            ('hostname', (YLeaf(YType.str, 'hostname'), ['str'])),
        ])
        self.version = None
        self.hostname = None

        self.interface = Native.Interface()
        self.interface.parent = self
        self._children_name_map["interface"] = "interface"
        self._segment_path = lambda: "ydktest-sanity:native"
        self._is_frozen = True

    def __setattr__(self, name, value):
        self._perform_setattr(Native, ['version', 'hostname'], name, value)


    class Interface(_Entity_):
        """
        Configure Interfaces
        
        .. attribute:: gigabitethernet
        
        	GigabitEthernet IEEE 802.3z
        	**type**\: list of  		 :py:class:`GigabitEthernet <ydk.models.ydktest.ydktest_sanity.Native.Interface.GigabitEthernet>`
        
        .. attribute:: loopback
        
        	Loopback interface
        	**type**\: list of  		 :py:class:`Loopback <ydk.models.ydktest.ydktest_sanity.Native.Interface.Loopback>`
        
        .. attribute:: tunnel
        
        	Tunnel interface
        	**type**\: list of  		 :py:class:`Tunnel <ydk.models.ydktest.ydktest_sanity.Native.Interface.Tunnel>`
        
        

        """

        _prefix = 'ydkut'
        _revision = '2015-11-17'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Native.Interface, self).__init__()

            self.yang_name = "interface"
            self.yang_parent_name = "native"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("GigabitEthernet", ("gigabitethernet", Native.Interface.GigabitEthernet)), ("Loopback", ("loopback", Native.Interface.Loopback)), ("Tunnel", ("tunnel", Native.Interface.Tunnel))])
            self._leafs = OrderedDict()

            self.gigabitethernet = YList(self)
            self.loopback = YList(self)
            self.tunnel = YList(self)
            self._segment_path = lambda: "interface"
            self._absolute_path = lambda: "ydktest-sanity:native/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Native.Interface, [], name, value)


        class GigabitEthernet(_Entity_):
            """
            GigabitEthernet IEEE 802.3z
            
            .. attribute:: name  (key)
            
            	
            	**type**\: str
            
            .. attribute:: media_type
            
            	Media type
            	**type**\:  :py:class:`MediaType <ydk.models.ydktest.ydktest_sanity.Native.Interface.GigabitEthernet.MediaType>`
            
            .. attribute:: description
            
            	Interface specific description
            	**type**\: str
            
            	**length:** 0..240
            
            .. attribute:: mtu
            
            	Set the interface Maximum Transmission Unit (MTU)
            	**type**\: int
            
            	**range:** 64..18000
            
            .. attribute:: ipv4
            
            	
            	**type**\:  :py:class:`Ipv4 <ydk.models.ydktest.ydktest_sanity.Native.Interface.GigabitEthernet.Ipv4>`
            
            

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Native.Interface.GigabitEthernet, self).__init__()

                self.yang_name = "GigabitEthernet"
                self.yang_parent_name = "interface"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = ['name']
                self._child_classes = OrderedDict([("ipv4", ("ipv4", Native.Interface.GigabitEthernet.Ipv4))])
                self._leafs = OrderedDict([
                    ('name', (YLeaf(YType.str, 'name'), ['str'])),
                    ('media_type', (YLeaf(YType.enumeration, 'media-type'), [('ydk.models.ydktest.ydktest_sanity', 'Native', 'Interface.GigabitEthernet.MediaType')])),
                    ('description', (YLeaf(YType.str, 'description'), ['str'])),
                    ('mtu', (YLeaf(YType.uint16, 'mtu'), ['int'])),
                ])
                self.name = None
                self.media_type = None
                self.description = None
                self.mtu = None

                self.ipv4 = Native.Interface.GigabitEthernet.Ipv4()
                self.ipv4.parent = self
                self._children_name_map["ipv4"] = "ipv4"
                self._segment_path = lambda: "GigabitEthernet" + "[name='" + str(self.name) + "']"
                self._absolute_path = lambda: "ydktest-sanity:native/interface/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Native.Interface.GigabitEthernet, ['name', 'media_type', 'description', 'mtu'], name, value)

            class MediaType(Enum):
                """
                MediaType (Enum Class)

                Media type

                .. data:: auto_select = 0

                .. data:: rj45 = 1

                .. data:: sfp = 2

                """

                auto_select = Enum.YLeaf(0, "auto-select")

                rj45 = Enum.YLeaf(1, "rj45")

                sfp = Enum.YLeaf(2, "sfp")



            class Ipv4(_Entity_):
                """
                
                
                .. attribute:: address
                
                	The list of configured IPv4 addresses on the interface
                	**type**\: list of  		 :py:class:`Address <ydk.models.ydktest.ydktest_sanity.Native.Interface.GigabitEthernet.Ipv4.Address>`
                
                

                """

                _prefix = 'ydkut'
                _revision = '2015-11-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Native.Interface.GigabitEthernet.Ipv4, self).__init__()

                    self.yang_name = "ipv4"
                    self.yang_parent_name = "GigabitEthernet"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([("address", ("address", Native.Interface.GigabitEthernet.Ipv4.Address))])
                    self._leafs = OrderedDict()

                    self.address = YList(self)
                    self._segment_path = lambda: "ipv4"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Native.Interface.GigabitEthernet.Ipv4, [], name, value)


                class Address(_Entity_):
                    """
                    The list of configured IPv4 addresses on the interface.
                    
                    .. attribute:: ip  (key)
                    
                    	The IPv4 address on the interface
                    	**type**\: str
                    
                    	**pattern:** (([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])\\.){3}([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])
                    
                    .. attribute:: prefix_length
                    
                    	The length of the subnet prefix
                    	**type**\: int
                    
                    	**range:** 0..32
                    
                    .. attribute:: netmask
                    
                    	The subnet specified as a netmask
                    	**type**\: str
                    
                    	**pattern:** (([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])\\.){3}([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])
                    
                    

                    """

                    _prefix = 'ydkut'
                    _revision = '2015-11-17'

                    def __init__(self):
                        if sys.version_info > (3,):
                            super().__init__()
                        else:
                            super(Native.Interface.GigabitEthernet.Ipv4.Address, self).__init__()

                        self.yang_name = "address"
                        self.yang_parent_name = "ipv4"
                        self.is_top_level_class = False
                        self.has_list_ancestor = True
                        self.ylist_key_names = ['ip']
                        self._child_classes = OrderedDict([])
                        self._leafs = OrderedDict([
                            ('ip', (YLeaf(YType.str, 'ip'), ['str'])),
                            ('prefix_length', (YLeaf(YType.uint8, 'prefix-length'), ['int'])),
                            ('netmask', (YLeaf(YType.str, 'netmask'), ['str'])),
                        ])
                        self.ip = None
                        self.prefix_length = None
                        self.netmask = None
                        self._segment_path = lambda: "address" + "[ip='" + str(self.ip) + "']"
                        self._is_frozen = True

                    def __setattr__(self, name, value):
                        self._perform_setattr(Native.Interface.GigabitEthernet.Ipv4.Address, ['ip', 'prefix_length', 'netmask'], name, value)





        class Loopback(_Entity_):
            """
            Loopback interface
            
            .. attribute:: name  (key)
            
            	
            	**type**\: int
            
            	**range:** 0..4294967295
            
            .. attribute:: description
            
            	Interface specific description
            	**type**\: str
            
            	**length:** 0..240
            
            .. attribute:: mtu
            
            	Set the interface Maximum Transmission Unit (MTU)
            	**type**\: int
            
            	**range:** 64..18000
            
            .. attribute:: ipv4
            
            	
            	**type**\:  :py:class:`Ipv4 <ydk.models.ydktest.ydktest_sanity.Native.Interface.Loopback.Ipv4>`
            
            

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Native.Interface.Loopback, self).__init__()

                self.yang_name = "Loopback"
                self.yang_parent_name = "interface"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = ['name']
                self._child_classes = OrderedDict([("ipv4", ("ipv4", Native.Interface.Loopback.Ipv4))])
                self._leafs = OrderedDict([
                    ('name', (YLeaf(YType.uint32, 'name'), ['int'])),
                    ('description', (YLeaf(YType.str, 'description'), ['str'])),
                    ('mtu', (YLeaf(YType.uint16, 'mtu'), ['int'])),
                ])
                self.name = None
                self.description = None
                self.mtu = None

                self.ipv4 = Native.Interface.Loopback.Ipv4()
                self.ipv4.parent = self
                self._children_name_map["ipv4"] = "ipv4"
                self._segment_path = lambda: "Loopback" + "[name='" + str(self.name) + "']"
                self._absolute_path = lambda: "ydktest-sanity:native/interface/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Native.Interface.Loopback, ['name', 'description', 'mtu'], name, value)


            class Ipv4(_Entity_):
                """
                
                
                .. attribute:: address
                
                	The list of configured IPv4 addresses on the interface
                	**type**\: list of  		 :py:class:`Address <ydk.models.ydktest.ydktest_sanity.Native.Interface.Loopback.Ipv4.Address>`
                
                

                """

                _prefix = 'ydkut'
                _revision = '2015-11-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Native.Interface.Loopback.Ipv4, self).__init__()

                    self.yang_name = "ipv4"
                    self.yang_parent_name = "Loopback"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([("address", ("address", Native.Interface.Loopback.Ipv4.Address))])
                    self._leafs = OrderedDict()

                    self.address = YList(self)
                    self._segment_path = lambda: "ipv4"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Native.Interface.Loopback.Ipv4, [], name, value)


                class Address(_Entity_):
                    """
                    The list of configured IPv4 addresses on the interface.
                    
                    .. attribute:: ip  (key)
                    
                    	The IPv4 address on the interface
                    	**type**\: str
                    
                    	**pattern:** (([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])\\.){3}([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])
                    
                    .. attribute:: prefix_length
                    
                    	The length of the subnet prefix
                    	**type**\: int
                    
                    	**range:** 0..32
                    
                    .. attribute:: netmask
                    
                    	The subnet specified as a netmask
                    	**type**\: str
                    
                    	**pattern:** (([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])\\.){3}([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])
                    
                    

                    """

                    _prefix = 'ydkut'
                    _revision = '2015-11-17'

                    def __init__(self):
                        if sys.version_info > (3,):
                            super().__init__()
                        else:
                            super(Native.Interface.Loopback.Ipv4.Address, self).__init__()

                        self.yang_name = "address"
                        self.yang_parent_name = "ipv4"
                        self.is_top_level_class = False
                        self.has_list_ancestor = True
                        self.ylist_key_names = ['ip']
                        self._child_classes = OrderedDict([])
                        self._leafs = OrderedDict([
                            ('ip', (YLeaf(YType.str, 'ip'), ['str'])),
                            ('prefix_length', (YLeaf(YType.uint8, 'prefix-length'), ['int'])),
                            ('netmask', (YLeaf(YType.str, 'netmask'), ['str'])),
                        ])
                        self.ip = None
                        self.prefix_length = None
                        self.netmask = None
                        self._segment_path = lambda: "address" + "[ip='" + str(self.ip) + "']"
                        self._is_frozen = True

                    def __setattr__(self, name, value):
                        self._perform_setattr(Native.Interface.Loopback.Ipv4.Address, ['ip', 'prefix_length', 'netmask'], name, value)





        class Tunnel(_Entity_):
            """
            Tunnel interface
            
            .. attribute:: name  (key)
            
            	
            	**type**\: int
            
            	**range:** 0..4294967295
            
            .. attribute:: description
            
            	Interface specific description
            	**type**\: str
            
            	**length:** 0..240
            
            .. attribute:: mtu
            
            	Set the interface Maximum Transmission Unit (MTU)
            	**type**\: int
            
            	**range:** 64..18000
            
            .. attribute:: ipv4
            
            	
            	**type**\:  :py:class:`Ipv4 <ydk.models.ydktest.ydktest_sanity.Native.Interface.Tunnel.Ipv4>`
            
            .. attribute:: ipsec
            
            	Use ipsec to protect this tunnel interface
            	**type**\:  :py:class:`Ipsec <ydk.models.ydktest.ydktest_sanity.Native.Interface.Tunnel.Ipsec>`
            
            .. attribute:: nhrp
            
            	NHRP Interface commands
            	**type**\:  :py:class:`Nhrp <ydk.models.ydktest.ydktest_sanity.Native.Interface.Tunnel.Nhrp>`
            
            .. attribute:: tunnel
            
            	protocol\-over\-protocol tunneling
            	**type**\:  :py:class:`Tunnel_ <ydk.models.ydktest.ydktest_sanity.Native.Interface.Tunnel.Tunnel_>`
            
            

            """

            _prefix = 'ydkut'
            _revision = '2015-11-17'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Native.Interface.Tunnel, self).__init__()

                self.yang_name = "Tunnel"
                self.yang_parent_name = "interface"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = ['name']
                self._child_classes = OrderedDict([("ipv4", ("ipv4", Native.Interface.Tunnel.Ipv4)), ("ipsec", ("ipsec", Native.Interface.Tunnel.Ipsec)), ("ydktest-sanity-augm:nhrp", ("nhrp", Native.Interface.Tunnel.Nhrp)), ("ydktest-sanity-augm:tunnel", ("tunnel", Native.Interface.Tunnel.Tunnel_))])
                self._leafs = OrderedDict([
                    ('name', (YLeaf(YType.uint32, 'name'), ['int'])),
                    ('description', (YLeaf(YType.str, 'description'), ['str'])),
                    ('mtu', (YLeaf(YType.uint16, 'mtu'), ['int'])),
                ])
                self.name = None
                self.description = None
                self.mtu = None

                self.ipv4 = Native.Interface.Tunnel.Ipv4()
                self.ipv4.parent = self
                self._children_name_map["ipv4"] = "ipv4"

                self.ipsec = Native.Interface.Tunnel.Ipsec()
                self.ipsec.parent = self
                self._children_name_map["ipsec"] = "ipsec"

                self.nhrp = Native.Interface.Tunnel.Nhrp()
                self.nhrp.parent = self
                self._children_name_map["nhrp"] = "ydktest-sanity-augm:nhrp"

                self.tunnel = Native.Interface.Tunnel.Tunnel_()
                self.tunnel.parent = self
                self._children_name_map["tunnel"] = "ydktest-sanity-augm:tunnel"
                self._segment_path = lambda: "Tunnel" + "[name='" + str(self.name) + "']"
                self._absolute_path = lambda: "ydktest-sanity:native/interface/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Native.Interface.Tunnel, ['name', 'description', 'mtu'], name, value)


            class Ipv4(_Entity_):
                """
                
                
                .. attribute:: address
                
                	The list of configured IPv4 addresses on the interface
                	**type**\: list of  		 :py:class:`Address <ydk.models.ydktest.ydktest_sanity.Native.Interface.Tunnel.Ipv4.Address>`
                
                

                """

                _prefix = 'ydkut'
                _revision = '2015-11-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Native.Interface.Tunnel.Ipv4, self).__init__()

                    self.yang_name = "ipv4"
                    self.yang_parent_name = "Tunnel"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([("address", ("address", Native.Interface.Tunnel.Ipv4.Address))])
                    self._leafs = OrderedDict()

                    self.address = YList(self)
                    self._segment_path = lambda: "ipv4"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Native.Interface.Tunnel.Ipv4, [], name, value)


                class Address(_Entity_):
                    """
                    The list of configured IPv4 addresses on the interface.
                    
                    .. attribute:: ip  (key)
                    
                    	The IPv4 address on the interface
                    	**type**\: str
                    
                    	**pattern:** (([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])\\.){3}([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])
                    
                    .. attribute:: prefix_length
                    
                    	The length of the subnet prefix
                    	**type**\: int
                    
                    	**range:** 0..32
                    
                    .. attribute:: netmask
                    
                    	The subnet specified as a netmask
                    	**type**\: str
                    
                    	**pattern:** (([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])\\.){3}([0\-9]\|[1\-9][0\-9]\|1[0\-9][0\-9]\|2[0\-4][0\-9]\|25[0\-5])
                    
                    

                    """

                    _prefix = 'ydkut'
                    _revision = '2015-11-17'

                    def __init__(self):
                        if sys.version_info > (3,):
                            super().__init__()
                        else:
                            super(Native.Interface.Tunnel.Ipv4.Address, self).__init__()

                        self.yang_name = "address"
                        self.yang_parent_name = "ipv4"
                        self.is_top_level_class = False
                        self.has_list_ancestor = True
                        self.ylist_key_names = ['ip']
                        self._child_classes = OrderedDict([])
                        self._leafs = OrderedDict([
                            ('ip', (YLeaf(YType.str, 'ip'), ['str'])),
                            ('prefix_length', (YLeaf(YType.uint8, 'prefix-length'), ['int'])),
                            ('netmask', (YLeaf(YType.str, 'netmask'), ['str'])),
                        ])
                        self.ip = None
                        self.prefix_length = None
                        self.netmask = None
                        self._segment_path = lambda: "address" + "[ip='" + str(self.ip) + "']"
                        self._is_frozen = True

                    def __setattr__(self, name, value):
                        self._perform_setattr(Native.Interface.Tunnel.Ipv4.Address, ['ip', 'prefix_length', 'netmask'], name, value)




            class Ipsec(_Entity_):
                """
                Use ipsec to protect this tunnel interface
                
                .. attribute:: profile
                
                	Determine the ipsec policy profile to use
                	**type**\: str
                
                .. attribute:: ikev2_profile
                
                	ikev2 policy profile
                	**type**\: str
                
                

                """

                _prefix = 'ydkut'
                _revision = '2015-11-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Native.Interface.Tunnel.Ipsec, self).__init__()

                    self.yang_name = "ipsec"
                    self.yang_parent_name = "Tunnel"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([])
                    self._leafs = OrderedDict([
                        ('profile', (YLeaf(YType.str, 'profile'), ['str'])),
                        ('ikev2_profile', (YLeaf(YType.str, 'ikev2-profile'), ['str'])),
                    ])
                    self.profile = None
                    self.ikev2_profile = None
                    self._segment_path = lambda: "ipsec"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Native.Interface.Tunnel.Ipsec, ['profile', 'ikev2_profile'], name, value)



            class Nhrp(_Entity_):
                """
                NHRP Interface commands
                
                .. attribute:: event_publisher
                
                	Enable NHRP smart spoke feature
                	**type**\:  :py:class:`EventPublisher <ydk.models.ydktest.ydktest_sanity.Native.Interface.Tunnel.Nhrp.EventPublisher>`
                
                .. attribute:: group
                
                	group name string
                	**type**\: str
                
                

                """

                _prefix = 'ysanity-augm'
                _revision = '2015-11-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Native.Interface.Tunnel.Nhrp, self).__init__()

                    self.yang_name = "nhrp"
                    self.yang_parent_name = "Tunnel"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([("event-publisher", ("event_publisher", Native.Interface.Tunnel.Nhrp.EventPublisher))])
                    self._leafs = OrderedDict([
                        ('group', (YLeaf(YType.str, 'group'), ['str'])),
                    ])
                    self.group = None

                    self.event_publisher = Native.Interface.Tunnel.Nhrp.EventPublisher()
                    self.event_publisher.parent = self
                    self._children_name_map["event_publisher"] = "event-publisher"
                    self._segment_path = lambda: "ydktest-sanity-augm:nhrp"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Native.Interface.Tunnel.Nhrp, ['group'], name, value)


                class EventPublisher(_Entity_):
                    """
                    Enable NHRP smart spoke feature
                    
                    .. attribute:: max_event_timeout
                    
                    	Number of seconds
                    	**type**\: int
                    
                    	**range:** 1..22
                    
                    

                    """

                    _prefix = 'ysanity-augm'
                    _revision = '2015-11-17'

                    def __init__(self):
                        if sys.version_info > (3,):
                            super().__init__()
                        else:
                            super(Native.Interface.Tunnel.Nhrp.EventPublisher, self).__init__()

                        self.yang_name = "event-publisher"
                        self.yang_parent_name = "nhrp"
                        self.is_top_level_class = False
                        self.has_list_ancestor = True
                        self.ylist_key_names = []
                        self._child_classes = OrderedDict([])
                        self._leafs = OrderedDict([
                            ('max_event_timeout', (YLeaf(YType.uint8, 'max-event-timeout'), ['int'])),
                        ])
                        self.max_event_timeout = None
                        self._segment_path = lambda: "event-publisher"
                        self._is_frozen = True

                    def __setattr__(self, name, value):
                        self._perform_setattr(Native.Interface.Tunnel.Nhrp.EventPublisher, ['max_event_timeout'], name, value)




            class Tunnel_(_Entity_):
                """
                protocol\-over\-protocol tunneling
                
                .. attribute:: bandwidth
                
                	Set tunnel bandwidth informational parameter
                	**type**\:  :py:class:`Bandwidth <ydk.models.ydktest.ydktest_sanity.Native.Interface.Tunnel.Tunnel_.Bandwidth>`
                
                .. attribute:: source
                
                	source of tunnel packets
                	**type**\: str
                
                .. attribute:: destination
                
                	destination of tunnel
                	**type**\: str
                
                

                """

                _prefix = 'ysanity-augm'
                _revision = '2015-11-17'

                def __init__(self):
                    if sys.version_info > (3,):
                        super().__init__()
                    else:
                        super(Native.Interface.Tunnel.Tunnel_, self).__init__()

                    self.yang_name = "tunnel"
                    self.yang_parent_name = "Tunnel"
                    self.is_top_level_class = False
                    self.has_list_ancestor = True
                    self.ylist_key_names = []
                    self._child_classes = OrderedDict([("bandwidth", ("bandwidth", Native.Interface.Tunnel.Tunnel_.Bandwidth))])
                    self._leafs = OrderedDict([
                        ('source', (YLeaf(YType.str, 'source'), ['str'])),
                        ('destination', (YLeaf(YType.str, 'destination'), ['str'])),
                    ])
                    self.source = None
                    self.destination = None

                    self.bandwidth = Native.Interface.Tunnel.Tunnel_.Bandwidth()
                    self.bandwidth.parent = self
                    self._children_name_map["bandwidth"] = "bandwidth"
                    self._segment_path = lambda: "ydktest-sanity-augm:tunnel"
                    self._is_frozen = True

                def __setattr__(self, name, value):
                    self._perform_setattr(Native.Interface.Tunnel.Tunnel_, ['source', 'destination'], name, value)


                class Bandwidth(_Entity_):
                    """
                    Set tunnel bandwidth informational parameter
                    
                    .. attribute:: receive
                    
                    	Receive bandwidth
                    	**type**\: int
                    
                    	**range:** 0..4294967295
                    
                    .. attribute:: transmit
                    
                    	Transmit bandwidth
                    	**type**\: int
                    
                    	**range:** 0..4294967295
                    
                    

                    """

                    _prefix = 'ysanity-augm'
                    _revision = '2015-11-17'

                    def __init__(self):
                        if sys.version_info > (3,):
                            super().__init__()
                        else:
                            super(Native.Interface.Tunnel.Tunnel_.Bandwidth, self).__init__()

                        self.yang_name = "bandwidth"
                        self.yang_parent_name = "tunnel"
                        self.is_top_level_class = False
                        self.has_list_ancestor = True
                        self.ylist_key_names = []
                        self._child_classes = OrderedDict([])
                        self._leafs = OrderedDict([
                            ('receive', (YLeaf(YType.uint32, 'receive'), ['int'])),
                            ('transmit', (YLeaf(YType.uint32, 'transmit'), ['int'])),
                        ])
                        self.receive = None
                        self.transmit = None
                        self._segment_path = lambda: "bandwidth"
                        self._is_frozen = True

                    def __setattr__(self, name, value):
                        self._perform_setattr(Native.Interface.Tunnel.Tunnel_.Bandwidth, ['receive', 'transmit'], name, value)





    def clone_ptr(self):
        self._top_entity = Native()
        return self._top_entity



class CascadingTypes(_Entity_):
    """
    
    
    .. attribute:: comp_insttype
    
    	this is enum type value
    	**type**\:  :py:class:`CompInstType_ <ydk.models.ydktest.ydktest_sanity.CompInstType_>`
    
    .. attribute:: comp_nicinsttype
    
    	this is enum type value
    	**type**\:  :py:class:`CompInstType_ <ydk.models.ydktest.ydktest_sanity.CompInstType_>`
    
    

    """

    _prefix = 'ydkut'
    _revision = '2015-11-17'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(CascadingTypes, self).__init__()
        self._top_entity = None

        self.yang_name = "cascading-types"
        self.yang_parent_name = "ydktest-sanity"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([])
        self._leafs = OrderedDict([
            ('comp_insttype', (YLeaf(YType.enumeration, 'comp_InstType'), [('ydk.models.ydktest.ydktest_sanity', 'CompInstType_', '')])),
            ('comp_nicinsttype', (YLeaf(YType.enumeration, 'comp_NicInstType'), [('ydk.models.ydktest.ydktest_sanity', 'CompInstType_', '')])),
        ])
        self.comp_insttype = None
        self.comp_nicinsttype = None
        self._segment_path = lambda: "ydktest-sanity:cascading-types"
        self._is_frozen = True

    def __setattr__(self, name, value):
        self._perform_setattr(CascadingTypes, ['comp_insttype', 'comp_nicinsttype'], name, value)

    def clone_ptr(self):
        self._top_entity = CascadingTypes()
        return self._top_entity



class ConditionalInterface(_Entity_):
    """
    
    
    .. attribute:: iftype
    
    	
    	**type**\:  :py:class:`IfType <ydk.models.ydktest.ydktest_sanity.ConditionalInterface.IfType>`
    
    	**default value**\: ethernet
    
    .. attribute:: ifmtu
    
    	
    	**type**\: int
    
    	**range:** 0..4294967295
    
    	**default value**\: 1500
    
    .. attribute:: ds0channelnumber
    
    	
    	**type**\: int
    
    	**range:** 0..65535
    
    

    """

    _prefix = 'ydkut'
    _revision = '2015-11-17'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(ConditionalInterface, self).__init__()
        self._top_entity = None

        self.yang_name = "conditional-interface"
        self.yang_parent_name = "ydktest-sanity"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([])
        self._leafs = OrderedDict([
            ('iftype', (YLeaf(YType.enumeration, 'ifType'), [('ydk.models.ydktest.ydktest_sanity', 'ConditionalInterface', 'IfType')])),
            ('ifmtu', (YLeaf(YType.uint32, 'ifMTU'), ['int'])),
            ('ds0channelnumber', (YLeaf(YType.uint16, 'ds0ChannelNumber'), ['int'])),
        ])
        self.iftype = None
        self.ifmtu = None
        self.ds0channelnumber = None
        self._segment_path = lambda: "ydktest-sanity:conditional-interface"
        self._is_frozen = True

    def __setattr__(self, name, value):
        self._perform_setattr(ConditionalInterface, ['iftype', 'ifmtu', 'ds0channelnumber'], name, value)

    class IfType(Enum):
        """
        IfType (Enum Class)

        .. data:: ethernet = 0

        .. data:: atm = 1

        .. data:: ds0 = 2

        """

        ethernet = Enum.YLeaf(0, "ethernet")

        atm = Enum.YLeaf(1, "atm")

        ds0 = Enum.YLeaf(2, "ds0")


    def clone_ptr(self):
        self._top_entity = ConditionalInterface()
        return self._top_entity



class ChildIdentity(BaseIdentity):
    """
    
    
    

    """

    _prefix = 'ydkut'
    _revision = '2015-11-17'

    def __init__(self, ns="http://cisco.com/ns/yang/ydktest-sanity", pref="ydktest-sanity", tag="ydktest-sanity:child-identity"):
        if sys.version_info > (3,):
            super().__init__(ns, pref, tag)
        else:
            super(ChildIdentity, self).__init__(ns, pref, tag)



class ChildChildIdentity(ChildIdentity):
    """
    
    
    

    """

    _prefix = 'ydkut'
    _revision = '2015-11-17'

    def __init__(self, ns="http://cisco.com/ns/yang/ydktest-sanity", pref="ydktest-sanity", tag="ydktest-sanity:child-child-identity"):
        if sys.version_info > (3,):
            super().__init__(ns, pref, tag)
        else:
            super(ChildChildIdentity, self).__init__(ns, pref, tag)



