# -*- coding: utf-8 -*-

from astropy.extern import six
from astropy.io.fits.diff import FITSDiff
from astropy.io import fits
from contextlib import nested
from astropy.extern.six.moves import StringIO

__all__ = ['fits_osiris_allclose']

def fits_osiris_allclose(a, b):
    """Assert that two OSIRIS fits files are close."""
    
    a = fits.open(a)
    b = fits.open(b)
    
    try:
        del a[0].header['COMMENT']
        del b[0].header['COMMENT']
    
        report = StringIO()
        diff = FITSDiff(
            a, b,
            ignore_keywords=["COMMENT"],
            ignore_comments=["SIMPLE"],
            ignore_fields=[],
            ignore_blanks=True,
            ignore_blank_cards=True,
            tolerance=1e-5)
        diff.report(fileobj=report)
        assert diff.identical, report.getvalue()
    
    finally:
        a.close()
        b.close()
