import os
from celery import Celery
import argparse
import sys
sys.path.insert(0,'/data/array_tomography/ForSharmi/allen_SB_code/celery/')
sys.path.insert(0,os.getcwd())
from tasks import run_celerycommand
from renderapi import Render


def get_immediate_subdirs(a_dir):
	return [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir,name))]


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Create xml from stack")
	parser.add_argument('--chunkDirectory', nargs=1, help='Input stack in render', type=str)
	parser.add_argument('--outputDirectory', nargs=1, help='Input stack in render', type=str)
	args = parser.parse_args()

	dirs = get_immediate_subdirs(args.chunkDirectory[0])

	for i in range(0,len(dirs)):
			inchunkdir = args.chunkDirectory[0] + "/" + dirs[i]
			outchunkdir = args.outputDirectory[0]+"/"+dirs[i]
			if not os.path.exists( outchunkdir):
				os.makedirs(outchunkdir)
			if not os.path.isfile(outchunkdir+"/intersection_Affine.xml"):
				cmd = "xvfb-run -a /data/array_tomography/ForSharmi/allen_SB_code/Fiji.app/ImageJ-linux64 -Xms50g -Xmx50g "
				cmd = cmd + " -Dproj=" + inchunkdir + "/project.xml"
				cmd = cmd + " -Doutdir="+ outchunkdir 
				cmd = cmd + " -- --no-splash align3d_affine.bsh >" + outchunkdir + "/logfile"
				if not os.path.isfile(outchunkdir+"/intersection_Affine.xml"):
					print cmd
					os.system(cmd)
					#result = run_celerycommand.apply_async(args=[cmd, os.getcwd()])
			if os.path.isfile(outchunkdir+"/intersection_Affine.xml"):
				print "Now uploading.."				
				os.system("mkdir ../processed/temp")
				strrep = dirs[i]
				strrep = strrep.replace("-","to")
				uploadcmd = "python create_json_from_xml.py "
				uploadcmd = uploadcmd + " --inputfile " + outchunkdir + "/intersection_Affine.xml" 
				uploadcmd = uploadcmd + " --Owner Sharmishtaas --Project M270907_Scnn1aTg2Tdt_13 "
				uploadcmd = uploadcmd + " --outputStack CHUNK1000_"+strrep 
				uploadmcd = uploadcmd + " --outputDir ../processed/temp "
				uploadcmd = uploadcmd + " --inputStack STITCHEDSTACKFINAL_DAPI_1_DAPI_1"
				#uploadcmd = uploadcmd + " --inputStack STITCHEDSTACKFINAL_DROPPED_AND_CORRECTED_DAPI_1"
				print "This is upload command"
				print uploadcmd
				#zvalues = 
				render = Render("ibs-forrestc-ux1.corp.alleninstitute.org", 8080, "Sharmishtaas", "M270907_Scnn1aTg2Tdt_13")
    				zval = render.get_z_values_for_stack("CHUNK1000_"+strrep )
    				print(len(zval))

    				#if (len(zval) ==0):
				os.system(uploadcmd)
				os.system("rm -rf ../processed/temp")

		print "All done!"
