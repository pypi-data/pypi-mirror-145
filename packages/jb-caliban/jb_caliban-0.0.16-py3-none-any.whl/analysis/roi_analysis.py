import numpy as np
import pandas as pd
import os
import pickle
import sys
import tables
from scipy.spatial import distance
import warnings
import time_in_rois as tr
from collections import namedtuple

def roi_analysis(rois,tracking_file_path):
    #currently finding time spent by mouse in the traning dataset
    
    Dataframe = pd.read_hdf(tracking_file_path)
    
    #Filtering (check threshold)
    DLCscorer = 'DLC_resnet50_OIT_OLTAug8shuffle1_1030000'
    bpt='nose'

    Dataframe = Dataframe[Dataframe[DLCscorer][bpt]['likelihood'] > 0.95]
    
    position = namedtuple('position', ['topleft', 'bottomright'])
    rois = {'Arena': position(rois[0][1][0],rois[0][1][2]),
            'Object1_Day1': position(rois[1][1][0],rois[1][1][2]),
            'Object2_Day1': position(rois[2][1][0],rois[2][1][2])} 
            
    xnose=Dataframe[DLCscorer][bpt]['x'].values
    ynose=Dataframe[DLCscorer][bpt]['y'].values
    
    bp_tracking = np.array((xnose,ynose))
    res = tr.get_timeinrois_stats(bp_tracking.T, rois, 10, False, False)
    
    return res