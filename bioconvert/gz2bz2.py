# -*- coding: utf-8 -*-
##############################################################################
#  This file is part of Bioconvert software
#
#  Copyright (c) 2017 - Bioconvert Development Team
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/biokit/bioconvert
#  documentation: http://bioconvert.readthedocs.io
##############################################################################
"""Convert :term:`GZ` file to :term:`BZ2` file"""
from bioconvert import ConvBase, extensions
from bioconvert.core.base import ConvArg

__all__ = ["GZ2BZ2"]


class GZ2BZ2(ConvBase):
    """Convert :term:`GZ` file to :term:`BZ2` file

    unzip input file using pigz and compress using pbzip2

    """
    #_is_compressor = True

    def __init__(self, infile, outfile, *args, **kargs):
        """.. rubric:: constructor

        :param str infile: input GZ file
        :param str outfile: output BZ2 filename

        """
        super(GZ2BZ2, self).__init__(infile, outfile, *args, **kargs)

    def _method_pigz_pbzip2(self, threads=1, *args, **kwargs):
        """some description"""
        # check integrity
        # cmd = "pigz -p{threads} --test {input}"
        # shell(cmd)
        if isinstance(threads, str):
            threads = str(threads)

        # conversion
        cmd = "pigz -d -c -p {threads} {input} | pbzip2 -p{threads} > {output}"
        self.execute(cmd.format(
            threads=threads,
            input=self.infile,
            output=self.outfile))

        # integrity output
        # cmd = "pbzip2 {output} -p{threads} --test"
        # shell(cmd)

        # use self.infile, self.outfile

    @classmethod
    def get_additional_arguments(cls):
        yield ConvArg(
            names=["-x", "--threads", ],
            default=1,
            help="Number of threads. Depends on the underlying tool",
        )
