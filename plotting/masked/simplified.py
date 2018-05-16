import ROOT as root
from os import getenv
from array import array
from tdrStyle import *
import plotConfig
from math import sqrt
setTDRStyle()
import cPickle as pickle


#basedir = getenv('CMSSW_BASE') + '/src/MonoXFit_MonoH/'
basedir = '../../'
f_mlfit = root.TFile(basedir+'/datacards/mlfit.root','READ')
f_data = root.TFile(basedir+'/mono-x.root','READ')

processes = [
      'zvv',
      'ttbar',
      'wjets',
#      'qcd',
      'dibosons',
      'stop',
      'data',
]

def corr():
  hbkg = f_mlfit.Get('shapes_fit_b/sig/total_background')
  hcovar = f_mlfit.Get('shapes_fit_b/sig/total_covar')
  hcorr = hcovar.Clone('corr')

  nbins = hbkg.GetNbinsX()

  for ib in xrange(1,nbins+1):
    width_i = hbkg.GetBinWidth(ib)
    for jb in xrange(1,nbins+1):
      width_j = hbkg.GetBinWidth(jb)
      hcovar.SetBinContent(ib,jb,
                           hcovar.GetBinContent(ib,jb)*width_i*width_j)

  for ib in xrange(1,nbins+1):
    for jb in xrange(1,nbins+1):
      sig_i = sqrt(hcovar.GetBinContent(ib,ib))
      sig_j = sqrt(hcovar.GetBinContent(jb,jb))
      hcorr.SetBinContent(ib,jb,hcovar.GetBinContent(ib,jb)/(sig_i*sig_j))

  root.gStyle.SetPaintTextFormat('1.2f')
  root.gStyle.SetOptStat(0)
  root.gStyle.SetPalette(root.kBird)

  c = root.TCanvas("c","c",600,700)  
  root.SetOwnership(c,False)
  c.cd()
  c.SetBottomMargin(0.3)
  hcorr.GetZaxis().SetTitle('Correlation')
  hcorr.GetZaxis().SetTitleOffset(1.2)
  c.SetRightMargin(0.15)
  
  hcorr.Draw('COLZTEXT')
            
  latex2 = root.TLatex()
  latex2.SetNDC()
  latex2.SetTextSize(0.5*c.GetTopMargin())
  latex2.SetTextFont(42)
  latex2.SetTextSize(0.6*c.GetTopMargin())
  latex2.SetTextAlign(31) # align right
  latex2.SetTextSize(0.5*c.GetTopMargin())
  latex2.DrawLatex(0.85, 0.94,"%.0f fb^{-1} (13 TeV)"%(plotConfig.lumi))
  #latex2.DrawLatex(0.9, 0.94,"2.32 fb^{-1} (13 TeV)")
  latex2.SetTextSize(0.6*c.GetTopMargin())
  latex2.SetTextFont(62)
  latex2.SetTextAlign(11) # align left
  latex2.DrawLatex(0.12, 0.94, "CMS")
  latex2.SetTextSize(0.5*c.GetTopMargin())
  latex2.SetTextFont(52)
  latex2.SetTextAlign(11)
  latex2.DrawLatex(0.21, 0.94, "Preliminary")          

  root.gPad.RedrawAxis()

  plotDir = plotConfig.plotDir

  for ext in ['pdf','png','C']:
    c.SaveAs(plotDir+"corr."+ext)

def yields(cat):
  hists = {}
  N = None
  for p in processes:
    hists[p] = f_mlfit.Get('shapes_fit_b/'+cat+'_sig/'+p)
    if not N:
      N = hists[p].GetNbinsX()
  d = {}
  for ib in xrange(1,N+1):
    d[ib] = {}
    width = hists['ttbar'].GetBinWidth(ib)
    s = '%20s& '%('$%i$-$%i$'%(int(hists['ttbar'].GetBinLowEdge(ib)), int(width + hists['ttbar'].GetBinLowEdge(ib))))
    d[ib]['title'] = s 
    total = 0
    total_err = 0
    for p in processes:
      if p == 'data':
        val = hists[p].GetY()[ib-1]
        s += '$%15i$ & '%int(val*width)
        d[ib][p] = (val*width,0)
      else:
        val = hists[p].GetBinContent(ib) * width
        err = hists[p].GetBinError(ib) * width
        if val>1:
          s += '$%7.1f \\pm %5.1f$ & '%(val, err)
        else:
          s += '$%7.2f \\pm %5.2f$ & '%(val, err)
        d[ib][p] = (val,err)
        total += val
        total_err += pow(err, 2)
    s += '$%7.1f \\pm %5.1f$ \\\\'%(total,sqrt(total_err))
    d[ib]['total'] = (total,sqrt(total_err))

    with open('all/' + cat+'.pkl','w') as fdump:
      pickle.dump(d, fdump)

    print s


# corr()

yields('loose')
yields('tight')
