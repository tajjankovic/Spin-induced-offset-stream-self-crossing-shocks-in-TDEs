# -*- coding: utf-8 -*-

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')
from outflow_parameters import *
import outflow_plot as plot_data
import numpy as np
from pylab import *
import argparse
from scipy import interpolate, spatial

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Script for running the code and calculating the normalized mass flux'''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


# defined command line options
# this also generates --help and error handling
CLI=argparse.ArgumentParser()
CLI.add_argument(
  "--dz_list",  # name on the CLI - drop the `--` for positional/required parameters
  nargs="*",  # 0 or more values expected => creates a list
  type=float,
  default=[0.],  # default if nothing is provided
)

# parse the command line
args = CLI.parse_args()
# access CLI options
print("dz_list: %r" % args.dz_list)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''function to calculate data (by lin. interpolation) for values of dz not in the simulated range' '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def interpolate_data(dz):
    dz_sim = np.arange(0,1.81,0.1)
    dz_sim = np.delete(dz_sim,7) #remove for dz=0.7 (not simulated)

    'find two closest values of dz of simulated data'
    idx = (np.abs(dz_sim - float(dz))).argmin()
    if float(dz)<=dz_sim[idx]:
        dz1, dz2 = dz_sim[idx-1], dz_sim[idx]
    else:
        dz1, dz2 = dz_sim[idx], dz_sim[idx+1]

    print("Interpolating between dz={0} and dz={1}".format(round(dz1,1),round(dz2,1)))

    data_all1 = np.genfromtxt(path_data_in + 'dz' + str(round(dz1,1)) + '_nside=64.txt', skip_header=1)
    data_all2 = np.genfromtxt(path_data_in + 'dz' + str(round(dz2,1)) + '_nside=64.txt', skip_header=1)

    data = np.empty([len(data_all1[:,0]),3])
    for i in range(0,len(data_all1[:,0])):
        data[i,0],data[i,1] = data_all1[i,0],data_all1[i,1]
        data[i,2] = interpolate.interp1d([dz1,dz2],[data_all1[i,2], data_all2[i,2]])(dz)

    return data



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Finding index of nearest point in numpy arrays of x and y coordinates' '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''https://stackoverflow.com/questions/10818546/finding-index-of-nearest-point-in-numpy-arrays-of-x-and-y-coordinates'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def do_kdtree(combined_x_y_arrays, points):
    mytree = spatial.cKDTree(combined_x_y_arrays)
    dist, indexes = mytree.query(points)
    return indexes


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''main script for calculation' '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def calculate(dz_list, theta_out,phi_out):
    """assign pixel indices to 2D array of the output theta, phi grid"""
    pix_out = hp.ang2pix(nside, theta_out, phi_out)

    for i in range(0, len(dz_list)):
        'load data'
        dz = str(dz_list[i])
        print('Calculations for dz=',dz)
        try:
            data_all = np.genfromtxt(path_data_in + 'dz'+dz+'_nside=64.txt',skip_header=1)
        except OSError:
            'interpolate between closest values'
            data_all = interpolate_data(float(dz))

        theta_hp, phi_hp, hpxmap = data_all[:,0], data_all[:,1], data_all[:,2]

        'same_limits" option'

        if float(dz)<0.7:
            plot_min_hp_map, plot_max_hp_map = 1e-10, 5.5e-5
            plot_min_contourf, plot_max_contourf = plot_min_hp_map/pix_area, plot_max_hp_map/pix_area
            lmax_smooth = 15
        else:

            plot_min_hp_map, plot_max_hp_map = 1e-10, 8e-4
            plot_min_contourf, plot_max_contourf = plot_min_hp_map/pix_area,  plot_max_hp_map/pix_area
            lmax_smooth = 40

        'smooth map if necessary'
        if smooth:
            hpxmap = hp.smoothing(hpxmap, fwhm=fwhm, iter=3, lmax=lmax_smooth)

        print("Integrated value of dotM/dotM_tot from the HEALPix map is:", np.sum(hpxmap))

        'calculate F for arbitrary theta, phi'
        hpmap_out = np.take(hpxmap,pix_out)/pix_area

        'a few pixel can have negative flux'
        hpmap_out[hpmap_out<0.] = 0.
        print('Integrated value of F from the 2D grid on a unit sphere is:', np.sum(hpmap_out)*delta_cos_theta*delta_phi)


        'save output f in a 1D array'
        name_save_data = path_data_out + "dz{0}_nside={1}_xsize={2}_ysize={3}".format(dz, nside, xsize,ysize)
        datafile_path = name_save_data + '.txt'
        np.savetxt(datafile_path, np.column_stack([hpmap_out]),header="columns: f",fmt='%.12f')
        np.savetxt(datafile_path, np.column_stack([theta_out, phi_out, hpmap_out]),header="columns: theta,phi,f",fmt=('%.12f', '%12f', '%.12f'))

        'plotting functions'
        if plot_hp_map_bool and not specific_value:
            plot_data.plot_healpix_map(hpxmap, dz, plot_min_hp_map, plot_max_hp_map,lmax_smooth)
        if plot_contourf_bool and not specific_value:
            plot_data.plot_contourf(dz, hpmap_out.reshape(ysize,xsize),phi_out.reshape(ysize,xsize),theta_out.reshape(ysize,xsize),plot_min_contourf, plot_max_contourf,lmax_smooth)



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''call to function' '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
calculate(args.dz_list, theta_array.ravel(), phi_array.ravel())

