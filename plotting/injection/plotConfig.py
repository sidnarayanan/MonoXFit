#!/usr/bin/env python


plotDir = '/home/snarayan/public_html/figs/monotop/v14//fits_unblind/2cat/injeced/'
scansDir = '/data/t3home000/snarayan/store/panda/v_8026_0_4/fitting/scans_injected/'
lumi = 35.8

if __name__=="__main__":
  from os import system
  system('mkdir -p '+plotDir)
