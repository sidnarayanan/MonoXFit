import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining cmodel provide, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "wjets"
def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  
  # Some setup
  _fin    = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)


  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # but for now this is just kept simple 
  processName  = "WJets" # Give a name of the process being modelled
  metname      = "met"    # Observable variable name 
  targetmc     = _fin.Get("signal_wjets")      # define monimal (MC) of which process this config will model
  controlmc    = _fin.Get("singlemuonw_wjets")  # defines in / out acceptance
  controlmc_e  = _fin.Get("singleelectronw_wjets")  # defines in / out acceptance

  # btag systs
  targetmcbtagUp = _fin.Get("signal_wjets_btagUp")
  targetmcbtagDown = _fin.Get("signal_wjets_btagDown")
  controlmcbtagUp = _fin.Get("singlemuonw_wjets_btagUp"); controlmcbtagUp_e = _fin.Get("singleelectronw_wjets_btagUp")
  controlmcbtagDown = _fin.Get("singlemuonw_wjets_btagDown"); controlmcbtagDown_e = _fin.Get("singleelectronw_wjets_btagDown")
  targetmcsjbtagUp = _fin.Get("signal_wjets_sjbtagUp")
  targetmcsjbtagDown = _fin.Get("signal_wjets_sjbtagDown")
  controlmcsjbtagUp = _fin.Get("singlemuonw_wjets_sjbtagUp"); controlmcsjbtagUp_e = _fin.Get("singleelectronw_wjets_sjbtagUp")
  controlmcsjbtagDown = _fin.Get("singlemuonw_wjets_sjbtagDown"); controlmcsjbtagDown_e = _fin.Get("singleelectronw_wjets_sjbtagDown")

  # mistag systs
  targetmcmistagUp = _fin.Get("signal_wjets_mistagUp")
  targetmcmistagDown = _fin.Get("signal_wjets_mistagDown")
  controlmcmistagUp = _fin.Get("singlemuonw_wjets_mistagUp"); controlmcmistagUp_e = _fin.Get("singleelectronw_wjets_mistagUp")
  controlmcmistagDown = _fin.Get("singlemuonw_wjets_mistagDown"); controlmcmistagDown_e = _fin.Get("singleelectronw_wjets_mistagDown")
  targetmcsjmistagUp = _fin.Get("signal_wjets_sjmistagUp")
  targetmcsjmistagDown = _fin.Get("signal_wjets_sjmistagDown")
  controlmcsjmistagUp = _fin.Get("singlemuonw_wjets_sjmistagUp"); controlmcsjmistagUp_e = _fin.Get("singleelectronw_wjets_sjmistagUp")
  controlmcsjmistagDown = _fin.Get("singlemuonw_wjets_sjmistagDown"); controlmcsjmistagDown_e = _fin.Get("singleelectronw_wjets_sjmistagDown")

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  
  WScales = targetmc.Clone(); WScales.SetName("wmn_weights_%s"%cid)
  WScales.Divide(controlmc);  _fOut.WriteTObject(WScales)  

  WScales_e = targetmc.Clone(); WScales_e.SetName("wen_weights_%s"%cid)
  WScales_e.Divide(controlmc_e);  _fOut.WriteTObject(WScales_e)  

  ### BTAG ###  
  WScalesbtagUp = targetmcbtagUp.Clone(); WScalesbtagUp.SetName("wmn_weights_%s_btag_Up"%cid)
  WScalesbtagUp.Divide(controlmcbtagUp);  _fOut.WriteTObject(WScalesbtagUp)  

  WScalesbtagDown = targetmcbtagDown.Clone(); WScalesbtagDown.SetName("wmn_weights_%s_btag_Down"%cid)
  WScalesbtagDown.Divide(controlmcbtagDown);  _fOut.WriteTObject(WScalesbtagDown)

  WScalesbtagUp_e = targetmcbtagUp.Clone(); WScalesbtagUp_e.SetName("wen_weights_%s_btag_Up"%cid)
  WScalesbtagUp_e.Divide(controlmcbtagUp_e);  _fOut.WriteTObject(WScalesbtagUp_e)  

  WScalesbtagDown_e = targetmcbtagDown.Clone(); WScalesbtagDown_e.SetName("wen_weights_%s_btag_Down"%cid)
  WScalesbtagDown_e.Divide(controlmcbtagDown_e);  _fOut.WriteTObject(WScalesbtagDown_e)  

  WScalessjbtagUp = targetmcsjbtagUp.Clone(); WScalessjbtagUp.SetName("wmn_weights_%s_sjbtag_Up"%cid)
  WScalessjbtagUp.Divide(controlmcsjbtagUp);  _fOut.WriteTObject(WScalessjbtagUp)  

  WScalessjbtagDown = targetmcsjbtagDown.Clone(); WScalessjbtagDown.SetName("wmn_weights_%s_sjbtag_Down"%cid)
  WScalessjbtagDown.Divide(controlmcsjbtagDown);  _fOut.WriteTObject(WScalessjbtagDown)

  WScalessjbtagUp_e = targetmcsjbtagUp.Clone(); WScalessjbtagUp_e.SetName("wen_weights_%s_sjbtag_Up"%cid)
  WScalessjbtagUp_e.Divide(controlmcsjbtagUp_e);  _fOut.WriteTObject(WScalessjbtagUp_e)  

  WScalessjbtagDown_e = targetmcsjbtagDown.Clone(); WScalessjbtagDown_e.SetName("wen_weights_%s_sjbtag_Down"%cid)
  WScalessjbtagDown_e.Divide(controlmcsjbtagDown_e);  _fOut.WriteTObject(WScalessjbtagDown_e)  

  ### MISTAG ###  
  WScalesmistagUp = targetmcmistagUp.Clone(); WScalesmistagUp.SetName("wmn_weights_%s_mistag_Up"%cid)
  WScalesmistagUp.Divide(controlmcmistagUp);  _fOut.WriteTObject(WScalesmistagUp)  

  WScalesmistagDown = targetmcmistagDown.Clone(); WScalesmistagDown.SetName("wmn_weights_%s_mistag_Down"%cid)
  WScalesmistagDown.Divide(controlmcmistagDown);  _fOut.WriteTObject(WScalesmistagDown)

  WScalesmistagUp_e = targetmcmistagUp.Clone(); WScalesmistagUp_e.SetName("wen_weights_%s_mistag_Up"%cid)
  WScalesmistagUp_e.Divide(controlmcmistagUp_e);  _fOut.WriteTObject(WScalesmistagUp_e)  

  WScalesmistagDown_e = targetmcmistagDown.Clone(); WScalesmistagDown_e.SetName("wen_weights_%s_mistag_Down"%cid)
  WScalesmistagDown_e.Divide(controlmcmistagDown_e);  _fOut.WriteTObject(WScalesmistagDown_e)  

  WScalessjmistagUp = targetmcsjmistagUp.Clone(); WScalessjmistagUp.SetName("wmn_weights_%s_sjmistag_Up"%cid)
  WScalessjmistagUp.Divide(controlmcsjmistagUp);  _fOut.WriteTObject(WScalessjmistagUp)  

  WScalessjmistagDown = targetmcsjmistagDown.Clone(); WScalessjmistagDown.SetName("wmn_weights_%s_sjmistag_Down"%cid)
  WScalessjmistagDown.Divide(controlmcsjmistagDown);  _fOut.WriteTObject(WScalessjmistagDown)

  WScalessjmistagUp_e = targetmcsjmistagUp.Clone(); WScalessjmistagUp_e.SetName("wen_weights_%s_sjmistag_Up"%cid)
  WScalessjmistagUp_e.Divide(controlmcsjmistagUp_e);  _fOut.WriteTObject(WScalessjmistagUp_e)  

  WScalessjmistagDown_e = targetmcsjmistagDown.Clone(); WScalessjmistagDown_e.SetName("wen_weights_%s_sjmistag_Down"%cid)
  WScalessjmistagDown_e.Divide(controlmcsjmistagDown_e);  _fOut.WriteTObject(WScalessjmistagDown_e)  

  ### met trig ###
  ftrig = r.TFile.Open('files/unc/all_trig2.root')
  h_trig_down = ftrig.Get('trig_sys_down')
  h_trig_up = ftrig.Get('trig_sys_up')

  wmn_ratio_trig_up = targetmc.Clone(); wmn_ratio_trig_up.SetName('wmn_weights_%s_mettrig_Up'%cid)
  for b in range(wmn_ratio_trig_up.GetNbinsX()): wmn_ratio_trig_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wmn_ratio_trig_up,h_trig_up,metname,metname,_wspace.data("signal_wjets"))
  wmn_ratio_trig_up.Divide(controlmc)
  _fOut.WriteTObject(wmn_ratio_trig_up)

  wmn_ratio_trig_down = targetmc.Clone(); wmn_ratio_trig_down.SetName('wmn_weights_%s_mettrig_Down'%cid)
  for b in range(wmn_ratio_trig_down.GetNbinsX()): wmn_ratio_trig_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wmn_ratio_trig_down,h_trig_down,metname,metname,_wspace.data("signal_wjets"))
  wmn_ratio_trig_down.Divide(controlmc)
  _fOut.WriteTObject(wmn_ratio_trig_down)

  wen_ratio_trig_up = targetmc.Clone(); wen_ratio_trig_up.SetName('wen_weights_%s_mettrig_Up'%cid)
  for b in range(wen_ratio_trig_up.GetNbinsX()): wen_ratio_trig_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wen_ratio_trig_up,h_trig_up,metname,metname,_wspace.data("signal_wjets"))
  wen_ratio_trig_up.Divide(controlmc_e)
  _fOut.WriteTObject(wen_ratio_trig_up)

  wen_ratio_trig_down = targetmc.Clone(); wen_ratio_trig_down.SetName('wen_weights_%s_mettrig_Down'%cid)
  for b in range(wen_ratio_trig_down.GetNbinsX()): wen_ratio_trig_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wen_ratio_trig_down,h_trig_down,metname,metname,_wspace.data("signal_wjets"))
  wen_ratio_trig_down.Divide(controlmc_e)
  _fOut.WriteTObject(wen_ratio_trig_down)



  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(targetmc.GetNbinsX()+1):
    _bins.append(targetmc.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  #   (name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg WScales

  CRs = [
   Channel("singlemuonwModel",_wspace,out_ws,cid+'_'+model,WScales),
   Channel("singleelectronwModel",_wspace,out_ws,cid+'_'+model,WScales_e),
  ]

  for c in CRs:
    c.add_nuisance_shape('mettrig',_fOut)


  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)

  for cr in [0,1]:
    #for uncert in ['btag','mistag','sjbtag','sjmistag']:
    for uncert in ['sjbtag','sjmistag']:
      CRs[cr].add_nuisance_shape(uncert,_fOut)
  
  def addStatErrs(hx,cr,crname1,crname2):
    for b in range(1,targetmc.GetNbinsX()+1):
      err = hx.GetBinError(b)
      if not hx.GetBinContent(b)>0:
        continue
      relerr = err/hx.GetBinContent(b)
      if relerr<0.01:
        continue
      byb_u = hx.Clone(); byb_u.SetName('%s_weights_%s_%s_stat_error_%s_bin%d_Up'%(crname1,cid,cid,crname2,b))
      byb_u.SetBinContent(b,hx.GetBinContent(b)+err)
      byb_d = hx.Clone(); byb_d.SetName('%s_weights_%s_%s_stat_error_%s_bin%d_Down'%(crname1,cid,cid,crname2,b))
      if err<hx.GetBinContent(b):
        byb_d.SetBinContent(b,hx.GetBinContent(b)-err)
      else:
        byb_d.SetBinContent(b,0)
      _fOut.WriteTObject(byb_u)
      _fOut.WriteTObject(byb_d)
      cr.add_nuisance_shape('%s_stat_error_%s_bin%d'%(cid,crname2,b),_fOut) # HERE

  addStatErrs(WScales,CRs[0],'wmn','singlemuonwModel')
  addStatErrs(WScales_e,CRs[1],'wen','singleelectronwModel')

  # # Statistical uncertainties too!, one per bin 
  # for b in range(targetmc.GetNbinsX()):
  #   err = WScales.GetBinError(b+1)
  #   if not WScales.GetBinContent(b+1)>0: continue 
  #   relerr = err/WScales.GetBinContent(b+1)
  #   if relerr<0.001: continue
  #   byb_u = WScales.Clone(); byb_u.SetName("wmn_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"singlemuonwModel",b))
  #   byb_u.SetBinContent(b+1,WScales.GetBinContent(b+1)+err)
  #   byb_d = WScales.Clone(); byb_d.SetName("wmn_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"singlemuonwModel",b))
  #   byb_d.SetBinContent(b+1,WScales.GetBinContent(b+1)-err)
  #   _fOut.WriteTObject(byb_u)
  #   _fOut.WriteTObject(byb_d)
  #   print "Adding an error -- ", byb_u.GetName(),err
  #   CRs[0].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"singlemuonwModel",b),_fOut)

  # # Statistical uncertainties too!, one per bin 
  # for b in range(targetmc.GetNbinsX()):
  #   err_e = WScales_e.GetBinError(b+1)
  #   if not WScales_e.GetBinContent(b+1)>0: continue 
  #   relerr_e = err_e/WScales_e.GetBinContent(b+1)
  #   if relerr_e<0.001: continue
  #   byb_u_e = WScales_e.Clone(); byb_u_e.SetName("wen_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"singleelectronwModel",b))
  #   byb_u_e.SetBinContent(b+1,WScales_e.GetBinContent(b+1)+err_e)
  #   byb_d_e = WScales_e.Clone(); byb_d_e.SetName("wen_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"singleelectronwModel",b))
  #   byb_d_e.SetBinContent(b+1,WScales_e.GetBinContent(b+1)-err_e)
  #   _fOut.WriteTObject(byb_u_e)
  #   _fOut.WriteTObject(byb_d_e)
  #   print "Adding an error -- ", byb_u_e.GetName(),err_e
  #   CRs[1].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"singleelectronwModel",b),_fOut)

  #######################################################################################################

  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,targetmc.GetName(),CRs,diag)
  cat.setDependant("zjets","wzModel")  # Can use this to state that the "BASE" of this is already dependant on another process
  # EG if the W->lv in signal is dependant on the Z->vv and then the W->mv is depenant on W->lv, then 
  # give the arguments model,channel name from the config which defines the Z->vv => W->lv map! 
  # Return of course
  return cat

