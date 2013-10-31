#!/usr/bin/env python

import sys
PATH_INSTALL = "../../androguard"

sys.path.append(PATH_INSTALL)

import arff, os
import androlyze
from os import listdir

from androlyze import AnalyzeAPK

from androguard.core import *
from androguard.core.androgen import *
from androguard.core.androconf import *
from androguard.core.bytecode import *
from androguard.core.bytecodes.jvm import *
from androguard.core.bytecodes.dvm import *
from androguard.core.bytecodes.apk import *

from androguard.core.analysis.analysis import *
from androguard.core.analysis.ganalysis import *
from androguard.core.analysis.risk import *
from androguard.decompiler.decompiler import *
import cPickle

ALL_PERMISSIONS = cPickle.load(open('perms.pickle','r'))

def get_app_data(folder, app_path, malware):
	#app, d, dx = AnalyzeAPK(os.path.join(folder, app_path))
	app = APK(os.path.join(folder, app_path))
	app_perms = set(app.get_permissions())
	data = [malware]
	for perm in ALL_PERMISSIONS:
		if perm in app_perms:
			data.append(True)
		else:
			data.append(False)
	return data

if __name__ == "__main__" :
	if len(sys.argv) < 3:
		print("python extract.py <apps-folder> <malware-folder> <output>")
	else:
		if len(sys.argv) == 4:
			output = argv[3]
		else:
			output = "training.arff"
		apps = listdir(sys.argv[1])
		malware = listdir(sys.argv[2])
		data = []
		i = 1
		for app in apps:
			print(str(i) + "/" + str(len(apps)) + " " + app)
			data.append(get_app_data(sys.argv[1], app, False))
			i += 1
		i = 1
		for mal in malware:
			print(str(i) + "/" + str(len(malware)) + " " + mal)
			data.append(get_app_data(sys.argv[1], app, True))
			i += 1
			
		arff.dump(output, data, relation="APK", names=["MALWARE"] + ALL_PERMISSIONS)
