# -*- coding: utf-8 -*-
import os
import sys 

osgeo4w_local_dir = sys.argv[1]

for (path, dirs, files) in os.walk(osgeo4w_local_dir):
	print path, ">> ", dirs