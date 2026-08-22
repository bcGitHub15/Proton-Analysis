# Proton-Analysis
Notes on my investigations of the data from the BL3 proton detector.

First is an investigation of the trapezoidal analysis algorithm used by Jason and Gerard. It is applied to some of the first preliminary data from a dubious proton detector.

ChannelNoise.ipynb contains histograms of noise in each of the channels in the data. It reveals two shorted pixels (ADC's 25 and 31) and then two different kinds of noise spectrum for the rest of the channels, many have noise in the range 100-200 ADC units but the rest have noise in the range 150-300 ADC units.
