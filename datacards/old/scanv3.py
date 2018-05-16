#!/usr/bin/env python

from os import system
from re import sub


def run(modelClass,modelsList,runObserved=True):
  s=''
  logfile = '%sv3_%slimits.txt'%(modelClass,'obs_' if runObserved else '')
  runOption = '' if runObserved else ' --run=blind'
  for l in modelsList:
    print l
    mass = sub('[A-z]*','',l.split('_')[0])
    if 'nr' in l:
      mass = l.split('-')[3]
    else:
      mass = sub('_dm','',l.split('-')[1])
    print mass
    s += 'echo "MASS %s" \n'%(mass)
    s += "sed 's/XXXX/%s/g' combined_tmpl.txt > combined_run.txt \n"%(l)
    s += "combine -M Asymptotic combined_run.txt %s > tmp.txt\n"%(runOption)
    s += 'grep "<" tmp.txt \n'
  with open('run.sh','w') as runFile:
    runFile.write(s)
  system('sh run.sh > '+logfile)
    

run('fcnc',['monotop-nr-v3-%i-10_med-%i_dm-10'%(m,m) for m in range(300,2300,200)],True)
run('resonant',['monotop_med-%i_dm-100'%(m) for m in range(900,3100,200)],True)
