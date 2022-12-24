# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.ticker as tck

from outflow_parameters import *
from mpl_toolkits.basemap import Basemap


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Script for plotting the data: either a HEALPix map or a Matplotlib contour plot'''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''use Times New Roman font'''
plt.rcParams.update({"text.usetex": True,"font.family": "serif","font.sans-serif": ["Times"]})

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
        hp.mollview(hpxmap, cmap=plt.cm.hot, title=None, rot=(180,0,180), min=plot_min, max=plot_max, cbar=None,hold=True) #map needs to be rotated because theta=0 is at the south pole
    else:
        hp.mollview(hpxmap, cmap=plt.cm.hot, title=None, rot=(180,0,180), cbar=None, hold=True)

    fig = plt.gcf()
    ax = plt.gca()
    image = ax.get_images()[0]
    hp.graticule() #I don't know why but it prints theta and phi boundaries

    # Make axis labels.
    font_size = 30
    meridians = [45, 90, 135, 180, 225,270,315]
    meridians_name = [45, 90, 135, 180, 225,270,315]

    for kl in range(0, len(meridians)):
         hp.projtext(meridians[kl], -2, str(meridians_name[kl]) + r'$^\circ$', lonlat=True,fontsize=font_size, color='gray')

    plt.text(0.765, 0.52, '90' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)
    plt.text(0.74, 0.377, '120' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)
    plt.text(0.655, 0.26, '150' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)
    plt.text(0.74, 0.644, '60' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)
    plt.text(0.655, 0.76, '30' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)

    plt.text(0.069, 0.52, '90' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)
    plt.text(0.08, 0.377, '120' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)
    plt.text(0.165, 0.26, '150' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)
    plt.text(0.1, 0.644, '60' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)
    plt.text(0.190, 0.76, '30' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)

    plt.title('HP map of data, ' + r'$\Delta z=$' + "{:.2f}".format(float(dz)), fontsize=font_size)

    'add new axes for colorbar and adjust as you wish'
    position = fig.add_axes([0.11, 0.1, 0.64,0.05])  ## the parameters are the specified position you set because cbar is not exactly in the center  [left, bottom, width, height]
    cbar = fig.colorbar(image, cax=position, extend="both", orientation='horizontal',format=tck.FuncFormatter(fmt))

    cbar.set_label(r"$\dot{M}/\dot{M}_\mathrm{tot}\,$", rotation=0, fontsize=font_size)

    'set colorbar ticks'
    cbar.ax.tick_params(labelsize=font_size)
    cbar.ax.locator_params(nbins=3)
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
    locator_f = MaxNLocator(nbins=4)
    bounds = np.linspace(plot_min, plot_max, 201)


    RAD = 180 / np.pi

    len_xaxis, len_yaxis = 15.3, 10.5  # fix here your numbers
    xspace, yspace = .76, .99  # change the size of the void border here.

    x_fig, y_fig = len_xaxis / xspace, len_yaxis / yspace
    fig = plt.figure(figsize=(x_fig, y_fig))
    plt.subplots_adjust(left=0.1, right=0.76, top=0.94, bottom=0.1)


    ax = Basemap(projection='moll', lon_0=0,lat_0=0, resolution='c')

    #theta has to be in range [-90,90], phi in [-180,180]
    if same_limits:
        dotMcountour = ax.contourf(x_list * RAD, (y_list - np.pi / 2) * RAD, Zfit, 50, cmap=plt.cm.hot,latlon=True, locator=locator_f, levels=bounds, extend="both")  # extend=max to color parts outside of range
        cbar = ax.colorbar(dotMcountour, pad=0.6, size='8%', extend="both", location="bottom")
    else:
        dotMcountour = ax.contourf((x_list - np.pi) * RAD, (y_list - np.pi/2) * RAD, Zfit, 50, cmap=plt.cm.hot, latlon=True, extend="both")  # extend=max to color parts outside of range
        #cbar = ax.colorbar(dotMcountour, size='3%', extend="both", location="bottom",format=tck.FuncFormatter(fmt), aspect=10)
        #dotMcountour = ax.contourf(x_list * RAD, (y_list - np.pi / 2) * RAD, Zfit, 50, cmap=plt.cm.hot,latlon=True, locator=locator_f, levels=bounds, extend="both")  # extend=max to color parts outside of range
        cbar = ax.colorbar(dotMcountour, pad=0.6, size='8%', extend="both", location="bottom")

    font_size = 40
    meridians = np.arange(-180., 181., 45.)
    meridians_name = np.arange(0, 361., 45.)

    'set colorbar ticks'
    cbar.ax.tick_params(labelsize=font_size)
    locator_f = MaxNLocator(nbins=3)
    cbar.locator = locator_f
    cbar.update_ticks()

    if float(dz) > 0.7:
        ax.drawparallels(np.arange(-90., 91., 30.), labels=[0, 0, 0, 0], fontsize=font_size, color='lightgray')
        ax.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=font_size, color='gray')

    else:
        ax.drawparallels(np.arange(-90., 91., 30.), labels=[0, 0, 0, 0], fontsize=font_size, color='black')
        ax.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=font_size, color='black')

    'meridians label have to added manually (automatic positioning not supported at the current time)'
    for k in range(1, len(meridians) - 1):
        if float(dz) > 0.7:
            plt.annotate(str(int(meridians_name[k])) + r'$^\circ$', xy=ax(meridians[k], 2), xycoords='data', zorder=5,
                         fontsize=font_size, color='lightgray')
        else:
            plt.annotate(str(int(meridians_name[k])) + r'$^\circ$', xy=ax(meridians[k], 2), xycoords='data', zorder=5,
                         fontsize=font_size, color='white')

    plt.text(0.761, 0.575, '90' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)
    plt.text(0.74, 0.422, '120' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)
    plt.text(0.659, 0.305, '150' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)
    plt.text(0.735, 0.699, '60' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)
    plt.text(0.645, 0.815, '30' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)

    plt.text(0.063, 0.575, '90' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)
    plt.text(0.075, 0.422, '120' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)
    plt.text(0.151, 0.305, '150' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)
    plt.text(0.1, 0.699, '60' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)
    plt.text(0.190, 0.815, '30' + r'$^\circ$', fontsize=font_size, transform=plt.gcf().transFigure)



    plt.title(r'$\Delta z=$' + "{:.2f}".format(float(dz)), fontsize=font_size)
    cbar.set_label(r'${F}\,$', rotation=0, fontsize=font_size)

    'options for saving the figure'
    name_save = 'normalized_map_dz='+"{:.2f}".format(float(dz))
    name_save +='_nside='+str(int(nside)) +'_xsize='+str(int(xsize))+'_ysize='+str(int(ysize))
    name_save = fig_name(name_save,lmax_smooth)

    if save:
        plt.savefig(path_fig_out + name_save  + ".png",   dpi=200)

    if show:
        plt.show()
    plt.close(fig)


