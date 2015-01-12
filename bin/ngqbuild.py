# -*- coding: utf-8 -*-
import os
import sys
import ConfigParser
import argparse

import tempfile
import subprocess
import shutil

ngqbuilder_home_dir = os.environ['NGQBUILDER_HOME']
ngqbuilder_builds_dir = os.environ['NGQBUILDER_BUILDS_DIR']

config_filename = os.path.join(ngqbuilder_home_dir, "config.ini")
if not os.path.exists(config_filename):
	print "ERROR: NGQ Builder config file (%s) not found"%config_filename
	sys.exit()
config = ConfigParser.RawConfigParser()
config.read(config_filename)

def GetQGISsrc(tag_name, qgis_src_dir):
	print "=========== \n Get QGIS sources \n tag: %s \n==========="% tag_name
	
	if not os.path.exists(qgis_src_dir):
		sys.exit( "ERROR: QGIS sources dir (%s) not found"%qgis_src_dir)
		
	cwd = os.getcwd()
	os.chdir(qgis_src_dir)
	
	try:
		cmd = "git checkout ."
		print "%s\n"%cmd
		r = subprocess.call(cmd, stdout=sys.stdout)
		if r != 0:
			print "ERROR: %s\n"% cmd
			return None
		
		cmd = "git clean -df"
		print "%s\n"% cmd
		r = subprocess.call(cmd, stdout=sys.stdout)
		if r != 0:
			print "ERROR: %s\n"% cmd
			return None
		
		cmd = "git checkout master"
		print "%s\n"% cmd
		r = subprocess.call(cmd, stdout=sys.stdout)
		if r != 0:
			print "ERROR: %s\n"% cmd
			return None
		
		cmd = "git pull"
		print "%s\n"% cmd
		r = subprocess.call(cmd, stdout=sys.stdout)
		if r != 0:
			print "ERROR: %s\n"% cmd
			return None
		
		cmd = "git checkout %s"%tag_name
		print "%s\n"% cmd
		r = subprocess.call(cmd, stdout=sys.stdout)
		if r != 0:
			print "ERROR: %s\n"%cmd
			return None
			
	except e:
		print "ERROR: %s\n" % str(e)
		return None	
	
	os.chdir(cwd)
		
	return qgis_src_dir
		

def GetInstallerProjectSrc(project_src_dir):
	print "=========== \n Get NGQ installer project sources \n==========="
	if not os.path.exists(project_src_dir):
		sys.exit( "ERROR: NGQ installer project dir (%s) not found"%project_src_dir)
		
	cwd = os.getcwd()
	os.chdir(project_src_dir)
	
	try:
		cmd = "git checkout ."
		print "%s\n"%cmd
		r = subprocess.call(cmd, stdout=sys.stdout)
		if r != 0:
			print "ERROR: %s\n"% cmd
			return None
		
		cmd = "git clean -df"
		print "%s\n"% cmd
		r = subprocess.call(cmd, stdout=sys.stdout)
		if r != 0:
			print "ERROR: %s\n"% cmd
			return None
		
		cmd = "git checkout master"
		print "%s\n"% cmd
		r = subprocess.call(cmd, stdout=sys.stdout)
		if r != 0:
			print "ERROR: %s\n"% cmd
			return None
		
		cmd = "git pull"
		print "%s\n"% cmd
		r = subprocess.call(cmd, stdout=sys.stdout)
		if r != 0:
			print "ERROR: %s\n"% cmd
			return None
			
	except e:
		print "ERROR: %s\n" % str(e)
		return None	
	
	os.chdir(cwd)
		
	return project_src_dir

def PatchQGISsrc(qgis_src_dir, patch_filename, addition_files):
	if not os.path.exists(patch_filename):
		sys.exit( "ERROR: Patch file (%s) not found"%patch_filename)
	
	cmd = "git apply --ignore-whitespace  --directory \"%(qgis_src_dir)s\" \"%(patch)s\" " % {
		"qgis_src_dir": qgis_src_dir,
		"patch": patch_filename
	}
	
	try:
		subprocess.call(cmd, stdout=sys.stdout)
	except:
		print "ERROR: Patching QGIS sources faild. cmd:\n", cmd
		
	for root, dirs, files in os.walk(addition_files):
		src_dir = root
		dst_dir = root.replace(addition_files, qgis_src_dir)
		for file in files:
			shutil.copyfile(os.path.join(src_dir, file), os.path.join(dst_dir, file))

