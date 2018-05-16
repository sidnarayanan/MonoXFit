from ROOT import TCanvas, TGraph, TGraphAsymmErrors, TLegend, TLatex, TFile, TTree, TH2D, TGraph2D
import ROOT as root
from array import array
from sys import argv,stdout,exit
from tdrStyle import *
import plotConfig
from glob import glob 
from collections import namedtuple
from math import log10

root.gROOT.SetBatch(1)

##Color palette
ncontours = 999;
root.TColor.InitializeColors();
##stops = [ 0.0000, 0.1250, 0.2500, 0.3750, 0.5000, 0.6250, 0.7500, 0.8750, 1.0000]
#stops = [ 0.0000,       0.10,   0.200,     0.30,      0.4000,      0.50,    0.7500,    0.8750,    1.0000]
#red =   [     0/255.,     0/255.,    0/255.,    0/255.,   0/255.,   0/255.,   0/255.,   0/255.,   0/255.]
#green = [   255./255.,  240./255.,  225./255., 200./255., 160./255., 120./255., 80./255., 40./255., 0./255.]
#blue  = [   255/255.,   255/255.,  255/255.,  255/255., 255/255., 255/255., 255/255., 255/255., 255/255.]
##red   = [ 243./255., 243./255., 240./255., 240./255., 241./255., 239./255., 186./255., 151./255., 129./255.]
##green = [   0./255.,  46./255.,  99./255., 149./255., 194./255., 220./255., 183./255., 166./255., 147./255.]
##blue  = [   6./255.,   8./255.,  36./255.,  91./255., 169./255., 235./255., 246./255., 240./255., 233./255.]
#
#stopsArray = array('d',stops)
#redArray   = array('d',red)
#greenArray = array('d',green)
#blueArray  = array('d',blue)
#
#root.TColor.CreateGradientColorTable(len(stops), stopsArray, redArray, greenArray, blueArray, ncontours);
#root.gStyle.SetPalette(root.kInvertedDarkBodyRadiator)
stops  = array('d', [0.0000,  0.400, 0.50, 0.6000, 0.70, 0.800, 0.90, 1.0000])
stops  = array('d', [0, 0.25, 0.4, 0.47, 0.54, 0.6, 0.75, 1.0])
reds   = array('d', [ 102./255., 157./255., 188./255., 196./255., 214./255., 223./255., 235./255., 251./255.])
greens = array('d', [  29./255.,  25./255.,  37./255.,  67./255.,  91./255., 132./255., 185./255., 251./255.])
blues  = array('d', [  32./255.,  33./255.,  45./255.,  66./255.,  98./255., 137./255., 187./255., 251./255.])
for a in [reds, greens, blues]:
  a.reverse()
Idx = root.TColor.CreateGradientColorTable(len(stops), stops, reds, greens, blues, 255);
root.gStyle.SetNumberContours(ncontours);

root.gStyle.SetLabelSize(0.035,"X");
root.gStyle.SetLabelSize(0.035,"Y");
root.gStyle.SetLabelSize(0.035,"Z");


setTDRStyle()

XSECUNCERT=0.1
VERBOSE=False

drawLegend=True

iC=0
class Limit():
  def __init__(self,mMed,gQ,xsec=1):
    self.mMed=mMed
    self.gQ=gQ
    self.xsec=xsec
    self.cent=0
    self.up1=0
    self.up2=0
    self.down1=0
    self.down2=0
    self.obs=0

def get_contours(h2, cold):
  ctmp = TCanvas()
  ctmp.cd()
  h2.Draw("contlist")
  ctmp.Update()

  conts = root.gROOT.GetListOfSpecials().FindObject("contours")
  graphs = []
  for ib in xrange(conts.GetSize()):
    l = conts.At(ib)
    #graph = root.TGraph(l.First())
    graph = l.First()
    if not graph:
      continue
    graph = root.TGraph(graph) # clone
    graph.SetLineColor(h2.GetLineColor())
    graph.SetLineWidth(h2.GetLineWidth())
    graph.SetLineStyle(h2.GetLineStyle())
    graphs.append(graph)

  cold.cd()
  return graphs

LimitPoint = namedtuple('LimitPoint',['mV','mChi','gdmv','gdma','gqv','gqa','limit'])
def parseLimitFiles2D(filepath):
  # returns a list of LimitPoints 
  limits = [] 
  filelist = glob(filepath)
  for f in filelist:
    ff = f.split('/')[-1].split('_')
    mMed = int(ff[1])
    mChi = int(ff[2].split('.')[0])
    ff = f.split('/')[-2].split('_')
    gdmv = float(ff[1].replace('p','.'))
    gdma = float(ff[3].replace('p','.'))
    gqv = float(ff[5].replace('p','.'))
    gqa = float(ff[7].replace('p','.'))
    l = Limit(mMed/1000.,max(gqv,gqa))
    try:
      fin = TFile(f)
      t = fin.Get('limit')
      if not t:
        continue
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
      lp = LimitPoint(mMed/1000.,mChi,gdmv,gdma,gqv,gqa,l)
      limits.append(lp)
    except Exception as e:
      pass
    fin.Close()
  return limits

