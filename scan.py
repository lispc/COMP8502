#!/usr/bin/env python

import sys
PATH_INSTALL = "../androguard"

sys.path.append(PATH_INSTALL)

from feature_extract import extract
import arff
import os
import subprocess

MODELS = [("Naive Bayes", "weka.classifiers.bayes.NaiveBayes"), ("Decision Tree", "weka.classifiers.trees.J48 -C 0.25 -M 2"), ("Bayesian Network", "weka.classifiers.bayes.BayesNet -D -Q weka.classifiers.bayes.net.search.local.K2 -- -P 1 -S BAYES -E weka.classifiers.bayes.net.estimate.SimpleEstimator -- -A 0.5"), ("SVM", "weka.classifiers.functions.SMO -C 1.0 -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 -K \\\"weka.classifiers.functions.supportVector.PolyKernel -C 250007 -E 1.0\\\""), ("Boosted Decision Tree", "weka.classifiers.meta.AdaBoostM1 -P 100 -S 1 -I 10 -W weka.classifiers.trees.J48 -- -C 0.25 -M 2")]

DEFAULT_MODEL = 3
TEST_INSTANCE = "test.arff"
COMMAND = "java -cp predict/final.jar Test data/training.arff " + TEST_INSTANCE

def print_models():
        print("Default model: SVM")
        for i in range(0, len(MODELS)):
                print(str(i) + ": " + MODELS[i][0])

        print("For other models, please input the full class name and parameters for Weka.")

def get_model():
    try:
        if len(sys.argv) < 3:
            model = MODELS[DEFAULT_MODEL]
        else:
            choice = int(sys.argv[2])
            model = MODELS[choice]
        print("Classification Model: " + model[0])
        return model[1]
    except:
        model = " ".join(sys.argv[2:])
        print("Classification Model: " + model)
        return model

def load_model(model_str):
    parts = model_str.split()
    model = parts[0]
    if len(parts) == 1:
        rest = " \"\""
    else:
        rest = " \"" + ' '.join(parts[1:]) + "\""
    command = COMMAND + " " + model + rest
    out = subprocess.check_output(command, shell=True)
    result = out.split()
    return result[len(result) - 1] == 'True'

if __name__ == "__main__" :
	if len(sys.argv) < 2:
		print("Usage: python scan.py <app> [model]")
                print_models()

	else:
	    print("=============================================")
	    print("Android Malware Detection (COMP8502 Project)")
	    print("(c) 2013 Tomas Tauber & Zhang Zhuo")
	    print("=============================================")
	    app_path = sys.argv[1]
	    app_name = os.path.basename(app_path)
	    print("App: " + app_name)
            model = get_model()
            #os.chdir('predict') 
	    print("")
	    print("Starting malware scanning")
	    print("Extracting features...")
	    data = extract.analyze(app_path, [False, app_name])
            arff.dump(TEST_INSTANCE, [data], relation="APK", names=extract.NAMES)
	    print("Loading the model...")
            result = load_model(model)
	    print("Classifying...")
	    if result:
	        print("")
	        print("MALWARE DETECTED")
	    else:
		print("")
		print("NO MALWARE FOUND")			
