
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

from __future__ import absolute_import
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt

#from clawpack.geoclaw import topotools
#from six.moves import range
#from importlib import reload

import os

cmax = 5.
cmin = -cmax

cmax_land = 40.

bg_image = True

if bg_image:
    GE_image = plt.imread('EagleHarborGE.jpg')
    GE_extent = [-122.55,-122.48,47.61,47.64]

    def background_image(current_data):
        from pylab import imshow
        imshow(GE_image,extent=GE_extent)

#--------------------------
def setplot(plotdata=None):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """ 


    from clawpack.visclaw import colormaps, geoplot
    from numpy import linspace

    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()


    plotdata.clearfigures()  # clear any old figures,axes,items data
    plotdata.format = 'binary'


    # To plot gauge locations on pcolor or contour plot, use this as
    # an afteraxis function:

    def addgauges(current_data):
        from clawpack.visclaw import gaugetools
        gaugetools.plot_gauge_locations(current_data.plotdata, \
             gaugenos='all', format_string='ko', add_labels=True)
    

    def timeformat(t):
        from numpy import mod
        hours = int(t/3600.)
        tmin = mod(t,3600.)
        min = int(tmin/60.)
        sec = int(mod(tmin,60.))
        timestr = '%s:%s:%s' % (hours,str(min).zfill(2),str(sec).zfill(2))
        return timestr

    def title_hours(current_data):
        from pylab import title
        t = current_data.t
        timestr = timeformat(t)
        title('%s after earthquake' % timestr)


    #-----------------------------------------
    # Figure for surface
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Surface', figno=0)
    plotfigure.kwargs = {'figsize':(8,5)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Surface'
    plotaxes.scaled = False # need to set aspect ratio properly for lat/long

    def aa(current_data):
        from pylab import ticklabel_format, xticks, gca, cos, pi, savefig
        gca().set_aspect(1./cos(48*pi/180.))
        title_hours(current_data)
        ticklabel_format(useOffset=False)
        xticks(rotation=20)

    plotaxes.afteraxes = aa
    #plotaxes.xlimits = [-122.7,-122.16]
    #plotaxes.ylimits = [47.2,48.3]

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.pcolor_cmap = geoplot.tsunami_colormap
    plotitem.pcolor_cmin = cmin
    plotitem.pcolor_cmax = cmax
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = 0.8
    plotitem.amr_celledges_show = [0]
    #plotitem.celledges_show = 0
    #plotitem.patchedges_show = 0
    plotitem.amr_patchedges_show = [0]


    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    plotitem.pcolor_cmap = geoplot.land_colors
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = cmax_land
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0]
    plotitem.patchedges_show = 0




    #-----------------------------------------
    # Figure for zoom on Eagle Harbor
    #-----------------------------------------
    
    plotfigure = plotdata.new_plotfigure(name="fgmax region", figno=11)
    #plotfigure.show = False
    plotfigure.kwargs = {'figsize': (9,6)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.scaled = False

    plotaxes.xlimits = [-122.55,-122.48]
    plotaxes.ylimits = [47.61,47.64]
    if bg_image:
        plotaxes.beforeaxes = background_image

    plotaxes.afteraxes = aa

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.pcolor_cmap = geoplot.tsunami_colormap
    plotitem.pcolor_cmin = cmin
    plotitem.pcolor_cmax = cmax
    plotitem.add_colorbar = True
    plotitem.amr_data_show = [0,0,1] # only show on finest
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 0

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.show = False
    plotitem.plot_var = geoplot.land
    plotitem.pcolor_cmap = geoplot.land_colors
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = cmax_land
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0]
    plotitem.patchedges_show = 0

    # add contour lines of bathy if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    #plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = [0]
    plotitem.amr_contour_colors = ['yellow']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':2}
    plotitem.amr_contour_show = [0,0,1]  
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0
    
    #-----------------------------------------
    # Figure for zoom on Bainbridge / Seattle
    #-----------------------------------------
    
    plotfigure = plotdata.new_plotfigure(name="Bainbridge", figno=12)
    # not needed for this small domain
    plotfigure.show = False
    plotfigure.kwargs = {'figsize': (9,6)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.scaled = False

    plotaxes.xlimits = [-122.65, -122.3]
    plotaxes.ylimits = [47.5, 47.76]

    plotaxes.afteraxes = aa

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.pcolor_cmap = geoplot.tsunami_colormap
    plotitem.pcolor_cmin = cmin
    plotitem.pcolor_cmax = cmax
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 0

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    plotitem.pcolor_cmap = geoplot.land_colors
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = cmax_land
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0]
    plotitem.patchedges_show = 0

    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------

    plotfigure = plotdata.new_plotfigure(name='gauge plot', figno=300, \
                    type='each_gauge')
    plotfigure.kwargs = {'figsize': (11,6)}
    #plotfigure.clf_each_gauge = False

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,1,1)'
    #plotaxes.ylimits = [-1,10]
    plotaxes.title = 'Flow depth'
    plotaxes.time_scale = 1./60.
    plotaxes.time_label = ''
    
    def add_ylabel_depth(current_data):
        from pylab import ylabel, grid
        ylabel('water depth (m)')
        grid(True)
        
    plotaxes.afteraxes = add_ylabel_depth

    # Plot depth as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 0
    plotitem.plotstyle = 'b-'


    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(2,1,2)'
    #plotaxes.ylimits = [-1,10]
    plotaxes.title = 'Flow speed (m/s)'
    plotaxes.time_scale = 1./60.
    plotaxes.time_label = 'minutes'

    def add_ylabel_speed(current_data):
        from pylab import ylabel, tight_layout, grid
        ylabel('speed (m/s)')
        grid(True)
        tight_layout()
        
    plotaxes.afteraxes = add_ylabel_speed
    
    def speed(current_data):
        from numpy import sqrt, maximum
        q = current_data.q
        h = q[0,:]
        hu = q[1,:]
        hv = q[2,:]
        s = sqrt(hu**2 + hv**2) / maximum(h,0.001)
        return s
        
    # Plot depth as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = speed
    plotitem.plotstyle = 'b-'
    

    #-----------------------------------------
    # Figures for fgmax plots
    #-----------------------------------------
    # Note: need to move fgmax png files into _plots after creating with
    #   python run_process_fgmax.py
    # This just creates the links to these figures...

    if 0:
        otherfigure = plotdata.new_otherfigure(name='max depth',
                        fname='depth.png')
        otherfigure = plotdata.new_otherfigure(name='max speed',
                        fname='speed.png')



    #-----------------------------------------
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'         # list of frames to print
    plotdata.print_gaugenos = 'all'          # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    plotdata.parallel = True                 # make multiple frame png's at once

    return plotdata

