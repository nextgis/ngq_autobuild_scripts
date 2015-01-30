# -*- coding: utf-8 -*-
import os
import sys
import ConfigParser
import argparse

import tempfile
import subprocess
import shutil

from ftplib import FTP

ngqbuilder_home_dir = os.environ['NGQBUILDER_HOME']
ngqbuilder_builds_dir = os.environ['NGQBUILDER_BUILDS_DIR']

config_filename = os.path.join(ngqbuilder_home_dir, "projects.ini")
if not os.path.exists(config_filename):
	sys.exit("ERROR: NGQ Builder config file (%s) not found"%config_filename)
config = ConfigParser.RawConfigParser()
config.read(config_filename)

def CallExternalApplication(args):
	try:
		res = subprocess.call(args, stdout=sys.stdout)
		if res != 0:
			sys.exit( "ERROR: Patch file (%s) not found"%patch_filename)
			
	except subprocess.CalledProcessError as ex:
		sys.exit( "ERROR: Patch file (%s) not found"%patch_filename)
	
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
	except:
		print "ERROR: GetQGISsrc\n"
		return None	
	
	os.chdir(cwd)
		
	return qgis_src_dir

def GetInstallerProjectSrc(project_src_dir):
	print "=========== \n Get NGQ installer project sources \n==========="
	if not os.path.exists(project_src_dir):
		sys.exit( "ERROR: NGQ installer project dir (%s) not found"%project_src_dir)
		
	cwd = os.getcwd()
	os.chdir(project_src_dir)
	"""
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
			
	except:
		print "ERROR: GetInstallerProjectSrc\n"
		return None	
	"""
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

def Configurating(qgis_src_dir, conf_env_script_filename, conf_qgis_script_filename, install_dirname):
	#print "\t conf_env_script_filename: ", conf_env_script_filename
	#print "\t conf_qgis_script_filename: ", conf_qgis_script_filename

	qgis_build_dir = tempfile.mkdtemp('','qgis_build_')
	
	try:
		res = subprocess.check_call([conf_qgis_script_filename, qgis_build_dir, conf_env_script_filename, qgis_src_dir, install_dirname], stdout=sys.stdout)
	except subprocess.CalledProcessError as ex:
		sys.exit("ERROR! Configuration qgis faild: %s\n"%str(ex))
	except:
		sys.exit("ERROR! Configuration qgis faild: Unexpected error: %s\n"%sys.exc_info()[0])
	
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
	
	qgis_version = qgis_version + ".%d"%nextgis_build_number
	
	return qgis_version
	
def GetVersion(qgis_config_filename):
	import re

	f = open( qgis_config_filename, 'r+')
	lines = f.readlines()
	f.close()

	qgis_version_int = 0
	for line in lines:
		m = re.search('^#define VERSION_INT \d+', line)
		if m is not None:
			m = re.search('\d+',m.group(0))
			if m is not None:
				qgis_version_int = int(m.group(0))
	
	ngq_build_number = 0
	for line in lines:
		m = re.search('^#define NEXTGIS_BUILD_NUMBER \d+', line)
		if m is not None:
			m = re.search('\d+',m.group(0))
			if m is not None:
				ngq_build_number = int(m.group(0))
				
	qgis_version = "%d.%d.%d.%d"%(qgis_version_int/10000, qgis_version_int%10000/100, qgis_version_int%100, ngq_build_number)
	return qgis_version

def Building(conf_env_filname, qgis_build_dir, project_file):
	builder_bat = os.path.join(ngqbuilder_home_dir, "scripts", "builder.bat")
	
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

def MakeInstaller(proj_name, install_dirname, nsis_script, nsis_adapter, version, platform):
	installer_filename = "setup-" + proj_name + "-" + str(version) + "-" + platform + ".exe"
	try:
		res = subprocess.check_call([nsis_adapter, install_dirname, nsis_script, version, installer_filename], stdout=sys.stdout)
	except subprocess.CalledProcessError as ex:
		sys.exit("ERROR! Make installer error: %s\n"%str(ex))
	except:
		sys.exit("ERROR! Make installer error: Unexpected error: %s\n"%sys.exc_info()[0])
	
	return installer_filename

def SendToFTPserevr(filename, ftp_server):
	from ftplib import FTP
	
	config_filename = os.path.join(ngqbuilder_home_dir, "ftp.ini")
	if not os.path.exists(config_filename):
		sys.exit("ERROR: NGQ Builder ftp config file (%s) not found"%config_filename)
	ftp_config = ConfigParser.RawConfigParser()
	ftp_config.read(config_filename)

	try:
		ftp = FTP(ftp_server)
		
		ftp.login(ftp_config.get(ftp_server,'user'), ftp_config.get(ftp_server,'pass'))
		ftp.cwd(ftp_config.get(ftp_server,'rdir'))
		ftp.storbinary("STOR %s"%filename, open(os.path.join(ngqbuilder_builds_dir, filename), 'rb'))
	except:
		sys.exit("ERROR! SendToFTPserevr: Unexpected error: %s\n"%sys.exc_info()[0])
	
