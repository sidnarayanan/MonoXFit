from ROOT import TCanvas, TGraph, TGraphAsymmErrors, TLegend, TLatex, TFile, TTree, TH2D, TGraph2D
import ROOT as root
from array import array
from sys import argv,stdout,exit
from tdrStyle import *
import plotConfig
from glob import glob 

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
stops  = array('d', [x/7. for x in xrange(8)])
stops  = array('d', [0, 0.25, 0.4, 0.47, 0.54, 0.6, 0.75, 1.0])
reds   = array('d', [ 102./255., 157./255., 188./255., 196./255., 214./255., 223./255., 235./255., 251./255.])
greens = array('d', [  29./255.,  25./255.,  37./255.,  67./255.,  91./255., 132./255., 185./255., 251./255.])
blues  = array('d', [  32./255.,  33./255.,  45./255.,  66./255.,  98./255., 137./255., 187./255., 251./255.])
for a in [reds, greens, blues]:
  a.reverse()
Idx = root.TColor.CreateGradientColorTable(len(stops), stops, reds, greens, blues, 255);
#root.gStyle.SetPalette(root.kInvertedDarkBodyRadiator)
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
  def __init__(self,mMed,mChi,xsec=1):
    self.mMed=mMed*0.001
    self.mChi=mChi*0.001
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

def parseLimitFiles2D(filepath):
  # returns a dict (mMed,mChi) : Limit
  # if xsecs=None, Limit will have absolute xsec
  # if xsecs=dict of xsecs, Limit will have mu values
  limits = {}
  filelist = glob(filepath)
  for f in filelist:
    ff = f.split('/')[-1].split('_')
    mMed = int(ff[1])
    mChi = int(ff[2].split('.')[0])
    l = Limit(mMed,mChi)
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
      limits[(mMed*0.001,mChi*0.001)] = l
    except:
      pass
    fin.Close()
  print 'Successfully parsed %i points'%(len(limits))
  return limits

def makePlot2D(filepath,foutname,medcfg,chicfg,header='g_{q}^{V} = 0.25, g_{DM}^{V} = 1 [FCNC]',offshell=False):
  limits = parseLimitFiles2D(filepath)
  gs = {}
  for g in ['exp','expup','expdown','obs','obsup','obsdown']:
    gs[g] = TGraph2D()

  iP=0
  hgrid = TH2D('grid','grid',medcfg[0],medcfg[1],medcfg[2],chicfg[0],chicfg[1],chicfg[2])
  for p in limits:
    mMed = p[0]; mChi = p[1]
    '''
    if mMed<0.5*medcfg[1] or mMed>1.2*medcfg[2]:
      continue
    if mChi<0.5*chicfg[1] or mChi>1.2*chicfg[2]:
      continue
    '''
    l = limits[p]
    if l.obs==0 or l.cent==0:
      print mMed,mChi
      continue
    hgrid.Fill(mMed,mChi,100)
    gs['exp'].SetPoint(iP,mMed,mChi,l.cent)
    gs['expup'].SetPoint(iP,mMed,mChi,l.up1)
    gs['expdown'].SetPoint(iP,mMed,mChi,l.down1)
    gs['obs'].SetPoint(iP,mMed,mChi,l.obs)
    gs['obsup'].SetPoint(iP,mMed,mChi,l.obs/(1-XSECUNCERT))
    gs['obsdown'].SetPoint(iP,mMed,mChi,l.obs/(1+XSECUNCERT))
    iP += 1

  hs = {}
  for h in ['exp','expup','expdown','obs','obsup','obsdown']:
    hs[h] = TH2D(h,h,medcfg[0],medcfg[1],medcfg[2],chicfg[0],chicfg[1],chicfg[2])
    # hs[h].SetStats(0); hs[h].SetTitle('')
    for iX in xrange(0,medcfg[0]):
      for iY in xrange(0,chicfg[0]):
        x = medcfg[1] + (medcfg[2]-medcfg[1])*iX/medcfg[0]
        y = chicfg[1] + (chicfg[2]-chicfg[1])*iY/chicfg[0]
        if not(offshell) and 2*y>x:
          val = 9999
        else:
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
      for iY in xrange(1,chicfg[0]+1):
        if hs[h].GetBinContent(iX,iY)<=0:
          hs[h].SetBinContent(iX,iY,100)

  global iC
  canvas = ROOT.TCanvas("canvas%i"%iC, '',  1000, 800)
  canvas.SetLogz()
  iC+=1

  frame = canvas.DrawFrame(medcfg[1],chicfg[1],medcfg[2],chicfg[2],"")

  frame.GetYaxis().CenterTitle();
  frame.GetYaxis().SetTitle("m_{#chi} [TeV]");
  frame.GetXaxis().SetTitle("m_{V} [TeV]");
  frame.GetXaxis().SetTitleOffset(1.15);
  frame.GetYaxis().SetTitleOffset(1.15);
