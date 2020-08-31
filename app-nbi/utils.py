# -*- coding: utf-8 -*-
import os
import errno

def createfolder(path_):
	if not os.path.exists(os.path.dirname(path_)):
		try:
			os.makedirs(os.path.dirname(path_))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
