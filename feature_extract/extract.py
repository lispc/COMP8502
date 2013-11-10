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
FILE_EXTENSIONS = ['.tdat', '.peg', '.db', '.pem', '.obj', '.kl', '.ko', '.bitbase', '.ucls', '.conf', u'.bz2', u'.orig', '.dict', '.info-6', '.providers', u'.graph', '.nt', '.lvl', u'.jar', '.raw', '.ptc', '.crt', '.pattern', '.original', '.info', '.alias', '.mpl', u'.opml', '.gui', '.puz', '.ja', u'.xwd', '.lgpl', '.int', '.pspimage', '.ttf', '.t', '.bmp', '.blend', '.js', u'.sample_java', u'.bc', '.cfg', '.java-rendering', u'.plugin', '.php', '.new', '.ics', '.csv', '.css', u'.msg', '.tga', '.otf', '.pdn', '.ico', '.rs', '.pdb', '.pdf', u'.sh', u'.zim', '.in', u'.properties', '.cht', '.kml', '.idl', u'.cpt', u'.jpg', u'.kdbx', '.xml', '.icu', '.atlas', u'.it', '.htm', u'.tbl', '.lua', u'.javafiles', '.proto', '.xspf', '.mtl', '.dey', '.dex', u'.xm', '.pro', '.pzx', '.fb2', '.tmpl', u'.so', '.markdown', '.sf', '.bks', '.act', '.arsc', u'.dtd', '.anki', '.spp', u'.vrt', '.piece_set', '.acal', '.mbm', '.license', '.properties-prod', '.winmasks', u'.lng', '.html', '.tmx', '.apk', u'.wiki', '.adk', '.escaped', '.provider', '.default', u'.po', '.rej', u'.wnin', '.dsa', '.res', u'.vm', u'.owl', '.info-1', '.bak', '.fb', '.gif', '.woff', '.properties-uat', '.aut', u'.mod', '.pub', '.brk', '.jardesc', '.lif', '.info-4', '.0', '.1', '.2', '.info-5', '.xcf', '.xhtml', u'.frg', u'.xsl', '.ctd', '.cow', '.lesser_024', u'.ini', '.arr', '.binary', '.zt1', '.export', '.h', '.manifest', '.jad', '.mesh', '.m', '.ad', '.aj', '.json', '.c', u'.d', '.rle', u'.g', '.wav', '.jav', '.z', '.svgz', '.rsa', u'.hex', u'.txt', '.psd', u'.p', '.out', '.ogg', '.midi', '.oga', '.patch', u'.kdb', '.plist', '.sql', '.fnt', '.mf', '.odt', u'.md', '.gfs', '.ent', u'.mo', u'.static', '.img', u'.afm', '.s3m', '.idx', '.ft2', '.tmp', '.hmb', '.gnaural', '.pgt', '.svg', '.bin', '.jpeg', '.dat', u'.pot', '.mid', '.coffee', u'.props', u'.pgf', u'.zip', '.pvr', '.gcm', '.eof', u'.gpg', u'.sfd', u'.map', '.lesser', u'.sqlite', u'.dic', '.jsm', '.mp3', u'.jso', '.backup', '.eot', '.info-2', '.info-3', '.xsd', '.cur', '.info-7', '.level', '.temp', '.png', '.cfu', '.ser', '.java-e', u'.reginfo', u'.nameservicedescriptor', u'.key', '.lst', '.nrm', u'.example', '.cff', u'.swf', '.nki', '.bbs', '.java', '.mp4'] 

API_CALLS = ["getDeviceId", "getCellLocation", "setFlags", "addFlags", "setDataAndType", "putExtra", "init", "query", "insert", "update", "writeBytes", "write", "append", "indexOf", "substring", "startService", "getFilesDir", "openFileOutput", "getApplicationInfo", "getRunningServices", "getMemoryInfo", "restartPackage", "getInstalledPackages", "sendTextMessage", "getSubscriberId", "getLine1Number", "getSimSerialNumber", "getNetworkOperator", "loadClass", "loadLibrary", "exec", "getNetworkInfo", "getExtraInfo", "getTypeName", "isConnected", "getState", "setWifiEnabled", "getWifiState", "setRequestMethod", "getInputStream", "getOutputStream", "sendMessage", "obtainMessage", "myPid", "killProcess", "readLines", "available", "delete", "exists", "mkdir", "ListFiles", "getBytes", "valueOf", "replaceAll", "schedule", "cancel", "read", "close", "getNextEntry", "closeEntry", "getInstance", "doFinal", "DESKeySpec", "getDocumentElement", "getElementByTagName", "getAttribute" ]

NAMES = ["MALWARE", "APP_NAME"] + ALL_PERMISSIONS + map(lambda x: x[1:].upper(), FILE_EXTENSIONS) + API_CALLS + ["DEXLEN", "PACKLEN", "FILENO", "ACTNO", "SERVICENO", "PROVIDERNO", "CRYPTO", "TELEPHONY", "NET", "DYN_CODE", "NATIVE_CODE", "REFLECTION", "CLASSES", "METHODS", "FIELDS"]


def get_app_data(folder, app_path, malware):
	app, d, dx = AnalyzeAPK(os.path.join(folder, app_path))
	#app = APK(os.path.join(folder, app_path))
	app_perms = set(app.get_permissions())
	data = [malware, app_path]
	for perm in ALL_PERMISSIONS:
		if perm in app_perms:
			data.append(True)
		else:
			data.append(False)
	extcount = dict()
	for f in app.get_files():
		ext = os.path.splitext(f)[1]
		if ext in extcount:
			extcount[ext] += 1
		else:
			extcount[ext] = 1
	for ext in FILE_EXTENSIONS:
		if ext in extcount:
			data.append(extcount[ext])
		else:
			data.append(0)

	for call in API_CALLS:
		data.append(len(dx.tainted_packages.search_methods(".", call, ".")))

	return data + [len(app.get_file("classes.dex")), len(app.get_package()), len(app.get_files()), len(app.get_activities()), len(app.get_services()), len(app.get_providers()), len(dx.tainted_packages.search_crypto_packages()), len(dx.tainted_packages.search_telephony_packages()), len(dx.tainted_packages.search_net_packages()), is_dyn_code(dx), is_native_code(dx), is_reflection_code(dx), len(d.get_classes()), len(d.get_methods()), len(d.get_fields())]

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
			data.append(get_app_data(sys.argv[2], mal, True))
			i += 1
			
		arff.dump(output, data, relation="APK", names=NAMES)
