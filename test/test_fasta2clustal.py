import os
import pytest
from easydev import TempFile, md5

from bioconvert import bioconvert_data
from bioconvert.fasta2clustal import FASTA2CLUSTAL

skiptravis = pytest.mark.skipif("TRAVIS_PYTHON_VERSION" in os.environ
                                and os.environ['TRAVIS_PYTHON_VERSION'].startswith("2"), reason="On travis")



@skiptravis
def test_fasta2clustal_biopython():
    infile = bioconvert_data("biopython.fasta")
    outfile = bioconvert_data("biopython.clustal")
    with TempFile(suffix=".clustal") as tempfile:
        converter = FASTA2CLUSTAL(infile, tempfile.name)
        converter(method='biopython')

        # Check that the output is correct with a checksum
        assert md5(tempfile.name) == md5(outfile)


@skiptravis
@pytest.mark.skipif(FASTA2CLUSTAL._method_squizz.is_disabled, reason="missing dependencies")
def test_fasta2clustal_squizz():
    infile = bioconvert_data("squizz.fasta")
    outfile = bioconvert_data("squizz.clustal")
    with TempFile(suffix=".clustal") as tempfile:
        converter = FASTA2CLUSTAL(infile, tempfile.name)
        converter(method='squizz')

        # Check that the output is correct with a checksum
        assert md5(tempfile.name) == md5(outfile)
