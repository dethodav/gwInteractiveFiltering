if __name__ == '__main__':

  from gwInteractiveFiltering import filtering
  from scipy import *


  source_file = raw_input(' What is the file name? ')

  channel,time,glitch_class = loadtxt(str(source_file),unpack=True, usecols= [0,1,2], skiprows = 1)

  time_start = time - 5
  time_end = time + 5

  item = 0
  source = zeros(3)

  golden = ['L1:GDS-CALIB_STRAIN',1126593017,1126593037]

  while (item < len(time)):

    source[0] = channel[item]
    source[1] = time_start[item]
    source[2] = time_end[item]

    path = './'+str(glitch_class[item])+'/'+ str(time[item]) + '.wav'

    filtering(path,source, golden)

  item = item + 1
