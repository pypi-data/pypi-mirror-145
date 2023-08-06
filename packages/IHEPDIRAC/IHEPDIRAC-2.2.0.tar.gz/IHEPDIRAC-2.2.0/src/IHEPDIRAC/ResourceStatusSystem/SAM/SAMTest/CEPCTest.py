""" JUNOTest

  A test class to test the software for the vo cepc.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library
standard_library.install_aliases()
from builtins import *
from IHEPDIRAC.ResourceStatusSystem.SAM.SAMTest.CEBaseTest import CEBaseTest


__RCSID__ = '$Id: $'


class CEPCTest( CEBaseTest ):
  """
    JUNOTest is used to test whether the cepc's software is fine to run jobs.
  """

  def __init__( self, args = None, apis = None ):
    super( CEPCTest, self ).__init__( args, apis )


  @staticmethod
  def _judge( log ):
    idx = log.find( 'Job Done.' )
    if idx != -1:
      return 'OK'
    else:
      return 'Bad'
