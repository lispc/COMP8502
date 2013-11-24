java -cp /usr/share/java/weka.jar weka.attributeSelection.InfoGainAttributeEval -s "weka.attributeSelection.Ranker 
-T 0.0 -N 20"  -i training_trimmed.arff -c 1 | tee select_feature_result.txt
