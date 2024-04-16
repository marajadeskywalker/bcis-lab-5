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


def get_sources(eeg, unmixing_matrix, fs, sources_to_plot=None):
    """
    Transforms EEG data into source space using the provided unmixing matrix and plots the activity of specified sources.

    Parameters:
    - eeg (numpy.ndarray): The EEG data array, with shape (n_channels, n_samples).
    - unmixing_matrix (numpy.ndarray): The ICA unmixing matrix, with shape (n_components, n_channels).
    - fs (float): The sampling rate of the EEG data.
    - sources_to_plot (list of int, optional): The indices of the sources to plot. Default is an empty list, which means no plots are generated.

    Returns:
    - U (numpy.ndarray): The source activation timecourses obtained from the transformation, with shape (n_components, n_samples).
    """
    if sources_to_plot is None:
        sources_to_plot = []

    # Perform matrix multiplication to transform the EEG data into source space
    U = np.dot(unmixing_matrix, eeg)

    # If there are sources to be plotted, generate the plots
    if sources_to_plot:
        # Determine the time axis based on the sampling rate and number of samples
        time_axis = np.arange(eeg.shape[1]) / fs

        # Create a figure for plotting
        fig, axs = plt.subplots(len(sources_to_plot), 1, figsize=(10, len(sources_to_plot) * 2), sharex=True)

        # If there's only one source to plot, axs may not be an array
        if not isinstance(axs, np.ndarray):
            axs = [axs]

        for ax, source_index in zip(axs, sources_to_plot):
            ax.plot(time_axis, U[source_index, :], label=f'reconstructed')
            ax.set_xlabel('time (s)')
            ax.set_ylabel(f'Source {source_index} (uV)')
            # ax.set_xlim([55, 60])
            ax.legend()

        plt.suptitle("AudVis EEG Data in ICA source space")
        plt.tight_layout()
        plt.show()

        fig.savefig('AudVisICA_source.png')

    return U
    
def remove_sources(source_activations, mixing_matrix, sources_to_remove):
    """
    Function to remove artifacts from the data by zeroing selected sources using the mixing matrix.
    
    Parameters:
    - source_activations (array): The source activation timecourses obtained from the transformation, with shape (n_components, n_samples), and type float
    - mixing_matrix (array): The ICA mixing matrix where each column represents the weights of a component across the EEG channels, with shape(n_components, n_channels) and type float
    - sources_to_remove (array): a list/array of the indices of the sources that you would like removed from the data, with shape (n x 1) and type int, n being the number of sources being removed from the data. 
    
    Returns:
    - cleaned_eeg (array): The cleaned eeg data with the selected sources removed, transformed back into electrode space. Has shape (n_components, n_channels), and type float
    """
    if sources_to_remove is not None and len(sources_to_remove) > 0: 
        #given indices of signals set to zero: set those to zero
        for source_index in sources_to_remove:
            source_activations[source_index] = np.zeros(np.shape(source_activations)[1])
        
    #multiply source activations by mixing matrix and this will give you electrode data.
    cleaned_eeg = np.matmul(mixing_matrix, source_activations)

    #return electrode data
    return cleaned_eeg
