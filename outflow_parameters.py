# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('TkAgg')
import healpy as hp
import pathlib
from pylab import *

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Script with paths (for output and input directories) and relevant parameters (for plotting and calculations)'''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Path to data  (input and output)'''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
path = str(pathlib.Path(__file__).parent.resolve())
path_data_in = path + "/Data_input/"
path_data_out = path + "/Data_output/"
path_fig_out = path + "/Figures/"

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Simulation parameters'''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
dotM = 1.

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Global variables - different options for plotting and saving the output'''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
save = True
show = True
same_limits = False
smooth = False
make_symmetric = True
plot_hp_map_bool = True
plot_contourf_bool= False
specific_value = False

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''HEALPix parameters'''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
nside = 64
npix = hp.nside2npix(nside)
pix_area = 4 * np.pi / npix
print('HEALPix map with Npix=', npix, ', for nside=', nside)

'for smoothing'
R = 1.02 / nside  # size of 1 pixel
fwhm = 3 * R  # one generally recommends FWHM >~ 3R to obtain a smooth enough result


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''define the 2D grid of the output'''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
size = 800
Ncdf = 1e5

xsize, ysize = size, size
print('Output 2D array with xsize=', xsize, 'and ysize=', ysize)

'get grid points'
theta_array_1d  = np.arccos(np.linspace(1, -1,    ysize))
phi_array_1d    = np.linspace(0, 2 * np.pi, xsize)
delta_cos_theta, delta_phi = 2/(ysize-1), 2*np.pi/(xsize-1) #change to

'set specific values of theta,phi'
if specific_value:
    theta_specific, phi_specific = [0.2,0.3], [0.1,0.15]
    phi_array_1d, theta_array_1d = phi_specific,theta_specific
'create grid'
phi_array,theta_array = np.meshgrid(phi_array_1d,theta_array_1d)