def Configurating(qgis_src_dir, conf_env_filname, conf_qgis_filename, conf_qgis_adapter, install_dirname):
	qgis_build_dir = tempfile.mkdtemp('','qgis_build_')
	
	cmd = "%(conf_qgis_adapter)s %(qgis_build_dir)s %(conf_env_filname)s %(conf_qgis_filename)s %(qgis_src_dir)s %(install_dirname)s" % {
		"conf_qgis_adapter": conf_qgis_adapter,
		"qgis_build_dir": qgis_build_dir,
		"conf_env_filname": conf_env_filname,
		"conf_qgis_filename": conf_qgis_filename,
		"qgis_src_dir": qgis_src_dir,
		"install_dirname": install_dirname
	}
	
	try:
		print "cmd: ", cmd
		subprocess.call(cmd, stdout=sys.stdout)
	except:
		print "ERROR: Configuration QGIS faild (%s). cmd:\n"%qgis_build_dir, cmd
	
	return qgis_build_dir

def AddBuildVersionInQGISconfig(qgis_config_filename, nextgis_build_number):
	import re
	qgis_version = None

	f = open( qgis_config_filename, 'r+')
	lines = f.readlines()
	f.close()

	new_lines = []
	for line in lines:
		new_lines.append(line)
		m = re.search('^#define VERSION_INT \d+', line)
		if m is not None:
			m = re.search('\d+',m.group(0))
			if m is not None:
				qgis_version = m.group(0)
				new_lines.append('#define NEXTGIS_BUILD_NUMBER %d\n'%nextgis_build_number)
				
	f = open( qgis_config_filename, 'w+')
	f.writelines(new_lines)
	f.close()
	
	return qgis_version

def Building(conf_env_filname, qgis_build_dir, project_file):
	builder_bat = os.path.join(ngqbuilder_home_dir, "builder.bat")
	
	cmd = "%(builder_bat)s %(qgis_build_dir)s %(conf_env_filname)s %(project_file)s" % {
		"builder_bat": builder_bat,
		"qgis_build_dir": qgis_build_dir,
		"conf_env_filname": conf_env_filname,
		"project_file": project_file
	}
	
	try:
		print "cmd: ", cmd
		res = subprocess.call(cmd, stdout=sys.stdout)
	except:
		print "ERROR: Building QGIS faild (%s). cmd:\n"%qgis_build_dir, cmd
		return False
	
	if res == 0:
		return True
	else:
		return False

def MakeInstaller(install_dirname, nsis_script, nsis_adapter, qgis_version):
	cmd = "%(nsis_adapter)s %(install_dirname)s %(nsis_script)s %(qgis_version)s" % {
		"nsis_adapter": nsis_adapter,
		"install_dirname": install_dirname,
		"nsis_script": nsis_script,
		"qgis_version": qgis_version
	}
	
	try:
		print "cmd: ", cmd
		res = subprocess.call(cmd, stdout=sys.stdout)
		
	except:
		print "ERROR: Make installer. cmd:\n"% cmd
		return False
	
	if res == 0:
		return True
	else:
		return False
"""
def SendToFTPserevr():
	from ftplib import FTP
	ftp = FTP('ftp.nextgis.ru')
	ftp = FTP('nextgis.ru')
	ftp.login('lisovenko', 'jux2Xak2')
	ftp.cwd('qgis')
	ftp.storbinary("STOR qgis-install.exe", open("d:\\builds\\NextGIS_QGIS_Compulink_0.0.5.exe", 'rb'))
"""
	
parser = argparse.ArgumentParser(description='Script for build NextGIS QGIS')
   
parser.add_argument('-l', '--list', action='store_true', dest='list', help='list of projects')
parser.add_argument('-b', '--build', dest='project', help='project name for build')

