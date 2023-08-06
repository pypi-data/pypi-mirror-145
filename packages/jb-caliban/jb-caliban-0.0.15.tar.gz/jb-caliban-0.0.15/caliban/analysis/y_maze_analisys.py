"""
This module contains helper functions to analyze Y maza data

@authors: Gergo Turi gt2253@cumc.columbia.edu, Tingyi Lu tl3025@columbia.edu
"""
import os
import copy
import numpy as np
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.path as mplPath
from itertools import groupby
import matplotlib.patches as patches
import cv2
from google.colab.patches import cv2_imshow

def error_counter(data):
	"""
	Calculates the number of incorrect alternations

	Parameters:
	==========
	data : str
		the sequence of arm alternations.

	Return:
	=======
	errors: int
		number of alternation errors
	"""

	entries = list(data)
	# need to get rid of the first entries
	shortened_entries = entries[2:]
	errors = 0
	for i, letter in enumerate(shortened_entries):
		if shortened_entries[i] == (entries[i] or entries[i+1]):
			errors+=1
		
	return errors

def performance(data, errors):
	"""
	Calculates the Y maze performance of a mouse

	Parameters:
	===========
	data : str
		a single sequence of arm alternations.
	errors : int
		number of incorrect choices

	Return:
	=======
	performnce : float
	"""

	total_entries = len(list(data))
	potential_alternations = total_entries-2
	correct_choices = potential_alternations - errors
	performance = correct_choices / potential_alternations
	return performance

def plot_rois(rois, frame_file):
	'''
	Plots & marks ROIs that overlay the extracted frame from Y maze videos. Currently only works on Y mazes.
	
	Parameters:
	===========
	rois: nested list
		list of all ROIs; each sublist contains name of the ROI and the coodinates of its vertices
	frame_file: str
		a string that contains the directory of the extracted frame from the video being analyzed.
	
	Return:
	=======
	Returns nothing but the function outputs a plot.
	'''
	fig, ax = plt.subplots()
	for roi in rois:
		verts = np.array(roi[1])
		verts = np.append(verts, [verts[0]], axis=0)
		codes = [mplPath.Path.MOVETO, mplPath.Path.LINETO, mplPath.Path.LINETO,
		     mplPath.Path.LINETO, mplPath.Path.CLOSEPOLY]
		path = mplPath.Path(verts, codes) 
		patch = patches.PathPatch(path, facecolor=(1,1,1,0.5), lw=1, label=rois[0])
		ax.add_patch(patch)
		x = (verts[1][0]+verts[3][0])/2
		y = (verts[1][1]+verts[3][1])/2

		#Modify here for different font styles
		font = {'family' : 'sans',
		  'weight' : 'bold',
		  'size'   : 15,
		  'color': 'red'}
		plt.text(x, y, roi[0], **font)

	pic = cv2.imread(frame_file)
	plt.imshow(pic)
	ax.set_xlim(0, pic.shape[1])
	ax.set_ylim(0, pic.shape[0])
	ax.set_axis_off()
	plt.show()

def if_inside(roi, nose, tail_base):
	'''
	Checks whether the mouse is inside an ROI based on the coordinates of its nose tip and tail base.

	Parameters:
	===========
	roi: list of tuples
		the coordinates of all vertices of an ROI
	nose: tuple
		the coordinates of the nose of the mouse
	tail_base: tuple
		coordinates of the tail base of the mouse

	Return:
	=======
	inside: boolean
		True if the nose and tail_base are both inside the given ROI, False if otherwise
	'''
	inside=False

	roi = np.append(roi, [roi[0]], axis=0)
	poly_path = mplPath.Path(np.array(roi))
	nose = poly_path.contains_point(nose)
	tb = poly_path.contains_point(tail_base)

	if (nose==True) & (tb==True):
		inside=True

	return inside
	
def tracking_preprocess(tracking_data, likelihood_cutoff=0.8):
	'''
	Preprocesses the tracking data frame (contains coodinates of body parts of a mouse for every frame), drop unlikely data, and combine x, y coodinates

	Parameters:
	===========
	tracking_data: pandas data frame
		data frame of raw tracking data
	likelihood_cutoff: float
		default 0.8, threshold of likelihood, remove data points that have likelihood less than 0.8

	Return:
	=======
	df2: pandas data frame
		data frame of coordinates of nose and tail base to be used for processing arm entry later; each column contains coordinates in form of tuples
	'''
	df = tracking_data.copy()
	for part in df.columns.levels[0]:
		df_part = df[part]
		df = df.drop(df_part[df_part.likelihood < likelihood_cutoff].index)

	nose = df.loc[:, 'nose_tip']
	tb = df.loc[:, 'tail_base']

	nose_coord = [(x, y) for x, y in zip(nose.x, nose.y)]
	tb_coord = [(x, y) for x, y in zip(tb.x, tb.y)] 

	df2 = pd.DataFrame({'nose':nose_coord, 'tail_base':tb_coord})

	return df2

def generate_entry_sequence(df_body_coords, rois):
	'''
	generates the entry sequence of the mouse and grouped by three for better visibility

	Parameters:
	===========
	df_body_coords: pandas dataframe
	dataframe of nose and tail base coordinates generated from tracking_preprocess, obtained from function tracking_preprocess
	rois: nested list
	list of all ROIs; each sublist contains name of the ROI and the coodinates of its vertices

	Returns:
	========
	result_str: str
	the resulting arm entry sequence of the mouse, does not get rid of the first entry!
	'''
	df3 = pd.DataFrame()
	for arm in rois:
		df3[arm[0][-1]] = df_body_coords.apply(lambda x: if_inside(arm[1], x['nose'], x['tail_base']), axis=1)
	df4 = df3.stack().reset_index().drop(columns='level_0')
	df4.columns=['arm', 'is_in']
	df4 = df4.drop(df4[df4.is_in==False].index)
	result_seq = [x[0] for x in groupby(df4.arm.tolist())]

	result_str = (''.join([x for x in result_seq]))
	result_str = ' '.join([result_str[i:i+3] for i in range(0, len(result_str), 3)])

	return result_str
