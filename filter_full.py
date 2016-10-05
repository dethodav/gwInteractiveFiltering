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

#=============================================================

# First we ask for all the inputs needed
# In the ldvw implementation, this would be selected on the website 

channel_base = raw_input('''What channel would you like to filter?
	
	I would like to filter: ''')

timestart_base = raw_input('''What time would you like to start at?
        
	I would like to start at: ''')

timeend_base = raw_input('''What time would you like to end at?
        
	I would like to end at: ''')

whiten_choice = raw_input('''What would you like to do?
	1. I would like to filter the selected time series against itself.
	2. I would like to filter this channel against a different time series.
	
	My choice is: ''')


#===========================================================
# Now we begin the actual filtering process

timeseries_base = TimeSeries.fetch(channel_base, timestart_base, timeend_base)

# Based on the whiten choice, there are two possibilites for the filtering

# The first is whitening the time series against its own ASD

if whiten_choice == '1':
	timeseries_filtered = whiten(timeseries_base)

# The second is whitening against a different time series, either a different time, or an entirely different channel
# This needs inputs for the second channel
# In the ldvw implementation, these inputs would also be on the website

elif whiten_choice == '2':
	channel_choice = raw_input('''Would you like to whiten using 
		1. The same channel
		2. A different channel
		
		My choice is: ''')
	if channel_choice == '1':
		channel_second = channel_base
	elif channel_choice == '2':
		channel_second = raw_input('''What channel would you like to use instead?
        	
        	I would like to use the channel: ''')

	timestart_second = raw_input('''What time would you like to start at?
        
        	I would like to start at: ''')

	timeend_second = raw_input('''What time would you like to end at?
        
        	I would like to end at: ''')
	
	timeseries_second = TimeSeries.fetch(channel_second, timestart_second, timeend_second)

# Now we actually do the cross filtering

	timeseries_filtered = crosswhiten(timeseries_base,timeseries_second)

# At this point we can ask for any additional fitering processes

add_choice = 0

while add_choice != '3': 
	add_choice = raw_input('''What would you like to do?
		 1. I would like to filter the whitened time series with a band pass filter.
        	 2. I would like to frequency shift the whitened time series.
        	 3. I do not want to add anything else.
	
       		 My choice is: ''')
	
	if add_choice == '1':
		pass_choice = raw_input('''What would you like to do?
                 	1. I would like to add a high pass filter.
                 	2. I would like to add a low pass filter.
        
                 My choice is: ''')

		freq_cutoff = input('''At what frequency would you like to place the filter?
        
                 My choice is: ''')
		if pass_choice == '2':		
			timeseries_filtered = timeseries_filtered.lowpass(freq_cutoff)
		if pass_choice == '1':
			timeseries_filtered = timeseries_filtered.highpass(freq_cutoff)

	if add_choice == '2':
		freq_shift = input('''By what factor would you like to shift the frequency?
        
                 My choice is: ''')

		timeseries_filtered.sample_rate = timeseries_filtered.sample_rate * freq_shift

# At this point, we have filtered our time series, so we just need to write the .wav file

file_name = raw_input('''What would you like to name this file?
                
                My choice is: ''')

file_path = str(file_name) + '.wav'

wavwrite(timeseries_filtered,file_path)

print
print 'Audio Editing Complete'
	




