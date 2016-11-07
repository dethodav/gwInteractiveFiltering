#!/usr/bin/env python

# This version of array_inputs was set up to run 
# the specific chirp-like triggers that occured
# on 161106


from gwInteractiveFiltering.filtering import filter_defs
from scipy import *

if __name__ == '__main__':

  goldenL_time = 
  goldenH_time = 
  
  source1_time = 1162473846.548
  source2_time = 1162464558.119
  source3_time = source2_time

  
  goldenL = ['L1:GDS-CALIB_STRAIN',(goldenL_time - 10) , (goldenL_time + 10)]
  goldenH = ['H1:GDS-CALIB_STRAIN',(goldenH_time - 10) , (goldenH_time + 10)]
  
  source1 = ['L1:GDS-CALIB_STRAIN',(source1_time - 10) , (source1_time + 10)]
  source2 = ['L1:GDS-CALIB_STRAIN',(source2_time - 10) , (source2_time + 10)]
  source3 = ['H1:GDS-CALIB_STRAIN',(source3_time - 10) , (source3_time + 10)]
  
  
  filter_defs.filtering('L1_BHNS_0Hz.wav',source1,goldenL,freqshift=0)
  filter_defs.filtering('L1_BHNS_60Hz.wav',source1,goldenL,freqshift=60)
  filter_defs.filtering('L1_BNS_0Hz.wav',source2,goldenL,freqshift=0)
  filter_defs.filtering('L1_BNS_60Hz.wav',source2,goldenL,freqshift=60)
  filter_defs.filtering('H1_BNS_0Hz.wav',source3,goldenH,freqshift=0)
  filter_defs.filtering('H1_BNS_60Hz.wav',source3,goldenH,freqshift=60)
  
  
  #--------------------
  
 