if len(sys.argv) <= 1:
	parser.print_usage()
	sys.exit()

args = parser.parse_args()
print "args.list: ", args.list
print "args.project: ", args.project

if args.list:
	print "Configurated projects:"
	for prj_name in config.sections():
		print "\t %s" %prj_name
		
	sys.exit()

if args.project is not None:
	if  args.project not in config.sections():
		msg = "ERROR: Project \"%s\" not found"%args.project
		sys.exit(msg)
	
	'''
		Getsources
	'''
	print "Get sources..."
	qgis_src_dir = GetQGISsrc(config.get(args.project,"qgis_tag"), config.get(args.project,"qgis_src_dir"))
	
	if qgis_src_dir is None:
		sys.exit("ERROR: getting QGIS sources")
		
	print "getQGISsrc: ",qgis_src_dir
	
	'''
		GetProject
	'''
	print "Get project..."
	project_src_dir = GetInstallerProjectSrc(config.get(args.project,"ngq_proj"))
	
	'''
		Patching
	'''
	#patching
	patch_filename = os.path.join(project_src_dir, config.get(args.project,"patch"))
	addition_files = os.path.join(project_src_dir, config.get(args.project,"addition_files"))
	print "Patching..."
	PatchQGISsrc(qgis_src_dir, patch_filename, addition_files)
	
	'''
		Configurating
	'''
	print "Configurating..."
	conf_env_filname =  os.path.join(ngqbuilder_home_dir, config.get(args.project,"build_env"))
	conf_qgis_filename =  os.path.join(project_src_dir, config.get(args.project,"configure_qgis"))
	
	conf_qgis_adapters_dir = os.path.join(ngqbuilder_home_dir, "configuration")
	conf_qgis_adapter =  os.path.join(conf_qgis_adapters_dir, config.get(args.project,"configure_qgis_adapter"))
	
	install_dirname = os.path.join(ngqbuilder_builds_dir, args.project)
	
	qgis_build_dir = Configurating(qgis_src_dir, conf_env_filname, conf_qgis_filename, conf_qgis_adapter, install_dirname)
	#qgis_build_dir = os.path.normpath("E:\\temp\\qgis_build_pqdvwd")

	build_number = int( config.get(args.project,"build_number") ) + 1
	qgis_version = AddBuildVersionInQGISconfig( os.path.join(qgis_build_dir, "qgsconfig.h"), build_number)
	qgis_version = str(qgis_version) + "." + str(build_number)
	#qgis_version = 12345567
	
	'''
		Building
	'''
	print "Building..."
	project_file = None
	for file in os.listdir(qgis_build_dir):
		if file.endswith(".sln"):
			project_file = file
    
	if project_file is None:
		sys.exit("ERROR: MS project not found in directory: %s"%qgis_build_dir)
		
	print "\tFound project: ", project_file
	
	res = Building(conf_env_filname, qgis_build_dir, project_file)
	if res == False:
		sys.exit("ERROR: NSIS error")
	
	config.set(args.project, "build_number", build_number)
	
	with open(config_filename, 'wb') as configfile:
		config.write(configfile)
		
	'''
		Make installer
	'''
	print "Make installer..."
	nsis_script =  os.path.join(project_src_dir, config.get(args.project,"nsis"))
	nsis_adapters_dir = os.path.join(ngqbuilder_home_dir, "nsis")
	nsis_adapter =  os.path.join(nsis_adapters_dir, config.get(args.project,"nsis_adapter"))
	
	if not os.path.exists(nsis_script):
		msg = "ERROR: NSIS script (%s) not found in project directory (%s)"%(nsis_script, project_src_dir)
		sys.exit(msg)
	if not os.path.exists(nsis_adapter):
		msg = "ERROR: NSIS adapter (%s) not found"%(nsis_adapter)
		sys.exit(msg)
	
	res = MakeInstaller(install_dirname, nsis_script, nsis_adapter, qgis_version)
	
	if res == False:
		sys.exit("ERROR: NSIS error")
		
	shutil.rmtree(qgis_build_dir)