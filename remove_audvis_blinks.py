#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Name: remove_audvis_blinks.py
Description: Defines functions to remove artifacts from data containing multiple electrodes.
Authors: Ashley Heath, Arthur Dolimier
"""
#import libraries
import numpy as np
from matplotlib import pyplot as plt

#%%
def load_data(data_dictionary, channels_to_plot=None):
    """
    Loads in raw EEG Audvis data as a dictionary and plots user-selected channels.
    
    Parameters:
        - data_dictionary: string, the file path to the file containing the EEG data.
        - channels_to_plot: N x 1 array of integers, where each number corresponds to one of the channels that the function will plot.
    Returns:
        - data, dictionary, a dictionary containing the information that 
    """
    data = np.load(data_dictionary, allow_pickle=True).item()
    
    #if there are channels to be plotted:
    if channels_to_plot is not None:
        #create the overall figure
        figure, axis = plt.subplots(len(channels_to_plot),1, sharex=True)
        figure.suptitle("Raw AudVis EEG Data")
        
        #iterate over channels to be plotted and plot each
        for channel_index in range(len(channels_to_plot)):
            axis[channel_index].plot(np.arange(0, 41700, 1)/data['fs'], data["eeg"][channels_to_plot[channel_index],:])
            axis[channel_index].set_xlabel("time (s)")
            axis[channel_index].set_ylabel(f"Voltage on {data['channels'][channels_to_plot[channel_index]]} (uV)")
        #zoom and scale plots
        plt.xlim(55, 60)
        plt.tight_layout()
        
        return data
    else:
        return data
