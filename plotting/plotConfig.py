#!/usr/bin/env python


plotDir = '/home/snarayan/public_html/figs/monotop/v14//papers/fits_maxlikelihood/'
scansDir = '/data/t3home000/snarayan/store/panda/v_8026_0_5_slim/fitting/scans/' # resonant
#scansDir = '/data/t3home000/snarayan/store/panda/v_003_0/fitting/scans2_couplings2/' # coupling scans
#scansDir = '/data/t3home000/snarayan/store/panda/v_003_0/fitting/scans2_mass/' # mass-mass and mass-g-g
lumi = 35.8

from os import system
system('mkdir -p '+plotDir)
