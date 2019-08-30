#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
__author__ = 'James T. Dietrich'
__contact__ = 'james.dietrich@uni.edu'
__copyright__ = '(c) James Dietrich 2019'
__license__ = 'MIT'
__date__ = "8/19/2019"
__version__ = '1.0'
__status__ = "initial release"
__url__ = "https://github.com/geojames/..."

"""
Name:           hyperscale_rivers_v1.py
Compatibility:  Python 3.7
Description:    This program ccreate hyperscale correlation graphs for 
                two variables. Originally developed for river environment to
                examine multi-spatial scale downstream relationships 
                (e.g. downstream distane vs. width)
                
                Citations:
                    
                Dietrich JT. 2016. Riverscape mapping with helicopter-based 
                    Structure-from-Motion photogrammetry. 
                    Geomorphology 252 : 114–157. DOI: 10.1016/j.geomorph.2015.05.008
                    
                Carbonneau P, Fonstad MA, Marcus WA, Dugdale SJ. 2012. 
                    Making riverscapes real. Geomorphology 137 : 74–86. 
                    DOI: 10.1016/j.geomorph.2010.09.030
                

Requires:       pandas, numpy, scipy, matplotlib

Dev ToDo:       Needs GUI for real release...

AUTHOR:         James T. Dietrich
ORGANIZATION:   University of Northern Iowa
Contact:        james.dietrich@uni.edu
Copyright:      (c) James Dietrich 2019

Licence:        MIT
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
"""
# *** INSTRUCTIONS ***
#   1) edit the inputs section of this file and save the file
#   2) Run the saved file
#       Option 1 - in an editor (Spyder, PyCharm, IDLE...)
#       Option 2 - from the command line
#                   > change dir to the folder with the code
#                   > run: python hyperscale_rivers_v1.py

#------------------------------------------------------------------------------
# Imports
import os
import pandas as pd
import numpy as np
import scipy.stats  as stats
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.ticker import MultipleLocator

#--- INPUTS --- (make changes here)
    
# Input data: full path to your input data as a CSV 
#   Assumptions:
#       Data are arranged in columns
#       Data are sorted in the downstream direction
infile = 'D:/Dropbox/Python/hyperscale_translate/Dist_Width.csv'

# Which columns are data in?
#   "zero-indexed", so the first column would be 0, second column would be 1...
ind_var = 0     # indepentant variable
dep_var = 1     # depensant variable

# output graph name (just the name you want for your graphs in quotes)
#   will be output in the same folder as the data (will overwrite!) 
out_name = 'riverName_HS_dist_width'

# Choose a correlation method (use # to comment out the one you DO NOT want)
corr_method = 'pearson'
#corr_method = 'spearman'

# Significance threshold - the "p-value" you want to test for inthe correlation
#   ie 90% = 0.1, 95% = 0.05, 99% = 0.01, 99.9% = 0.001
sig = 0.01

# Total distance of the river segment in meters (first data point to the last)
# !!! This is all assuming the data points are equally spaced (regularly sampled)
riv_length = 218444

# Window skip size (even number)
#   depending on the resolution of your data, this will change the resolution of
#   output graph. For smaller datasets use the minimum (2) for larger datasets
#   use 6 or 10. <smaller number = longer processing time>
#       minimum skip size is 2 - this would calulate every odd group of points (3,5,7,9...all points)
#       size 10  - calculates for muliple of 10 (3,13,23,33,43...all points)
win_skip = 10

# Graphing options (you may need to play in here a little)
# x_dist will be the starting point and the separation between ticks on the x-axis
#   in meters. Change based on requirments.
#       Example: if x_dist = 2000 and riv_dist = 32300 meters the ticks will be 
#               at 2000, 4000,..., 32000
# y_dist is the basically the same for the y-axis ticks. 
#   The way these are calculated is different, but the idea is the same.
#   >It's basically the window sizes/scale used for each line in the graph
x_dist = 10000
y_dist = 10000

# minor ticks (minor tick marks on the graph)
minor_ticks = 2000