#  frame.GetXaxis().SetNdivisions(5)

  frame.Draw()

  htest = hs['exp']

  obs_color = root.kOrange

  hs['obs'].SetMinimum(0.01)
  hs['obs'].SetMaximum(100.)

  hs['obs'].Draw("COLZ SAME")

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

  root.gStyle.SetLineStyleString(11, '40 80')

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
  tex2.SetTextAngle(90);
  tex2.SetTextAlign(33)
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
  
  canvas.SetGrid()

  hgrid.Draw('BOX')
  hs['obsup'].Draw('CONT3 SAME')

  hs['obsdown'].Draw('CONT3 SAME')

  hs['exp'].Draw('CONT3 SAME')

  hs['expup'].Draw('CONT3 SAME')

  hs['expdown'].Draw('CONT3 SAME')

  canvas.SaveAs(foutname+'_grid.png')
  canvas.SaveAs(foutname+'_grid.pdf')

  fsave = root.TFile(foutname+'.root','RECREATE')
  fsave.WriteTObject(hs['obs'],'hobserved')
  fsave.WriteTObject(gs['obs'],'gobserved')
  fsave.WriteTObject(hs['exp'],'hexp')
  fsave.WriteTObject(gs['exp'],'gexp')
  fsave.WriteTObject(saveobs,'observed')
  fsave.Close()
#  canvas.SaveAs(foutname+'.C')

plotsdir = plotConfig.plotDir

