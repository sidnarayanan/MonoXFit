import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining cmodel provide, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "ttbar"
metname      = "met"    # Observable variable name 
convertHistograms = []

### helper functions ###

def makeTop(cid,_fOut,newName,targetmc,controlmc,diag,wspace,systs=None,isW=False):
  TopScales = targetmc.Clone(); TopScales.SetName(newName+"_weights_%s"%cid)
  TopScales.Divide(controlmc)
  _fOut.WriteTObject(TopScales)

  if isW:
    uncerts = ['sjbtag', 'sjmistag']
  else: 
    uncerts = ['btag', 'mistag']

  if not(systs==None):
    for uncert in uncerts:
      TopScalesUp = systs['targetmc%sUp'%(uncert)].Clone(); TopScalesUp.SetName(newName+"_weights_%s_%s_Up"%(cid,uncert))
      TopScalesUp.Divide(systs['controlmc%sUp'%(uncert)])

      TopScalesDown = systs['targetmc%sDown'%(uncert)].Clone(); TopScalesDown.SetName(newName+"_weights_%s_%s_Down"%(cid,uncert))
      TopScalesDown.Divide(systs['controlmc%sDown'%(uncert)])

      _fOut.WriteTObject(TopScalesUp)
      _fOut.WriteTObject(TopScalesDown)

  ### met trig ###
  ftrig = r.TFile.Open('files/unc/all_trig2.root')
  h_trig_down = ftrig.Get('trig_sys_down')
  h_trig_up = ftrig.Get('trig_sys_up')

  ratio_trig_up = targetmc.Clone(); ratio_trig_up.SetName(newName+'_weights_%s_mettrig_Up'%cid)
  for b in range(ratio_trig_up.GetNbinsX()): ratio_trig_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(ratio_trig_up,h_trig_up,metname,metname,wspace.data("signal_ttbar"))
  ratio_trig_up.Divide(controlmc)
  _fOut.WriteTObject(ratio_trig_up)

  ratio_trig_down = targetmc.Clone(); ratio_trig_down.SetName(newName+'_weights_%s_mettrig_Down'%cid)
  for b in range(ratio_trig_down.GetNbinsX()): ratio_trig_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(ratio_trig_down,h_trig_down,metname,metname,wspace.data("signal_ttbar"))
  ratio_trig_down.Divide(controlmc)
  _fOut.WriteTObject(ratio_trig_down)

  return TopScales


