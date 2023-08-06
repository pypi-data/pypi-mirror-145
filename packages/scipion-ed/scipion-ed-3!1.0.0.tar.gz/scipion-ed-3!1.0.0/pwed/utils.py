# **************************************************************************
# *
# * Authors:     J.M. De la Rosa Trevin (delarosatrevin@scilifelab.se) [1]
# *              V. E.G: Bengtsson (viktor.bengtsson@mmk.su.se) [2]
# *
# * [1] SciLifeLab, Stockholm University
# * [2] Department of Materials and Environmental Chemistry, Stockholm University
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

import pyworkflow.protocol as pwprot
from pwed.protocols import EdBaseProtocol


class CutRes(EdBaseProtocol):
    def _defineResolutionParams(self, form,
                                dminHelp="The maximum resolution limit",
                                dmaxHelp="The minimum resolution limit"):
        form.addParam('dMin', pwprot.FloatParam,
                      default=None,
                      allowsNull=True,
                      label="High resolution limit",
                      help=dminHelp)

        form.addParam('dMax', pwprot.FloatParam,
                      default=None,
                      allowsNull=True,
                      label="Low resolution limit",
                      help=dmaxHelp)

    def getDMax(self):
        return self.dMax.get()

    def getDMin(self):
        return self.dMin.get()

    def swappedResolution(self):
        # d_min (high resolution) should always be smaller than d_max (low resolution).
        if self.getDMin() is not None and self.getDMax() is not None:
            # Check for the case where both d_min and d_max are set and have wrong relative values
            return self.getDMin() > self.getDMax()
        else:
            # If at least one value is None, then no swap is possible
            return False

    def resSwapMsg(self):
        msg = (f"High ({self.getDMin()} Å) and low ({self.getDMax()} Å) "
               f"resolution limits appear swapped.")
        return msg
