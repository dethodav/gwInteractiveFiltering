#!/usr/bin/env python

if __name__ == '__main__':

  from gwInteractiveFiltering.filtering import filter_defs
  from scipy import *


  source_file = raw_input(' What is the file name? ')

  glitch_number,time,channel = loadtxt(str(source_file),unpack=True, usecols= [0,12,13], skiprows = 1)

  time_start = time - 5
  time_end = time + 5

  item = 0
  source = zeros(3)

  golden = ['L1:GDS-CALIB_STRAIN',1126593017,1126593037]

  while (item < len(time)):

    source[0] = str(channel[item])
    source[1] = time_start[item]
    source[2] = time_end[item]

    path = str(time[item]) + '_' + str(glitch_number[item])+ '.wav'

    filter_defs.filtering(path,source, golden)

    item = item + 1
