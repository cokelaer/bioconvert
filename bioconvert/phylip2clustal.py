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
"""Converts :term:`PHYLIP` file to :term:`CLUSTAL` format."""
import colorlog
from Bio import SeqIO

from bioconvert import ConvBase
from bioconvert.core.decorators import compressor, requires

_log = colorlog.getLogger(__name__)


__all__ = ["PHYLIP2CLUSTAL"]


class PHYLIP2CLUSTAL(ConvBase):
    """
    Converts a sequence alignment from :term:`PHYLIP` format to :term:`CLUSTAL` format

    Methods available are based on biopython [BIOPYTHON]_, squiz [SQUIZZ]_.

    """

    #: Default value
    _default_method = "biopython"

    def __init__(self, infile, outfile=None, alphabet=None, *args, **kwargs):
        """.. rubric:: constructor

        :param str infile: input :term:`PHYLIP` file.
        :param str outfile: (optional) output :term:`FASTA` file
        """
        super().__init__(infile, outfile)
        self.alphabet = alphabet

    @requires(python_library="biopython")
    @compressor
    def _method_biopython(self, *args, **kwargs):
        """Convert :term:`PHYLIP` interleaved file in :term:`CLUSTAL` format using biopython.

        `Bio.SeqIO Documentation <https://biopython.org/docs/1.76/api/Bio.SeqIO.html>`_"""
        sequences = list(SeqIO.parse(self.infile, "phylip", alphabet=self.alphabet))
        _ = SeqIO.write(sequences, self.outfile, "clustal")

    @requires("squizz")
    @compressor
    def _method_squizz(self, *args, **kwargs):
        """Convert :term:`PHYLIP` interleaved file in :term:`CLUSTAL` format using squizz tool."""
        cmd = "squizz -c CLUSTAL {infile} > {outfile}".format(infile=self.infile, outfile=self.outfile)
        self.execute(cmd)
