from ROOT import TCanvas, TGraph, TGraphAsymmErrors, TLegend, TLatex, TFile, TTree, TH2D, TGraph2D
import ROOT as root
from array import array
from sys import argv,stdout,exit
from tdrStyle import *
import plotConfig
from glob import glob 
from collections import namedtuple
from math import log10
import numpy as np
from scipy.interpolate import LinearNDInterpolator as LNDI

#root.gROOT.SetBatch(1)

##Color palette
#root.gStyle.SetPalette(root.kDarkBodyRadiator)
#ncontours = 999;
#root.TColor.InitializeColors();
##stops = [ 0.0000, 0.1250, 0.2500, 0.3750, 0.5000, 0.6250, 0.7500, 0.8750, 1.0000]
#stops = [0.,1.]
#green = blue = red = [1.,1.]
#stops = [ 0.0000,       0.10,   0.200,     0.30,      0.4000,      0.50,    0.7500,    0.8750,    1.0000]
#red   = [ 243./255., 243./255., 240./255., 240./255., 241./255., 239./255., 186./255., 151./255., 129./255.]
#green = [   0./255.,  46./255.,  99./255., 149./255., 194./255., 220./255., 183./255., 166./255., 147./255.]
#blue  = [   6./255.,   8./255.,  36./255.,  91./255., 169./255., 235./255., 246./255., 240./255., 233./255.]
#
#stopsArray = array('d',stops)
#redArray   = array('d',red)
#greenArray = array('d',green)
#blueArray  = array('d',blue)
#
#root.TColor.CreateGradientColorTable(2, array('d',stops), array('d',red), array('d',green), array('d',blue), 999);
root.gStyle.SetNumberContours(99);
root.gStyle.SetPalette(root.kBird)

root.gStyle.SetLabelSize(0.035,"X");
root.gStyle.SetLabelSize(0.035,"Y");
root.gStyle.SetLabelSize(0.035,"Z");


setTDRStyle()

XSECUNCERT=0.1
VERBOSE=False

drawLegend=True

def binary_search(x,y,zlo,zhi,interp,accuracy):
  if interp(x,y,zlo)>=1:
    return zlo # base case 
  while True:
    width = (zhi-zlo)/2
    z = zlo+width
    if width<accuracy:
      return z
    val = interp(x,y,z)
    if val==1:
      return z
    elif val > 1: # target is lower
      zhi -= width
    else:
      zlo += width
       

iC=0
class Limit():
  def __init__(self,gQ,gDM,mMed,xsec=1):
    self.gQ=gQ
    self.gDM=gDM
    self.mMed=mMed
    self.xsec=xsec
    self.cent=0
    self.up1=0
    self.up2=0
    self.down1=0
    self.down2=0
    self.obs=0

LimitPoint = namedtuple('LimitPoint',['mV','mChi','gdmv','gdma','gqv','gqa','limit'])
def parseLimitFiles2D(filepath):
  print filepath
  # returns a list of LimitPoints 
  limits = [] 
  filelist = glob(filepath)
  for f in filelist:
    ff = f.split('/')[-1].split('_')
    mMed = int(ff[1]) / 1000.
    mChi = int(ff[2].split('.')[0])
    ff = f.split('/')[-2].split('_')
    gdmv = float(ff[1].replace('p','.'))
    gdma = float(ff[3].replace('p','.'))
    gqv = float(ff[5].replace('p','.'))
    gqa = float(ff[7].replace('p','.'))
    l = Limit(max(gqv,gqa),max(gdmv,gdma),mMed)
    try:
      fin = TFile(f)
      t = fin.Get('limit')
      scaling = fin.Get('scaling')
      if scaling:
        scaling = float(scaling.GetTitle())
      else:
        scaling = 1.
      nL = t.GetEntries()
      limitNames = ['down2','down1','cent','up1','up2','obs']
      for iL in xrange(nL):
        t.GetEntry(iL)
        val = t.limit
        val = val * scaling
        val = val / 0.68
        setattr(l,limitNames[iL],val)
      lp = LimitPoint(mMed,mChi,gdmv,gdma,gqv,gqa,l)
      limits.append(lp)
    except Exception as e:
#      print e
      pass
    fin.Close()
  print len(limits)
  return limits

def makePlot3D(filepath,foutname,gqcfg,gdmcfg,medcfg):
  limits = parseLimitFiles2D(filepath)

  points = []
  values = []
  for l in limits:
    points.append((l.limit.gQ,l.limit.gDM,l.mV))
    values.append(l.limit.obs)

  interp = LNDI(points,values)

  #surface = TH2D('hsurf','',gqcfg[0],gqcfg[1],gqcfg[2],gdmcfg[0],gdmcfg[1],gdmcfg[2])
  surface = TH2D('hsurf','',gqcfg[0],0,gqcfg[2],gdmcfg[0],0,gdmcfg[2])
  surface.GetXaxis().SetTitle(gqcfg[3])
  surface.GetYaxis().SetTitle(gdmcfg[3])
  surface.GetZaxis().SetTitle('95% CL excluded m_{V} [TeV]')

  xstep = (gqcfg[2]-gqcfg[1])/gqcfg[0]
  ystep = (gdmcfg[2]-gdmcfg[1])/gdmcfg[0]

  for x in np.arange(gqcfg[1],gqcfg[2]+xstep,xstep):
    for y in np.arange(gdmcfg[1],gdmcfg[2]+ystep,ystep):
      z_limit = 0.
      z_limit = binary_search(x,y,medcfg[0],medcfg[1],interp,0.001)
