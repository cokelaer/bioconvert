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
"""Convert :term:`BPLINK` to :term:`PLINK` format"""
import colorlog

from bioconvert import ConvBase
from bioconvert.core.decorators import requires
from bioconvert.core.utils import generate_outfile_name

_log = colorlog.getLogger(__name__)


class BPLINK2PLINK(ConvBase):
    """Converts a genotype dataset bed+bim+fam in :term:`BPLINK` format to
    ped+map :term:`PLINK` format.

    Conversion is based on plink [PLINK]_ executable.

    .. warning:: **plink** takes several inputs and outputs and does not need
        extensions. What is required is a prefix. Bioconvert usage is therefore::

            bioconvert bplink2plink plink_toy

        Since there is no extension, you must be explicit by providing the
        conversion name (bplink2plink). This command will search for 3 input
        files plink_toy.bed, plink_toy.bim and plink_toy.fam. It will then
        create two output files named plink_toy.ped and plink_toy.map

    """

    #: Default value
    _default_method = "plink"

    def __init__(self, infile, outfile=None, *args, **kwargs):
        """.. rubric:: constructor

        :param str infile: input :term:`BPLINK` files.
        :param str outfile: (optional) output :term:`PLINK` files.
        """
        if not outfile:
            outfile = infile
        super(BPLINK2PLINK, self).__init__(infile, outfile)

    @requires("plink")
    def _method_plink(self, *args, **kwargs):
        """Convert plink file in text using plink executable.

        `plink documentation <http://hpc.ilri.cgiar.org/beca/training/data_mgt_2017/BackgroundMaterial/PlinkTutorial.pdf>`_"""
        cmd = "plink --bfile {infile} --recode --out {outfile}".format(infile=self.infile, outfile=self.outfile)
        self.execute(cmd)
