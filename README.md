# X-Ray Attenuation Through the Upper Atmosphere
## Introduction:
Nuclear Explosions release a wide spectrum of EM radiation with a considerable amount in the x-ray region.  As this radiation propagates through the atmosphere, the rays are attenuated at different rates based on their energy.  Modeling how a distribution will evolve as it propagates can be useful to better understand the signatures of a nuclear weapon and aid in their detection.
## Running the Code:
Required packages:
matplotlib
mpl_toolkits
numpy
Code can be run using:
$python3 attenuation.py
## Using the GUI
In the GUI the user may specify several parameters to be simulated such as detonation altitude, sensor altitude, and the rate of exponential decay used to generate an initial photons distribution for simulation. The program assumes the density of the atmosphere to be 0 (no attenuation) at all heights above 100000m.  For this reason, entering a sensor altitude higher than 100000m will return the same result but will just take more time to execute. 

After tweaking the inputs as desired, the user has the option to plot various different experiment such as a line plot of the attenuation transmission percentage across all energies, a line plot of the distribution before and after attenuation, or a surface plot showing the evolution of the distribution as it propagates through the atmosphere.

Furthermore, the user may define their own distribution by drawing on the canvas with their mouse. Then they may select weather to use their input as the initial distribution (in which case the program will compute and graph the final distribution in much the same way as it did in the “line plot of the attenuation” above) or as the final distribution (in which case the program will work backward to calculate a possible initial distribution that would result in the same final distribution that the user defined).  

Unfortunately, there is a level of uncertainty that accompanies working backwards.  To calculate attenuation moving forward in time, the program multiplies the photon intensity for a given energy by the transmission percentage to get the new intensity.  Working backward, we must instead divide by the percentage.  However, if the transmission percentage is or very close to 0% (as it is for all of the low energy photons over any significant distance) we are faced with an undefined result.  Keep this in mind if the resulting graph looks a bit weird or unexpected.

While the ability to let the user draw a distribution by hand is a bit of a gimmick, it is a fun python challenge as well as a proof of concept showing that it is possible to calculate attenuation, both forward and backward, with any input distribution. In practice, the code could be modified with little effort to allow for a user to enter a csv file defining a list of photon intensities for given energies.
