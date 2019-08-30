# Hyperscale Rivers

### INSTRUCTIONS

 1. edit the inputs section of the Python file and save the file
 2. Run the saved file:
	Option 1 - in an editor (Spyder, PyCharm, IDLE...)
	Option 2 - from the command line
			a) change dir to the folder with the code
			b) run: python hyperscale_rivers_v1.py
3. Python should display a Matplotlib window with the graph
4. There are also two outputs of the result in PNG and SVG formats.

Please Cite:
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3382267.svg)](https://doi.org/10.5281/zenodo.3382267)
Dietrich, James T., Patrice Carbonneau. 2019. Hyperscale Rivers v1.0. DOI: 10.5281/zenodo.3382267 (as developed on Github)

#### Background
Description taken from my paper:
Dietrich JT. 2016. Riverscape mapping with helicopter-based                     Structure-from-Motion photogrammetry. Geomorphology 252 : 114–157. DOI: [10.1016/j.geomorph.2015.05.008](http://doi.org/10.1016/j.geomorph.2015.05.008)
                    
>These pyramidal graphs illustrate the statistical relationship of two river variables across multiple spatial scales using a moving window approach. At the top of each graph, the window size encompasses all sample points from the river (n). The window size of the second row is n − 2, so the row has three
data points. The third row has a window size of n − 4, generating five data points. This continues with an ever-shrinking window size to the bottom row (window size = 2) where pairs of sample points are being compared (see Fig. 3 for an illustration of this process). The Y-axis of each graph shows the window sizes from largest at the top to smallest at the bottom. The X-axis provides the relative position of each sample in the downstream direction, upstream on the left. A variety of statistical measures/tests can be incorporated into the hyperscale framework, including the coefficient of determination (R2) for a given regression equation or a variety of correlation measures (e.g., Pearson product–moment, Spearman rank-order, or Kendall's τ). For this analysis, I examined the correlation between pairs of variables using the Pearson correlation coefficient, testing for statistical significance at a 99% confidence interval (p = 0.01). This type of analysis can illustrate patterns not always visible with other types of reach or segment scale analysis.

![Imgur](https://i.imgur.com/eLSRvDNl.png)

*Building hyperscale graphs*

![Imgur](https://i.imgur.com/HepJVAF.png)

*Hyperscale example - Correlation between downstream distance and active channel width (testing downstream hydraulic geometry) on 29km of the Middle Fork John Day River, Oregon*

**Other citations:**
Carbonneau P, Fonstad MA, Marcus WA, Dugdale SJ. 2012.Making riverscapes real. Geomorphology 137 : 74–86. DOI: [10.1016/j.geomorph.2010.09.030](http://doi.org/10.1016/j.geomorph.2010.09.030)
