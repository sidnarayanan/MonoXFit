# text2workspace:
text2workspace.py newewk_2cat.txt --channel-masks
# doesn't work (errors like [1])
combine newewk_2cat.root -M MaxLikelihoodFit --saveShapes --saveWithUncertainties --setPhysicsModelParameters mask_loose_sig=1,mask_tight_sig=1 --rMin=0 --rMax=0 2>/dev/null
# following all work
# combine newewk_2cat.root -M MaxLikelihoodFit --saveShapes --saveWithUncertainties --setPhysicsModelParameters mask_tight_sig=1
# combine newewk_2cat.root -M MaxLikelihoodFit --saveShapes --saveWithUncertainties --setPhysicsModelParameters mask_loose_sig=1
# combine newewk_2cat.root -M MaxLikelihoodFit --saveShapes --saveWithUncertainties # this should be the same as the nominal fit, right? 

