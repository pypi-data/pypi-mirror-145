"""
This module contains helper functions to analyze fear conditioning videos

@authors: Gergo Turi gt2253@cumc.columbia.edu"""

from os.path import join, basename
import struct
import subprocess
import time
from glob import glob

def ffii_locator(folder_path):
	""""
	finds FreezFrame (*.ffii) files within a folder

	Parameters:
	===========
	folder_path: str
		path like string where .ffii files are located

	Returns:
	========
	ffii_files: list
		list of .ffii files
	"""

	ffii_files  = []
	for name in glob(folder_path+'*.ffii'):
		ffii_files.append(name)
	return ffii_files

def ffii_converter(file_name, fps=4):
	"""
	converts Freezframe raw ffii binaries to .avi file. The output file
	will be located where the input was.

	Parameters:
	===========
	file_name = str
		path to a sigle file to process 
	fps = int or float
		the framerate the raw file will be converted with. 

	Return:
	=======
	Doesn't return anything. Writes the .ffii as avi.
	Note: could be used to save other types of videos as well by
	changing the extension in `of`.
	"""
  
	print(f'Converting {file_name}')

	#output file
	of = file_name[:-5]+'.avi'

	f = open(file_name,'rb')
	m = f.read(8)
	height, width= struct.unpack(">2I", m)
	rate = str(fps)

	cmdstr = ('ffmpeg', '-y', '-r', rate,\
	                    '-f', 'rawvideo',
	                    '-pix_fmt', 'gray',
	                    '-s', str(width)+"x"+str(height),
	                    '-i', '-',
	                    str(of))

	p = subprocess.Popen(cmdstr, stdin=subprocess.PIPE, shell=False)

	while True:
		img = f.read(width*height)
		p.stdin.write(img)
		m = f.read(8)
		if not m:
			break
		height, width = struct.unpack(">2I", m)

	print(f'File saved as {of}')
	f.close()              
	p.kill()


def ffii_counter(file_name):
	"""
	counts the number of frames in a raw Freezframe .ffii file.

	Parameters:
	===========
	file_name = str
		path to a sigle file to process 

	Returns:
	========
	frames: int
		number of frames
	"""
	frames = 0

	print(f'Counting frames in {file_name}')

	f = open(file_name,'rb')
	m = f.read(8)
	height, width= struct.unpack(">2I", m)

	while True:
		img = f.read(width*height)
		frames += 1
		m = f.read(8)
		if not m:
			break
	
	print(f'Number of frames: {frames}')
	                      
	f.close()

	return frames
