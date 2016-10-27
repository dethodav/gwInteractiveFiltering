#!/usr/bin/env python

# This version of array_inputs uses multiple golden 
# times to help account for changes in the overall 
# noise curve throughout the run.


if __name__ == '__main__':

  from gwInteractiveFiltering.filtering import filter_defs
  from scipy import *
  import multiprocessing


  source_file = raw_input(' What is the file name? ')

  glitch_number= genfromtxt(str(source_file),dtype=int,unpack=True, usecols= [0], skiprows = 1)
  time = genfromtxt(str(source_file),dtype=int,unpack=True, usecols= [12], skiprows = 1)
  channel = genfromtxt(str(source_file),dtype=str,unpack=True, usecols= [13], skiprows = 1)

  time_start = (time) - 5
  time_end = (time) + 5

  item = int(0)
  source = ['',0,0]
  
  golden1_time = 1126593027
  golden2_time = 1132948862

  golden1 = ['L1:GDS-CALIB_STRAIN',(golden1_time - 10) , (golden1_time + 10)]
  golden2 = ['L1:GDS-CALIB_STRAIN',(golden2_time - 10) , (golden2_time + 10)]
  

  while (item < len(time)):

    source[0] = channel[item]
    source[1] = time_start[item]
    source[2] = time_end[item]
    
    if (time_end[item] < golden2_time):
      golden = golden1
    else:
      golden = golden2

    path = str(time[item]) + '_' + str(glitch_number[item]) + '.wav'
    
    #Using multiprocessing in order to allow fetching to time out after 30 sec
    p = multiprocessing.Process(target=filter_defs.filtering,args=(path,source,golden,freqshift=60,))
    p.start()
    p.join(30)
    if p.is_alive():
      print "Fetching time out: Could not download item " + item
      p.terminate()
      p.join()
      
    item = item + 1
