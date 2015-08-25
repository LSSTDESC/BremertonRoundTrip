import os
import galsim
import h5py
import lsstetc
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('h5read', type=str,
                    help="Fastcat hdf5 input file.")
parser.add_argument('--nx', default=24, type=int,
                    help="Postage stamp size in pixels.")
parser.add_argument('--PSF_FWHM', default=0.7, type=float,
                    help="PSF FWHM in arcsec (default 0.7)")
parser.add_argument('--PSF_e1', default=0.0, type=float,
                    help="PSF e1 (default 0.0)")
parser.add_argument('--PSF_e2', default=0.0, type=float,
                    help="PSF e2 (default 0.0)")
parser.add_argument('--outdir', default='out/', type=str,
                    help="Output directory (default 'out/')")
args = parser.parse_args()

psf = galsim.Gaussian(fwhm=args.PSF_FWHM).shear(e1=args.PSF_e1, e2=args.PSF_e2)
etc = lsstetc.ETC('r', pixel_scale=0.2)
noise = galsim.GaussianNoise(sigma=etc.sigma_sky)
print "Sky noise: {}".format(etc.sigma_sky)

try:
    os.mkdir(args.outdir)
except:
    pass

psfimg = psf.drawImage(nx=args.nx, ny=args.nx, scale=0.2)
psfimg.write(os.path.join(args.outdir, 'psf.fits'))

infile = h5py.File(args.h5read)
for i, datum in enumerate(infile['data']):
    ra, dec, z, r, mag, e1, e2, g1, g2 = datum
    flux = etc.flux(mag)
    print i, mag, flux, e1, e2
    gal = (galsim.Exponential(half_light_radius=0.3)
           .shear(e1=e1, e2=e2)
           .shear(e1=g1, e2=g2)
           .withFlux(flux))

    obj = galsim.Convolve(gal, psf)
    img = obj.drawImage(nx=args.nx, ny=args.nx, scale=0.2)
    img.addNoise(noise)
    h1 = galsim.FitsHeader()
    h1['RA'] = ra
    h1['DEC'] = dec
    h1['z'] = z
    h1['r'] = r
    h1['mag'] = mag
    h1['e1'] = e1
    h1['e2'] = e2
    h1['g1'] = g1
    h1['g2'] = g2
    img.header = h1
    img.write(os.path.join(args.outdir, 'gal{0}.fits'.format(i)))
