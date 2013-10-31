#!/usr/bin/env python

import sys
PATH_INSTALL = "../../androguard"

sys.path.append(PATH_INSTALL)

import arff
import androlyze

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

if __name__ == "__main__" :
	if len(sys.argv) < 3:
		print("python extract.py <path-to-apk> <output>")
	else:
		a, d, dx = AnalyzeAPK(sys.argv[1])
		app_perms = set(map(lambda x: x.rsplit('.', 1)[-1], a.get_permissions()))
		data = []
		for perm in ALL_PERMISSIONS:
			if perm in app_perms:
				data.append(True)
			else:
				data.append(False)

		arff.dump(sys.argv[2], [data], relation="APK", names=ALL_PERMISSIONS)
