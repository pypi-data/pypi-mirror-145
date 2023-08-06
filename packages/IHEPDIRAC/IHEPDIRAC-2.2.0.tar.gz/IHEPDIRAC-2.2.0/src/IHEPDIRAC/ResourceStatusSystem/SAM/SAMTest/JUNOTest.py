""" JUNOTest

  A test class to test the software for the vo juno.

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


class JUNOTest( CEBaseTest ):
  """
    JUNOTest is used to test whether the juno's software is fine to run jobs.
  """

  def __init__( self, args = None, apis = None ):
    super( JUNOTest, self ).__init__( args, apis )


  @staticmethod
  def _judge( log ):
    idx = log.find( 'SNiPER::Context Terminated Successfully' )
    print("++++++++++++++++++++++++correct or not:", idx)
    if idx != -1:
      return 'OK'
    else:
      return 'Bad'
