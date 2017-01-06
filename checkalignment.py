import os
import argparse

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

	parser = argparse.ArgumentParser(description="Check Alignment")
        parser.add_argument('--alignedDirectory', nargs=1, help='aligned directory', type=str)
        args = parser.parse_args()

	rootdir = args.alignedDirectory[0]
	dirs = get_immediate_subdirs(rootdir)

	numoferrors = 0

	for inputdirectory in dirs:
		arr = inputdirectory.rsplit("-")
		num1 = int(arr[0])
		num2 = int(arr[1])

		for x in range(num1, num2):
	        	cmd = "grep z=" + str(x) +  " " + rootdir + "/"+ inputdirectory + "/logfile > test"
			#print cmd
			os.system(cmd)
			with open("test") as f:
				content = f.readlines()
			for i in content:
				linearr = i.rsplit("displacement")
				if len(linearr)==1:
					#print "Empty"
					a = 1
				else:
					#print linearr[1]
					strarr = linearr[1].split()
					#print strarr[1]
					numarr = strarr[1].rsplit("px")
					value = float(numarr[0])
					if value > 100:
						print cmd
						print i
						numoferrors = numoferrors + 1

	numoferrorsections = numoferrors /2
	print "Number of problem sections: %d"%numoferrorsections