def makePlot2D(filepath,foutname,medcfg,gqcfg,header):
  limits = parseLimitFiles2D(filepath)
  gs = {}
  for g in ['exp','expup','expdown','obs','obsup','obsdown']:
    gs[g] = TGraph2D()

  iP=0
  hgrid = TH2D('grid','grid',medcfg[0],medcfg[1],medcfg[2],gqcfg[0],gqcfg[1],gqcfg[2])
  for p in limits:
    l = p.limit 
    if l.obs==0 or l.cent==0:
      print l.mMed,l.gQ
      continue
    hgrid.Fill(l.mMed,l.gQ)
    gs['exp'].SetPoint(iP,l.mMed,l.gQ,l.cent)
    gs['expup'].SetPoint(iP,l.mMed,l.gQ,l.up1)
    gs['expdown'].SetPoint(iP,l.mMed,l.gQ,l.down1)
    gs['obs'].SetPoint(iP,l.mMed,l.gQ,l.obs)
    gs['obsup'].SetPoint(iP,l.mMed,l.gQ,l.obs/(1-XSECUNCERT))
    gs['obsdown'].SetPoint(iP,l.mMed,l.gQ,l.obs/(1+XSECUNCERT))
    iP += 1

  hs = {}
  for h in ['exp','expup','expdown','obs','obsup','obsdown']:
    hs[h] = TH2D(h,h,medcfg[0],medcfg[1],medcfg[2],gqcfg[0],gqcfg[1],gqcfg[2])
    # hs[h].SetStats(0); hs[h].SetTitle('')
    for iX in xrange(0,medcfg[0]):
      for iY in xrange(0,gqcfg[0]):
        x = medcfg[1] + (medcfg[2]-medcfg[1])*iX/medcfg[0]
        y = gqcfg[1] + (gqcfg[2]-gqcfg[1])*iY/gqcfg[0]
        val = gs[h].Interpolate(x,y)
        if val == 0:
          val = 9999
        val = max(0.01,min(100,val))
        hs[h].SetBinContent(iX+1,iY+1,val)
        # if h=='obs':
        #   print iX+1,iY+1,x,y,gs[h].Interpolate(x,y)

  '''
  zaxis = hs['obs'].GetZaxis()
  nbins = zaxis.GetNbins()
  print nbins
  zaxis.SetBinLabel(1,'<10^{-2}')
  zaxis.SetBinLabel(nbins,'>10')
  '''

  hs['obsclone'] = hs['obs'].Clone() # clone it so we can draw with different settings
  for h in ['exp','expup','expdown','obsclone','obsup','obsdown']:
    hs[h].SetContour(2)
    hs[h].SetContourLevel(1,1)
    for iX in xrange(1,medcfg[0]+1):
      for iY in xrange(1,gqcfg[0]+1):
        if hs[h].GetBinContent(iX,iY)<=0:
          hs[h].SetBinContent(iX,iY,100)

  global iC
  canvas = ROOT.TCanvas("canvas%i"%iC, '',  1000, 800)
  canvas.SetLogz()
  iC+=1

  frame = canvas.DrawFrame(medcfg[1],gqcfg[1],medcfg[2],gqcfg[2],"")

  frame.GetYaxis().CenterTitle();
  frame.GetYaxis().SetTitle(gqcfg[3]);
  frame.GetXaxis().SetTitle("m_{V} [TeV]");
  frame.GetXaxis().SetTitleOffset(1.15);
  frame.GetYaxis().SetTitleOffset(1.15);

  frame.Draw()

  hs['obs'].SetMinimum(0.01)
  hs['obs'].SetMaximum(100.)

  hs['obs'].Draw("COLZ SAME")

  obs_color = root.kOrange

  hs['obsclone'].SetLineStyle(1)
  hs['obsclone'].SetLineWidth(3)
  hs['obsclone'].SetLineColor(obs_color)
  hs['obsclone'].Draw('CONT3 SAME')

  ctemp = root.TCanvas()
  hs['obsclone'].Draw('contlist')
  ctemp.Update()
  objs = root.gROOT.GetListOfSpecials().FindObject('contours')
  saveobs = root.TGraph((objs.At(0)).First())

  canvas.cd()

  conts = {}

  hs['obsup'].SetLineStyle(3)
  hs['obsup'].SetLineWidth(2)
  hs['obsup'].SetLineColor(obs_color)
  conts['obsup'] = get_contours(hs['obsup'], canvas)[0]
  conts['obsup'].Draw('L SAME')
