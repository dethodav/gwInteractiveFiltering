#!/usr/bin/env python

# This version of array_inputs was set up to run 
# the specific chirp-like triggers that occured
# on 161106


from gwInteractiveFiltering.filtering import filter_defs
from  gwpy.timeseries import TimeSeries
from scipy import *

if __name__ == '__main__':

  goldenL_time = 1162462258
  goldenH_time = goldenL_time
  
  source1_time = 1162473846.548
  source2_time = 1162464558.119
  source3_time = source2_time

  
  goldenL = ['L1:GDS-CALIB_STRAIN',(goldenL_time - 20) , (goldenL_time + 20)]
  goldenH = ['H1:GDS-CALIB_STRAIN',(goldenH_time - 20) , (goldenH_time + 20)]
  
  source1 = ['L1:GDS-CALIB_STRAIN',(source1_time - 10) , (source1_time + 10)]
  source2 = ['L1:GDS-CALIB_STRAIN',(source2_time - 10) , (source2_time + 10)]
  source3 = ['H1:GDS-CALIB_STRAIN',(source3_time - 10) , (source3_time + 10)]
  
  goldenL_time = TimeSeries.fetch(goldenL_time[0], goldenL_time[1], goldenL_time[2])
  goldenH_time = TimeSeries.fetch(goldenH_time[0], goldenH_time[1], goldenH_time[2])
  
  source1_time = TimeSeries.fetch(source1[0], source1[1], source1[2])
  source2_time = TimeSeries.fetch(source2[0], source2[1], source2[2])
  source3_time = TimeSeries.fetch(source3[0], source3[1], source3[2])
  
  
  timeseries_filtered = source1_time
  timeseries_filtered = timeseries_filtered.lowpass(400)
  timeseries_filtered = timeseries_filtered.highpass(30)
  timeseries_filtered = filter_defs.LPF(source1_time,goldenL_time)
  wavwrite(timeseries_filtered,'L1_BHNS_+0Hz_LPF.wav')
  
  timeseries_filtered = source2_time 
  timeseries_filtered = timeseries_filtered.lowpass(1000)
  timeseries_filtered = timeseries_filtered.highpass(30)
  timeseries_filtered = filter_defs.LPF(source2_time,goldenL_time)
  wavwrite(timeseries_filtered,'L1_BNS_+0Hz_LPF.wav')
  
  timeseries_filtered = source3_time  
  timeseries_filtered = timeseries_filtered.lowpass(1000)
  timeseries_filtered = timeseries_filtered.highpass(30)
  timeseries_filtered = filter_defs.LPF(source3_time,goldenH_time)
  wavwrite(timeseries_filtered,'H1_BNS_+0Hz_LPF.wav')
