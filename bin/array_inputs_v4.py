#!/usr/bin/env python

# This version of array_inputs uses multiple golden 
# times to help account for changes in the overall 
# noise curve throughout the run.

from gwInteractiveFiltering.filtering import filter_defs
from scipy import *
import multiprocessing

def filter_timeout(path_t,source_t,golden_t,freqshift_t):
  filter_defs.filtering(path_t,source_t,golden_t,freqshift=freqshift_t)


if __name__ == '__main__':

  source_file = raw_input(' What is the file name? ')

  glitch_number= genfromtxt(str(source_file),dtype=int,unpack=True, usecols= [0], skiprows = 1)
  time = genfromtxt(str(source_file),dtype=int,unpack=True, usecols= [2], skiprows = 1)
 

  time_start = (time) - 5
  time_end = (time) + 5

  item = int(0)
  source = ['',0,0]
  
  golden1_time = 1126593027
  golden2_time = 1132948862

  golden1 = ['L1:GDS-CALIB_STRAIN',(golden1_time - 10) , (golden1_time + 10)]
  golden2 = ['L1:GDS-CALIB_STRAIN',(golden2_time - 10) , (golden2_time + 10)]
  

  while (item < len(time)):

    source[0] = 'L1:GDS-CALIB_STRAIN'
    source[1] = time_start[item]
    source[2] = time_end[item]
    
    if (time_end[item] < golden2_time):
      golden = golden1
    else:
      golden = golden2

    path = str(time[item]) + '.wav'

    filter_defs.filtering(path,source, golden, freqshift=60)

    print item
    
    item = item + 1
