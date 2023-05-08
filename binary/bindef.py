# -*- coding: utf-8 -*-
#
# John C. Thomas 2023
import numpy as np


def binread(fid, nel, dtype = float):
     if dtype is np.str_:
         dt = np.uint8 
     else:
         dt = dtype
     darray = np.fromfile(fid, dt, nel)
     darray.shape = (nel, 1)
     return darray  
 
def fixprint(din):
    pout1 = din.decode('utf-8', errors='ignore')
    ptmp = ''
    for k in pout1:
        if k.isprintable():
            ptmp += k
    if ptmp == 'ngstroms':
        ptmp = 'angstroms'
    return ptmp
