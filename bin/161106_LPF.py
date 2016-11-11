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

  
  goldenL = ['L1:GDS-CALIB_STRAIN',(goldenL_time - 10) , (goldenL_time + 10)]
  goldenH = ['H1:GDS-CALIB_STRAIN',(goldenH_time - 10) , (goldenH_time + 10)]
  
  source1 = ['L1:GDS-CALIB_STRAIN',(source1_time - 15) , (source1_time + 15)]
  source2 = ['L1:GDS-CALIB_STRAIN',(source2_time - 15) , (source2_time + 15)]
  source3 = ['H1:GDS-CALIB_STRAIN',(source3_time - 15) , (source3_time + 15)]
  
  goldenL_time = TimeSeries.fetch(goldenL[0], goldenL[1], goldenL[2])
  goldenH_time = TimeSeries.fetch(goldenH[0], goldenH[1], goldenH[2])
  
  source1_time = TimeSeries.fetch(source1[0], source1[1], source1[2])
  source2_time = TimeSeries.fetch(source2[0], source2[1], source2[2])
  source3_time = TimeSeries.fetch(source3[0], source3[1], source3[2])
  
  source1_base_time = TimeSeries.fetch(source1[0], source1[1], source1[1]+10)
  source2_base_time = TimeSeries.fetch(source2[0], source2[1], source2[1]+10)
  source3_base_time = TimeSeries.fetch(source3[0], source3[1], source3[1]+10)
  
  
  timeseries_filtered = source1_time
  timeseries_filtered = timeseries_filtered.lowpass(400)
  timeseries_filtered = timeseries_filtered.highpass(30)
  timeseries_filtered = filter_defs.LPF(source1_time,source1_base_time)
  filter_defs.wavwrite(timeseries_filtered,'L1_BHNS_+0Hz_LPF.wav')
  
  timeseries_filtered = source2_time 
  timeseries_filtered = timeseries_filtered.lowpass(1000)
  timeseries_filtered = timeseries_filtered.highpass(30)
  timeseries_filtered = filter_defs.LPF(source2_time,source2_base_time)
  filter_defs.wavwrite(timeseries_filtered,'L1_BNS_+0Hz_LPF.wav')
  
  timeseries_filtered = source3_time  
  timeseries_filtered = timeseries_filtered.lowpass(1000)
  timeseries_filtered = timeseries_filtered.highpass(30)
  timeseries_filtered = filter_defs.LPF(source3_time,source3_base_time)
  filter_defs.wavwrite(timeseries_filtered,'H1_BNS_+0Hz_LPF.wav')