#      for z in np.arange(medcfg[0],medcfg[1],zstep):
#        if y>gdmcfg[2]:
#          break
#        exp = interp(x,y,z)
##        print x,y,z,exp
#        if exp >= 1:
#          z_limit = z
#          break
#      print x,y,z_limit
      # if z_limit==medcfg[0]:
      #   z_limit = 0
      surface.SetBinContent(surface.FindBin(x,y),z_limit)

  global iC

  canvas = ROOT.TCanvas("canvas%i"%iC, '',  1000, 800)
  iC+=1
  canvas.SetRightMargin(0.2);
  canvas.SetTopMargin(0.07);
  canvas.SetBottomMargin(0.15);
  surface.GetXaxis().SetTitleOffset(1.2)
  surface.GetYaxis().SetTitleOffset(1.2)
  surface.GetZaxis().SetTitleOffset(1.2)
  surface.GetXaxis().SetNdivisions(508)
  surface.GetYaxis().SetNdivisions(508)
  surface.GetXaxis().CenterTitle()
  surface.GetYaxis().CenterTitle()
  surface.SetMinimum(medcfg[0])

  surface.Draw('CONT4Z')

  tex = root.TLatex();
  tex.SetNDC();
  tex.SetTextFont(42);
  tex.SetLineWidth(2);
  tex.SetTextSize(0.040);
  tex.Draw();
  tex.DrawLatex(0.57,0.94,"35.8 fb^{-1} (13 TeV)");

  texCMS = root.TLatex(0.12,0.94,"#bf{CMS}");
  texCMS.SetNDC();
  texCMS.SetTextFont(42);
  texCMS.SetLineWidth(2);
  texCMS.SetTextSize(0.05); texCMS.Draw();

  canvas.SaveAs(foutname.replace('3d','3dproj')+'.png')
  canvas.SaveAs(foutname.replace('3d','3dproj')+'.pdf')
  
  texPrelim = root.TLatex(0.2,0.94,"#it{Preliminary}");
  texPrelim.SetNDC();
  texPrelim.SetTextFont(42);
  texPrelim.SetLineWidth(2);
  texPrelim.SetTextSize(0.05); texPrelim.Draw();

  canvas.SaveAs(foutname.replace('3d','3dproj_prelim')+'.png')
  canvas.SaveAs(foutname.replace('3d','3dproj_prelim')+'.pdf')
  

  canvas = ROOT.TCanvas("canvas%i"%iC, '',  1000, 800)
  iC+=1

  canvas.SetLeftMargin(0.15)
  surface.GetXaxis().SetTitleOffset(1.5)
  surface.GetYaxis().SetTitleOffset(1.7)
  surface.GetZaxis().SetTitleOffset(1.3)
  surface.Draw('SURF1')

  tex = root.TLatex();
  tex.SetNDC();
  tex.SetTextFont(42);
  tex.SetLineWidth(2);
  tex.SetTextSize(0.040);
  tex.Draw();
  tex.DrawLatex(0.05,0.9,"35.8 fb^{-1} (13 TeV)");

  texCMS = root.TLatex(0.05,0.94,"#bf{CMS}");
  texCMS.SetNDC();
  texCMS.SetTextFont(42);
  texCMS.SetLineWidth(2);
  texCMS.SetTextSize(0.05); texCMS.Draw();

  canvas.SaveAs(foutname+'.png')
  canvas.SaveAs(foutname+'.pdf')
  
  texPrelim = root.TLatex(0.13,0.94,"#it{Preliminary}");
  texPrelim.SetNDC();
  texPrelim.SetTextFont(42);
  texPrelim.SetLineWidth(2);
  texPrelim.SetTextSize(0.05); texPrelim.Draw();

  canvas.SaveAs(foutname+'_prelim.png')
  canvas.SaveAs(foutname+'_prelim.pdf')
  

  fsave = root.TFile(foutname+'.root','RECREATE')
  fsave.WriteTObject(surface,'hexp')
  fsave.Close()
#  canvas.SaveAs(foutname+'.C')

plotsdir = plotConfig.plotDir


makePlot3D(plotConfig.scansDir+'vector/gdmv_*_gdma_0_gv_*_ga_0/higgsCombinefcnc_*_1.Asymptotic.mH120.root',
           plotsdir+'fcnc3d_obs_vector',
           (20,0.01,1.,'g_{q}^{V}'),
           (20,0.05,2,'g_{#chi}^{V}'),
           (0.2,3.))

# makePlot3D(plotConfig.scansDir+'vector/gdmv_0_gdma_*_gv_0_ga_*/higgsCombinefcnc_*_1.Asymptotic.mH120.root',
#            plotsdir+'fcnc3d_obs_axial',
#            (20,0.01,1.,'g_{q}^{A}'),
#            (20,0.05,2,'g_{#chi}^{A}'),
#            (300,3000))
