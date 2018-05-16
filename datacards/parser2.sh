#!/bin/bash

rm -f nuisances.sh

echo "nuisance_name,fit_data_onlysource,fit_data_fixed,fit_asimov_onlysource,fit_asimov_fixed" > limits.csv

#DETECTING ALL THE GROUPS IN THE DATACARD AND WRITING THE PROPER COMBINE COMMANDS FOR EACH NUISANCE PARAMETER (GROUP)

while read line           
do           
     case "$line" in
       *group*)

	##GET NUISANCE NAME
    	nuisancename=`echo $line | awk '{print $1;}'`


	#####
	#####POST FIT SECTION
	#####


	##
	##PERFORM ASYMPTOTIC LIMIT CALCULATION WITH NUISANCE AS ONLY SOURCE
	##
        echo "combine higgsCombineTest.MultiDimFit.mH120.root --snapshotName MultiDimFit -M Asymptotic  -n randomtest   --bypassFrequentistFit  --freezeNuisanceGroups ^$nuisancename" > nuisance.sh
 
	. nuisance.sh | tee nuisance_${nuisancename}_limit_tmp.txt
	median_expected_postfit_data_onlysource=`cat nuisance_${nuisancename}_limit_tmp.txt | grep 'Median for expected limits' | awk '{print $5}'`

	rm nuisance.sh
	rm nuisance_${nuisancename}_limit_tmp.txt
	
	#ASYMPTOTIC LIMIT IS NOW SAVED IN median_expected_postfit_data_onlysource


	##
	##PERFORM ASYMPTOTIC LIMIT CALCULATION WITH NUISANCE REMOVED AND FIXED TO ITS POST-FIT VALUE
	##
	echo "combine higgsCombineTest.MultiDimFit.mH120.root --snapshotName MultiDimFit -M Asymptotic  -n randomtest  --bypassFrequentistFit   --freezeNuisanceGroups $nuisancename" > nuisance.sh

        . nuisance.sh | tee nuisance_${nuisancename}_limit_tmp.txt
        median_expected_postfit_data_fixed=`cat nuisance_${nuisancename}_limit_tmp.txt | grep 'Median for expected limits' | awk '{print $5}'`

        rm nuisance.sh
        rm nuisance_${nuisancename}_limit_tmp.txt
        
        #ASYMPTOTIC LIMIT IS NOW SAVED IN median_expected_postfit_data_onlysource




# 	#####
# 	#####PRE FIT SECTION	
# 	#####
# 	
# 	##
#         ##PERFORM ASYMPTOTIC LIMIT CALCULATION WITH NUISANCE AS ONLY SOURCE
#         ##
# 	echo "combine higgsCombinePreFit.MultiDimFit.mH120.root --snapshotName MultiDimFit -M Asymptotic  -n randomtest      --freezeNuisanceGroups ^$nuisancename" > nuisance.sh
# 
# 	. nuisance.sh | tee nuisance_${nuisancename}_limit_tmp.txt
# 	median_expected_prefit_onlysource=`cat nuisance_${nuisancename}_limit_tmp.txt | grep 'Median for expected limits' | awk '{print $5}'`
# 
#         rm nuisance.sh
#         rm nuisance_${nuisancename}_limit_tmp.txt
# 
#         #ASYMPTOTIC LIMIT IS NOW SAVED IN median_expected_prefit_onlysource
# 
# 
#         ##
#         ##PERFORM ASYMPTOTIC LIMIT CALCULATION WITH NUISANCE REMOVED AND FIXED TO ITS VALUE FROM THE FIT TO TOY
#         ##
#         echo "combine higgsCombinePreFit.MultiDimFit.mH120.root --snapshotName MultiDimFit -M Asymptotic  -n randomtest    --minimizerAlgo Minuit --freezeNuisanceGroups $nuisancename" > nuisance.sh
# 
#         . nuisance.sh | tee nuisance_${nuisancename}_limit_tmp.txt
#         median_expected_prefit_fixed=`cat nuisance_${nuisancename}_limit_tmp.txt | grep 'Median for expected limits' | awk '{print $5}'`
# 
#         rm nuisance.sh
#         rm nuisance_${nuisancename}_limit_tmp.txt
# 
#         #ASYMPTOTIC LIMIT IS NOW SAVED IN median_expected_prefit_fixed
# 
# 
# 
         echo "${nuisancename},${median_expected_postfit_data_onlysource},${median_expected_postfit_data_fixed},${median_expected_prefit_onlysource},${median_expected_prefit_fixed}" >> limits.csv	


     esac


	
done < test.txt
