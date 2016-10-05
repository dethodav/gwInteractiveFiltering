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
        path = '/home/derek.davis/public_html/' + file_name
        newrate = 4096
        timeseries_down = timeseries.resample(newrate)
        if ( max(timeseries_down.value) > 1):
		print "Max value exceeded! Audio damped by factor of " + str( max(timeseries_down.value))
		timeseries_down  = 1 * timeseries_down.value / (max(timeseries_down.value))
        wav.write(path,newrate,timeseries_down)
