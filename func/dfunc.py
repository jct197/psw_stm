# -*- script: utf-8 -*-
#
# John C. Thomas 2023
import matplotlib.pyplot as plt
import numpy as np


def image_plot(imagein, title='WinSTM Image', cbar=1, imsave = 0, loc = None):
    fig, ax = plt.subplots()
    z_min, z_max = imagein.min(), imagein.max()
    x, y = np.meshgrid(np.linspace(1, imagein.shape[0], imagein.shape[0]), np.linspace(1, imagein.shape[1], imagein.shape[1]))
    cout = ax.pcolormesh(x, y, imagein, cmap='bone', vmin=z_min, vmax=z_max, shading='auto')
    ax.set_title(title)
    ax.axis([x.min(), x.max(), y.min(), y.max()])
    if cbar == 1:
        fig.colorbar(cout, ax=ax)
    plt.axis('scaled')
    fig.tight_layout()
    if imsave == 1:
        if loc == None:
            print("File location not specified.")
        else:
            fig.savefig(loc, dpi=fig.dpi)
    plt.show() 
    
def spec_plot(dictin,title='STS'):
    specin = dictin['Data']
    labels = dictin['descriptions']
    units = dictin['units']
    rev = dictin['rev']
    for spectra in range(1,specin.shape[0]):
        fig = plt.figure(figsize = (6,4))   
        ax = fig.add_subplot(1,1,1)
        ax.set_xlabel(units,fontsize=14)
        ax.set_ylabel(labels[spectra-1][0],fontsize=14) 
        ax.margins(x=0)
        davg = []
        if rev == 2:
            for sweep in range(0,specin.shape[1]):
                ax.scatter(specin[0,sweep,:],specin[spectra,sweep,:],s=20)
                davg.append(specin[spectra,sweep,:])
        else:
            for sweep in range(0,specin.shape[1]):
                ax.scatter(specin[0,sweep,:],specin[spectra,sweep,:],s=20)
                if sweep % 2 != 0:
                    davg.append(specin[spectra,sweep,:])
                else:
                    davg.append(specin[spectra,sweep,::-1])
        ax.set_title(title)
        davg = np.array(davg)
        avg = np.average(davg,axis=0)
        ax.plot(specin[0,sweep,:],avg,linewidth=4,c='k')
        fig.tight_layout()
        plt.show()