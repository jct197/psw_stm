# -*- script: utf-8 -*-
from binary.readstm import OpenWinSTM
from func.dfunc import image_plot, spec_plot


test = OpenWinSTM('test_data/035005.stm')
test.readfil()

out = test.get_data()
 
for key, value in out.items():
    if 'spec' not in key:
        image_plot(out[key]['Data'],title=str(key)+', '+'(V = '+str(out[key]['bias'])+' V'
                   +', I = '+str(out[key]['current'])+' nA'+')')
    else:
        spec_plot(out[key],title=str(key))