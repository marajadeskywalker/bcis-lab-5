#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Name: remove_audvis_blinks.py
Description: Defines functions to remove artifacts from data containing multiple electrodes.
Authors: Ashley Heath, Arthur Dolimier
"""
#import libraries
import numpy as np

#%%
def load_data(data_dictionary, channels_to_plot=None):
    data = np.load(data_dictionary).item()
    
    if channels_to_plot is not None:
        for channel in channels_to_plot:
            data['eeg'][]
    else:
        return data