#makePlot2D(plotConfig.scansDir+'vector/nominal/higgsCombinefcnc_*.Asymptotic.mH120.root',plotsdir+'fcnc2d_obs_vector',(100,200.,2200.),(100,10.,1050.),'g_{q}^{V} = 0.25, g_{DM}^{V} = 1 [FCNC]',True)
makePlot2D(plotConfig.scansDir+'vector/nominal/higgsCombinefcnc_*.Asymptotic.mH120.root',plotsdir+'fcnc2d_obs_vector',(100,.2,2.3),(100,0.010,1.050),'g_{q}^{V} = 0.25, g_{#chi}^{V} = 1 [FCNC]',True)
makePlot2D(plotConfig.scansDir+'vector/gdmv_0_gdma_1p0_gv_0_ga_0p25/higgsCombinefcnc_*.Asymptotic.mH120.root',plotsdir+'fcnc2d_obs_axial',(100,.2,2.3),(100,0.010,1.050),'g_{q}^{A} = 0.25, g_{#chi}^{A} = 1 [FCNC]',True)
#makePlot2D(plotConfig.scansDir+'vector/gdmv_0p25_gdma_0_gv_0p25_ga_0/higgsCombinefcnc_*.Asymptotic.mH120.root',plotsdir+'fcnc2d_obs_vector_dm0p25_q0p25',(100,.3,2.5),(100,10.,1200.),'g_{q}^{V} = 0.25, g_{DM}^{V} = 0.25 [FCNC]',True)
#makePlot2D(plotConfig.scansDir+'vector/gdmv_2p0_gdma_0_gv_1_ga_0/higgsCombinefcnc_*.Asymptotic.mH120.root',plotsdir+'fcnc2d_obs_vector_dm2p0_q1',(100,.3,3),(100,10.,1500.),'g_{q}^{V} = 1, g_{DM}^{V} = 2 [FCNC]',True)
#makePlot2D(plotConfig.scansDir+'vector/gdmv_1p0_gdma_0_gv_0p01_ga_0/higgsCombinefcnc_*.Asymptotic.mH120.root',plotsdir+'fcnc2d_obs_vector_dm210_q0p01',(100,.3,2.5),(100,10.,1250.),'g_{q}^{V} = 0.01, g_{DM}^{V} = 2 [FCNC]',True)
#makePlot2D(plotConfig.scansDir+'vector/gdmv_1p0_gdma_0_gv_0p05_ga_0/higgsCombinefcnc_*.Asymptotic.mH120.root',plotsdir+'fcnc2d_obs_vector_dm210_q0p05',(100,.3,2.5),(100,10.,1250.),'g_{q}^{V} = 0.05, g_{DM}^{V} = 1 [FCNC]',True)
#makePlot2D(plotConfig.scansDir+'vector/gdmv_1p0_gdma_0_gv_0p1_ga_0/higgsCombinefcnc_*.Asymptotic.mH120.root',plotsdir+'fcnc2d_obs_vector_dm210_q0p1',(100,.3,2.5),(100,10.,1250.),'g_{q}^{V} = 0.1, g_{DM}^{V} = 1 [FCNC]',True)
#makePlot2D(plotConfig.scansDir+'vector/gdmv_1p0_gdma_0_gv_0p3_ga_0/higgsCombinefcnc_*.Asymptotic.mH120.root',plotsdir+'fcnc2d_obs_vector_dm210_q0p3',(100,.3,2.5),(100,10.,1250.),'g_{q}^{V} = 0.3, g_{DM}^{V} = 1 [FCNC]',True)
#makePlot2D(plotConfig.scansDir+'vector/gdmv_1p0_gdma_0_gv_0p5_ga_0/higgsCombinefcnc_*.Asymptotic.mH120.root',plotsdir+'fcnc2d_obs_vector_dm210_q0p5',(100,.3,2.5),(100,10.,1250.),'g_{q}^{V} = 0.5, g_{DM}^{V} = 1 [FCNC]',True)
#makePlot2D(plotConfig.scansDir+'vector/gdmv_1p0_gdma_0_gv_0p75_ga_0/higgsCombinefcnc_*.Asymptotic.mH120.root',plotsdir+'fcnc2d_obs_vector_dm210_q0p75',(100,.3,2.5),(100,10.,1250.),'g_{q}^{V} = 0.75, g_{DM}^{V} = 1 [FCNC]',True)
#makePlot2D(plotConfig.scansDir+'vector/gdmv_1p0_gdma_0_gv_1_ga_0/higgsCombinefcnc_*.Asymptotic.mH120.root',plotsdir+'fcnc2d_obs_vector_dm210_q1',(100,.3,2.5),(100,10.,1250.),'g_{q}^{V} = 1, g_{DM}^{V} = 1 [FCNC]',True)
#makePlot2D(plotConfig.scansDir+'fcnc/gdmv_0_gdma_1p0_gv_0_ga_0p25/higgsCombinefcnc_*.Asymptotic.mH120.root',plotsdir+'fcnc2d_obs_axial',(50,200.,2200.),(50,100.,1200.),'g_{q}^{A} = 0.25, g_{DM}^{A} = 1 [FCNC]',True)
#makePlot2D(plotConfig.scansDir+'fcnc/gdmv_1p0_gdma_1p0_gv_0p25_ga_0p25/higgsCombinefcnc_*.Asymptotic.mH120.root',plotsdir+'fcnc2d_obs_VpA',(50,200.,2200.),(50,100.,1200.),'g_{q}^{A} = g_{q}^{V} = 0.25, g_{DM}^{A} = g_{DM}^{V} = 1 [FCNC]',True)
