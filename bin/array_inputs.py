#!/usr/bin/env python

if __name__ == '__main__':

  from gwInteractiveFiltering.filtering import filter_defs
  from scipy import *


  source_file = raw_input(' What is the file name? ')

  glitch_number= genfromtxt(str(source_file),dtype=int,unpack=True, usecols= [0], skiprows = 1)
  time = genfromtxt(str(source_file),dtype=int,unpack=True, usecols= [12], skiprows = 1)
  channel = genfromtxt(str(source_file),dtype=str,unpack=True, usecols= [13], skiprows = 1)

  time_start = (time) - 5
  time_end = (time) + 5

  item = int(0)
  source = ['',0,0]

  golden = ['L1:GDS-CALIB_STRAIN',1126593017,1126593037]

  while (item < len(time)):

    source[0] = channel[item]
    source[1] = time_start[item]
    source[2] = time_end[item]

    path = str(glitch_number[item]) + '_' + str(time[item]) + '.wav'

    filter_defs.filtering(path,source, golden)

    print item
    
    item = item + 1
