#!/usr/bin/env python

from os import system,environ
from re import sub
from sys import argv
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
# ## config format:
# # first line: input_directory  output_directory
# # subsequent lines: model mass_string coupling_string 
# with open(args.cfg) as fcfg:
#     lines = fcfg.readlines()
#     indir, outdir = lines[0].strip().split()
#     models = []
#     lines = [l.strip() for l in lines[1:]]
#     for i in args.torun:
#         models.append(Model(*(lines[i].split())))

def makeHists(model,infile):
    name_ = sub('-','_',sub('\.','p',model.name))
    fout = root.TFile(name_+'_model.root','RECREATE')
    bins = array('f',[250,280,310,350,400,450,600,1000])
    N = len(bins)-1
    fin = root.TFile(infile)
    #fin = root.TFile(environ['PANDA_FLATDIR']+'/limits/limitForest.root')
    #fin = root.TFile('/afs/cern.ch/user/s/snarayan/work/skims/monotop_limits_v1/'+model.name+'.root')

    wspace = root.RooWorkspace("signalws")
#  wspace._import = SafeWorkspaceImporter(wspace)

    fout.cd()
    counter=0
    tags = {
            'loose_' : 'top_ecf_bdt>0.1 && top_ecf_bdt<0.45',
            '' : 'top_ecf_bdt>0.45',
            }

    fhists = root.TFile('signalmodel.root','RECREATE')

    vmets = {}

    for tag_label,tag in tags.iteritems():
        vmet = root.RooRealVar('min(999.9999,met)','min(999.9999,met)',250,1000)
        if 'loose' in tag_label:
            vmet.SetName('min(999.9999,met)_monotop_loose')
        else:
            vmet.SetName('min(999.9999,met)_monotop')
        vmet.setMin(250); vmet.setMax(1000)
        getattr(wspace,'import')(vmet,root.RooFit.RecycleConflictNodes())
        vmets[tag_label] = vmet

        for syst in ['','btagUp','btagDown','mistagUp','mistagDown',
                        'sjbtagUp','sjbtagDown','sjmistagUp','sjmistagDown']:
            tin = fin.Get(model.name+'_signal')
            hist = root.TH1F('h%i'%counter,'h',N,bins)
            weight = 'weight' if syst=='' else syst
            if model.coupling!='nominal':
                weight = '(%s*%s)'%(weight,model.coupling)
            tin.Draw('min(met,999.9999)>>h%i'%counter,'%s*(met>250 && %s)'%(weight,tag))

            print model.name,name_,syst,hist.Integral(),tin.GetEntries(),hist.GetEntries()

            if syst!='':
                syst = '_'+syst
            dhist = root.RooDataHist('monotop_%ssignal_%s%s'%(tag_label,name_,syst),
                                     '%ssignal %s %s'%(tag_label,name_,syst),
                                     root.RooArgList(vmet),
                                     hist)
            getattr(wspace,'import')(dhist,root.RooFit.RecycleConflictNodes())

            # histsToWrite['hmonotop_%ssignal_%s%s'%(tag_label,name_,syst)] = hist
            fhists.WriteTObject(hist,'hmonotop_%ssignal_%s%s'%(tag_label,name_,syst))
            counter += 1

    fhists.Close()

    fout.Close()
    wspace.writeToFile(name_+'_dmodel.root')
    fout = root.TFile(name_+'_dmodel.root')
    fout.ls()
    fout.Close()


def run(model,infile,runObserved=True):
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
    # flimit = root.TFile('higgsCombinefcnc_%i_%i.Asymptotic.mH120.root'%(model.mMed,model.mChi))
    # tlimit = flimit.Get('limit')
    # tlimit.GetEntry(2)

    # system("combine -M Asymptotic combined_%s.txt -n %s -m %i"%(label,model.mMed*1000+mChi))

for m in models:
    run(m,indir+'/signals_2/fittingForest_signal_%s_%s.root'%(m.model,m.mass))
    outdir_ = '%s/%s/%s'%(outdir,m.model,m.coupling)
    system('mkdir -p %s' %outdir_)
    system('mv higgs*root %s'%outdir_)
