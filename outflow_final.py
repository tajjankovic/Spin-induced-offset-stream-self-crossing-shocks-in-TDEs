# -*- coding: utf-8 -*-

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')
from outflow_parameters_final import *
import outflow_plot_final as plot_data
import numpy as np
from pylab import *
import argparse
from scipy import interpolate

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
  #default=np.arange(0.8,1.5,0.01),  # default if nothing is provided
  default=[0.8,1.2,1.5],  # default if nothing is provided
#    default=[0.9, 1.0, 1.2, 1.5, 1.8],  # default if nothing is provided
)

# parse the command line
args = CLI.parse_args()
# access CLI options
print("dz_list: %r" % args.dz_list)



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''function for CDF calculation' '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def cdf_bivariate(hpmap):
    hpmap_out_2d = hpmap.reshape(xsize, ysize)

    "empty 2d array for theta, empty 1d array for phi because cdfphi doesn't depend on theta (cdfs of rows are the same)"
    cdf_theta_out_2d = np.empty([xsize,ysize])
    cdf_phi_1d = np.empty([xsize])

    for j in range(0, xsize):
        'double integration for phi (wrt phi and then wrt theta)'
        cdf_phi_1d[j] = np.trapz(y=[np.trapz(y=zz_phi, x=phi_array_1d[:j]) for zz_phi in hpmap_out_2d[:, :j]]*np.sin(theta_array_1d), x=theta_array_1d) #zz_phi is a row up to column j

        'single integration for theta (wrt theta at fixed phi)'
        for k in range(0, ysize):
            cdf_theta_out_2d[k,j] = np.trapz(y=hpmap_out_2d[:k,j]*np.sin(theta_array[:k, j]),x=theta_array[:k, j])/np.trapz(y=hpmap_out_2d[:,j]*np.sin(theta_array[:, j]),x=theta_array[:,j])

    cdf_phi_out_2d = np.tile(cdf_phi_1d,(ysize,1))#copy the same array N-times

    'normalize to 1'
    cdf_theta_out_2d  = cdf_theta_out_2d / np.max(cdf_theta_out_2d)
    cdf_phi_out_2d    = cdf_phi_out_2d / np.max(cdf_phi_out_2d)

    return cdf_theta_out_2d,cdf_phi_out_2d






''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''function to calculate data (by lin. interpolation) for values of dz not in the simulated range' '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def interpolate_data(dz):
    dz_sim = np.arange(0,1.51,0.1)
    dz_sim = np.delete(dz_sim,7) #remove for dz=0.7 (not simulated)
    #dz_sim = np.array([0., 0.1 ,0.2, 0.3, 0.4,0.5,0.6,0.8,0.9,1.0,1.2])

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

        'smoothing parameters limits for "same_limits" option'
        if float(dz)<0.7:
            #plot_min, plot_max = 1e-10, 0.3#old limits - for j=rho*v=dotM/area_pix
            if nside==32:
                plot_min_hp_map, plot_max_hp_map = 1e-10, 2e-4
            elif nside==64:
                plot_min_hp_map, plot_max_hp_map = 1e-10, 4e-5
            plot_min_contourf, plot_max_contourf = 1e-10*pix_area/(2*dotM), 0.3*pix_area/(2*dotM)

            lmax_smooth = 15
        else:
            plot_min_hp_map, plot_max_hp_map = 1e-10, 8e-4
            plot_min, plot_max = 1e-10*pix_area/(2*dotM), 5*pix_area/(2*dotM)
            lmax_smooth = 40

        'smooth map if necessary'
        if smooth:
            hpxmap = hp.smoothing(hpxmap, fwhm=fwhm, iter=3, lmax=lmax_smooth)

        print("Integrated value of dotM/dotM_tot from the HEALPix map is:", np.sum(hpxmap))

        'calculate f for arbitrary theta, phi'
        hpmap_out = np.take(hpxmap,pix_out)/pix_area
        'maybe a few pixel have negative flux?'
        hpmap_out[hpmap_out<0.] = 0.
        print('Integrated value of f from the 2D grid on a unit sphere is:', np.sum(hpmap_out)*delta_cos_theta*delta_phi)

        'calculate cumulative distribution function CDF for theta and conditional prob. for phi'
        cdf_theta_out, cdf_phi_out = cdf_bivariate(hpmap_out)

        'save output in a 2D array (theta, phi, f)'
        name_save_data = path_data_out + "dz{0}_nside={1}_size={2}".format(dz, nside, xsize)
        datafile_path = name_save_data + '.txt'
        np.savetxt(datafile_path, np.column_stack([theta_out, phi_out, hpmap_out,cdf_theta_out.ravel(),cdf_phi_out.ravel()]),header="columns: theta,phi,f,cdf (theta),cdf (phi)",fmt=('%.12f', '%12f', '%.12f', '%.12f', '%.12f'))


        'plotting functions'
        if plot_hp_map_bool:
            plot_data.plot_healpix_map(hpxmap, dz, plot_min_hp_map, plot_max_hp_map,lmax_smooth)
        if plot_contourf_bool:
            plot_data.plot_contourf(dz, hpmap_out.reshape(xsize,ysize),phi_out.reshape(xsize,ysize),theta_out.reshape(xsize,ysize),lmax_smooth)



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''call to function' '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
calculate(args.dz_list, theta_array.ravel(), phi_array.ravel())

