''' SEAccessTest

A test class to test the access to ses.

'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import object
import subprocess, re
from datetime import datetime
from DIRAC import S_OK, S_ERROR, gConfig


class SEAccessTest(object):
  ''' SEAccessTest
  '''

  def _getAccessParams( self, element ):
    '''
      get the access host and port for the specified se.
    '''

    _basePath = 'Resources/StorageElements'

    host = gConfig.getValue( '%s/%s/AccessProtocol.1/Host' % ( _basePath, element ), '' )
    if not host:
      host = gConfig.getValue( '%s/%s/GFAL2_XROOT/Host' % ( _basePath, element ), '' )
    port = gConfig.getValue( '%s/%s/AccessProtocol.1/Port' % ( _basePath, element ), '' )
    if not port:
      port = gConfig.getValue( '%s/%s/GFAL2_XROOT/Port' % ( _basePath, element ), '' )

    return S_OK( ( host, port ) )
