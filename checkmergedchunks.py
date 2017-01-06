import os
import argparse
import sys

def get_immediate_subdirs(a_dir):
	return [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir,name))]

def find_full_dir_name_with_sub(mystring,mylist):
	starts = [n for n, l in enumerate(mylist) if l.startswith(mystring)]
	if len(starts)==1:
		return mylist[starts[0]]
	else:
		print "Something is wrong! Cannot find subdirectory %s in the given input directory!"%mystring
		

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Create xml from stack")
	parser.add_argument('--chunkDirectory', nargs=1, help='Input stack in render', type=str)
	parser.add_argument('--outputStack', nargs=1, help='Input stack in render', type=str)
	parser.add_argument('--firstSection',nargs=1,help='First Section',type=int)
	parser.add_argument('--lastSection',nargs=1,help='Last Section',type=int)
	parser.add_argument('--sectionsPerChunk',nargs=1,help='Sections per chunk',type=int)

	args = parser.parse_args()
	spc = args.sectionsPerChunk[0]
	dirs = get_immediate_subdirs(args.chunkDirectory[0])

	print dirs
	x = args.firstSection[0]
	while x < args.lastSection[0]:
		os.system("mkdir ../processed/aligned_tilespec")
		str1 = str(x)+"-"
		dir1 = find_full_dir_name_with_sub(str1,dirs)
		chunkdir = args.chunkDirectory[0] + "/" + dir1

		print "This is chunkdir : %s"%chunkdir

		uploadcmd = "python create_json_from_xml.py "
		uploadcmd = uploadcmd + " --inputfile " + chunkdir + "/intersection_Affine.xml" 
		uploadcmd = uploadcmd + " --Owner Sharmishtaas --Project M270907_Scnn1aTg2Tdt_13 "
		uploadcmd = uploadcmd + " --outputStack " + args.outputStack[0]
		uploadcmd = uploadcmd + " --outputDir ../processed/aligned_tilespec "
		uploadcmd = uploadcmd + " --inputStack STITCHEDSTACKFINAL_DROPPED_AND_CORRECTED_DAPI_1"
		print "This is upload command"
		print uploadcmd
		os.system(uploadcmd)
		x = x+spc

		#os.system("rm -rf ../processed/aligned_tilespec")

	print "All done!"
