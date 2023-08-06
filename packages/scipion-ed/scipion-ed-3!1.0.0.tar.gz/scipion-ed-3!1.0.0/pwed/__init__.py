# **************************************************************************
# *
# * Authors:     J.M. De la Rosa Trevin (delarosatrevin@scilifelab.se) [1]
# *              Viktor E. G. Bengtsson (viktor.bengtsson@mmk.su.se)   [2]
# *
# * [1] SciLifeLab, Stockholm University
# * [2] MMK, Stockholm University
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************
"""
This modules contains classes related with ED
"""

import os

import pyworkflow as pw
import pyworkflow.utils as pwutils
import pyworkflow.plugin as pwplugin
from pyworkflow.viewer import Viewer
from pyworkflow.wizard import Wizard
from pyworkflow.protocol import Protocol, HostConfig

from .utils import *
from .constants import *
from .objects import EdBaseObject

# Epoch indicates compatible main Scipion version
# major.minor.micro versioning starting with 1.0.0 in the new epoch
__version__ = '3!1.0.0'


class Domain(pwplugin.Domain):
    _name = __name__
    _objectClass = EdBaseObject
    _protocolClass = Protocol
    _viewerClass = Viewer
    _wizardClass = Wizard
    _baseClasses = globals()


class Plugin(pwplugin.Plugin):
    pass


class Config:
    # scipion-pyworkflow will generate the path $SCIPION_HOME/software/bindings
    # The path will be created in the working directory if SCIPION_HOME is not set
    SCIPION_ED_HOME = os.environ.get('SCIPION_HOME',
                                     pwutils.expandPattern("~/.scipion-ed-home"))
    # Allowing the user to set SCIPION_ED_USERDATA at installation is issue #8
    SCIPION_ED_USERDATA = os.environ.get('SCIPION_ED_USERDATA',
                                         pwutils.expandPattern("~/ScipionEdUserData"))
    # Location of the contents from scipion-ed-testdata
    SCIPION_ED_TESTDATA = os.environ.get('SCIPION_ED_TESTDATA', None)

    SCIPION_ED_TEST_OUTPUT = os.environ.get('SCIPION_ED_TEST_OUTPUT',
                                            os.path.join(SCIPION_ED_USERDATA, 'Tests'))


# ----------- Override some pyworkflow config settings ------------------------

# Create Config.SCIPION_ED_HOME if it does not already exist. It is required
# pyworkflow.Config
if not os.path.exists(Config.SCIPION_ED_HOME):
    os.mkdir(Config.SCIPION_ED_HOME)
# Create Config.SCIPION_ED_USERDATA if it does not already exist.
if not os.path.exists(Config.SCIPION_ED_USERDATA):
    os.mkdir(Config.SCIPION_ED_USERDATA)
# Create default hosts.conf
hostsFile = os.path.join(Config.SCIPION_ED_USERDATA, 'hosts.conf')
if not os.path.exists(hostsFile):
    HostConfig.writeBasic(hostsFile)


os.environ['SCIPION_VERSION'] = "ED - " + __version__
os.environ['SCIPION_HOME'] = pw.Config.SCIPION_HOME = Config.SCIPION_ED_HOME
os.environ['SCIPION_USER_DATA'] = pw.Config.SCIPION_USER_DATA = Config.SCIPION_ED_USERDATA
os.environ['SCIPION_HOSTS'] = pw.Config.SCIPION_HOSTS = hostsFile
os.environ['SCIPION_TESTS_OUTPUT'] = pw.Config.SCIPION_TESTS_OUTPUT = Config.SCIPION_ED_TEST_OUTPUT

pw.Config.setDomain('pwed')


Domain.registerPlugin(__name__)
