rm -f *root
echo $@
text2workspace.py ../newewk_2cat.txt -m 125
echo 1
combineTool.py -M Impacts -d ../newewk_2cat.root -m 125 --doInitialFit --robustFit 1 $@
echo 2
combineTool.py -M Impacts -d ../newewk_2cat.root -m 125 --robustFit 1 --doFits --parallel 20 $@
echo 3
combineTool.py -M Impacts -d ../newewk_2cat.root -m 125 -o impacts.json 
echo 4
plotImpacts.py -i impacts.json -o impacts_monotop
