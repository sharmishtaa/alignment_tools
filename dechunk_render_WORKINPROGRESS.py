import os
from renderapi import Render


def intersect(a,b):
	return list(set(a) & set(b))

if __name__=='__main__':
	parser = argparse.ArgumentParser(description="Dechunk directly from render stacks")
	parser.add_argument('--chunk1', nargs='1', help='Chunk 1', type=str)
	parser.add_argument('--chunk2', nargs='1', help='Chunk 2', type=str)
	p.add_argument('--Owner',          help="name of project owner to read project from",default = "Forrest")
   	p.add_argument('--Project',        help="name of the input Project")
    	p.add_argument('--outputDir',           help="name of the output directory", default='.')
    	p.add_argument('--host',                help="host name of the render server",default="ibs-forrestc-ux1.corp.alleninstitute.org")
    	p.add_argument('--port',                help="port for render server",default=8080)
    	p.add_argument('--java_home',           help="directory for java jdk",default='/pipeline/renderdev/deploy/jdk1.8.0_73')
	a = p.parse_args()
	
	render = Render(a.host, a.port, a.Owner, a.Project)

	z1 = render.get_z_values_for_stack(a.chunk1)
	z2 = render.get_z_values_for_stack(a.chunk2)
	z = intersect(z1,z2)

	
	
