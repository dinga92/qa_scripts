import nibabel as nb
import numpy as np
import sys


mask1_path = sys.argv[1]

other_masks = sys.argv[2:]

print 'Mask overlay with ', mask1_path

fractions = []
for mask2_path in other_masks:

    threshold1 = 0
    threshold2 = 0
    
    mask1 = nb.load(mask1_path).get_data().flatten() > threshold1
    mask2 = nb.load(mask2_path).get_data().flatten() > threshold2
    
    overlay = np.logical_and(mask1, mask2)
    overlay_fraction = sum(overlay)/float(sum(mask2))
    
    fractions.append(overlay_fraction)
    print mask2_path, overlay_fraction
    
print 'Fractions: ', fractions