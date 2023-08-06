""" TestBase

  Base class for all tests.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import object
import threading
from abc   import ABCMeta,abstractmethod
from future.utils import with_metaclass


__RCSID__ = '$Id:  $'

LOCK = threading.Lock()


class TestBase( with_metaclass(ABCMeta, object) ):
  """
    TestBase is a simple base class for all tests. Real test classes should
    implement its doTest and getTestResult method.
  """

  def __init__( self, args = None, apis = None ):
    self.apis = apis or {}
    self.args = args or {}


  @abstractmethod
  def doTest( self, elementDict ):
    """
      to be extended by real tests.
    """

    return None
