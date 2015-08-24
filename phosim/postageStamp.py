import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy import ndimage

# Read in a PhoSim fits file with a single galaxy.  Find the weighted
# mean to center a 50x50 pixel postage stamp around it.  Rewrite the header
# to include the updated physical plane information at the center of the postage
# stamp and write it as a new file.

# Get the file
fileName = 'lsst_e_999999991_f2_R02_S10_E000.fits.gz'

(chipImage, header) = fits.getdata('/Users/walter/LSST/PhoSim/phosim/output/'+fileName,
                                   header=True)

# Transpose X and Y.  Why??
chipImage = chipImage.T

print "Reading ", fileName, "with size", chipImage.shape

# Find the weighted center of the of the image.
# Manually centerX = 2891, centerY = 2397
(centerX, centerY) = ndimage.measurements.center_of_mass(chipImage)

print "Found centerX =", centerX, "centerY = ", centerY

# Extract Postage Stamp
stampSizeX = 50
stampSizeY = 50
postageStamp = chipImage[centerX - stampSizeX/2: centerX + stampSizeX/2,
                         centerY - stampSizeY/2: centerY + stampSizeY/2]

# Plot to the screen
plt.imshow(postageStamp, cmap='gray')
plt.show()

# modify fits image

# Get the center of this chip
chipCenterX = header["CENTX"]
chipCenterY = header["CENTY"]
chipSizeX = header["PIXX"]
chipSizeY = header["PIXY"]

imageOffsetX = centerX - chipSizeX/2
imageOffsetY = centerY - chipSizeY/2

# Change the center to the position of the galaxy
print "ChipX = ", chipCenterX
print "GalaxyX = ", centerX
print "ImageOffsetX =", imageOffsetX
print "PostageX = ", chipCenterX + imageOffsetX

header["CENTX"] = chipCenterX + imageOffsetX
header["CENTY"] = chipCenterY + imageOffsetY
header["PIXX"] = stampSizeX
header["PIXY"] = stampSizeY

print(header["CENTX"])

# Write out new postage stamp. Use the postageStamp and the modified header.

#newHDU =  PrimaryHDU(postageStamp, header)

fits.writeto('postageStamp.fits', postageStamp, header, clobber=True)
