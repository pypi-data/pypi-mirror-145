import math
import pandas as pd
import analysis.analysis_utils as au
import copy

def pair(x, y):
    z = (((x + y + 1) * (x + y)) / 2) + y
    return z

def invert(z):
    w = math.floor(((math.sqrt(8*z + 1) - 1) / 2))
    t = (w**2 + w) / 2
    y = z - t
    x = w - y
    return x, y

def apply_cantor_pairing(x_coords, y_coords):
    """Reduce dimensionality from 2d to 1d.

    Args:
        x_coords: list

        y:coords: list

    Returns:
        z_coords: list
    """
    if len(x_coords) != len(y_coords):
        raise ValueError("The length of x_coords must equal the length of y_coords!")

    z_coords = []
    for x, y in zip(x_coords, y_coords):
        z = pair(x, y)
        z_coords.append(z)

    return z_coords


def bin_cantor_spatial(mouse, bin_size=5):
    """
    Bins the x and y coordinates, and transforms the new x,y cords to z, to be used for 
    spatial information computations

    Inputs
        mouse: Mouse object
        bin_size: bin size, in cm. Default is 5
        
    Returns:
        x_coords: Series, binned x coordinates
        y_coords: Series, binned y coordinates
        z_coords: Series, unique labels for (x,y) bins
    """
   
    # Extract the X and Y coordinate column vectors
    x_coords = mouse.spikes_and_beh["X_center"].astype(float)
    y_coords = mouse.spikes_and_beh["Y_center"].astype(float)

    # Subtract the mean value of the coordinate to ensure that the binning centers around
    # the main track
    x_coords -= x_coords.mean() 
    y_coords -= y_coords.mean()

    ## Bin X and Y coordinates by bin_factor (ie bin_factor=5 -> 5cm x 5cm bins)
    bin_factor=bin_size
    x_coords = (x_coords/bin_factor).astype(int)
    y_coords = (y_coords/bin_factor).astype(int)


    # Shift all coordinate values by increasing all of them by the minimum value. This
    # is necessary in order to apply the cantor pairing function, since the cantor 
    # pairing function is only defined on the natural numbers, i.e., {0, 1, 2, 3, ...}.
    x_coords += abs(x_coords.min())
    y_coords += abs(y_coords.min())

    #plt.scatter(x_coords,y_coords)
    
    # Reduce the dimensionality of the coordinates, since sklearn's mutual information 
    # function only allows you to compute the MI between two arrays.
    z_coords = apply_cantor_pairing(x_coords.tolist(), y_coords.tolist())
    z_coords = pd.Series(data=z_coords)
    
    return x_coords,y_coords,z_coords

def modify_mouse(mouse, spatial_bin, min_time):
    """
    Modifies a mouse object so that it is ready for spatial/place cell analysis.
    Specifically, immobile times bins are removed, the spatial positions are 
    binned, and spatial bins with low occupancy are removed. The return from this function
    is a mouse object that can be used to compute spatial information, and plot
    spatial heatmaps using functions in the visualize module.
    
    Inputs:
        mouse: Mouse object
            The mouse object to be modified
        spatial_bin: int
            Size of the spatial bins, in cm
        min_time: int
            The minimum number of frames that a mouse can occupy a spatial bin
    
    """
    
    mobile_mouse = remove_immobile(mouse)
    #mobile_mouse = copy.deepcopy(mouse)
    x,y,z = bin_cantor_spatial(mobile_mouse, bin_size = spatial_bin)    
    modified_mouse = remove_low_occupancy(mobile_mouse, x, y, min_occupancy=min_time)    
    
    return modified_mouse

def remove_immobile(mouse):
    """
    Removes immobile time bins from mouse. Assumes that mouse.behavior has an "immobile" column.
    Intended to be used as a helper function for modify_mouse
    
    Inputs:
        mouse: Mouse object
    
    Return:
        Mouse object with immobile time bins removed
    """
    
    
    mobile_S = mouse.spikes.loc[mouse.behavior.immobile == 0]
    mobile_beh = mouse.behavior[mouse.behavior.immobile == 0]
    mobile_C = mouse.cell_transients.loc[mouse.behavior.immobile == 0]
    mobile_raw = mouse.raw.loc[mouse.behavior.immobile == 0]
    mobile_sb = mouse.spikes_and_beh[mouse.behavior.immobile == 0]
    #mobile_sb = mobile_S.join(mobile_beh,how='left')
    
    new_mouse = copy.deepcopy(mouse)
    new_mouse.spikes = mobile_S
    new_mouse.behavior = mobile_beh
    new_mouse.cell_transients = mobile_C
    new_mouse.spikes_and_beh = mobile_sb
    new_mouse.raw = mobile_raw
    
    return new_mouse

def remove_low_occupancy(mouse, x_bin, y_bin, min_occupancy = 1):
    """
    Removes spatial bins that were not visited much. 
    Intended to be used as a helper function for modify_mouse

    
    Inputs:
        mouse: Mouse object upon which to modify
        x_bin: Series of binned x coordinates
        y_bin: Series of binned y coordinates
        min_occupancy: minimum number of time bins for a spatial bin to be included
        
    Returns:
        Mouse object with low-occupancy spatial bins removed, and 
        the new columns (X_bin, Y_bin, Z) in the behavior and 
        spikes_and_beh dataframes     
    """
    
    z_coords = apply_cantor_pairing(x_bin.tolist(), y_bin.tolist())
    z_coords = pd.Series(data=z_coords)
    
    df = mouse.spikes_and_beh
    df.loc[:,'X_bin'] = x_bin
    df.loc[:,'Y_bin'] = y_bin
    df.loc[:,'Z'] = z_coords
    df.loc[:,'time_bin'] = df.index
    df.set_index(['X_bin','Y_bin'],inplace=True)
    occupancy = df.groupby(['X_bin','Y_bin']).size().to_frame()
    occupancy.rename({0:'occupancy'},axis=1,inplace=True)

    df_merge = df.merge(occupancy,left_index=True,right_index=True)
    df_merge.reset_index(inplace=True)
    df_merge.set_index('time_bin',inplace=True)
    df_merge.sort_index(inplace=True)

    df.reset_index(inplace=True)
    df.set_index('time_bin',inplace=True)
    df.sort_index(inplace=True)
    df
    df_merge
    df_filtered = df_merge[df_merge.iloc[:,-1]>=min_occupancy]

    z_coords = apply_cantor_pairing(df_filtered.X_bin.tolist(), df_filtered.Y_bin.tolist())
    z_coords = pd.Series(data=z_coords, index = df_filtered.index)
    
    new_mouse = copy.deepcopy(mouse)
    
    new_mouse.raw = mouse.raw[mouse.raw.index.isin(df_filtered.index)]
    new_mouse.spikes = mouse.spikes[mouse.spikes.index.isin(df_filtered.index)]
    filtered_binned_beh = mouse.behavior[mouse.behavior.index.isin(df_filtered.index)]
    filtered_binned_beh.loc[:,'Z'] = z_coords
    filtered_binned_beh.loc[:,'X_bin'] = df_filtered.X_bin
    filtered_binned_beh.loc[:,'Y_bin'] = df_filtered.Y_bin
    new_mouse.behavior=filtered_binned_beh
    
    new_mouse.cell_transients = mouse.cell_transients[mouse.cell_transients.index.isin(df_filtered.index)]
    new_mouse.spikes_and_beh = new_mouse.spikes.join(new_mouse.behavior, how='left')
    
    return new_mouse
