import os
from celery import Celery
import argparse
import sys
sys.path.insert(0,'/data/array_tomography/ForSharmi/allen_SB_code/celery/')
sys.path.insert(0,os.getcwd())
from tasks import run_celerycommand


def get_immediate_subdirs(a_dir):
	return [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir,name))]

def find_full_dir_name(mystring,mylist):
	print mystring
	print mylist
	print mystring
	if mystring in mylist:
		return mystring
	else:
		print "Something is wrong! Cannot find subdirectory %s in the given input directory!"%mystring


def find_full_dir_name_with_sub(mystring,mylist):
	starts = [n for n, l in enumerate(mylist) if l.startswith(mystring)]
	if len(starts)==1:
		return mylist[starts[0]]
	else:
		print "Something is wrong! Cannot find subdirectory %s in the given input directory!"%mystring
		

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Dechunk me")
	parser.add_argument('--alignedDirectory', nargs=1, help='aligned directory', type=str)
	parser.add_argument('--firstSection',nargs=1,help='First Section',type=int)
	parser.add_argument('--lastSection',nargs=1,help='Last Section',type=int)
	parser.add_argument('--sectionsPerChunk',nargs=1,help='Sections per chunk',type=int)
	parser.add_argument('--overlap',nargs=1,help='Number of Sections that Overlap',type=int)
	
	args = parser.parse_args()
	spc = args.sectionsPerChunk[0]
	fs = args.firstSection[0]
	ls = args.lastSection[0]
	overlap = args.overlap[0]
	sectionsPerChunk = args.sectionsPerChunk[0]
	backupdir = args.alignedDirectory[0]+"_backup"

	dirs = get_immediate_subdirs(args.alignedDirectory[0])

	if not os.path.exists(backupdir):
		os.mkdir(backupdir)

	x = fs
	for i in range(1,len(dirs)):
	#for i in range(1,1):
		str1 = str(x)+"-"
		#if (x+args.overlap[0]) > args.lastSection[0]:
		#else:
		str2 = str(x+args.overlap[0])+"-"
		
		print "Str 1 and 2: "
		print str1
		print str2

		dir1 = find_full_dir_name_with_sub(str1,dirs)
		dir2 = find_full_dir_name_with_sub(str2,dirs)
		
		

		fulldir1 = args.alignedDirectory[0]+ "/"+ dir1
		fulldir2 = args.alignedDirectory[0]+ "/"+ dir2
		cmd = "xvfb-run -a /media/sharmishtaas/local2/home/sharmishtaas/fiji2/Fiji.app/ImageJ-linux64 "
		cmd = cmd + " -Ddir1=" + fulldir1
		cmd = cmd + " -Ddir2="+ fulldir2
		cmd = cmd + " -- --no-splash align-overlapping-projects-pair-manypatches.bsh " 
		#print cmd
		x = x+overlap
		
		#os.system(cmd)
		#exit(0)
		#result = run_celerycommand.apply_async(args=[cmd, os.getcwd()])

		
		backupdir1 = backupdir+"/"+dir1
		backupdir2 = backupdir+"/"+dir2
		if not os.path.exists(backupdir1+"/logfile"):
			if not os.path.exists(backupdir1):
				os.mkdir(backupdir1)
			cmd1 = "cp %s/intersection_Affine.xml %s/intersection_Affine.xml"%(fulldir1,backupdir1) 
			print cmd1
			os.system(cmd1)
			cmd3 = "cp %s/logfile %s/logfile"%(fulldir2,backupdir2) 
                        print cmd3
                        os.system(cmd3)

		print backupdir2+"/logfile"
		if not os.path.exists(backupdir2+"/logfile"):
			if not os.path.exists(backupdir2):
				os.mkdir(backupdir2)
			cmd2 = "cp %s/intersection_Affine.xml %s/intersection_Affine.xml"%(fulldir2,backupdir2) 
			print cmd2
			os.system(cmd2)
			cmd3 = "cp %s/logfile %s/logfile"%(fulldir2,backupdir2) 
                        print cmd3
                        os.system(cmd3)
			
		#os.system(cmd)
	#exit(0)

	cmd = "xvfb-run -a /media/sharmishtaas/local2/home/sharmishtaas/fiji2/Fiji.app/ImageJ-linux64 "
	cmd = cmd + " -Ddir=" + args.alignedDirectory[0]
	cmd = cmd + " -Dstart=" + str(fs) 
	cmd = cmd + " -Dend=" + str(ls) 
	cmd = cmd + " -Doverlap=" + str(overlap)
	cmd = cmd + " -- --no-splash apply-aligned-overlapping-projects_russell.bsh"
	print cmd
	os.system(cmd)

