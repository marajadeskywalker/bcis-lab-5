#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Name: test_remove_audvis_blinks.py
Description: Functions which test the code written for lab 5 (whether or not artifacts are removed from the data successfully)
Authors: Ashley Heath, Arthur Dolimier
"""
from remove_audvis_blinks import load_data, plot_components, get_sources, remove_sources, compare_reconstructions

#%%%
data = load_data("AudVisData.npy", [1, 29, 58])
"""
I believe that a blink occurred at slightly after 59 seconds. All of the three channels display a significant voltage spike at this time, 
notably larger in amplitude than the rest of the oscillations around this peak. To me, that suggests an artifact appearing on all channels.
The blink registers most clearly on the Fpz electrode, and least clearly on the Iz electrode, which may be due to the placement of the electrodes:
they're in more or less a straight line from the front to the back of the brain, and Fpz is the electrode closest to the front. It's therefore closest 
to the electrical disruption of the blink.
"""

channels_names = data['channels'].tolist()  # Convert to list for the plotting function
plot_components_path = plot_components(data['mixing_matrix'], channels_names)

"""
- Component 0 displays a frontal dominant distribution with symmetry, which could be associated with blinks or vertical eye movements.
- Component 1 shows a high-intensity area over the frontal scalp, which indicates frontal EEG activity but could also be due to blinks, given the proximity to the eyes.
- Component 2 shows significant frontal lobe activity but it is mostly uniform which suggests that it is most likely brain activity.
- In the other components is it hard to know for sure that they are caused by an artifact. 
"""
sources_to_plot_example = [0, 2, 10]
source_activations_example = get_sources(data["eeg"], data["unmixing_matrix"], data["fs"], sources_to_plot_example)

#%%
cleaned_eeg = remove_sources(source_activations_example.copy(), data["mixing_matrix"], [0])
reconstructed_eeg = remove_sources(source_activations_example.copy(), data["mixing_matrix"], [])

compare_reconstructions(data["eeg"], reconstructed_eeg, cleaned_eeg, data["fs"], data["channels"], [1, 29, -1]) # [1, 29, -1]

"""
- The ICA artifact removal did its job by preserving the data with no artifacts but it removed the peaks caused by artifacts
- From the previous plots, using the topo maps and the graph of the data in source space we can see
  that electrodes near the frontal lobe seem to have the most artifacts due to blinks. So these electrodes will show the biggest difference
  after removing a particular independent component.
- After plotting the raw, reconstructed and cleaned data side by side we can see that all electrodes near the frontal lobe show
  a significant difference between the cleaned and raw data. For instance the one that shows the most difference is Fpz as it is the closest to the frontal lobe.
  channels up to number 15 show a difference between raw and cleaned data, meaning that they are affected by the artifacts.
"""