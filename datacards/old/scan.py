#!/usr/bin/env python

from os import system
from re import sub


def run(modelClass,modelsList,runObserved):
  if runObserved:
    print 'UNBLINDING'
  s=''
  logfile = '%s_%slimits.txt'%(modelClass,'obs_' if runObserved else '')
#  s += 'rm -f %s\n'%(logfile)
  runOption = '' if runObserved else ' --run=blind'
  for l in modelsList:
    print l
    mass = sub('[A-z]*','',l.split('_')[-1])
    s += 'echo "MASS %s" \n'%(mass)
    s += "sed 's/XXXX/%s/g' combined_tmpl.txt > combined_run.txt \n"%(l)
    s += "combine -M Asymptotic combined_run.txt %s > tmp.txt\n"%(runOption)
    s += 'grep "<" tmp.txt \n'
  with open('run.sh','w') as runFile:
    runFile.write(s)
  system('sh run.sh > '+logfile)
    
run('fcnc',['monotop_fcnc_mMed%i'%m for m in xrange(300,1700,200)+[2100]],True)
run('resonant',['monotop_res_mMed%i'%(x) for x in xrange(900,2300,200)],True)
