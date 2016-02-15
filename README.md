# BremertonRoundTrip

This is the repository for an informal hack project launched Aug 20-22 during the LSST collaboration meeting in Bremerton, WA.

The goal of this project is try and assemble a "round-trip" weak-lensing reference analysis that is suitable for
studying the impact of pixel-level systematics on cosmology.  The flow chart below shows the basic round-trip structure. Dashed blue lines show short cuts that provide intermediate comparison points and allow higher- and lower-level paths to be developed and tested independently.

Although our goals sound ambitious, the idea is to ruthlessly simplify each component and aim for a chain that is
complete rather than of high fidelity. A lot of detailed work is already in progress on pieces of this, so the
goal here is to "see the whole elephant" rather than work on an ear or a tusk.

Many of necessary pieces already exist so much of the work will involve selecting suitable code or algorithms from
the literature and figuring out how to connect them together.  The results will hopefully have some pedagogical value,
at least, and the process should help reveal where more effort is most needed to get scientifically useful results.

Our initial goal is to build a functional complete round trip rather than designing a software framework.  With this in mind, we are aiming for a set of reproducible recipes for performing each step and transfering data between them.

## Update for LSS WG

Here is the LSS version of the original plot (see below)
![round-trip flowchart-lss]
(https://github.com/DarkEnergyScienceCollaboration/BremertonRoundTrip/blob/master/images/Ladder_LSS.png?raw=true)

Different shaded boxes correspond to roughly independent pieces of analysis.
Blue lines show plausible shortcuts
Possible loops:
 * Create true power spectrum, fisher version of "estimated power spectrum",  fit cosmo
 * Create lognormal distribution of density fields, populate with galaxies, measure Cls, fit cosmo
 * Create lognormal distribution of density fields, populate with galaxies, add PZ errors, catastrophic outliers, mistyped stars, measure Cls, fit cosmo
 * Create lognormal distribution of density fields, populate with galaxies, realize on chips, deblend, measure fluxes, get PZ, measure Cls, fit cosmo
 * Create realistic distribution of density fields, populate with galaxies, realize on chips, deblend, measure fluxes, get PZ, measure Cls, fit cosmo

Many versions of this will need to be done before we call it a day. Gaussian/lognormal fields should go a long way in testing
many features of the code.


## Update for the 24-Aug-2015 WL telecon

We had a brief meeting as a group (Kirkby, Slosar, Walter, Burchat, Meyers, Roodman, Boutingy) on Wednesday evening and came up with the partition shown below (the original un-annotated diagram is [here](https://github.com/DarkEnergyScienceCollaboration/BremertonRoundTrip/blob/master/images/Ladder.png?raw=true)). We did not have time for any further meetings and our subsequent progress is documented in our issues.

![round-trip flowchart]
(https://github.com/DarkEnergyScienceCollaboration/BremertonRoundTrip/blob/master/images/Ladder-annotated.png?raw=true)

## Generating self-consistent 3D delta fields and shear potentials

See the evolving examples in [this ipython notebook](https://github.com/DarkEnergyScienceCollaboration/BremertonRoundTrip/blob/master/notebooks/GaussianRandomFieldGeneration.ipynb).

## Generating galaxies

Prerequisites: randomfield (dkirkby/randomfield), fastcat (slosar/fastcat)

See fastcat doc for what are the limitations of this approach

### Generating phosim input catalogs

Use the generic driver in the fastcat.py

```
> test/driver.py --help
Usage: driver.py [options]

Options:
  -h, --help            show this help message and exit
  --fov=value           Field of view (degrees)
  --fast                Settings very fast options for quick test, sets N=10
  -N value              Number of objects to create
  --grid_spacing=value  Grid Spacing
  --smooth=value        Smoothing in Mpc/h
  --bias=value          bias of tracer
  --zmean=value         Mean redhisft
  --deltaz=value        variance in redshift
  --iesig=value         intrinsic ellipiticy sigma
  --seed=value          Smoothing in Mpc/h
  --algo=value          Algorithm to use: peaks, lognormal, random
  --phosim=value        Set to make a phosim file
  --phosim_header=value
                        Where to read phosim header from. Empty for no header
  --phosim_many         If true, create per obj file
  --phosim_size=value   Size in arcsec of sersic gals
  --h5read=value        Instead of creating dataset, read it from H5
  --h5write=value       Write to hdf5 file specified on command line
  --treecorr=TREECORR   Set to use TreeCorr to calculate corr functions.
                        Output to filename specified
```

If you run it with --fast, it will set quick options: large pixels, massive smoothing, just 10 objects.

If you don't specify any post-processing options (just phosim at the moment), the results of the run will be lost in the mists of computer memory.
At minimum you run:

```
> test/driver.py --fast --phosim test.txt
```
which results in test.txt containing something like
```
object 0 0.000116787895692 -0.000434462140413 18.1945668055 ../sky/sed_flat.txt 1.95804892476 0.0 0.0 0.0 0.0 0.0 sersic2D 1.89172397066 2.11447339148 -30.6698445182 1
object 1 -5.43940050857e-05 0.000360472912017 16.0542534239 ../sky/sed_flat.txt 1.29824264367 0.0 0.0 0.0 0.0 0.0 sersic2D 1.85363329517 2.15792412147 -51.3304201462 1
object 2 0.000312944544007 -0.000327613995252 21.0248453622 ../sky/sed_flat.txt 1.29639576885 0.0 0.0 0.0 0.0 0.0 sersic2D 1.88483461942 2.12220210663 39.8307047576 1
object 3 -0.000301197992241 -0.000112510868186 19.9390718888 ../sky/sed_flat.txt 1.39070626725 0.0 0.0 0.0 0.0 0.0 sersic2D 1.86595520808 2.14367417968 84.2823603184 1
object 4 -0.000101031835465 -0.000219235237017 17.9739768469 ../sky/sed_flat.txt 1.50510311872 0.0 0.0 0.0 0.0 0.0 sersic2D 1.91606902881 2.08760746083 3.36968745407 1
object 5 -1.29271967738e-05 0.000329361192013 16.9903611641 ../sky/sed_flat.txt 1.39293534538 0.0 0.0 0.0 0.0 0.0 sersic2D 1.85011159196 2.16203174845 13.4624556986 1
object 6 6.59416981271e-05 1.81869826351e-05 16.1464334991 ../sky/sed_flat.txt 1.48559910364 0.0 0.0 0.0 0.0 0.0 sersic2D 1.88375673492 2.12341642944 1.91586929106 1
object 7 -9.78657970765e-05 0.000314333143467 19.9665720571 ../sky/sed_flat.txt 1.39956369942 0.0 0.0 0.0 0.0 0.0 sersic2D 1.93175448963 2.070656505 36.0039096324 1
object 8 0.000382797392061 0.000126114771564 18.3297360331 ../sky/sed_flat.txt 1.38433204132 0.0 0.0 0.0 0.0 0.0 sersic2D 1.96353943813 2.03713759058 79.5402631768 1
object 9 -0.000443908304726 -2.00479428436e-07 19.0918630381 ../sky/sed_flat.txt 1.38125312121 0.0 0.0 0.0 0.0 0.0 sersic2D 1.83319761879 2.18197970529 -89.5408360632 1
```

To generate per object file with some header, run something like
```
./test/driver.py --fast --phosim test%04d.txt --phosim_many --phosim_header=thead
```
This will, not surprisingly, create test0000.txt ... test0001.txt.

### Generating HDF5 files

You can store result of a file into a HDF5 format. E.g

```
> test/driver.py --fast --phosim test.txt
```

can be done as two steps with an intermediate h5 files as

```
test/driver.py --fast -h5write test.h5
test/driver.py --h5read test.h5 --phosim test.txt
```

The HDF5 has one dataset which contains the structured python array.

## Running TreeCorr directly on fastcat catalogs

TreeCorr calculation has been integrated with fastcat and driver.py
will call treecorr directly (in prinicple, measurement can't be but back into
a hdf5 file and read as fastcat Catalog and theen treecorr measurement done directly).
To do that specify -treecorr on command line e.g.

```
./test/driver.py   --smooth=4 --grid_spacing=2 --deltaz=0.02 -N 10000 --treecorr tctest
```

This will produce a tctest file that will contain 12 columns:
* nominal r (arcsec, log spaced)
* actual r
* density-density and error
* shear-shear-plus and error
* shear-shear-minus and error
* density-shear and error
* density-sehar imaginary and error


## Drawing galaxies with GalSim

The galsim/postageStamp.py script will take a fastcat hdf5 output file as its input, and draw
postage stamp images into `galsim/out/gal0.fits`, `galsim/out/gal1.fits`, etc.  These are assumed to
be full-depth (180 visits) stacks in r-band.   The galaxy profile is exponential fixed at 0.3
arcseconds half light radius.  There are also options to specify the (Gaussian) PSF and postage
stampe size:

```
> python galsim/postageStamp.py --help
usage: postageStamp.py [-h] [--nx NX] [--PSF_FWHM PSF_FWHM] [--PSF_e1 PSF_E1]
                       [--PSF_e2 PSF_E2] [--outdir OUTDIR]
                       h5read

positional arguments:
  h5read               Fastcat hdf5 input file.

optional arguments:
  -h, --help           show this help message and exit
  --nx NX              Postage stamp size in pixels.
  --PSF_FWHM PSF_FWHM  PSF FWHM in arcsec (default 0.7)
  --PSF_e1 PSF_E1      PSF e1 (default 0.0)
  --PSF_e2 PSF_E2      PSF e2 (default 0.0)
  --outdir OUTDIR      Output directory (default 'out/')
```

## Fitting GalSim-drawn galaxies with HSM

The HSM/HSM.py script will take take postage stamp image(s) of galaxies and a single postage stamp
image of a PSF and used these to estimate that galaxy's shape using the HSM algorithm implemented
inside of GalSim.  This script produces a single HDF5 output catalog that includes all of the
columns in the original fastcat catalog, as well as shape measurement columns and a crude estimated
flux column, which is just the sum of the pixels in the (assumed background subtracted) postage
stamp.  This won't work for phoSim-generated postage stamps at the moment, since those won't have
the right header keywords, but I think it should be possible to fix this relatively quickly.

```
> python HSM/HSM.py --help
usage: HSM.py [-h] [--outfile OUTFILE] psf galstr

positional arguments:
  psf                Input PSF fits file.
  gals               Input galaxies. (Either single file, a directory, or a
                     glob.)

optional arguments:
  -h, --help         show this help message and exit
  --outfile OUTFILE  Output hdf5 catalog file (default: HSMcat.h5)

```



