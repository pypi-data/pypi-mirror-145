''' CEAccessTest

A test class to test the access to ces.

'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import object
from DIRAC import S_OK, S_ERROR, gConfig


class CEAccessTest(object):
  ''' CEAccessTest
  '''

  def _getAccessParams( self, element ):
    '''
      get the access host and port for the specified ce.
    '''

    _basePath = 'Resources/Sites'

    domains = gConfig.getSections( _basePath )
    if not domains[ 'OK' ]:
      return domains
    domains = domains[ 'Value' ]

    for domain in domains:
      sites = gConfig.getSections( '%s/%s' % ( _basePath, domain ) )
      if not sites[ 'OK' ]:
        return sites
      sites = sites[ 'Value' ]

      for site in sites:
        ces = gConfig.getValue( '%s/%s/%s/CE' % ( _basePath, domain, site ), '' ).split(',')
        ces = [str.strip() for str in ces]

        if element in ces:
          host = gConfig.getValue('%s/%s/%s/CEs/%s/SSHHost' % ( _basePath, domain, site, element ))
          cetype = gConfig.getValue('%s/%s/%s/CEs/%s/CEType' % ( _basePath, domain, site, element ))
          if host:
            idx = host.find('/')
            if idx != -1: host = host[ 0 : idx ]
            return S_OK((host, 22))
          elif cetype == 'CREAM':
            return S_OK((element, 8443))
          elif cetype == 'HTCondorCE':
            return S_OK((element, 9619))
          elif cetype == 'ARC':
            return S_OK((element, 2135))
          else:
            return S_OK((element, 8443))

    return S_ERROR('%s is not a vaild CE.' % element)
