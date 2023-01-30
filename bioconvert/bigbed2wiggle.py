###########################################################################
# Bioconvert is a project to facilitate the interconversion               #
# of life science data from one format to another.                        #
#                                                                         #
# Copyright © 2018-2022  Institut Pasteur, Paris and CNRS.                #
#                                                                         #
# bioconvert is free software: you can redistribute it and/or modify      #
# it under the terms of the GNU General Public License as published by    #
# the Free Software Foundation, either version 3 of the License, or       #
# (at your option) any later version.                                     #
#                                                                         #
# bioconvert is distributed in the hope that it will be useful,           #
# but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# GNU General Public License for more details.                            #
#                                                                         #
# You should have received a copy of the GNU General Public License       #
# along with this program (COPYING file).                                 #
# If not, see <http://www.gnu.org/licenses/>.                             #
#                                                                         #
# Repository: https://github.com/bioconvert/bioconvert                    #
# Documentation: http://bioconvert.readthedocs.io                         #
###########################################################################
"""Convert :term:`BIGBED` format to :term:`WIGGLE` format"""
import os
from tempfile import NamedTemporaryFile
import colorlog

from bioconvert import ConvBase
from bioconvert.core.decorators import requires

_log = colorlog.getLogger(__name__)


__all__ = ["BIGBED2WIGGLE"]


class BIGBED2WIGGLE(ConvBase):
    """Convert sorted :term:`BIGBED` file into :term:`WIGGLE` file

    Methods available are based on wiggletools [WIGGLETOOLS]_.
    """

    #: Default value
    _default_method = "wiggletools"

    def __init__(self, infile, outfile):
        """
        :param str infile: The path to the input BIGBED file. **It must be sorted**.
        :param str outfile: The path to the output file
        """
        super(BIGBED2WIGGLE, self).__init__(infile, outfile)

    @requires("wiggletools")
    def _method_wiggletools(self, *args, **kwargs):
        """Conversion using wiggletools

        `wiggletools documentation <https://github.com/Ensembl/WiggleTools>`_"""

        # with need a unique name, that does not exists for the symlink
        # Fixes #233
        fname = None
        with NamedTemporaryFile(suffix=".bb") as ftemp:
            fname = ftemp.name

        os.symlink(os.path.abspath(self.infile), ftemp.name)

        try:
            cmd = "wiggletools {} > {}".format(ftemp.name, self.outfile)
            self.execute(cmd)
        except Exception as err:
            raise (err)
        finally:
            # clean symlink
            os.unlink(fname)
