# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.ticker as tck

from outflow_parameters_final import *
from mpl_toolkits.basemap import Basemap


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Script for plotting the data: either a HEALPix map or a Matplotlib contour plot'''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''scientific notation for colorbar:https://stackoverflow.com/questions/25983218/scientific-notation-colorbar-in-matplotlib'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def fmt(x,pos):
    a, b = '{:.1e}'.format(x).split('e')
    b = int(b)
    return r'${} \times 10^{{{}}}$'.format(a, b)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''name of the output figure'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def fig_name(name_save,lmax_smooth):
    if same_limits:           name_save += '_same_limits'
    if smooth:                name_save +='_lmaxsmooth='+str(lmax_smooth) + '_smooth_fwhm='+str(round(fwhm,2))
    if make_symmetric:        name_save +='_symm'
    if orthographic:        name_save +='_ortho'

    return name_save



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Plot a HEALPIX map'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def plot_healpix_map(hpxmap,dz,plot_min,plot_max,lmax_smooth):
    len_xaxis, len_yaxis = 15.3, 10.5  # fix here your numbers
    xspace, yspace = .76, .99  # change the size of the void border here.

    x_fig, y_fig = len_xaxis / xspace, len_yaxis / yspace
    plt.figure(figsize=(x_fig, y_fig))
    plt.subplots_adjust(left=0.1, right=0.76, top=0.94, bottom=0.1)
    plt.axes()


    if same_limits:
        hp.mollview(hpxmap, cmap=plt.cm.jet, title=None, rot=(180, 0, 180), min=plot_min, max=plot_max, cbar=None,hold=True)
    else:
        if orthographic:
            hp.orthview(hpxmap, cmap=plt.cm.jet,title=None,cbar=None, hold=True,rot=(rot_lat, rot_lon)) #orthographic projection - to see if dotM at dz>0.7 is spherical
        else:
            hp.mollview(hpxmap, cmap=plt.cm.jet, title=None, rot=(180, 0, 180), cbar=None, hold=True)

    fig = plt.gcf()
    ax = plt.gca()
    image = ax.get_images()[0]
    hp.graticule() #I don't know why but it prints theta and phi boundaries

    # Make axis labels.
    meridians = np.arange(0., 360., 45.)
    parallels = np.arange(-90., 90, 30.)
    for kl in range(1, len(meridians)):
        if meridians[kl] < 180:
            hp.projtext(meridians[kl], -2, str(180 - abs(int(meridians[kl]))) + r'$^\circ$W', lonlat=True, fontsize=20,color='white')
        elif meridians[kl] > 180:
            hp.projtext(meridians[kl], -2, str(abs(int(180 - meridians[kl]))) + r'$^\circ$E', lonlat=True, fontsize=20,color='white')
        else:
            hp.projtext(meridians[kl], -2, str(abs(180 - int(meridians[kl]))) + r'$^\circ$', lonlat=True, fontsize=20,color='white')

    plt.text(0.765, 0.52, '0' + r'$^\circ$', fontsize=20, transform=plt.gcf().transFigure)
    plt.text(0.74, 0.377, '30' + r'$^\circ$S', fontsize=20, transform=plt.gcf().transFigure)
    plt.text(0.655, 0.26, '60' + r'$^\circ$S', fontsize=20, transform=plt.gcf().transFigure)
    plt.text(0.74, 0.644, '30' + r'$^\circ$N', fontsize=20, transform=plt.gcf().transFigure)
    plt.text(0.655, 0.76, '60' + r'$^\circ$N', fontsize=20, transform=plt.gcf().transFigure)

    plt.text(0.084, 0.52, '0' + r'$^\circ$', fontsize=20, transform=plt.gcf().transFigure)
    plt.text(0.08, 0.377, '30' + r'$^\circ$S', fontsize=20, transform=plt.gcf().transFigure)
    plt.text(0.165, 0.26, '60' + r'$^\circ$S', fontsize=20, transform=plt.gcf().transFigure)
    plt.text(0.08, 0.644, '30' + r'$^\circ$N', fontsize=20, transform=plt.gcf().transFigure)
    plt.text(0.165, 0.76, '60' + r'$^\circ$N', fontsize=20, transform=plt.gcf().transFigure)

    plt.title('HP map of data, ' + r'$\Delta z=$' + "{:.2f}".format(float(dz)), fontsize='24')

    'add new axes for colorbar and adjust as you wish'
    position = fig.add_axes([0.11, 0.1, 0.64,0.05])  ## the parameters are the specified position you set because cbar is not exactly in the center  [left, bottom, width, height]
    cbar = fig.colorbar(image, cax=position, extend="both", orientation='horizontal',format=tck.FuncFormatter(fmt))

    cbar.set_label(r"$\dot{M}/\dot{M}_\mathrm{tot}\,$", rotation=0, fontsize=20)

    'set colorbar ticks'
    cbar.ax.tick_params(labelsize=18)
    cbar.ax.locator_params(nbins=5)
    #cbar.formatter.set_powerlimits((0, 0))

    name_save = 'normalized_healpix_map_dz='+"{:.2f}".format(float(dz))

    name_save +='_nside='+str(int(nside))
    name_save = fig_name(name_save,lmax_smooth)
    if save:
        plt.savefig(path_fig_out + name_save  + ".png",   dpi=200)
    if show:
        plt.show()
    plt.close(fig)



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Plot a spherical (Mollweide) contour projection with Matplotlib'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def plot_contourf(dz,Zfit,x_list,y_list,plot_min, plot_max,lmax_smooth):

    """ticks locator"""
    locator_f = MaxNLocator(nbins=5)
    bounds = np.linspace(plot_min, plot_max, 201)


    RAD = 180 / np.pi

    len_xaxis, len_yaxis = 15.3, 10.5  # fix here your numbers
    xspace, yspace = .76, .99  # change the size of the void border here.

    x_fig, y_fig = len_xaxis / xspace, len_yaxis / yspace
    fig = plt.figure(figsize=(x_fig, y_fig))
    plt.subplots_adjust(left=0.1, right=0.76, top=0.94, bottom=0.1)


    if orthographic:
        ax = Basemap(projection='ortho', lon_0=rot_lon,lat_0=rot_lat, resolution='c')
    else:
        ax = Basemap(projection='moll', lon_0=0, resolution='c')


    if same_limits:
        dotMcountour = ax.contourf((x_list - np.pi) * RAD, (y_list - np.pi/2) * RAD, Zfit, 50, cmap=plt.cm.jet, latlon=True, locator=locator_f, levels=bounds, extend="both")  # extend=max to color parts outside of range
        cbar = ax.colorbar(dotMcountour, size='3%', extend="both", location="bottom", format=tck.FuncFormatter(fmt))
    else:
        dotMcountour = ax.contourf((x_list - np.pi) * RAD, (y_list - np.pi/2) * RAD, Zfit, 50, cmap=plt.cm.jet, latlon=True, extend="both")  # extend=max to color parts outside of range
        cbar = ax.colorbar(dotMcountour, size='3%', extend="both", location="bottom",format=tck.FuncFormatter(fmt), aspect=10)


    meridians = np.arange(-180., 181., 45.)
    # set minor ticks
    cbar.ax.tick_params(labelsize=20)
    cbar.locator = locator_f
    cbar.update_ticks()


    ax.drawparallels(np.arange(-90., 91., 30.), labels=[1, 1, 0, 0], fontsize=20)
    ax.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=20)
    'meridians label have to added manually (automatic positioning not supported at the current time)'
    for k in range(1, len(meridians) - 1):
        if meridians[k] < 0:
            plt.annotate(str(abs(int(meridians[k]))) + r'$^\circ$W', xy=ax(meridians[k], 2), xycoords='data',fontsize=18, color='white')
        elif meridians[k] > 0:
            plt.annotate(str(int(meridians[k])) + r'$^\circ$E', xy=ax(meridians[k], 2), xycoords='data', fontsize=18,color='white')
        else:
            plt.annotate(str(int(meridians[k])) + r'$^\circ$', xy=ax(meridians[k], 2), xycoords='data', fontsize=18,color='white')

    else:
        plt.title('Data from 2D array, ' + r'$\Delta z=$'+  "{:.2f}".format(float(dz)) , fontsize='24')
        cbar.set_label(r'${f}\,$', rotation=0, fontsize=20)

    'options for saving the figure'
    name_save = 'normalized_map_dz='+"{:.2f}".format(float(dz))
    name_save +='_nside='+str(int(nside)) +'_xsize='+str(int(xsize))+'_ysize='+str(int(ysize))
    name_save = fig_name(name_save,lmax_smooth)

    if save:
        plt.savefig(path_fig_out + name_save  + ".png",   dpi=200)

    if show:
        plt.show()
    plt.close(fig)