# -----------------------------------------------------------------------------
#--- SETUP --- (no changes here)

df = pd.read_csv(infile)
df_ind = df.iloc[:,ind_var]
df_dep = df.iloc[:,dep_var]

# array of window sizes (reversed)
windows = np.arange(3,df.shape[0]+1,win_skip)
windows[:] = windows[::-1]

#out array
out = np.full((windows.shape[0],df.shape[0]),np.nan)


#--- MAIN PROG ---
for idx, win in enumerate(windows):
    # calc Pearson corr. coefficient, transpose to row vector
    #corr = df.rolling(win,min_periods=None, freq=None, center=True).corr()[:,0,1]
    #line = np.atleast_2d(corr.values)
    
    corr = df_ind.rolling(win,center=True).corr(df_dep,corr_method)
    line = np.atleast_2d(corr.values)
    
    # calculate the t-stat and p-value for each correlation
    if corr_method == 'pearson':
        #t_stat = line * np.sqrt(win - 2) / np.sqrt(1 - line**2)
        t_stat = line / np.sqrt((1 - line**2)/(win-2))
        pval = stats.t.sf(np.absolute(t_stat), win)
    if corr_method == 'spearman':
        t_stat = line / np.sqrt((1 - line**2)/(win-2))
        pval = stats.t.sf(np.absolute(t_stat), win)
        
    
    # mask non-sig correlations in line, output the result to the out array
    line[pval >= sig] = np.nan
    out[idx,:] = line
    
    # user feedback
    if idx % 100 == 0:
        print("finished %i rows of %i" %(idx, windows.shape[0]))

# calc the length of the smallest window size (3 samples)
samp_length = out.shape[0] / riv_length;
long_length = out.shape[1] / riv_length;

# These are your X tick markers and their labels
xt = np.arange(x_dist,riv_length,x_dist)
xtick = xt * long_length
xticklbl = (xt/1000).astype('int').astype('str')
x_minor = MultipleLocator(minor_ticks * long_length)

# There are the Y ticks and Label
# They represent you window sizes and are based on the spacing of the data you used
yt = np.arange(y_dist,riv_length,y_dist)
ytick = yt * samp_length;
yticklbl = (yt/1000).astype('int').astype('str')
y_minor = MultipleLocator(minor_ticks * samp_length)

# figure aspect for square output
aspect = out.shape[1]/out.shape[0]

# Custom color ramp (Purple-Blue-Green-White-Yellow-Orange-Red)
cdict = [(0.333333333333333,0,0.498039215686275),
(0,0,1),
(0.333333333333333,1,0),
(0.55,0.55,0.55),
(1,1,0),
(1,0,0),
(0.474509803921569,0,0)]

cmap_pwr = colors.LinearSegmentedColormap.from_list("Purple_White_Red", cdict)

# create matplotlib figure
fig, ax = plt.subplots()
ax.grid(True, axis = 'y',zorder=-1)
ax.set_axisbelow(True)
plt.xlabel("Downstream Distance (km)")
plt.ylabel("Window Size (km)")

# plot the data as an image
hs = ax.imshow(np.flipud(out),norm=colors.Normalize(vmin=-1.0, vmax=1.0),cmap=cmap_pwr,
               interpolation='none', aspect = aspect, origin='lower',zorder=1)

# set ticks
ax.xaxis.set_ticks(xtick)
ax.xaxis.set_ticklabels(xticklbl)
ax.yaxis.set_ticks(ytick)
ax.yaxis.set_ticklabels(yticklbl)

ax.xaxis.set_minor_locator(x_minor)
ax.yaxis.set_minor_locator(y_minor)

# graph cleanup
hs.cmap.set_under('k',alpha=0)
bar = fig.colorbar(hs, extend='both')
bar.set_label('Corr. Coeff')
plt.show()
plt.tight_layout()

# output
out_path = os.path.dirname(infile) + "/" + out_name
fig.savefig(out_path+ '.png',format='png')
fig.savefig(out_path+ '.svg',format='svg')