#  hs['obsup'].Draw('CONT3 SAME')

  hs['obsdown'].SetLineStyle(3)
  hs['obsdown'].SetLineWidth(2)
  hs['obsdown'].SetLineColor(obs_color)
  conts['obsdown'] = get_contours(hs['obsdown'], canvas)[0]
  conts['obsdown'].Draw('L SAME')
  #hs['obsdown'].Draw('CONT3 SAME')

  hs['exp'].SetLineStyle(1)
  hs['exp'].SetLineWidth(3)
  hs['exp'].SetLineColor(1)
  hs['exp'].Draw('CONT3 SAME')

  hs['expup'].SetLineStyle(3)
  hs['expup'].SetLineWidth(2)
  hs['expup'].SetLineColor(1)
  conts['expup'] = get_contours(hs['expup'], canvas)[0]
  conts['expup'].Draw('L SAME')
  #hs['expup'].Draw('CONT3 SAME')

  hs['expdown'].SetLineStyle(3)
  hs['expdown'].SetLineWidth(2)
  hs['expdown'].SetLineColor(1)
  conts['expdown'] = get_contours(hs['expdown'], canvas)[0]
  conts['expdown'].Draw('L SAME')
  #hs['expdown'].Draw('CONT3 SAME')

  if drawLegend:
    leg = root.TLegend(0.16,0.65,0.5,0.88);#,NULL,"brNDC");
    leg.SetHeader(header)
    leg.AddEntry(hs['exp'],"Median expected 95% CL","L");
    leg.AddEntry(hs['expup'],"Exp. #pm 1 #sigma_{experiment}","L");
    leg.AddEntry(hs['obsclone'],"Observed 95% CL","L");
    leg.AddEntry(hs['obsup'],"Obs. #pm 1 #sigma_{theory}","L");
    leg.SetFillColor(0); leg.SetBorderSize(0)
    leg.Draw("SAME");


#  hgrid.Draw('same')

  tex = root.TLatex();
  tex.SetNDC();
  tex.SetTextFont(42);
  tex.SetLineWidth(2);
  tex.SetTextSize(0.040);
  tex.Draw();
  tex.DrawLatex(0.65,0.94,"36 fb^{-1} (13 TeV)");
  tex2 = root.TLatex();
  tex2.SetNDC();
  tex2.SetTextFont(42);
  tex2.SetLineWidth(2);
  tex2.SetTextSize(0.04);
  tex2.SetTextAlign(33)
  tex2.SetTextAngle(90);
  tex2.DrawLatex(0.965,0.93,"Observed #sigma_{95% CL}/#sigma_{theory}");

  texCMS = root.TLatex(0.12,0.94,"#bf{CMS}");
  texCMS.SetNDC();
  texCMS.SetTextFont(42);
  texCMS.SetLineWidth(2);
  texCMS.SetTextSize(0.05); texCMS.Draw();

  root.gPad.SetRightMargin(0.15);
  root.gPad.SetTopMargin(0.07);
  root.gPad.SetBottomMargin(0.15);
  root.gPad.RedrawAxis();
  root.gPad.Modified(); 
  root.gPad.Update();

  canvas.SaveAs(foutname+'.png')
  canvas.SaveAs(foutname+'.pdf')

  texPrelim = root.TLatex(0.2,0.94,"#it{Preliminary}");
  texPrelim.SetNDC();
  texPrelim.SetTextFont(42);
  texPrelim.SetLineWidth(2);
  texPrelim.SetTextSize(0.05); texPrelim.Draw();

  canvas.SaveAs(foutname+'_prelim.png')
  canvas.SaveAs(foutname+'_prelim.pdf')

  fsave = root.TFile(foutname+'.root','RECREATE')
  fsave.WriteTObject(hs['exp'],'hexp')
  fsave.WriteTObject(gs['exp'],'gexp')
  fsave.Close()
#  canvas.SaveAs(foutname+'.C')

plotsdir = plotConfig.plotDir

makePlot2D(plotConfig.scansDir+'vector/gdmv_1p0_gdma_0_gv_*_ga_0/higgsCombinefcnc_*_1.Asymptotic.mH120.root',
           plotsdir+'fcnc2d_obs_gqv_mV',
           (100,0.2,2.3),
           (100,0.01,1.,'g_{q}^{V}'),
           'm_{#chi} = 1 GeV, g_{#chi}^{V} = 1 [FCNC]')

makePlot2D(plotConfig.scansDir+'vector/gdmv_0_gdma_1p0_gv_0_ga_*/higgsCombinefcnc_*_1.Asymptotic.mH120.root',
           plotsdir+'fcnc2d_obs_gqa_mV',
           (100,0.2,2.3),
           (100,0.01,1.,'g_{q}^{A}'),
           'm_{#chi} = 1 GeV, g_{#chi}^{A} = 1 [FCNC]')

# makePlot2D(plotConfig.scansDir+'fcnc/gdmv_*_gdma_1p0_gv_0_ga_*/higgsCombinefcnc_*_1.Asymptotic.mH120.root',
#            plotsdir+'fcnc2d_obs_gqa_mV',
#            (100,300.,2200.),
#            (40,0.01,1.,'g_{q}^{A}'),
#            'm_{#chi} = 1 GeV, g_{#chi}^{A} = 1 [FCNC]')
