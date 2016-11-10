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
	elif ( max(timeseries_down.value) < .2):
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
	

# lpc_ref is used to calculate the LPF Coefficients
def lpc_ref(signal, order):
    """Compute the Linear Prediction Coefficients.

    Return the order + 1 LPC coefficients for the signal. c = lpc(x, k) will
    find the k+1 coefficients of a k order linear filter:

      xp[n] = -c[1] * x[n-2] - ... - c[k-1] * x[n-k-1]

    Such as the sum of the squared-error e[i] = xp[i] - x[i] is minimized.

    Parameters
    ----------
    signal: array_like
        input signal
    order : int
        LPC order (the output will have order + 1 items)

    Notes
    ----
    This is just for reference, as it is using the direct inversion of the
    toeplitz matrix, which is really slow"""
    if signal.ndim > 1:
        raise ValueError("Array of rank > 1 not supported yet")
    if order > signal.size:
        raise ValueError("Input signal must have a lenght >= lpc order")

    if order > 0:
        p = order + 1
        r = np.zeros(p, signal.dtype)
        # Number of non zero values in autocorrelation one needs for p LPC
        # coefficients
        nx = np.min([p, signal.size])
        x = np.correlate(signal, signal, 'full')
        r[:nx] = x[signal.size-1:signal.size+order]
        phi = np.dot(sp.linalg.inv(sp.linalg.toeplitz(r[:-1])), -r[1:])
        return np.concatenate(([1.], phi))
    else:
        return np.ones(1, dtype = signal.dtype)

#levinson_1d solves the toeplitz matrices used in lpc_ref
def levinson_1d(r, order):
    """Levinson-Durbin recursion, to efficiently solve symmetric linear systems
    with toeplitz structure.

    Parameters
    ---------
    r : array-like
        input array to invert (since the matrix is symmetric Toeplitz, the
        corresponding pxp matrix is defined by p items only). Generally the
        autocorrelation of the signal for linear prediction coefficients
        estimation. The first item must be a non zero real.

    Notes
    ----
    This implementation is in python, hence unsuitable for any serious
    computation. Use it as educational and reference purpose only.

    Levinson is a well-known algorithm to solve the Hermitian toeplitz
    equation:

                       _          _
        -R[1] = R[0]   R[1]   ... R[p-1]    a[1]
         :      :      :          :      *  :
         :      :      :          _      *  :
        -R[p] = R[p-1] R[p-2] ... R[0]      a[p]
                       _
    with respect to a (  is the complex conjugate). Using the special symmetry
    in the matrix, the inversion can be done in O(p^2) instead of O(p^3).
    """
    r = np.atleast_1d(r)
    if r.ndim > 1:
        raise ValueError("Only rank 1 are supported for now.")

    n = r.size
    if n < 1:
        raise ValueError("Cannot operate on empty array !")
    elif order > n - 1:
        raise ValueError("Order should be <= size-1")

    if not np.isreal(r[0]):
        raise ValueError("First item of input must be real.")
    elif not np.isfinite(1/r[0]):
        raise ValueError("First item should be != 0")

    # Estimated coefficients
    a = np.empty(order+1, r.dtype)
    # temporary array
    t = np.empty(order+1, r.dtype)
    # Reflection coefficients
    k = np.empty(order, r.dtype)

    a[0] = 1.
    e = r[0]

    for i in xrange(1, order+1):
        acc = r[i]
        for j in range(1, i):
            acc += a[j] * r[i-j]
        k[i-1] = -acc / e
        a[i] = k[i-1]

        for j in range(order):
            t[j] = a[j]

        for j in range(1, i):
            a[j] += k[i-1] * np.conj(t[i-j])

        e *= 1 - k[i-1] * np.conj(k[i-1])

    return a, e, k

# LPF filters a timeseries against an example timeseries
# by using a Linear Predictive filter
def LPF(timeseries,baseseries,order=2**12):
	inputsig = timeseries.value
	testsig = baseseries.value

	newsig = np.zeros(len(power))

	if len(testsig.value) < order:
		order = len(testsig.value)

	coef1 = lpc_ref(np.array(testsig.value),order)
	
	endpoint = len(insputsig)

	#%%
	for n in range(0,endpoint-1):
	    x_n = 0
	    #x_n = power[n]
	    for m in range(0,order):
		if (n-m) < 0:
		    new_x_n = 0
		elif:
		    new_x_n = coef1[m]*inputsig[n-m]
		x_n = x_n + new_x_n
	    newsig[n] = x_n

	timeseries = newsig + timeseries*0

	#%%

	return timeseries





	
	
	
	
	
	
