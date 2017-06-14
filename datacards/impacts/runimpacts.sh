echo $@
text2workspace.py ../newewk_2cat.txt -m 125
combineTool.py -M Impacts -d ../newewk_2cat.root -m 125 --doInitialFit --robustFit 1 $@
combineTool.py -M Impacts -d ../newewk_2cat.root -m 125 --robustFit 1 --doFits --parallel 20 $@
combineTool.py -M Impacts -d ../newewk_2cat.root -m 125 -o impacts.json 
plotImpacts.py -i impacts.json -o impacts_monotop
