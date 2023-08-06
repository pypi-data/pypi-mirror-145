from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library
standard_library.install_aliases()
from builtins import *
TESTS = {

  'Access-Test' :
  {
    'module' : 'AccessTest',
    'match' : { 'ElementType' : ( 'ComputingElement', 'CLOUD', 'StorageElement' ) },
    'args' : { 'timeout' : 5 }
  },

  'WMS-Test' :
  {
    'module' : 'WMSTest',
    'match' : { 'ElementType' : ( 'ComputingElement', 'CLOUD' ) },
    'args' : { 'executable' : 'wms_test.py', 'timeout' : 2400 }
  },

  'CVMFS-Test' :
  {
    'module' : 'CVMFSTest',
    'match' : { 'ElementType' : ( 'ComputingElement', 'CLOUD' ), 'VO' : 'bes' },
    'args' : { 'executable' : 'cvmfs_test.py', 'timeout' : 2400 }
  },

  'BOSS-Test' :
  {
    'module' : 'BOSSTest',
    'match' : { 'ElementType' : ( 'ComputingElement', 'CLOUD' ), 'VO' : 'bes' },
    'args' : { 'executable' : 'boss_test.py', 'timeout' : 2400 }
  },

  'CEPC-Test' :
  {
    'module' : 'CEPCTest',
    'match' : { 'ElementType' : ( 'ComputingElement', 'CLOUD' ), 'VO' : 'cepc' },
    'args' : { 'executable' : 'cepc_test.py', 'timeout' : 2400 }
  },

  'JUNO-Test':
  {
   'module' : 'JUNOTest',
   'match' : { 'ElementType' : ( 'ComputingElement', 'CLOUD' ), 'VO' : 'juno' },
   'args' : { 'executable' : 'juno_test.py', 'timeout' : 2400 }
  },

  'SE-Test' :
  {
    'module' : 'SETest',
    'match' : { 'ElementType' : ( 'StorageElement', ) }
  },

}
