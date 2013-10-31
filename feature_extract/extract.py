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

from androguard.core.bytecodes.api_permissions import DVM_PERMISSIONS_BY_PERMISSION

ALL_PERMISSIONS = sorted(DVM_PERMISSIONS_BY_PERMISSION.keys())

def get_app_data(app, malware):
	app_perms = set(map(lambda x: x.rsplit('.', 1)[-1], app.get_permissions()))
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
		for app in apps:
			print(app)
			a, d, dx = AnalyzeAPK(os.path.join(sys.argv[1], app))
			data.append(get_app_data(a, False))
		for mal in malware:
			print(mal)
			a, d, dx = AnalyzeAPK(os.path.join(sys.argv[2], mal))
			data.append(get_app_data(a, True))
			
		arff.dump(output, data, relation="APK", names=["MALWARE"] + ALL_PERMISSIONS)
