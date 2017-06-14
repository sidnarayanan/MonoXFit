from ROOT import TCanvas, TGraph, TGraphErrors, TGraphAsymmErrors, TLegend, TLatex, TMarker, TFile, TTree, TH2D
import ROOT as root
from array import array
from sys import argv,stdout
from tdrStyle import *
import plotConfig
from glob import glob 
from xsecs import *

setTDRStyle()

VERBOSE=False

BLIND=False

class Limit():
  def __init__(self,mMed,mChi,xsec=1):
    self.mMed=mMed
    self.mChi=mChi
    self.xsec=xsec
    self.cent=0
    self.up1=0
    self.up2=0
    self.down1=0
    self.down2=0
    self.obs=0

def findIntersect1D(g1,g2,x1,x2):
  orientation = (g1.Eval(x1)<g2.Eval(x1))
  for iX in xrange(1000):
    x = (x2-x1)*iX/1000.+x1
    if orientation != (g1.Eval(x)<g2.Eval(x)):
      # return TGraph(1,array('f',[x]),array('f',[g1.Eval(x)]))
      print 'Found intersection at x=%.3f'%x
      return TMarker(x,g1.Eval(x),1)
      # return x
  print 'Could not find intersection!'
  return None

def parseLimitFiles2D(filepath,br=0.68):
  # returns a dict (mMed,mChi) : Limit
  # if xsecs=None, Limit will have absolute xsec
  # if xsecs=dict of xsecs, Limit will have mu values
  limits = {}
  filelist = glob(filepath)
  for f in filelist:
    ff = f.split('/')[-1].split('_')
    mMed = int(ff[1]) / 1000.
    mChi = int(ff[2].split('.')[0])
    l = Limit(mMed,mChi)
    try:
      fin = TFile(f)
      t = fin.Get('limit')
      nL = t.GetEntries()
      limitNames = ['down2','down1','cent','up1','up2','obs']
      for iL in xrange(nL):
        t.GetEntry(iL)
        val = t.limit
        val = val / br
        setattr(l,limitNames[iL],val)
      limits[mMed] = l
    except:
      pass
    fin.Close()
  return limits

