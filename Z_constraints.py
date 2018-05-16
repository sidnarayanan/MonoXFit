import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining *cmodel*, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "zjets"
correlate_ewk = True 
new_ewk = True 

def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  
  # Some setup
  _fin = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)

  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # example below for creating shape systematic for photon which is just every bin up/down 30% 

  metname    = "met"          # Observable variable name 
  gvptname   = "genBosonPt"    # Weights are in generator pT

  target                = _fin.Get("signal_zjets")            # define monimal (MC) of which process this config will model
  target_btagUp         = _fin.Get("signal_zjets_btagUp")
  target_btagDown       = _fin.Get("signal_zjets_btagDown")
  target_sjbtagUp       = _fin.Get("signal_zjets_sjbtagUp")
  target_sjbtagDown     = _fin.Get("signal_zjets_sjbtagDown")
  target_mistagUp       = _fin.Get("signal_zjets_mistagUp")
  target_mistagDown     = _fin.Get("signal_zjets_mistagDown")
  target_sjmistagUp     = _fin.Get("signal_zjets_sjmistagUp")
  target_sjmistagDown   = _fin.Get("signal_zjets_sjmistagDown")
  controlmc             = _fin.Get("dimuon_zll")              # defines Zmm MC of which process will be controlled by
  controlmc_photon      = _fin.Get("photon_gjets")            # defines Gjets MC of which process will be controlled by
  controlmc_e           = _fin.Get("dielectron_zll")          # defines Zmm MC of which process will be controlled by
  controlmc_w           = _fin.Get('signal_wjets')            # Wlv MC in signal region

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  ZmmScales = target.Clone(); ZmmScales.SetName("zmm_weights_%s"%cid)
  ZmmScales.Divide(controlmc)
  _fOut.WriteTObject(ZmmScales)  # always write out to the directory 

  ZeeScales = target.Clone(); ZeeScales.SetName("zee_weights_%s"%cid)
  ZeeScales.Divide(controlmc_e)
  _fOut.WriteTObject(ZeeScales)  # always write out to the directory 

  ### btag ###
  ZmmScales_btagUp = target_btagUp.Clone(); ZmmScales_btagUp.SetName("zmm_weights_%s_btag_Up"%cid)
  ZmmScales_btagUp.Divide(controlmc); _fOut.WriteTObject(ZmmScales_btagUp)
  
  ZmmScales_btagDown = target_btagDown.Clone(); ZmmScales_btagDown.SetName("zmm_weights_%s_btag_Down"%cid)
  ZmmScales_btagDown.Divide(controlmc); _fOut.WriteTObject(ZmmScales_btagDown)

  ZmmScales_mistagUp = target_mistagUp.Clone(); ZmmScales_mistagUp.SetName("zmm_weights_%s_mistag_Up"%cid)
  ZmmScales_mistagUp.Divide(controlmc); _fOut.WriteTObject(ZmmScales_mistagUp)
  
  ZmmScales_mistagDown = target_mistagDown.Clone(); ZmmScales_mistagDown.SetName("zmm_weights_%s_mistag_Down"%cid)
  ZmmScales_mistagDown.Divide(controlmc); _fOut.WriteTObject(ZmmScales_mistagDown)

  ZeeScales_btagUp = target_btagUp.Clone(); ZeeScales_btagUp.SetName("zee_weights_%s_btag_Up"%cid)
  ZeeScales_btagUp.Divide(controlmc_e); _fOut.WriteTObject(ZeeScales_btagUp)
  
  ZeeScales_btagDown = target_btagDown.Clone(); ZeeScales_btagDown.SetName("zee_weights_%s_btag_Down"%cid)
  ZeeScales_btagDown.Divide(controlmc_e); _fOut.WriteTObject(ZeeScales_btagDown)

  ZeeScales_mistagUp = target_mistagUp.Clone(); ZeeScales_mistagUp.SetName("zee_weights_%s_mistag_Up"%cid)
  ZeeScales_mistagUp.Divide(controlmc_e); _fOut.WriteTObject(ZeeScales_mistagUp)
  
  ZeeScales_mistagDown = target_mistagDown.Clone(); ZeeScales_mistagDown.SetName("zee_weights_%s_mistag_Down"%cid)
  ZeeScales_mistagDown.Divide(controlmc_e); _fOut.WriteTObject(ZeeScales_mistagDown)

  ZmmScales_sjbtagUp = target_sjbtagUp.Clone(); ZmmScales_sjbtagUp.SetName("zmm_weights_%s_sjbtag_Up"%cid)
  ZmmScales_sjbtagUp.Divide(controlmc); _fOut.WriteTObject(ZmmScales_sjbtagUp)
  
  ZmmScales_sjbtagDown = target_sjbtagDown.Clone(); ZmmScales_sjbtagDown.SetName("zmm_weights_%s_sjbtag_Down"%cid)
  ZmmScales_sjbtagDown.Divide(controlmc); _fOut.WriteTObject(ZmmScales_sjbtagDown)

  ZmmScales_sjmistagUp = target_sjmistagUp.Clone(); ZmmScales_sjmistagUp.SetName("zmm_weights_%s_sjmistag_Up"%cid)
  ZmmScales_sjmistagUp.Divide(controlmc); _fOut.WriteTObject(ZmmScales_sjmistagUp)
  
  ZmmScales_sjmistagDown = target_sjmistagDown.Clone(); ZmmScales_sjmistagDown.SetName("zmm_weights_%s_sjmistag_Down"%cid)
  ZmmScales_sjmistagDown.Divide(controlmc); _fOut.WriteTObject(ZmmScales_sjmistagDown)

  ZeeScales_sjbtagUp = target_sjbtagUp.Clone(); ZeeScales_sjbtagUp.SetName("zee_weights_%s_sjbtag_Up"%cid)
  ZeeScales_sjbtagUp.Divide(controlmc_e); _fOut.WriteTObject(ZeeScales_sjbtagUp)
  
  ZeeScales_sjbtagDown = target_sjbtagDown.Clone(); ZeeScales_sjbtagDown.SetName("zee_weights_%s_sjbtag_Down"%cid)
  ZeeScales_sjbtagDown.Divide(controlmc_e); _fOut.WriteTObject(ZeeScales_sjbtagDown)

  ZeeScales_sjmistagUp = target_sjmistagUp.Clone(); ZeeScales_sjmistagUp.SetName("zee_weights_%s_sjmistag_Up"%cid)
  ZeeScales_sjmistagUp.Divide(controlmc_e); _fOut.WriteTObject(ZeeScales_sjmistagUp)
  
  ZeeScales_sjmistagDown = target_sjmistagDown.Clone(); ZeeScales_sjmistagDown.SetName("zee_weights_%s_sjmistag_Down"%cid)
  ZeeScales_sjmistagDown.Divide(controlmc_e); _fOut.WriteTObject(ZeeScales_sjmistagDown)

  WZScales = target.Clone(); WZScales.SetName('w_weights_%s'%cid)
  WZScales.Divide(controlmc_w); _fOut.WriteTObject(WZScales)

  ### done btag ###

  ### met trig ###
  ftrig = r.TFile.Open('files/unc/all_trig2.root')
  h_trig_down = ftrig.Get('trig_sys_down')
  h_trig_up = ftrig.Get('trig_sys_up')

  zmm_ratio_trig_up = target.Clone(); zmm_ratio_trig_up.SetName('zmm_weights_%s_mettrig_Up'%cid)
  for b in range(zmm_ratio_trig_up.GetNbinsX()): zmm_ratio_trig_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(zmm_ratio_trig_up,h_trig_up,metname,metname,_wspace.data("signal_zjets"))
  zmm_ratio_trig_up.Divide(controlmc)
  _fOut.WriteTObject(zmm_ratio_trig_up)

  zmm_ratio_trig_down = target.Clone(); zmm_ratio_trig_down.SetName('zmm_weights_%s_mettrig_Down'%cid)
  for b in range(zmm_ratio_trig_down.GetNbinsX()): zmm_ratio_trig_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(zmm_ratio_trig_down,h_trig_down,metname,metname,_wspace.data("signal_zjets"))
  zmm_ratio_trig_down.Divide(controlmc)
  _fOut.WriteTObject(zmm_ratio_trig_down)

  zee_ratio_trig_up = target.Clone(); zee_ratio_trig_up.SetName('zee_weights_%s_mettrig_Up'%cid)
  for b in range(zee_ratio_trig_up.GetNbinsX()): zee_ratio_trig_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(zee_ratio_trig_up,h_trig_up,metname,metname,_wspace.data("signal_zjets"))
  zee_ratio_trig_up.Divide(controlmc_e)
  _fOut.WriteTObject(zee_ratio_trig_up)

  zee_ratio_trig_down = target.Clone(); zee_ratio_trig_down.SetName('zee_weights_%s_mettrig_Down'%cid)
  for b in range(zee_ratio_trig_down.GetNbinsX()): zee_ratio_trig_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(zee_ratio_trig_down,h_trig_down,metname,metname,_wspace.data("signal_zjets"))
  zee_ratio_trig_down.Divide(controlmc_e)
  _fOut.WriteTObject(zee_ratio_trig_down)


  ### PHOTONS ###
  my_function(_wspace,_fin,_fOut,cid,diag)
  PhotonScales = _fOut.Get("photon_weights_%s"%cid)

  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(target.GetNbinsX()+1):
    _bins.append(target.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg WScales

  CRs = [
   Channel("photonModel",_wspace,out_ws,cid+'_'+model,PhotonScales) 
  ,Channel("dimuonModel",_wspace,out_ws,cid+'_'+model,ZmmScales)
  ,Channel("dielectronModel",_wspace,out_ws,cid+'_'+model,ZeeScales)
  ,Channel("wzModel",_wspace,out_ws,cid+'_'+model,WZScales)
  ]

  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)

  # Bin by bin nuisances to cover statistical uncertainties ...

  # define function locally for convenient access to stuff
  def addStatErrs(hx,cr,crname1,crname2):
    for b in range(1,target.GetNbinsX()+1):
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

  addStatErrs(PhotonScales,CRs[0],'photon','photonModelCR')
  addStatErrs(ZmmScales,CRs[1],'zmm','dimuonModelCR')
  addStatErrs(ZeeScales,CRs[2],'zee','dielectronModelCR')
  addStatErrs(WZScales,CRs[3],'w','wzModelCR')


  #######################################################################################################

  for i in [0,1,2]:
    CRs[i].add_nuisance_shape("mettrig",_fOut)
  
  CRs[0].add_nuisance_shape("renscale",_fOut) 
  CRs[0].add_nuisance_shape("facscale",_fOut) 
  CRs[0].add_nuisance_shape("pdf",_fOut) 
  CRs[0].add_nuisance("PhotonEff",0.02) 
  for cr in [0,1,2]:
    # CRs[cr].add_nuisance_shape('btag',_fOut)
    # CRs[cr].add_nuisance_shape('mistag',_fOut)
    CRs[cr].add_nuisance_shape('sjbtag',_fOut)
    CRs[cr].add_nuisance_shape('sjmistag',_fOut)
  CRs[3].add_nuisance_shape('wrenscale',_fOut)
  CRs[3].add_nuisance_shape('wfacscale',_fOut)
  CRs[3].add_nuisance_shape('wpdf',_fOut)
  
  if correlate_ewk:
    if new_ewk:
      CRs[0].add_nuisance_shape("ewk",_fOut)
      CRs[0].add_nuisance_shape("ewk_missZ",_fOut)
      CRs[0].add_nuisance_shape("ewk_missA",_fOut)
      CRs[0].add_nuisance_shape("ewk_sudZ",_fOut)
      CRs[0].add_nuisance_shape("ewk_sudA",_fOut)
      CRs[3].add_nuisance_shape("ewkWZ",_fOut)
      CRs[3].add_nuisance_shape("ewk_missZ",_fOut)
      CRs[3].add_nuisance_shape("ewk_missW",_fOut)
      CRs[3].add_nuisance_shape("ewk_sudZ",_fOut)
      CRs[3].add_nuisance_shape("ewk_sudW",_fOut)
    else:
      CRs[0].add_nuisance_shape("ewk",_fOut)
      CRs[3].add_nuisance_shape("w_ewk",_fOut)
  else:
    for b in range(target.GetNbinsX()):
      CRs[0].add_nuisance_shape("ewk_%s_bin%d"%(cid,b),_fOut)
      CRs[3].add_nuisance_shape("w_ewk_%s_bin%d"%(cid,b),_fOut)

  #######################################################################################################

  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,target.GetName(),CRs,diag)
  # Return of course
  return cat

