# Psychopy-Exp
A psychological experiment built in Psychopy exclusively using python code.

After a dialog box obtaining demographics, an instruction screen, and a 'get ready' screen, the participant is given 100 trials in which they are presented with 2 images. They must respond by typing 'e' if the images are the same, or 'i' if the images are different. 50% of trials are 'same' trials. All images are pulled from a local directory and added to a list. On each trial, the images will be chosen at random, with all images having equal weight. The images are sampled without replacement. A csv file is written to hold Ps data with the subject number as the file name.
IV: trial type (same, different)
DV: response time (RT), accuracy 

The code is oiginal, but the experiment ideation is not. This particular experiment was not run on actual participants. This was a homework assignment, so I hold no particular interest in the outcome of such an experiment.
Code can be used and changed to fit your own needs for psychological experimentation. 
