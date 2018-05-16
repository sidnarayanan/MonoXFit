#!/usr/bin/env python

from argparse import ArgumentParser
from sys import argv, exit

parser = ArgumentParser()
parser.add_argument('datacard', type=str)
parser.add_argument('--best_r', type=float, default=-1)
parser.add_argument('--freeze', type=str, default=None)
parser.add_argument('--bypassFrequentistFit', action='store_true')
parser.add_argument('--pos', type=str, default='exp50')
args = parser.parse_args()

argv = []


from multiprocessing import Pool
from os import path, system, chdir
from ROOT import TFile, TTree
from numpy import linspace, inf, interp, argsort, array


if __name__ == '__main__':
    _pos = {
            'exp2p5' : 0,
            'exp16'  : 1,
            'exp50'  : 2,
            'exp84'  : 3,
            'exp97p5': 4,
            'obs'    : 5
        }
    pos = _pos[args.pos]

    ftmpl = 'higgsCombine%s.Asymptotic.mH120.root'

    def get_cls(name):
        f = TFile(ftmpl%name)
        t = f.Get('limit')
        t.GetEntry(pos)
        return t.limit

    def execute(cmd):
        print cmd
        system(cmd)

    system('mkdir -p tmp/')
    chdir('tmp')
    system('rm -f *root')

    cmd = 'combine -M Asymptotic --minimizerTolerance 0.001 '
    if 'MultiDimFit' in args.datacard: # picking up a snapshot
        cmd += ' ../%s --snapshotName MultiDimFit'%args.datacard
        if args.bypassFrequentistFit: # don't bother refitting theta_hat
            cmd += ' --bypassFrequentistFit'
    else:
        cmd += ' ../%s'%args.datacard

    cmd_prefit = cmd
    if args.freeze:
        cmd += ' --freezeNuisanceGroups %s'%args.freeze

    # refit if we don't have the nominal r
    if args.best_r < 0:
        execute(cmd_prefit + ' -n nominal')
        args.best_r = get_cls('nominal')

    mus = linspace(args.best_r*0.9, args.best_r*1.1, 41)

    cmdargs = [cmd + ' --singlePoint %.6f -n %.6f'%(x,x) for x in mus]

    pool = Pool(10)
    pool.map(execute, cmdargs)

    clss = array([get_cls('%.6f'%mu) for mu in mus])

#    print zip(mus, clss)

    idx = argsort(clss)

    best_mu = interp(0.05, clss[idx], mus[idx])

    print 'INTERPOLATED CLs=0.05 FOR %s, FREEZING %s, AT %f (%f CHANGE)'%(args.pos, args.freeze, best_mu, best_mu/args.best_r - 1)

    chdir('..')
    system('mkdir -p grouped_impacts')
    with open('grouped_impacts/%s.txt'%args.freeze, 'w') as fdump:
        fdump.write('%f %f'%(best_mu, best_mu/args.best_r - 1))
