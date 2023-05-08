# -*- coding: utf-8 -*-
#
# John C. Thomas 2023
# Modified and converted from openwinstm.m, written by Brent Mantooth (2002)
from .bindef import binread, fixprint
import numpy as np


def update_spec(imat,nsweep,offset,nschan,newsweep,nspts,sxout,rev):
    tmp1 = []
    tmp2 = []
    for i in range(0,imat.shape[0]):
        for j in range(0,imat.shape[1]):
            if j < int(imat.shape[1]/newsweep):
                tmp1.append(imat[i][j][0])
            else:
                tmp2.append(imat[i][j][0])
    tmp1a = []
    tmp2a = []
    t1alen = len(tmp1a)
    t2alen = len(tmp2a)
    idata = np.zeros((nschan+1,newsweep,nspts))
    itmp = np.zeros((1,1,nspts))
    offset = 1
    for newswp in range(0,newsweep):
        ind1 = offset + nspts-1
        ind3 = offset
        xinput = sxout[ind3-1:ind1]
        xinputa = []
        for xval in xinput:
            xinputa.append(xval)
        itmp[0,0,:] = xinputa    
        idata[0,newswp,:] = itmp[0,0,:]
        offset = offset + nspts
    for newchan in range(0,nschan):
        offset = 1
        for newswp in range(0,newsweep):
            if rev == 2:
                ind1 = offset + nspts-1
                ind2 = offset
                dinput = imat[newchan,ind2-1:ind1]
                dinputa = []
                for rval in dinput:
                    dinputa.append(rval)
                itmp[0,0,:] = dinputa
            else: 
                ind1 = offset + nspts-1
                ind2 = offset
                dinput = imat[newchan,ind2-1:ind1]
                dinputa = []
                for rval in dinput:
                    dinputa.append(rval)
                itmp[0,0,:] = dinputa
            idata[newchan+1,newswp,:] = itmp[0,0,:]
            offset = offset + nspts
    for aind in range(0,newsweep):
        if aind % 2 != 0:
            idata[:,aind,:] = idata[:,aind,::-1]
    return idata

class OpenWinSTM(object):
    def __init__(self, fil):
        """Constructor"""
        self.fil = fil
        self.stmdata = {}
        
    def readfil(self):
        ## read in header ##
        f = open(self.fil, 'rb')
        f.seek(0,0)
        tag = f.read(6)
        f.seek(932,0)
        NChan = binread(f,1,np.int32)[0][0]
        NSpec = binread(f,1,np.int32)[0][0]
        f.seek(1024,0)
        RangeX = binread(f,1,np.double)
        RangeY = binread(f,1,np.double)
        Headersize = 1368
        Datasize = 768
        Dataoffset = 1368
        ## read in image channel ##
        for i in range(0,NChan):
            f.seek(Dataoffset+2,0)
            description = f.read(100)
            dtmp = fixprint(description)
            self.stmdata[str(dtmp)] = {}
            f.seek(Dataoffset+624,0)
            ImageGain = binread(f,1,np.double)
            UnitName = f.read(64)
            utmp = fixprint(UnitName)
            f.seek(Dataoffset+696,0)
            bias = binread(f,1,np.double)
            current = binread(f,1,np.double)
            npts = binread(f,1,np.int32)
            nscan = binread(f,1,np.int32)
            f.seek(Dataoffset+Datasize,0)
            fsize = npts[0][0]*nscan[0][0]
            xx = npts[0][0]
            yy = nscan[0][0]
            out = binread(f,fsize,np.int32)
            Image = out
            Image = np.reshape(Image,[nscan[0][0],npts[0][0]],order='A')
            Image = ImageGain[0][0]*np.flipud((Image))
            self.stmdata[str(dtmp)]['Data'] = Image
            self.stmdata[str(dtmp)]['units'] = utmp
            self.stmdata[str(dtmp)]['gain'] = ImageGain[0][0]
            self.stmdata[str(dtmp)]['bias'] = bias[0][0]
            self.stmdata[str(dtmp)]['current'] = current[0][0]
            self.stmdata[str(dtmp)]['npts'] = npts[0][0]
            self.stmdata[str(dtmp)]['nscan'] = nscan[0][0]
            self.stmdata[str(dtmp)]['fsize'] = fsize
            self.stmdata[str(dtmp)]['RangeX'] = RangeX
            self.stmdata[str(dtmp)]['RangeY'] = RangeY
            Dataoffset = f.tell()
        ## read in spec ##    
        if NSpec > 0:
            for numspec in range(0,NSpec):
                f.seek(Dataoffset,0)
                bias = binread(f,1,np.float32)
                current = binread(f,1,np.float32)
                startval = binread(f,1,np.float32)
                endval = binread(f,1,np.float32)
                stepsize = binread(f,1,np.float32)
                rate = binread(f,1,np.float32)
                sampletime = binread(f,1,np.float32)
                nschan = binread(f,1,np.int32) 
                nsweep = binread(f,1,np.int32)
                nspts = binread(f,1,np.int32)
                conv = binread(f,1,np.int32)
                xpix = binread(f,1,np.int32)
                ypix = binread(f,1,np.int32)
                specmode = binread(f,1,np.int32)
                AcqRev = binread(f,1,np.uint8)
                rev = 1
                if AcqRev[0][0] == 1:
                    rev = 2
                idx = nspts[0][0]*nsweep[0][0]*rev
                snamed = f.read(100)
                snamed = fixprint(snamed)
                snamed2 = f.read(100)
                snamed2 = fixprint(snamed2)
                iaxis = []
                for k in range(0,nschan[0][0]):
                    tmp = []
                    sname = f.read(100)
                    sname2 = f.read(100)
                    ptmp = fixprint(sname)
                    tmp.append(ptmp)
                    ptmp = fixprint(sname2)
                    tmp.append(ptmp)
                    iaxis.append(tmp)
                sxout = binread(f,idx,np.float32)
                arrsxout = np.array(sxout)
                syout = []
                for spec in range(1,nschan[0][0]+1):
                    tmp = binread(f,idx,np.float32)
                    syout.append(tmp)
                newsweep = nsweep[0][0]*rev
                newpts = nspts[0][0]
                ispec = np.array(syout)
                ivals = update_spec(ispec,nsweep[0][0],1,int(nschan[0][0]),int(newsweep),int(newpts),sxout,rev)
                self.stmdata['spec_'+str(numspec+1)] = {}
                self.stmdata['spec_'+str(numspec+1)]['Data'] = ivals
                self.stmdata['spec_'+str(numspec+1)]['xpix'] = xpix[0][0]
                self.stmdata['spec_'+str(numspec+1)]['ypix'] = ypix[0][0]
                self.stmdata['spec_'+str(numspec+1)]['descriptions'] = iaxis
                self.stmdata['spec_'+str(numspec+1)]['units'] = snamed
                self.stmdata['spec_'+str(numspec+1)]['rev'] = rev
                Dataoffset = f.tell()
        
    def get_data(self):
        return self.stmdata