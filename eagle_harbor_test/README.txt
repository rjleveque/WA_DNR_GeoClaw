
To run this example:

python make_fgmax.py # to create fgmax_eagle_harbor.txt
make .exe            # to compile code
make data            # creates *.data files and kml files
make .output         # to run the code
make .plots          # to produce plots

The notebook process_fgmax.ipynb can then be used to view the fgmax results.

Note that this is currently set up for a 3 level run down to 2 arcsecond
resolution on the finest grid, so that it runs quickly.

For better resolution results, change to 4 levels in setrun.py, to add a 4th
level with 1/3" resolution.  But then you must also:

In make_fgmax.py: set
    fg.min_level_check = 4
and run "python make_fgmax.py" again, and

in setplot.py: for the zoom plot, figno=11, set
    plotitem.amr_data_show = [0,0,0,1]
so that data is plotted only on level 4 and the google earth image shows
through elsewhere.