# My Function. Just to put all of the complicated part into one function
def my_function(_wspace,_fin,_fOut,nam,diag):

  metname    = "met"          # Observable variable name 
  gvptname   = "genBosonPt"    # Weights are in generator pT

  target             = _fin.Get("signal_zjets")      # define monimal (MC) of which process this config will model
  target_btagUp        = _fin.Get("signal_zjets_btagUp")
  target_btagDown      = _fin.Get("signal_zjets_btagDown")
  target_mistagUp      = _fin.Get("signal_zjets_mistagUp")
  target_mistagDown    = _fin.Get("signal_zjets_mistagDown")
  target_sjbtagUp      = _fin.Get("signal_zjets_sjbtagUp")
  target_sjbtagDown    = _fin.Get("signal_zjets_sjbtagDown")
  target_sjmistagUp    = _fin.Get("signal_zjets_sjmistagUp")
  target_sjmistagDown  = _fin.Get("signal_zjets_sjmistagDown")
  
  controlmc          = _fin.Get("dimuon_zll")           # defines Zmm MC of which process will be controlled by
  controlmc_photon   = _fin.Get("photon_gjets")       # defines Gjets MC of which process will be controlled by
  controlmc_w        = _fin.Get('signal_wjets')            # Wlv MC in signal region
  
  _gjet_mcname 	     = "photon_gjets"
  GJet               = _fin.Get("photon_gjets")

  fztoa = r.TFile.Open("files/atoz_unc.root")
  
  ztoa_renscale_up   = fztoa.Get("znlo1_over_anlo1_renScaleUp")
  ztoa_renscale_down = fztoa.Get("znlo1_over_anlo1_renScaleDown")

  ztoa_facscale_up   = fztoa.Get("znlo1_over_anlo1_facScaleUp")
  ztoa_facscale_down = fztoa.Get("znlo1_over_anlo1_facScaleDown")

  ztoa_pdf_up   = fztoa.Get("znlo1_over_anlo1_pdfUp")
  ztoa_pdf_down = fztoa.Get("znlo1_over_anlo1_pdfDown")

  PhotonSpectrum = controlmc_photon.Clone(); PhotonSpectrum.SetName("photon_spectrum_%s_"%nam)
  ZvvSpectrum 	 = target.Clone(); ZvvSpectrum.SetName("zvv_spectrum_%s_"%nam)

  _fOut.WriteTObject( PhotonSpectrum )
  _fOut.WriteTObject( ZvvSpectrum )
  
  #################################################################################################################

  Pho = controlmc_photon.Clone(); Pho.SetName("photon_weights_denom_%s"%nam)
  Zvv = target.Clone(); Zvv.SetName("photon_weights_nom_%s"%nam)

  ### btag ###
  PhoScales_btagUp = target_btagUp.Clone(); PhoScales_btagUp.SetName("photon_weights_%s_btag_Up"%nam)
  PhoScales_btagUp.Divide(Pho); _fOut.WriteTObject(PhoScales_btagUp)
  
  PhoScales_btagDown = target_btagDown.Clone(); PhoScales_btagDown.SetName("photon_weights_%s_btag_Down"%nam)
  PhoScales_btagDown.Divide(Pho); _fOut.WriteTObject(PhoScales_btagDown)

  PhoScales_mistagUp = target_mistagUp.Clone(); PhoScales_mistagUp.SetName("photon_weights_%s_mistag_Up"%nam)
  PhoScales_mistagUp.Divide(Pho); _fOut.WriteTObject(PhoScales_mistagUp)
  
  PhoScales_mistagDown = target_mistagDown.Clone(); PhoScales_mistagDown.SetName("photon_weights_%s_mistag_Down"%nam)
  PhoScales_mistagDown.Divide(Pho); _fOut.WriteTObject(PhoScales_mistagDown)

  PhoScales_sjbtagUp = target_sjbtagUp.Clone(); PhoScales_sjbtagUp.SetName("photon_weights_%s_sjbtag_Up"%nam)
  PhoScales_sjbtagUp.Divide(Pho); _fOut.WriteTObject(PhoScales_sjbtagUp)
  
  PhoScales_sjbtagDown = target_sjbtagDown.Clone(); PhoScales_sjbtagDown.SetName("photon_weights_%s_sjbtag_Down"%nam)
  PhoScales_sjbtagDown.Divide(Pho); _fOut.WriteTObject(PhoScales_sjbtagDown)

  PhoScales_sjmistagUp = target_sjmistagUp.Clone(); PhoScales_sjmistagUp.SetName("photon_weights_%s_sjmistag_Up"%nam)
  PhoScales_sjmistagUp.Divide(Pho); _fOut.WriteTObject(PhoScales_sjmistagUp)
  
  PhoScales_sjmistagDown = target_sjmistagDown.Clone(); PhoScales_sjmistagDown.SetName("photon_weights_%s_sjmistag_Down"%nam)
  PhoScales_sjmistagDown.Divide(Pho); _fOut.WriteTObject(PhoScales_sjmistagDown)

  ### done btag ###

  ratio_ren_scale_up = Zvv.Clone();  ratio_ren_scale_up.SetName("photon_weights_%s_renscale_Up"%nam);
  for b in range(ratio_ren_scale_up.GetNbinsX()): ratio_ren_scale_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(ratio_ren_scale_up,ztoa_renscale_up,gvptname,metname,_wspace.data("signal_zjets"))
  ratio_ren_scale_up.Divide(Pho)
  _fOut.WriteTObject(ratio_ren_scale_up)
  
  ratio_ren_scale_down = Zvv.Clone();  ratio_ren_scale_down.SetName("photon_weights_%s_renscale_Down"%nam);
  for b in range(ratio_ren_scale_down.GetNbinsX()): ratio_ren_scale_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(ratio_ren_scale_down,ztoa_renscale_down,gvptname,metname,_wspace.data("signal_zjets"))
  ratio_ren_scale_down.Divide(Pho)
  _fOut.WriteTObject(ratio_ren_scale_down)

  ratio_fac_scale_up = Zvv.Clone();  ratio_fac_scale_up.SetName("photon_weights_%s_facscale_Up"%nam);
  for b in range(ratio_fac_scale_up.GetNbinsX()): ratio_fac_scale_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(ratio_fac_scale_up,ztoa_facscale_up,gvptname,metname,_wspace.data("signal_zjets"))
  ratio_fac_scale_up.Divide(Pho)
  _fOut.WriteTObject(ratio_fac_scale_up)
  
  ratio_fac_scale_down = Zvv.Clone();  ratio_fac_scale_down.SetName("photon_weights_%s_facscale_Down"%nam);
  for b in range(ratio_fac_scale_down.GetNbinsX()): ratio_fac_scale_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(ratio_fac_scale_down,ztoa_facscale_down,gvptname,metname,_wspace.data("signal_zjets"))
  ratio_fac_scale_down.Divide(Pho)
  _fOut.WriteTObject(ratio_fac_scale_down)

  ratio_pdf_up = Zvv.Clone();  ratio_pdf_up.SetName("photon_weights_%s_pdf_Up"%nam);
  for b in range(ratio_pdf_up.GetNbinsX()): ratio_pdf_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(ratio_pdf_up,ztoa_pdf_up,gvptname,metname,_wspace.data("signal_zjets"))
  ratio_pdf_up.Divide(Pho)
  _fOut.WriteTObject(ratio_pdf_up)
  
  ratio_pdf_down = Zvv.Clone();  ratio_pdf_down.SetName("photon_weights_%s_pdf_Down"%nam);
  for b in range(ratio_pdf_down.GetNbinsX()): ratio_pdf_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(ratio_pdf_down,ztoa_pdf_down,gvptname,metname,_wspace.data("signal_zjets"))
  ratio_pdf_down.Divide(Pho)
  _fOut.WriteTObject(ratio_pdf_down)


  # met trigger
  ftrig = r.TFile.Open('files/unc/all_trig2.root')
  h_trig_down = ftrig.Get('trig_sys_down')
  h_trig_up = ftrig.Get('trig_sys_up')

  ratio_trig_up = Zvv.Clone(); ratio_trig_up.SetName('photon_weights_%s_mettrig_Up'%nam)
  for b in range(ratio_trig_up.GetNbinsX()): ratio_trig_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(ratio_trig_up,h_trig_up,metname,metname,_wspace.data("signal_zjets"))
  ratio_trig_up.Divide(Pho)
  _fOut.WriteTObject(ratio_trig_up)

  ratio_trig_down = Zvv.Clone(); ratio_trig_down.SetName('photon_weights_%s_mettrig_Down'%nam)
  for b in range(ratio_trig_down.GetNbinsX()): ratio_trig_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(ratio_trig_down,h_trig_down,metname,metname,_wspace.data("signal_zjets"))
  ratio_trig_down.Divide(Pho)
  _fOut.WriteTObject(ratio_trig_down)

  # fztoaewk = fztoa
  ewk_uncs = None
  if new_ewk:
    fztoaewk = r.TFile.Open('files/unc/gz_unc_v6.root')
    ztoa_ewk_up   = fztoaewk.Get("ZG_NNLOEWK_met")
    ztoa_ewk_down   = fztoaewk.Get("ZG_NNLOEWK_met_Down")

    def build_ewk(in_hist_name, unc_name):
      ratio = Zvv.Clone();
      ratio.SetName('photon_weights_%s_%s'%(nam,unc_name))
      for b in xrange(ratio.GetNbinsX()): ratio.SetBinContent(b+1,0)
      in_hist = fztoaewk.Get(in_hist_name)
      diag.generateWeightedTemplate(ratio,in_hist,metname,metname,_wspace.data('signal_zjets'))
      ratio.Divide(Pho)
      return ratio

    ratio_ewk_up = build_ewk('ZG_NNLOEWK_met', 'ewk_Up')
    ratio_ewk_down = build_ewk('ZG_NNLOEWK_met_Down', 'ewk_Down')
    ratio_missZ_up = build_ewk('ZG_NNLOMiss1_met', 'ewk_missZ_Up')
    ratio_missZ_down = build_ewk('ZG_NNLOMiss1_met_Down', 'ewk_missZ_Down')
    ratio_missA_up = build_ewk('ZG_NNLOMiss2_met', 'ewk_missA_Up')
    ratio_missA_down = build_ewk('ZG_NNLOMiss2_met_Down', 'ewk_missA_Down')
    ratio_sudZ_up = build_ewk('ZG_Sudakov1_met', 'ewk_sudZ_Up')
    ratio_sudZ_down = build_ewk('ZG_Sudakov1_met_Down', 'ewk_sudZ_Down')
    ratio_sudA_up = build_ewk('ZG_Sudakov2_met', 'ewk_sudA_Up')
    ratio_sudA_down = build_ewk('ZG_Sudakov2_met_Down', 'ewk_sudA_Down')

    ewk_uncs = [ratio_ewk_up, ratio_ewk_down,
                ratio_missZ_up, ratio_missZ_down,
                ratio_missA_up, ratio_missA_down,
                ratio_sudZ_up, ratio_sudZ_down,
                ratio_sudA_up, ratio_sudA_down]

    '''
    ratio_ewk_up = Zvv.Clone();  ratio_ewk_up.SetName("photon_weights_%s_ewk_Up"%(nam));
    for b in range(ratio_ewk_up.GetNbinsX()): ratio_ewk_up.SetBinContent(b+1,0)  
    diag.generateWeightedTemplate(ratio_ewk_up,ztoa_ewk_up,metname,metname,_wspace.data("signal_zjets"))
    ratio_ewk_up.Divide(Pho)
    
    ratio_ewk_down = Zvv.Clone();  ratio_ewk_down.SetName("photon_weights_%s_ewk_Down"%(nam));
    for b in range(ratio_ewk_down.GetNbinsX()): ratio_ewk_down.SetBinContent(b+1,0)  
    diag.generateWeightedTemplate(ratio_ewk_down,ztoa_ewk_down,metname,metname,_wspace.data("signal_zjets"))
    ratio_ewk_down.Divide(Pho)
    '''
  else:
    fztoaewk = r.TFile.Open('files/atoz_unc.root')
    ztoa_ewk_up   = fztoaewk.Get("a_ewkcorr_overz_Upcommon")
    ztoa_ewk_down = fztoaewk.Get("a_ewkcorr_overz_Downcommon")

    ratio_ewk_up = Zvv.Clone();  ratio_ewk_up.SetName("photon_weights_%s_ewk_Up"%(nam));
    for b in range(ratio_ewk_up.GetNbinsX()): ratio_ewk_up.SetBinContent(b+1,0)  
    diag.generateWeightedTemplate(ratio_ewk_up,ztoa_ewk_up,gvptname,metname,_wspace.data("signal_zjets"))
    ratio_ewk_up.Divide(Pho)
    
    ratio_ewk_down = Zvv.Clone();  ratio_ewk_down.SetName("photon_weights_%s_ewk_Down"%(nam));
    for b in range(ratio_ewk_down.GetNbinsX()): ratio_ewk_down.SetBinContent(b+1,0)  
    diag.generateWeightedTemplate(ratio_ewk_down,ztoa_ewk_down,gvptname,metname,_wspace.data("signal_zjets"))
    ratio_ewk_down.Divide(Pho)

    ewk_uncs = [ratio_ewk_up, ratio_ewk_down]

  if correlate_ewk:
    for u in ewk_uncs:
      _fOut.WriteTObject(u)
  else:
    for b in range(target.GetNbinsX()):
      ewk_up = Zvv.Clone(); ewk_up.SetName("photon_weights_%s_ewk_%s_bin%d_Up"%(nam,nam,b))
      ewk_down = Zvv.Clone(); ewk_down.SetName("photon_weights_%s_ewk_%s_bin%d_Down"%(nam,nam,b))
      for i in range(target.GetNbinsX()):
        if i==b:
          ewk_up.SetBinContent(i+1,ratio_ewk_up.GetBinContent(i+1))
          ewk_down.SetBinContent(i+1,ratio_ewk_down.GetBinContent(i+1))
          break


      _fOut.WriteTObject(ewk_up)
      _fOut.WriteTObject(ewk_down)


  # done with systematics
  Zvv.Divide(Pho); Zvv.SetName("photon_weights_%s"%nam)

  PhotonScales = Zvv.Clone()
  _fOut.WriteTObject(PhotonScales)
  


  #################################################################################################################                                                                   

  #################################################################################################################
  ### Now lets do the same thing for W

  fztow = r.TFile.Open("files/wtoz_unc.root")
  
  ztow_renscale_up   = fztow.Get("znlo1_over_wnlo1_renScaleUp")
  ztow_renscale_down = fztow.Get("znlo1_over_wnlo1_renScaleDown")

  ztow_facscale_up   = fztow.Get("znlo1_over_wnlo1_facScaleUp")
  ztow_facscale_down = fztow.Get("znlo1_over_wnlo1_facScaleDown")

  ztow_pdf_up   = fztow.Get("znlo1_over_wnlo1_pdfUp")
  ztow_pdf_down = fztow.Get("znlo1_over_wnlo1_pdfDown")

  WSpectrum = controlmc_w.Clone(); WSpectrum.SetName("w_spectrum_%s_"%nam)
  ZvvSpectrum 	 = target.Clone(); ZvvSpectrum.SetName("zvv_spectrum_%s_"%nam)

  _fOut.WriteTObject( WSpectrum )

  #################################################################################################################

  Wsig = controlmc_w.Clone(); Wsig.SetName("w_weights_denom_%s"%nam)
  Zvv_w = target.Clone(); Zvv_w.SetName("w_weights_nom_%s"%nam)

  wratio_dummy = Zvv_w.Clone();  wratio_dummy.SetName("w_weights_%s_dummy"%nam);
  for b in range(wratio_dummy.GetNbinsX()): wratio_dummy.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wratio_dummy,None,gvptname,metname,_wspace.data("signal_zjets"))
  wratio_dummy.Divide(Wsig)
  _fOut.WriteTObject(wratio_dummy)
  
  wratio_ren_scale_up = Zvv_w.Clone();  wratio_ren_scale_up.SetName("w_weights_%s_wrenscale_Up"%nam);
  for b in range(wratio_ren_scale_up.GetNbinsX()): wratio_ren_scale_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wratio_ren_scale_up,ztow_renscale_up,gvptname,metname,_wspace.data("signal_zjets"))
  wratio_ren_scale_up.Divide(Wsig)
  _fOut.WriteTObject(wratio_ren_scale_up)
  
  wratio_ren_scale_down = Zvv_w.Clone();  wratio_ren_scale_down.SetName("w_weights_%s_wrenscale_Down"%nam);
  for b in range(wratio_ren_scale_down.GetNbinsX()): wratio_ren_scale_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wratio_ren_scale_down,ztow_renscale_down,gvptname,metname,_wspace.data("signal_zjets"))
  wratio_ren_scale_down.Divide(Wsig)
  _fOut.WriteTObject(wratio_ren_scale_down)

  wratio_fac_scale_up = Zvv_w.Clone(); wratio_fac_scale_up.SetName("w_weights_%s_wfacscale_Up"%nam);
  for b in range(wratio_fac_scale_up.GetNbinsX()): wratio_fac_scale_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wratio_fac_scale_up,ztow_facscale_up,gvptname,metname,_wspace.data("signal_zjets"))
  wratio_fac_scale_up.Divide(Wsig)
  _fOut.WriteTObject(wratio_fac_scale_up)
  
  wratio_fac_scale_down = Zvv_w.Clone();  wratio_fac_scale_down.SetName("w_weights_%s_wfacscale_Down"%nam);
  for b in range(wratio_fac_scale_down.GetNbinsX()): wratio_fac_scale_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wratio_fac_scale_down,ztow_facscale_down,gvptname,metname,_wspace.data("signal_zjets"))
  wratio_fac_scale_down.Divide(Wsig)
  _fOut.WriteTObject(wratio_fac_scale_down)

  wratio_pdf_up = Zvv_w.Clone();  wratio_pdf_up.SetName("w_weights_%s_wpdf_Up"%nam);
  for b in range(wratio_pdf_up.GetNbinsX()): wratio_pdf_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wratio_pdf_up,ztow_pdf_up,gvptname,metname,_wspace.data("signal_zjets"))
  wratio_pdf_up.Divide(Wsig)
  _fOut.WriteTObject(wratio_pdf_up)
  
  wratio_pdf_down = Zvv_w.Clone();  wratio_pdf_down.SetName("w_weights_%s_wpdf_Down"%nam);
  for b in range(ratio_pdf_down.GetNbinsX()): wratio_pdf_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wratio_pdf_down,ztow_pdf_down,gvptname,metname,_wspace.data("signal_zjets"))
  wratio_pdf_down.Divide(Wsig)
  _fOut.WriteTObject(wratio_pdf_down)


  ewk_uncs = None
  if new_ewk:
    fztowewk = r.TFile.Open("files/unc/wz_unc_v6.root")
    ztow_ewk_up   = fztowewk.Get("ZW_NNLOEWK_met")
    ztow_ewk_down = fztowewk.Get("ZW_NNLOEWK_met_Down")

    def build_ewk(in_hist_name, unc_name):
      ratio = Zvv.Clone();
      ratio.SetName('w_weights_%s_%s'%(nam,unc_name))
      for b in xrange(ratio.GetNbinsX()): ratio.SetBinContent(b+1,0)
      in_hist = fztowewk.Get(in_hist_name)
      diag.generateWeightedTemplate(ratio,in_hist,metname,metname,_wspace.data('signal_zjets'))
      ratio.Divide(Wsig)
      return ratio

    w_ratio_ewk_up = build_ewk('ZW_NNLOEWK_met', 'ewkWZ_Up')
    w_ratio_ewk_down = build_ewk('ZW_NNLOEWK_met_Down', 'ewkWZ_Down')
    w_ratio_missZ_up = build_ewk('ZW_NNLOMiss1_met', 'ewk_missZ_Up')
    w_ratio_missZ_down = build_ewk('ZW_NNLOMiss1_met_Down', 'ewk_missZ_Down')
    w_ratio_missW_up = build_ewk('ZW_NNLOMiss2_met', 'ewk_missW_Up')
    w_ratio_missW_down = build_ewk('ZW_NNLOMiss2_met_Down', 'ewk_missW_Down')
    w_ratio_sudZ_up = build_ewk('ZW_Sudakov1_met', 'ewk_sudZ_Up')
    w_ratio_sudZ_down = build_ewk('ZW_Sudakov1_met_Down', 'ewk_sudZ_Down')
    w_ratio_sudW_up = build_ewk('ZW_Sudakov2_met', 'ewk_sudW_Up')
    w_ratio_sudW_down = build_ewk('ZW_Sudakov2_met_Down', 'ewk_sudW_Down')

    w_ewk_uncs = [w_ratio_ewk_up, w_ratio_ewk_down,
                w_ratio_missZ_up, w_ratio_missZ_down,
                w_ratio_missW_up, w_ratio_missW_down,
                w_ratio_sudZ_up, w_ratio_sudZ_down,
                w_ratio_sudW_up, w_ratio_sudW_down]


    '''
    wratio_ewk_up = Zvv_w.Clone();  wratio_ewk_up.SetName("w_weights_%s_w_ewk_Up"%(nam));
    for b in range(wratio_ewk_up.GetNbinsX()): wratio_ewk_up.SetBinContent(b+1,0)  
    diag.generateWeightedTemplate(wratio_ewk_up,ztow_ewk_up,metname,metname,_wspace.data("signal_zjets"))
    wratio_ewk_up.Divide(Wsig)
    
    wratio_ewk_down = Zvv_w.Clone();  wratio_ewk_down.SetName("w_weights_%s_w_ewk_Down"%(nam));
    for b in range(wratio_ewk_down.GetNbinsX()): wratio_ewk_down.SetBinContent(b+1,0)  
    diag.generateWeightedTemplate(wratio_ewk_down,ztow_ewk_down,metname,metname,_wspace.data("signal_zjets"))
    wratio_ewk_down.Divide(Wsig)
    '''
  else:
    fztowewk = r.TFile.Open("files/wtoz_unc.root")
    ztow_ewk_up   = fztowewk.Get("w_ewkcorr_overz_Upcommon")
    ztow_ewk_down = fztowewk.Get("w_ewkcorr_overz_Downcommon")

    wratio_ewk_up = Zvv_w.Clone();  wratio_ewk_up.SetName("w_weights_%s_w_ewk_Up"%(nam));
    for b in range(wratio_ewk_up.GetNbinsX()): wratio_ewk_up.SetBinContent(b+1,0)  
    diag.generateWeightedTemplate(wratio_ewk_up,ztow_ewk_up,gvptname,metname,_wspace.data("signal_zjets"))
    wratio_ewk_up.Divide(Wsig)
    
    wratio_ewk_down = Zvv_w.Clone();  wratio_ewk_down.SetName("w_weights_%s_w_ewk_Down"%(nam));
    for b in range(wratio_ewk_down.GetNbinsX()): wratio_ewk_down.SetBinContent(b+1,0)  
    diag.generateWeightedTemplate(wratio_ewk_down,ztow_ewk_down,gvptname,metname,_wspace.data("signal_zjets"))
    wratio_ewk_down.Divide(Wsig)

    w_ewk_uncs = [wratio_ewk_up, wratio_ewk_down]


  ############### GET SOMETHING CENTRAL PLEASE ############################
  Zvv_w.Divide(Wsig)

  if correlate_ewk:
    for u in w_ewk_uncs:
      _fOut.WriteTObject(u)
    '''
    _fOut.WriteTObject(wratio_ewk_up)
    _fOut.WriteTObject(wratio_ewk_down)
    '''
  else:
    #Now lets uncorrelate the bins:
    for b in range(target.GetNbinsX()):
      ewk_up_w = Zvv_w.Clone(); ewk_up_w.SetName("w_weights_%s_w_ewk_%s_bin%d_Up"%(nam,nam,b))
      ewk_down_w = Zvv_w.Clone(); ewk_down_w.SetName("w_weights_%s_w_ewk_%s_bin%d_Down"%(nam,nam,b))
      for i in range(target.GetNbinsX()):
        if i==b:
          ewk_up_w.SetBinContent(i+1,wratio_ewk_up.GetBinContent(i+1))
          ewk_down_w.SetBinContent(i+1,wratio_ewk_down.GetBinContent(i+1))
          break


      _fOut.WriteTObject(ewk_up_w)
      _fOut.WriteTObject(ewk_down_w)