def addTopErrors(TopScales,targetmc,newName,crName,_fOut,CRs,nCR,cid,isW=False):

  if isW:
    uncerts = ['sjbtag', 'sjmistag']
  else: 
    uncerts = ['btag', 'mistag']
  uncerts.append('mettrig')
  for uncert in uncerts:
    CRs[nCR].add_nuisance_shape(uncert,_fOut)

  bins = range(targetmc.GetNbinsX())

  for b in bins:
    err = TopScales.GetBinError(b+1)
    if not TopScales.GetBinContent(b+1)>0: continue 
    else: relerr = err/TopScales.GetBinContent(b+1)
    if relerr<0.001: continue
    byb_u = TopScales.Clone(); byb_u.SetName("%s_weights_%s_%s_stat_error_%sCR_bin%d_Up"%(newName,cid,cid,crName,b))
    byb_u.SetBinContent(b+1,TopScales.GetBinContent(b+1)+err)
    byb_d = TopScales.Clone(); byb_d.SetName("%s_weights_%s_%s_stat_error_%sCR_bin%d_Down"%(newName,cid,cid,crName,b))
    byb_d.SetBinContent(b+1,TopScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    CRs[nCR].add_nuisance_shape("%s_stat_error_%sCR_bin%d"%(cid,crName,b),_fOut) # HERE


def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  # Some setup
  _fin = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)

  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # but for now this is just kept simple 
  processName = "TTbar" # Give a name of the process being modelled
  metname = "met"    # Observable variable name 

  targetmc     = _fin.Get("signal_ttbar")      # define monimal (MC) of which process this config will model
  controlmc    = _fin.Get("singlemuontop_ttbar")
  controlmc_e  = _fin.Get("singleelectrontop_ttbar")
  controlmc_w    = _fin.Get("singlemuonw_ttbar")
  controlmc_w_e  = _fin.Get("singleelectronw_ttbar")
 

  systs = {}; systs_e = {}
  systs_w = {}; systs_w_e = {}

  # btag systs
  systs['targetmcbtagUp']      = _fin.Get("signal_ttbar_btagUp");           systs_e['targetmcbtagUp']      = systs['targetmcbtagUp']
  systs['targetmcbtagDown']    = _fin.Get("signal_ttbar_btagDown");         systs_e['targetmcbtagDown']    = systs['targetmcbtagDown']
  systs['controlmcbtagUp']     = _fin.Get("singlemuontop_ttbar_btagUp");    systs_e['controlmcbtagUp']     = _fin.Get("singleelectrontop_ttbar_btagUp")
  systs['controlmcbtagDown']   = _fin.Get("singlemuontop_ttbar_btagDown");  systs_e['controlmcbtagDown']   = _fin.Get("singleelectrontop_ttbar_btagDown")
  systs['targetmcsjbtagUp']      = _fin.Get("signal_ttbar_sjbtagUp");           systs_e['targetmcsjbtagUp']      = systs['targetmcsjbtagUp']
  systs['targetmcsjbtagDown']    = _fin.Get("signal_ttbar_sjbtagDown");         systs_e['targetmcsjbtagDown']    = systs['targetmcsjbtagDown']
  systs['controlmcsjbtagUp']     = _fin.Get("singlemuontop_ttbar_sjbtagUp");    systs_e['controlmcsjbtagUp']     = _fin.Get("singleelectrontop_ttbar_sjbtagUp")
  systs['controlmcsjbtagDown']   = _fin.Get("singlemuontop_ttbar_sjbtagDown");  systs_e['controlmcsjbtagDown']   = _fin.Get("singleelectrontop_ttbar_sjbtagDown")
  
  systs['targetmcmistagUp']      = _fin.Get("signal_ttbar_mistagUp");           systs_e['targetmcmistagUp']      = systs['targetmcmistagUp']
  systs['targetmcmistagDown']    = _fin.Get("signal_ttbar_mistagDown");         systs_e['targetmcmistagDown']    = systs['targetmcmistagDown']
  systs['controlmcmistagUp']     = _fin.Get("singlemuontop_ttbar_mistagUp");    systs_e['controlmcmistagUp']     = _fin.Get("singleelectrontop_ttbar_mistagUp")
  systs['controlmcmistagDown']   = _fin.Get("singlemuontop_ttbar_mistagDown");  systs_e['controlmcmistagDown']   = _fin.Get("singleelectrontop_ttbar_mistagDown")
  systs['targetmcsjmistagUp']      = _fin.Get("signal_ttbar_sjmistagUp");           systs_e['targetmcsjmistagUp']      = systs['targetmcsjmistagUp']
  systs['targetmcsjmistagDown']    = _fin.Get("signal_ttbar_sjmistagDown");         systs_e['targetmcsjmistagDown']    = systs['targetmcsjmistagDown']
  systs['controlmcsjmistagUp']     = _fin.Get("singlemuontop_ttbar_sjmistagUp");    systs_e['controlmcsjmistagUp']     = _fin.Get("singleelectrontop_ttbar_sjmistagUp")
  systs['controlmcsjmistagDown']   = _fin.Get("singlemuontop_ttbar_sjmistagDown");  systs_e['controlmcsjmistagDown']   = _fin.Get("singleelectrontop_ttbar_sjmistagDown")
  
  systs_w['targetmcbtagUp']      = _fin.Get("signal_ttbar_btagUp");           systs_w_e['targetmcbtagUp']      = systs_w['targetmcbtagUp']
  systs_w['targetmcbtagDown']    = _fin.Get("signal_ttbar_btagDown");         systs_w_e['targetmcbtagDown']    = systs_w['targetmcbtagDown']
  systs_w['targetmcsjbtagUp']    = _fin.Get("signal_ttbar_sjbtagUp");         systs_w_e['targetmcsjbtagUp']    = systs_w['targetmcsjbtagUp']
  systs_w['targetmcsjbtagDown']  = _fin.Get("signal_ttbar_sjbtagDown");       systs_w_e['targetmcsjbtagDown']  = systs_w['targetmcsjbtagDown']
  systs_w['controlmcbtagUp']     = _fin.Get("singlemuonw_ttbar_btagUp");      systs_w_e['controlmcbtagUp']     = _fin.Get("singleelectronw_ttbar_btagUp")
  systs_w['controlmcbtagDown']   = _fin.Get("singlemuonw_ttbar_btagDown");    systs_w_e['controlmcbtagDown']   = _fin.Get("singleelectronw_ttbar_btagDown")
  systs_w['controlmcsjbtagUp']   = _fin.Get("singlemuonw_ttbar_sjbtagUp");    systs_w_e['controlmcsjbtagUp']   = _fin.Get("singleelectronw_ttbar_sjbtagUp")
  systs_w['controlmcsjbtagDown'] = _fin.Get("singlemuonw_ttbar_sjbtagDown");  systs_w_e['controlmcsjbtagDown'] = _fin.Get("singleelectronw_ttbar_sjbtagDown")

  systs_w['targetmcmistagUp']      = _fin.Get("signal_ttbar_mistagUp");           systs_w_e['targetmcmistagUp']      = systs_w['targetmcmistagUp']
  systs_w['targetmcmistagDown']    = _fin.Get("signal_ttbar_mistagDown");         systs_w_e['targetmcmistagDown']    = systs_w['targetmcmistagDown']
  systs_w['targetmcsjmistagUp']    = _fin.Get("signal_ttbar_sjmistagUp");         systs_w_e['targetmcsjmistagUp']    = systs_w['targetmcsjmistagUp']
  systs_w['targetmcsjmistagDown']  = _fin.Get("signal_ttbar_sjmistagDown");       systs_w_e['targetmcsjmistagDown']  = systs_w['targetmcsjmistagDown']
  systs_w['controlmcmistagUp']     = _fin.Get("singlemuonw_ttbar_mistagUp");      systs_w_e['controlmcmistagUp']     = _fin.Get("singleelectronw_ttbar_mistagUp")
  systs_w['controlmcmistagDown']   = _fin.Get("singlemuonw_ttbar_mistagDown");    systs_w_e['controlmcmistagDown']   = _fin.Get("singleelectronw_ttbar_mistagDown")
  systs_w['controlmcsjmistagUp']   = _fin.Get("singlemuonw_ttbar_sjmistagUp");    systs_w_e['controlmcsjmistagUp']   = _fin.Get("singleelectronw_ttbar_sjmistagUp")
  systs_w['controlmcsjmistagDown'] = _fin.Get("singlemuonw_ttbar_sjmistagDown");  systs_w_e['controlmcsjmistagDown'] = _fin.Get("singleelectronw_ttbar_sjmistagDown")

  # systs['targetmcsjbtagUp'] = _fin.Get("signal_ttbar_sjbtagUp"); systs_e['targetmcsjbtagUp'] = systs['targetmcsjbtagUp']
  # systs['targetmcsjbtagDown'] = _fin.Get("signal_ttbar_sjbtagDown"); systs_e['targetmcsjbtagDown'] = systs['targetmcsjbtagDown']
  # systs['controlmcsjbtagUp'] = _fin.Get("singlemuontop_ttbar_sjbtagUp"); systs_e['controlmcsjbtagUp'] = _fin.Get("singleelectrontop_ttbar_sjbtagUp")
  # systs['controlmcsjbtagDown'] = _fin.Get("singlemuontop_ttbar_sjbtagDown"); systs_e['controlmcsjbtagDown'] = _fin.Get("singleelectrontop_ttbar_sjbtagDown")

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down

  TopScales      = makeTop(cid,_fOut,"topmn",targetmc,controlmc,diag,_wspace,systs,False)
  TopScales_e    = makeTop(cid,_fOut,"topen",targetmc,controlmc_e,diag,_wspace,systs_e,False)
  TopScales_w    = makeTop(cid,_fOut,"topwmn",targetmc,controlmc_w,diag,_wspace,systs_w,True)
  TopScales_w_e  = makeTop(cid,_fOut,"topwen",targetmc,controlmc_w_e,diag,_wspace,systs_w_e,True)


  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(targetmc.GetNbinsX()+1):
    _bins.append(targetmc.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg TopScales

  CRs = [
   Channel("singlemuontopModel",      _wspace,out_ws,cid+'_'+model,TopScales),
   Channel("singleelectrontopModel",  _wspace,out_ws,cid+'_'+model,TopScales_e),
   Channel("singlemuonwtopModel",     _wspace,out_ws,cid+'_'+model,TopScales_w),
   Channel("singleelectronwtopModel", _wspace,out_ws,cid+'_'+model,TopScales_w_e),
  ]


  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=TopScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)
  
  addTopErrors(TopScales,    targetmc,"topmn", "singlemuontopModel",     _fOut,CRs,0,cid)
  addTopErrors(TopScales_e,  targetmc,"topen", "singleelectrontopModel", _fOut,CRs,1,cid)
  addTopErrors(TopScales_w,  targetmc,"topwmn","singlemuonwtopModel",    _fOut,CRs,2,cid,True)
  addTopErrors(TopScales_w_e,targetmc,"topwen","singleelectronwtopModel",_fOut,CRs,3,cid,True)

  #######################################################################################################

  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,targetmc.GetName(),CRs,diag)
  #cat.setDependant("zjets","wjetsdependant")  # Can use this to state that the "BASE" of this is already dependant on another process
  # EG if the W->lv in signal is dependant on the Z->vv and then the W->mv is depenant on W->lv, then 
  # give the arguments model,channel name from the config which defines the Z->vv => W->lv map! 
  # Return of course
  return cat

