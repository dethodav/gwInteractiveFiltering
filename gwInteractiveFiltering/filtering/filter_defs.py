# -*- coding: utf-8 -*-
# Copyright (C) Derek Davis (2016)
#
# This file is part of gwInteractiveFiltering.
#
# gwInteractiveFiltering is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gwInteractiveFiltering is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.



from  gwpy.timeseries import TimeSeries
import scipy.io.wavfile as wav
import numpy as np
 

# whiten() is used to whiten a time series against itself
def whiten(timeseries):
	timeseries_whitened = timeseries.whiten(4,2)
	return timeseries_whitened

# crosswhiten() is used to whiten a time series against a different time series 
def crosswhiten(timeseries,timeseries_second):
	second_asd = timeseries_second.asd(4,2)
	timeseries_crosswhitened = timeseries.whiten(4,2,asd=second_asd)
	return timeseries_crosswhitened

# wavwrite() is used to set the amplitude and rate of the auido and then creates the .wav file
def wavwrite(timeseries,file_name):
        newrate = 4096
        timeseries_down = timeseries.resample(newrate)
        if ( max(timeseries_down.value) > 1):
		timeseries_down  = 1 * timeseries_down.value / (max(timeseries_down.value))
	elif ( max(timeseries_down.value) < .1):
		timeseries_down  = .2 * timeseries_down.value / (max(timeseries_down.value))
        wav.write(file_name,newrate,timeseries_down)
	
	
# filtering() is used to do the actual filtering, and involves setting your options for the final process. 
def filtering(path,source, golden,lowpass=None, highpass=None,freqshift=None):
	channel_base = source[0]
	timestart_base = source[1]
	timeend_base = source[2]
	timeseries_base = TimeSeries.fetch(channel_base, timestart_base, timeend_base)
	
	channel_gold = golden[0]
	timestart_gold = golden[1]
	timeend_gold = golden[2]
	timeseries_gold = TimeSeries.fetch(channel_gold, timestart_gold, timeend_gold)
	
	timeseries_filtered = crosswhiten(timeseries_base,timeseries_gold)
	
	if (lowpass != None):
		timeseries_filtered = timeseries_filtered.lowpass(lowpass)
		
	if (highpass != None):
		timeseries_filtered = timeseries_filtered.highpass(highpass)
		
	if (freqshift != None):
		timeseries_filtered = (timeseries_filtered * 
		                            np.cos( ( 2 * np.pi * freqshift ) * (timeseries_filtered.times.value - timestart_base) ) )

	wavwrite(timeseries_filtered,path)
	
	
	
	
	
	
