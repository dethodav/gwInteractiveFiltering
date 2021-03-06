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
import scipy as sp
import scipy.signal as sig
 


def whiten(timeseries):
	"""whiten() is used to whiten a time series against itself
	"""
	
	timeseries_whitened = timeseries.whiten(4,2)
	return timeseries_whitened

 
def crosswhiten(timeseries,timeseries_second):
	"""crosswhiten() is used to whiten a time series against a different time series
	"""
	
	second_asd = timeseries_second.asd(4,2)
	timeseries_crosswhitened = timeseries.whiten(4,2,asd=second_asd)
	return timeseries_crosswhitened


def wavwrite(timeseries,file_name):
	"""wavwrite() is used to set the amplitude and rate 
	of the auido and then creates the .wav file
	"""
	
        newrate = 4096
        timeseries_down = timeseries.resample(newrate)
        if ( max(timeseries_down.value) > .1):
		timeseries_down  = .1 * timeseries_down.value / (max(timeseries_down.value))
	elif ( max(timeseries_down.value) < .1):
		timeseries_down  = .1 * timeseries_down.value / (max(timeseries_down.value))
        wav.write(file_name,newrate,timeseries_down)
	
	
 
def filtering(path,source, golden,lowpass=None, highpass=None,freqshift=None):
	"""filtering() is used to do the actual filtering, and involves 
	setting your options for the final process.
	"""
	
	channel_base = source[0]
	timestart_base = source[1]
	timeend_base = source[2]
	timeseries_base = TimeSeries.get(channel_base, timestart_base, timeend_base)
	
	channel_gold = golden[0]
	timestart_gold = golden[1]
	timeend_gold = golden[2]
	timeseries_gold = TimeSeries.get(channel_gold, timestart_gold, timeend_gold)
	
	timeseries_filtered = crosswhiten(timeseries_base,timeseries_gold)
	
	if (lowpass != None):
		timeseries_filtered = timeseries_filtered.lowpass(lowpass)
		
	if (highpass != None):
		timeseries_filtered = timeseries_filtered.highpass(highpass)
		
	if (freqshift != None):
		timeseries_filtered = shift(timeseries_filtered,freqshift)

	wavwrite(timeseries_filtered,path)
	

	

def shift(timeseries,fshift):
	"""shift() is used to frequency shift the spectrum of the file by manually 
	changing the bins in the frequency domain
	"""
	
	data = timeseries.value
	samp_rate = timeseries.sample_rate.value
	time_length = len(data)/float(samp_rate)
	df = 1.0/time_length
	nbins = int(fshift/df)
	
	freq_rep = np.fft.rfft(data)
	shifted_freq = np.zeros(len(freq_rep),dtype=complex)
	for i in range(0,len(freq_rep)-1):
		if 0<(i-nbins)<len(freq_rep):
		       shifted_freq[i]=freq_rep[i-nbins]
	out = np.fft.irfft(shifted_freq)
	out_real = np.real(out)

	timeseries_output = TimeSeries(out_real,sample_rate=samp_rate)
		       
        return timeseries_output


def hil_shift(timeseries,fshift):
	"""hil_shift() is used to frequency shift the file by calculating the 
	analytic and then multiplying by a complex exponential
	"""
	
	x = timeseries.value
	samp_rate = timeseries.sample_rate.value
	dt = 1/samp_rate
	
	N_orig = len(x)
    	N_padded = 2**nextpow2(N_orig)
   	t = np.arange(0, N_padded)
    	out_real = (sig.hilbert(np.hstack((x, np.zeros(N_padded-N_orig, x.dtype))))*np.exp(2j*np.pi*fshift*dt*t))[:N_orig].real
	
	timeseries_output = TimeSeries(out_real,sample_rate=samp_rate)
		
	return timeseries_output
		
# nextpow2() is used to append the file with zeroes until the file
# has length 2^n, reducing computing time for the fft
def nextpow2(x):
    """Return the first integer N such that 2**N >= abs(x)
    used to append the file with zeroes until the file
    has length 2^n, reducing computing time for the fft
    """

    return int(np.ceil(np.log2(np.abs(x))))


def expand(timeseries,f,fftlength=.1,hop=.025):
	"""expand() stretches the sound by a factor `f` 
	without changing the frequency content
	utilizes phase vocoder method
	"""
	
	data = timeseries.value
	samp_rate = float(timeseries.sample_rate.value) 
	window_length = (fftlength*samp_rate)-( (fftlength*samp_rate) % 2) 
	hop_length = round(hop*samp_rate) 
	hop_time = (hop_length / samp_rate)
   	hanning_window = sig.hanning(window_length)
	
	out_length = int(hop_length*f) 
	segments = np.arange(0, len(data)-(window_length+hop_length), hop_length)
	num_segemnts = len(segments) 
    	out = np.zeros(out_length * num_segemnts + (window_length))
	
	w = np.linspace(0,(2 * np.pi * samp_rate / 2), (window_length/2) + 1)
	out_time = out_length / samp_rate
	
	#set up 0th chunk
	a0 = data[0:window_length]
	s0 =  np.fft.rfft(a0)# * hanning_window)
	phase = np.angle(s0)    
	a0_average = np.fft.irfft(s0)
	i2 = 0
	out[i2 : i2 + window_length] += a0_average*hanning_window

    	for i in segments:
		# two potentially overlapping subarrays
		a1 = data[i: i + window_length]
		a2 = data[i + hop_length: i + window_length + hop_length]

		# compute frequency spectra for each chunk
		s1 =  np.fft.rfft(a1)# * hanning_window)
		s2 =  np.fft.rfft(a2)# * hanning_window)

		# compute phase adjustment
		dw = ( (np.angle(s2) - np.angle(s1)) / (hop_time) ) - (w)
		w_wrapped = ( (dw + np.pi) % (2 * np.pi) ) - np.pi
		w_true = w + w_wrapped
		
		# resynchronize the second array on the first
		phase = (phase + out_time * w_true) % (2 * np.pi)
		a2_average = np.fft.irfft(abs(s2)*np.exp(1j*phase))

		# add to output
		i2 = i2+out_length
		out[i2 : i2 + window_length] += a2_average*hanning_window
	
	# create new timeseries to output
	timeseries_output = TimeSeries(out,sample_rate=samp_rate)
		       
        return timeseries_output


	
	
	
	
	
	
	
	
