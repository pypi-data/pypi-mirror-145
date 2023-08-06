
import matplotlib as mpl
import matplotlib.pyplot as plt

from astropy.visualization.wcsaxes import WCSAxes

def get_fig_ax(ax, **kwargs):

    if isinstance(ax, mpl.axes.Axes):

        fig = ax.get_figure()

    else:

        fig = plt.figure(figsize = [4,4], dpi = 150)        

        ax = fig.add_axes([0,0,1,1],
                          projection  = ax,
                          **kwargs)

    if not isinstance(ax, WCSAxes):
        raise ValueError("Axes is not a valid WCSAxes")

    return fig,ax

def healpy_coord_to_astropy(coord):

    if isinstance(coord, str):

        coord = coord.lower() 
        
        if coord == 'c':
            coord = 'icrs'
        elif coord == 'g':
            coord = 'galactic'
        elif coord == 'e':
            coord = 'barycentricmeanecliptic'

    return coord
