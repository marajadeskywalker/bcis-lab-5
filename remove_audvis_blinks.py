#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Name: remove_audvis_blinks.py
Description: Defines functions to remove artifacts from data containing multiple electrodes.
Authors: Ashley Heath, Arthur Dolimier
"""
import matplotlib as mtp
#import libraries
import numpy as np
from matplotlib import pyplot as plt
# mtp.use('TkAgg')
from plot_topo import plot_topo


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


def plot_components(mixing_matrix, channels, components_to_plot=None):
    """
    Plots the Independent Component Analysis (ICA) components' topographies.

    Parameters:
    - mixing_matrix (numpy.ndarray): The ICA mixing matrix where each column represents the weights of a component across the EEG channels.
    - channels (list of str): A list of channel names corresponding to the EEG data.
    - components_to_plot (list of int, optional): A list of component indices to be plotted. If not specified, the first ten components are plotted by default.
    """
    if components_to_plot is None:
        components_to_plot = list(range(10))  # Default to plot the first 10 components

    # Define the layout of the subplots
    num_rows = 2
    num_columns = 5

    fig = plt.figure(2, figsize=(20, 10))

    # Loop over each component to plot
    for index, component in enumerate(components_to_plot):
        # Extract the current component data from the mixing matrix
        component_data = mixing_matrix[:, component]

        # Create a new axis instance in the correct position
        plt.subplot(num_rows, num_columns, index + 1)

        # Call the plot_topo function to plot the topomap on the current axis
        plot_topo(channel_names=channels, channel_data=component_data, title=f'ICA component {component}',
                  cbar_label='', montage_name='standard_1005')

    # Tighten the layout
    plt.tight_layout()

    # show
    plt.show()

    fig.savefig('ICA_topomaps.png')
