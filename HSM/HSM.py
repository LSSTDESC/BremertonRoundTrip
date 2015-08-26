import os
import glob
import h5py
import galsim
from argparse import ArgumentParser


def HSMfit(galfn, psfimg):
    hdu, hdu_list, fin = galsim.fits.readFile(galfn)
    hdr = hdu.header
    galimg = galsim.fits.read(hdu_list=hdu_list)
    galsim.fits.closeHDUList(hdu_list, fin)
    HSMresult = galsim.hsm.EstimateShear(galimg, psfimg)
    return (hdr['RA'], hdr['DEC'], hdr['Z'], hdr['R'],
            hdr['MAG'], hdr['E1'], hdr['E2'], hdr['G1'],
            hdr['G2'], HSMresult.corrected_e1, HSMresult.corrected_e2,
            HSMresult.corrected_shape_err, HSMresult.correction_status,
            galimg.array.sum())


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('psf',
                        help="Input PSF fits file.")
    parser.add_argument('gals',
                        help="Input galaxies. (Either single file, a directory, or a glob.)")
    parser.add_argument('--outfile', default='HSMcat.h5',
                        help="Output hdf5 catalog file (default: HSMcat.h5)")
    args = parser.parse_args()

    psfimg = galsim.fits.read(args.psf)

    # gals could be a directory, in which case we will process all gal*.fits files in said
    # directory,
    # gals could be a single filename, in which case we will process that.
    # gals could be a globable string with python in which case we'll process files that
    # correspond to that glob.
    if os.path.isfile(args.gals):
        files = [args.gals]
    elif os.path.isdir(args.gals):
        files = glob.glob(os.path.join(args.gals, 'gal*.fits'))
    else:
        files = glob.glob(args.gals)

    outf = h5py.File(args.outfile, 'w')
    dset = outf.create_dataset('gals', (len(files), 14), dtype=float)
    dset.attrs['params'] = ['RA', 'DEC', 'Z', 'R', 'MAG_IN',
                            'E1_IN', 'E2_IN', 'G1_IN', 'G2_IN',
                            'HSM_E1', 'HSM_E2', 'HSM_EERR', 'HSM_STATUS',
                            'FLUX_EST']

    for i, f in enumerate(files):
        dset[i] = HSMfit(f, psfimg)
    outf.close()
