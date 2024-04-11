#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Name: test_remove_audvis_blinks.py
Description: Functions which test the code written for lab 5 (whether or not artifacts are removed from the data successfully)
Authors: Ashley Heath, Arthur Dolimier
"""
from remove_audvis_blinks import load_data

#%%%
load_data("AudVisData.npy", [1, 29, 58])

"""
I believe that a blink occurred at slightly after 59 seconds. All of the three channels display a significant voltage spike at this time, 
notably larger in amplitude than the rest of the oscillations around this peak. To me, that suggests an artifact appearing on all channels.
The blink registers most clearly on the Fpz electrode, and least clearly on the Iz electrode, which may be due to the placement of the electrodes:
they're in more or less a straight line from the front to the back of the brain, and Fpz is the electrode closest to the front. It's therefore closest 
to the electrical disruption of the blink.
"""
