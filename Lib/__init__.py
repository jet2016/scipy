#try:
    #import gui_thread
#except:
    #print "Warning:  wxPython not loaded"

from scipy_version import scipy_version as __version__

# SciPy has levels
# Level 0 -- Numeric and core routines in basic.py, misc.py, and handy.py
#
# Level 1 -- Level 0 + fft, special, linalg (these can depend on Level 0), stats
# Level 1a -- Core routines which depend on Level 1.
# Level 2 -- plotting interface.
# Packages which define own functions plus depend on Levels 0-2.
#
# Level 0, 1, 2 should be imported in order and then other levels imported
#   as available.


import Numeric
import os,sys
from helpmod import help, source
from Matrix import Matrix as Mat
import fastumath

Inf = inf = Numeric.array(1e308)**10
NaN = nan = Numeric.array(0.0) / Numeric.array(0.0)

import string
def somenames2all(alist, namedict, gldict):
    for key in namedict.keys():
        exec("from %s import %s" % (key, string.join(namedict[key],',')), gldict)
        alist.extend(namedict[key])
    
def names2all(alist, spaces, gldict):
    for name in spaces:
        exec("import %s" % name, gldict)
        thelist = eval(name,gldict).__dict__.keys()
        exec("from %s import *" % name, gldict)
        exec("del %s" % name, gldict)
        for key in thelist:
            if key[0] == "_":
                thelist.remove(key)
        alist.extend(thelist)

def modules2all(alist, mods, gldict):
    for name in mods:
        exec("import %s" % name, gldict)
        alist.append(name)
    
def objects2all(alist, objlist):
    alist.extend(objlist)

# modules to import under the scipy namespace
_level0 = ["fastumath", "basic", "handy", "misc", "scimath"]
_partials0 = {'Matrix' : ['Matrix']}
# these modules will just be imported (not subsumed)
_level0_importonly = []

_level1 = ["special", "io", "linalg", "stats"]  # fft is in this group.
_partials1_a = {'stats' : ['mean','median','std','cov','corrcoef']}
_level1a = ["basic1a"] # functions to be subsumed into scipy namespace which
                      # require level 0 and level 1
# these modules will just be imported (not subsumed)                      
_level1a_importonly = []


__all__=[]
somenames2all(__all__, _partials0, globals())
names2all(__all__, _level0, globals())
modules2all(__all__, _level0, globals())
modules2all(__all__, _level0_importonly, globals())
objects2all(__all__, ['help', 'source', "Inf", "inf", "NaN", "nan", "Mat"])

# Level 1
modules2all(__all__, _level1, globals())

try:
    import scipy.fftw
    __all__.append('fftw')
    _partials1 = {'fftw' : ['fft', 'fftnd', 'fft2d', 'fft3d',
                            'ifft', 'ifft2d', 'ifft3d', 'ifftnd']}
    somenames2all(__all__, _partials1, globals())
except ImportError:
    print sys.exc_value
    print "Warning: FFT package not found. Some names will not be available"

somenames2all(__all__,_partials1_a, globals())

# Level 1a
names2all(__all__, _level1a, globals())
from scimath import *
modules2all(__all__, _level1a, globals())
modules2all(__all__, _level1a_importonly, globals())


# Level 2

_level2 = ["optimize", "integrate", "signal", "special", "interpolate", "cow", "ga", "cluster", "weave"]
modules2all(__all__, _level2, globals())

# Level 3
_plot = []
#try:
#    import xplt
#    __all__.append('xplt')
#    _plot.append('xplt')
#except ImportError:
#    pass

try:
#   gplt on win32 messes up focus and takes up 99%
#   of processor -- works fine on *nix.
    if sys.platform != 'win32':
        import gplt
        __all__.append('gplt')
        _plot.append('gplt')
except ImportError:
    pass

#if _plot == []:
#    print "Warning: No plotting available."
#else:
#    print "Plotting methods available: ", _plot



#---- testing ----#

def test(level=1):
    """ From this top level, there are possibly many many tests.
        Test only the quick tests by default.
    """
    import unittest
    runner = unittest.TextTestRunner()
    runner.run(test_suite(level))
    return runner

def test_all(level=10):
    test(level)
    
def test_suite(level = 1):
    import scipy_test
    import scipy
    ignore = ['xplt','plt','gplt','gui_thread','linalg','sparse','scipy_version']
    return scipy_test.harvest_test_suites(scipy,ignore,level=level)












