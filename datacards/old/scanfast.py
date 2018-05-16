#!/usr/bin/env python

from os import system
from re import sub
from sys import argv
from argparse import ArgumentParser

parser = ArgumentParser(description='perform 2d scan')
parser.add_argument('template',metavar='template',type=str)
parser.add_argument('--mMed',type=int,default=None)
parser.add_argument('--mChi',type=int,default=None)
parser.add_argument('--isRes',dest='isRes',action='store_true')
parser.add_argument('--isFCNC',dest='isRes',action='store_false')
parser.set_defaults(isRes=False)
args = parser.parse_args()

class Model():
  def __init__(self,mMed,mChi,isRes):
    self.mMed=mMed
    self.mChi=mChi
    self.isRes=isRes
    if isRes:
      #self.name = 'monotop_med-%i_dm-%i'%(mMed,mChi)
      self.name = 'monotop_med-%i'%(mMed)
    else:
      #self.name = 'monotop-nr-v3-%i-%i_med-%i_dm-%i'%(mMed,mChi,mMed,mChi)
      self.name = 'MonoTop_%i_%i_0.25_1_801'%(mMed,mChi)

def run(model,runObserved=True):
  label = 'res_' if model.isRes else 'fcnc_'
  label += '%i_%i'%(model.mMed,model.mChi)
  runOption = '' if runObserved else '--run=blind'
  cmd = "sed 's?XXXX?%s?g' %s > combined_%s.txt"%(model.name,args.template,label)
  system(cmd)
  system("sed -i 's?combined_model\.root?../combined_model.root?g' combined_%s.txt"%(label))
  # system("sed 's/XXXX/%s/g %s > combined_%s.txt'"%(model.name,args.template,label))
  cmd = "combine -M Asymptotic combined_%s.txt -n %s"%(label,label)
  print cmd
  system(cmd)
  # system("combine -M Asymptotic combined_%s.txt -n %s -m %i"%(label,model.mMed*1000+mChi))

model = Model(args.mMed,args.mChi,args.isRes)
run(model,True)

