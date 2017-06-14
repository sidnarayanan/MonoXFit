#!/usr/bin/env python

from os import system,environ
from re import sub
from sys import argv, exit
from argparse import ArgumentParser
from array import array
from time import time

parser = ArgumentParser(description='perform 2d scan')
parser.add_argument('--template',metavar='template',type=str,default='newewk_tmpl.txt')
parser.add_argument('--cfg',type=str,nargs='+') 
parser.add_argument('--outdir',type=str)
parser.add_argument('--indir',type=str)
args = parser.parse_args()
argv = []

import ROOT as root
root.gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ");
root.gSystem.AddIncludePath("-I$ROOFITSYS/include");
root.gSystem.Load("libRooFit.so")
root.gSystem.Load("libRooFitCore.so")
from HiggsAnalysis.CombinedLimit.ModelTools import *

class Model():
    def __init__(self,model_name,mass_name,coupling_name):
        self.coupling = coupling_name
        self.mass = mass_name
        self.model = model_name
        if model_name=='vector':
            self.name = self.mass
        else:
            self.name = self.model +'_'+self.mass


indir = args.indir
outdir = args.outdir
models = [Model(*(args.cfg))]
scaling = None

def makeHists(model,infile):
    global scaling
    name_ = sub('-','_',sub('\.','p',model.name))
    fout = root.TFile(name_+'_model.root','RECREATE')
    bins = array('f',[250,280,310,350,400,450,600,1000])
    N = len(bins)-1
    print 'Opening %s'%infile
    fin = root.TFile(infile)

    wspace = root.RooWorkspace("signalws")

    fout.cd()
    tags = {
            'loose_' : 'loose',
            '' : 'tight',
            }

    fhists = root.TFile('signalmodel.root','RECREATE')

    vmets = {}

    for tag_label,tag_name in tags.iteritems():
        vmet = root.RooRealVar('min(999.9999,met)','min(999.9999,met)',250,1000)
        if 'loose' in tag_label:
            vmet.SetName('min(999.9999,met)_monotop_loose')
        else:
            vmet.SetName('min(999.9999,met)_monotop')
        vmet.setMin(250); vmet.setMax(1000)
        getattr(wspace,'import')(vmet,root.RooFit.RecycleConflictNodes())
        vmets[tag_label] = vmet

        if m.coupling=='nominal':
            print 'Opening folder: nominal'
            folder = fin.Get('nominal')
        else:
            print 'Opening folder: rw_%s_nlo'%(m.coupling)
            folder = fin.Get('rw_%s_nlo'%(m.coupling))

        for syst in ['','_btagUp','_btagDown','_mistagUp','_mistagDown',
                        '_sjbtagUp','_sjbtagDown','_sjmistagUp','_sjmistagDown']:
            hist = folder.Get('h_%s%s'%(tag_name,syst))
            if scaling:
                hist.Scale(scaling)
            elif hist.Integral() > 5000:
                scaling = 0.01
                hist.Scale(scaling)
            elif hist.Integral() > 500:
                scaling = 0.1
                hist.Scale(scaling)
            elif hist.Integral() < 0.001:
                scaling = 1000
                hist.Scale(scaling)
            elif hist.Integral() < 0.01:
                scaling = 100
                hist.Scale(scaling)
            if scaling:
                print 'SCALING BY',scaling
            dhist = root.RooDataHist('monotop_%ssignal_%s%s'%(tag_label,name_,syst),
                                     '%ssignal %s %s'%(tag_label,name_,syst),
                                     root.RooArgList(vmet),
                                     hist)
            getattr(wspace,'import')(dhist,root.RooFit.RecycleConflictNodes())
    wspace.Print()


    fout.Close()
    wspace.writeToFile(name_+'_dmodel.root')
    fout = root.TFile(name_+'_dmodel.root')
    fout.ls()
    fout.Close()


def run(model,infile,runObserved=True):
    global scaling
    start = time()
    if model.model=='vector':
        label = 'fcnc_'
    elif model.model=='scalar':
        label = 'res_'
    else:
        label = 'stdm_'
    label += model.mass
    name_ = sub('-','_',sub('\.','p',model.name))
    cmd = "sed 's?XXXX?%s?g' %s > scan_%s.txt"%(name_,args.template,label)
    #cmd = "sed 's?XXXX?%s?g' %s > combined_%s.txt"%(sub('1.0','1',model.name),args.template,label)
    system(cmd)
    cmd = "sed -i 's?signal_model\.root?%s_dmodel\.root?g' scan_%s.txt"%(name_,label)
    system(cmd)
    print 'setup took %i'%(time()-start); start = time()
    makeHists(model,infile)
    print 'drawing took %i'%(time()-start); start = time()
    cmd = "combine -M Asymptotic scan_%s.txt -n %s"%(label,label)
    print cmd
    system(cmd)
    print 'fitting took %i'%(time()-start); start = time()
    if scaling:
        print 'Adding scaling parameter'
        flimits = root.TFile('higgsCombine%s.Asymptotic.mH120.root'%label,'UPDATE')
        tscaling = root.TNamed('scaling', '%s'%scaling)
        print flimits, tscaling
        flimits.WriteTObject(tscaling,'scaling')
        flimits.Close()
    # flimit = root.TFile('higgsCombinefcnc_%i_%i.Asymptotic.mH120.root'%(model.mMed,model.mChi))
    # tlimit = flimit.Get('limit')
    # tlimit.GetEntry(2)

    # system("combine -M Asymptotic combined_%s.txt -n %s -m %i"%(label,model.mMed*1000+mChi))

for m in models:
    run(m,indir+'/interp_%s.root'%(m.mass))
    outdir_ = '%s/%s/%s'%(outdir,m.model,m.coupling)
    system('mkdir -p %s' %outdir_)
    system('mv higgs*root %s'%outdir_)
    exit(system('ls %s/higgs*%s*root'%(outdir_,m.mass)))
