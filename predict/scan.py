#!/usr/bin/env python

import sys
PATH_INSTALL = "../androguard"

sys.path.append(PATH_INSTALL)

from feature_extract import extract
import os

def default_model(data):
	return False

if __name__ == "__main__" :
	if len(sys.argv) < 1:
		print("python classify.py <app> [model]")
	else:
	    print("=============================================")
	    print("Android Malware Detection (COMP8502 Project)")
	    print("(c) 2013 Tomas Tauber & Zhang Zhuo")
	    print("=============================================")
	    app_path = sys.argv[1]
	    app_name = os.path.basename(app_path)
	    print("App: " + app_name)
	    print("Classification Model: default") # TODO: model choice
	    print("")
	    print("Starting malware scanning")
	    print("Extracting features...")
	    data = extract.analyze(app_path)
	    print("Loading the model...") # TODO: model choice
	    print("Classifying...")
	    result = default_model(data)
	    if result:
	        print("")
	        print("MALWARE DETECTED")
	    else:
		    print("")
		    print("NO MALWARE FOUND")			
