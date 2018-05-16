#!/usr/bin/env python

import cPickle as pickle
from math import sqrt

processes = [
      'zvv',
      'ttbar',
      'wjets',
#      'qcd',
#      'dibosons',
#      'stop',
      'minor',
      'data',
      'total',
]

def dump(cat):
    da = pickle.load(open('all/'+cat+'.pkl','r'))
    ds = pickle.load(open('statonly/'+cat+'.pkl','r'))

    print cat 

    N = len(da)
    for ib in xrange(1, N+1):
        for d in [ds[ib], da[ib]]:
            minor_val = 0; minor_err = 0;
            for p in ['stop', 'dibosons']:
                minor_val += d[p][0]
                minor_err += d[p][1]**2
            d['minor'] = (minor_val, sqrt(minor_err))
        s = [da[ib]['title'].replace('$','').replace('-','--').replace('&','')]
        for p in processes:
            if p == 'data':
                s.append( '$%10i$'%int(da[ib][p][0]) )
            else:
                val = da[ib][p][0]
                total_err = da[ib][p][1]
                stat_err = ds[ib][p][1]
                syst_err = sqrt(total_err**2 - stat_err**2)
                if val > 1:
                    s.append( r'$%6.1f \pm %4.1f \pm %4.1f$'%(val, stat_err, syst_err) )
                else:
                    s.append( r'$%6.2f \pm %4.2f \pm %4.2f$'%(val, stat_err, syst_err) )
        print (' & '.join(s)) + r'\\'

dump('loose')
dump('tight')
