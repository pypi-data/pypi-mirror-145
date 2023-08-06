""" ietf_aug_base_2 

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
    
    
    .. attribute:: tools
    
    	
    	**type**\:  :py:class:`Tools <ydk.models.ydktest.ietf_aug_base_2.Cpython.Tools>`
    
    

    """

    _prefix = 'ietf-aug-base-2'
    _revision = '2016-07-01'

    def __init__(self):
        if sys.version_info > (3,):
            super().__init__()
        else:
            super(Cpython, self).__init__()
        self._top_entity = None

        self.yang_name = "cpython"
        self.yang_parent_name = "ietf-aug-base-2"
        self.is_top_level_class = True
        self.has_list_ancestor = False
        self.ylist_key_names = []
        self._child_classes = OrderedDict([("tools", ("tools", Cpython.Tools))])
        self._leafs = OrderedDict()

        self.tools = Cpython.Tools()
        self.tools.parent = self
        self._children_name_map["tools"] = "tools"
        self._segment_path = lambda: "ietf-aug-base-2:cpython"
        self._is_frozen = True

    def __setattr__(self, name, value):
        self._perform_setattr(Cpython, [], name, value)


    class Tools(_Entity_):
        """
        
        
        .. attribute:: buildbot
        
        	
        	**type**\:  :py:class:`Buildbot <ydk.models.ydktest.ietf_aug_base_2.Cpython.Tools.Buildbot>`
        
        .. attribute:: gdb
        
        	
        	**type**\:  :py:class:`Gdb <ydk.models.ydktest.ietf_aug_base_2.Cpython.Tools.Gdb>`
        
        .. attribute:: aug_four
        
        	ydktest augmentation four
        	**type**\: str
        
        

        """

        _prefix = 'ietf-aug-base-2'
        _revision = '2016-07-01'

        def __init__(self):
            if sys.version_info > (3,):
                super().__init__()
            else:
                super(Cpython.Tools, self).__init__()

            self.yang_name = "tools"
            self.yang_parent_name = "cpython"
            self.is_top_level_class = False
            self.has_list_ancestor = False
            self.ylist_key_names = []
            self._child_classes = OrderedDict([("buildbot", ("buildbot", Cpython.Tools.Buildbot)), ("gdb", ("gdb", Cpython.Tools.Gdb))])
            self._leafs = OrderedDict([
                ('aug_four', (YLeaf(YType.str, 'ydktest-aug-ietf-4:aug-four'), ['str'])),
            ])
            self.aug_four = None

            self.buildbot = Cpython.Tools.Buildbot()
            self.buildbot.parent = self
            self._children_name_map["buildbot"] = "buildbot"

            self.gdb = Cpython.Tools.Gdb()
            self.gdb.parent = self
            self._children_name_map["gdb"] = "gdb"
            self._segment_path = lambda: "tools"
            self._absolute_path = lambda: "ietf-aug-base-2:cpython/%s" % self._segment_path()
            self._is_frozen = True

        def __setattr__(self, name, value):
            self._perform_setattr(Cpython.Tools, ['aug_four'], name, value)


        class Buildbot(_Entity_):
            """
            
            
            .. attribute:: build
            
            	
            	**type**\: str
            
            

            """

            _prefix = 'ietf-aug-base-2'
            _revision = '2016-07-01'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Cpython.Tools.Buildbot, self).__init__()

                self.yang_name = "buildbot"
                self.yang_parent_name = "tools"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('build', (YLeaf(YType.str, 'build'), ['str'])),
                ])
                self.build = None
                self._segment_path = lambda: "buildbot"
                self._absolute_path = lambda: "ietf-aug-base-2:cpython/tools/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Cpython.Tools.Buildbot, ['build'], name, value)



        class Gdb(_Entity_):
            """
            
            
            .. attribute:: libpython
            
            	
            	**type**\: str
            
            

            """

            _prefix = 'ietf-aug-base-2'
            _revision = '2016-07-01'

            def __init__(self):
                if sys.version_info > (3,):
                    super().__init__()
                else:
                    super(Cpython.Tools.Gdb, self).__init__()

                self.yang_name = "gdb"
                self.yang_parent_name = "tools"
                self.is_top_level_class = False
                self.has_list_ancestor = False
                self.ylist_key_names = []
                self._child_classes = OrderedDict([])
                self._leafs = OrderedDict([
                    ('libpython', (YLeaf(YType.str, 'libpython'), ['str'])),
                ])
                self.libpython = None
                self._segment_path = lambda: "gdb"
                self._absolute_path = lambda: "ietf-aug-base-2:cpython/tools/%s" % self._segment_path()
                self._is_frozen = True

            def __setattr__(self, name, value):
                self._perform_setattr(Cpython.Tools.Gdb, ['libpython'], name, value)



    def clone_ptr(self):
        self._top_entity = Cpython()
        return self._top_entity