def makePlot1D(filepath,foutname,plottitle='',masstitle=''):
  br = 1 if 'Resonant' in plottitle else 0.68
  limits = parseLimitFiles2D(filepath,br)


  xaxis = []; xseclist = []
  xsecerr = []
  cent = []; obs = []
  up1 = []; up2 = []
  down1 = []; down2 = []
  maxval = 0; minval = 999
  for m in sorted(limits):
    l = limits[m]
    xaxis.append(m)
    xseclist.append(l.xsec)
    xsecerr.append(l.xsec*.2)
    cent.append(l.cent)
    up1.append(l.up1-l.cent)
    up2.append(l.up2-l.cent)
    down1.append(l.cent-l.down1)
    down2.append(l.cent-l.down2)
    obs.append(l.obs)
    maxval = max(maxval,l.up2)
    minval = min(minval,l.down2)


  N = len(xaxis)
  
  up1Sigma = array('f',up1)
  up2Sigma = array('f',up2)
  down1Sigma = array('f',down1)
  down2Sigma = array('f',down2)
  cent = array('f',cent)
  obs = array('f',obs)
  xarray = array('f',xaxis)
  xsecarray = array('f',xseclist)
  xsecerrarray = array('f',xsecerr)
  zeros = array('f',[0 for i in xrange(N)])

  graphXsec = TGraphErrors(N,xarray,xsecarray,zeros,xsecerrarray)

  graphCent = TGraph(N,xarray,cent)
  graphObs = TGraph(N,xarray,obs)
  graph1Sigma = TGraphAsymmErrors(N,xarray,cent,zeros,zeros,down1Sigma,up1Sigma)
  graph2Sigma = TGraphAsymmErrors(N,xarray,cent,zeros,zeros,down2Sigma,up2Sigma)

  c = TCanvas('c','c',700,600)
  c.SetLogy()
  c.SetLeftMargin(.15)

  graph2Sigma.GetXaxis().SetTitle(masstitle+' [TeV]')
  graph2Sigma.GetYaxis().SetTitle('Observed #sigma_{95% CL}/#sigma_{theory}')  
  c2 = root.kOrange
  c1 = root.kGreen+1
  graph2Sigma.SetLineColor(c2)
  graph1Sigma.SetLineColor(c1)
  graph2Sigma.SetFillColor(c2)
  graph1Sigma.SetFillColor(c1)
  graph2Sigma.SetMinimum(0.5*minval)
  graph2Sigma.SetMaximum(100*maxval)
  graphCent.SetLineWidth(2)
  graphCent.SetLineStyle(2)
  graphObs.SetLineColor(1)
  graphObs.SetLineWidth(3)
  graphObs.SetMarkerStyle(20)
  graphObs.SetMarkerSize(1)
  graphObs.SetMarkerColor(1)
  graph1Sigma.SetLineStyle(0)
  graph2Sigma.SetLineStyle(0)
 
  leg = TLegend(0.55,0.7,0.9,0.9)
  leg.AddEntry(graphCent,'Expected','L')
  if not BLIND:
    leg.AddEntry(graphObs,'Observed','Lp')
  leg.AddEntry(graph1Sigma,'1 std. dev.','F')
  leg.AddEntry(graph2Sigma,'2 std. dev.','F')
  leg.SetFillStyle(0)
  leg.SetBorderSize(0)

  graph2Sigma.Draw('A3')
  graph1Sigma.Draw('3 same')
  graphCent.Draw('same L')
  if not BLIND:
    graphObs.Draw('same Lp')

  subscript = 'SR' if 'Resonant' in plottitle else 'FC'
  coupling = '0.1' if 'Resonant' in plottitle else '0.25'

  graphXsec.SetLineColor(2)
  graphXsec.SetLineWidth(2)
  graphXsec.SetLineStyle(2)
  graphXsec.SetFillColor(2)
  graphXsec.SetFillStyle(3005)
  graphXsec.Draw('same L3')
  '''
  if not scale:
    if 'Resonant' in plottitle:
      leg.AddEntry(graphXsec,'Theory #splitline{a_{%s}=b_{%s}=%s}{m_{#chi}=100 GeV}'%(subscript,subscript,coupling),'l')
    else:
      leg.AddEntry(graphXsec,'Theory #splitline{a_{%s}=b_{%s}=%s}{m_{#chi}=10 GeV}'%(subscript,subscript,coupling),'l')
  '''
  if not BLIND:
    findIntersect1D(graphObs,graphXsec,xaxis[0],xaxis[-1])
  findIntersect1D(graphCent,graphXsec,xaxis[0],xaxis[-1])

  leg.Draw()

  label = TLatex()
  label.SetNDC()
  label.SetTextSize(0.7*c.GetTopMargin())
  label.SetTextFont(62)
  label.SetTextAlign(11)
  label.DrawLatex(0.15,0.94,"CMS")
  label.SetTextFont(42)
  label.DrawLatex(0.19,0.83,plottitle)
  if 'Resonant' in plottitle:
    label.DrawLatex(0.19,0.75,"a_{SR}^{q} = b_{SR}^{q} = %s"%coupling)
    label.DrawLatex(0.19,0.68,"a_{SR}^{1/2} = b_{SR}^{1/2} = 0.2")
    label.DrawLatex(0.19,0.61,"m_{#chi}=100 GeV")
  else:
    label.DrawLatex(0.19,0.75,"g_{DM}^{V}=1,g_{q}^{V}=0.25")
    label.DrawLatex(0.19,0.68,"m_{#chi}=1 GeV")
  label.SetTextSize(0.6*c.GetTopMargin())
  label.SetTextFont(42)
  label.SetTextAlign(31) # align right
  label.DrawLatex(0.95, 0.94,"%.1f fb^{-1} (13 TeV)"%(plotConfig.lumi))

  c.SaveAs(foutname+'.pdf')
  c.SaveAs(foutname+'.png')

  label.SetTextFont(52)
  label.SetTextAlign(11)
  label.DrawLatex(0.23,0.94,"Preliminary")

  c.SaveAs(foutname+'_prelim.pdf')
  c.SaveAs(foutname+'_prelim.png')

plotsdir = plotConfig.plotDir

scansdir = '/data/t3home000/snarayan/store/panda/v_8026_0_4/fitting/scans_bkup/'
makePlot1D(scansdir+'/res/nominal/higgsCombineres_*.root',plotsdir+'/res_obs_limit','#splitline{Resonant}{scalar production}','M_{#phi}')
#makePlot1D(plotConfig.scansDir+'/higgsCombinefcnc_*_1.Asymptotic.mH120.root',plotsdir+'/fcnc_exp_limit','#splitline{Flavor-changing}{neutral current}','M_{V}')
