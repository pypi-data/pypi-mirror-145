"""
This module contains helper functions to analyze Object tests, 
such as object location and novel object recognition 

@authors: Ayush Sinha -- as6430@columbia.edu;  Gergo Turi -- gt2253@cumc.columbia.edu
"""

def roi_analysis(rois,tracking_file_path,DLCscorer,bpt):
	
    """finding time spent by mouse in the traning dataset

    Parameters:
    ===========
    rois: 
    tracking_file_path: str
    a path string to the location of tracking
    DLCscorer: 
    bpt: str
    a body part which can be found in the DLC dataframe

    Returns:
    ========
    res: 

    """
    
    Dataframe = pd.read_hdf(tracking_file_path)
    
    #Filtering (check threshold)
    #DLCscorer = 'DLC_resnet50_OIT_OLTAug8shuffle1_1030000'
    #bpt='nose'
    
    #setting likelihood to 95% for confident locations.
    Dataframe = Dataframe[Dataframe[DLCscorer][bpt]['likelihood'] > 0.95]
    
    position = namedtuple('position', ['topleft', 'bottomright'])
    rois = {'Arena': position(rois[0][1][0],rois[0][1][2]),
            'Object1': position(rois[1][1][0],rois[1][1][2]),
            'Object2': position(rois[2][1][0],rois[2][1][2])} 

    xnose=Dataframe[DLCscorer][bpt]['x'].values
    ynose=Dataframe[DLCscorer][bpt]['y'].values
    
    bp_tracking = np.array((xnose,ynose))
    
    #assuming an FPS of 16
    fps = du.get_fps(vid_path)
    res = tr.get_timeinrois_stats(bp_tracking.T, rois, 16, False, False)
    
    return res