parser = argparse.ArgumentParser(description='Script for build NextGIS QGIS')
   
parser.add_argument('-l', '--list', action='store_true', dest='list', help='list of projects')
parser.add_argument('-b', '--build', dest='project', help='project name for build')
parser.add_argument('-i', '--make_installer', dest='installer', help='project name for make_installer')
parser.add_argument('-p', '--platform', dest='platform', help='[x32|x64], default x32')
parser.add_argument('-f', '--ftp', action='store_true', dest='ftp', help='put installer to ftp server')

if len(sys.argv) <= 1:
	parser.print_usage()
	sys.exit(1)

args = parser.parse_args()

if args.list:
	print "Configurated projects:"
	for prj_name in config.sections():
		print "\t %s" %prj_name
		
	sys.exit(0)

platform = "win32"
platform_dir_name = "win32"
if args.platform is not None:
	if args.platform == "x64":
		platform = "win64"
		platform_dir_name = "win64"

if args.project is not None:
	if  args.project not in config.sections():
		msg = "ERROR: Project \"%s\" not found"%args.project
		sys.exit(msg)	
	
	'''
		Getsources
	'''
	print "Get sources..."
	qgis_tag = config.get(args.project,"qgis_tag")
	qgis_src_dir = config.get(args.project,"qgis_src_dir")
	qgis_src_dir = GetQGISsrc(qgis_tag, qgis_src_dir)
	if qgis_src_dir is None:
		sys.exit("ERROR: getting QGIS sources")
	
	'''
		GetProject
	'''
	print "Get project..."
	ngq_proj = config.get(args.project,"ngq_proj")
	project_src_dir = GetInstallerProjectSrc(ngq_proj)
	
	'''
		Patching
	'''
	print "Patching..."
	patch_filename = os.path.join(project_src_dir, config.get(args.project,"patch"))
	addition_files = os.path.join(project_src_dir, config.get(args.project,"addition_files"))
	PatchQGISsrc(qgis_src_dir, patch_filename, addition_files)
	
	'''
		Configurating
	'''
	print "Configurating..."
	conf_env_script_name = config.get(args.project,"build_env")
	conf_qgis_script_name = config.get(args.project,"configure_qgis")
	
	conf_env_script_filename =  os.path.join(ngqbuilder_home_dir, "scripts", platform_dir_name, "env", conf_env_script_name)
	conf_qgis_script_filename =  os.path.join(ngqbuilder_home_dir, "scripts", platform_dir_name, "configuration", conf_qgis_script_name)
	
	install_dirname = os.path.join(ngqbuilder_builds_dir, args.project, platform_dir_name)
	
	qgis_build_dir = Configurating(qgis_src_dir, conf_env_script_filename, conf_qgis_script_filename, install_dirname)

	build_number = int( config.get(args.project,"build_number") ) + 1
	AddBuildVersionInQGISconfig( os.path.join(qgis_build_dir, "qgsconfig.h"), build_number)
	
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
	
	res = Building(conf_env_script_filename, qgis_build_dir, project_file)
	if res == False:
		sys.exit("ERROR: NSIS error")
	
	'''
		Save build number
	'''
	config.set(args.project, "build_number", build_number)
	
	with open(config_filename, 'wb') as configfile:
		config.write(configfile)

	'''
		Remove tmp files
	'''
	shutil.rmtree(qgis_build_dir)
	
if args.installer is not None:	
	'''
		Make installer
	'''
	print "Make installer..."
	ngq_proj = config.get(args.installer,"ngq_proj")
	project_src_dir = GetInstallerProjectSrc(ngq_proj)
	
	nsis_script =  os.path.join(project_src_dir, config.get(args.installer,"nsis"))
	nsis_adapter =  os.path.join(ngqbuilder_home_dir, "scripts", platform_dir_name , "nsis", config.get(args.installer,"nsis_adapter"))
	
	if not os.path.exists(nsis_script):
		msg = "ERROR: NSIS script (%s) not found in project directory (%s)"%(nsis_script, project_src_dir)
		sys.exit(msg)
	if not os.path.exists(nsis_adapter):
		msg = "ERROR: NSIS adapter (%s) not found"%(nsis_adapter)
		sys.exit(msg)
	
	install_dirname = os.path.join(ngqbuilder_builds_dir, args.installer, platform_dir_name)
	
	nextgisqgis_version = GetVersion(os.path.join(os.path.join(install_dirname, "include"), "qgsconfig.h" ))
	
	installer_filename = MakeInstaller(args.installer, install_dirname, nsis_script, nsis_adapter, nextgisqgis_version, platform)
	
	if installer_filename is None:
		sys.exit("ERROR: NSIS error")
	
	if args.ftp:
		'''
			Put by FTP 
		'''
		print "Put by FTP"
		SendToFTPserevr(installer_filename, config.get(args.installer, "fpt_server"))