#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 20:21:17 2026
ChDat.py

Functions etc. to work with individual channel files. These have a
more well-defined format than Gerard's (which have extra blank lines to
confuse the reader).
Header line has form
pixel <n> (ring <m>)
Then blocks of 82 lines with format
Event begin <n>
80 lines of 10 numbers separated by spaces
Event end <n>

There are 80430 events in the 50V set and 62729 in the 70V set.

Start with a class to store a set of events from a single channel.

Add a class to store data for a single event that will help with fitting.
Add a method to the channel store to return a given event object.

@author: bcollett
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

class Event:
    def __init__(self, t, y, index = 0):
        self.times = t
        self.vals = y
        self.index = index
        self.fit_vals = None
        self.resids = None
    
    def set_index(self, i):
        self.index = int(i)
    
    def plot_on(self, ax):
        ax.plot(self.times, self.vals, '.')
        if self.fit_vals is not None:
            ax.plot(self.times, self.fit_vals)

    def plot(self):
        fig, ax = plt.subplots(figsize=(8,6))
        self.plot_on(ax)
        return ax
    
    # Model
    # First try two straight lines with different slopes and offsets
    # This version has a split of 100 channels about the center where we
    # ignore the data.
    # Since there are 800 points in a data set we fit 0:350 and 450: and
    # set the middle 100 to zero.
    def model(self, params):
#        print(f'In model params={params}')
        bkgnd = params[0] + params[1] * self.times
        tail = params[2] + params[3] * self.times
        mid = np.zeros(100)
        fit = np.concatenate((bkgnd[:350], mid, tail[450:]))
        return fit
    
    # helper for fits. Bind to a real method name before use.
    def fit_helper(params, args, m_name = 'model', ):
#        print(f'In helper params={params}')
        data = args
        func = getattr(data, m_name)
        data.fit_vals = func(params)
        fittable_data = data.vals.copy()
        fittable_data[350:450] = 0
        data.resids = data.vals - data.fit_vals
        res_sq = data.resids * data.resids
        return np.sum(res_sq)

    # The p0 argument should hold the initial values of the parameters.
    def fit_to(self, p0):
        result = optimize.minimize(Event.fit_helper, p0, args=(self, ), method='BFGS', options={'maxiter': 5000})
        Event.fit_helper(result.x, self)
        return result
    

class ChData:
    Dt = 0.032 # us
    
    def __init__(self, filename, npoint=1_000):
        self.npoint = npoint
        self.data = np.empty((800, npoint))
        with open(filename, 'r', encoding="utf-8") as ifp:
            header = ifp.readline()
            if header[:5] != 'pixel':
                raise ValueError(f'Expecting pixel header, found {header}')
            self.name = header
            for i in range(npoint):
                words = ifp.readline().split(' ')
                if words[0] != 'Event':
                    raise ValueError(f'Expecting event header, found {words}')
                evt_num = int(words[2])
                for j in range(80):
                    line = ifp.readline()
                    vals = line.split(' ')
                    for k in range(10):
                        self.data[j * 10 + k, i] = float(vals[k])
                words = ifp.readline().split(' ')
                if words[0] != 'Event':
                    raise ValueError(f'Expecting event trailer, found {words}')
                if int(words[2]) != evt_num:
                    raise ValueError(f'Expecting evt number {evt_num} but found {words[1]}')
        print(f'Read {npoint} events.')
        self.times = np.arange(0.0, 25.6, ChData.Dt)


    def plot_on(self, ax, evt_num):
        print(f'add line {evt_num}')
        print(self.data[:10, evt_num])
        ax.plot(self.times, self.data[:, evt_num], '.')
    
    def plot(self, evt_num):
        fig, ax = plt.subplots(figsize=(8,6))
        self.plot_on(ax, evt_num)
        return ax
    
    # Early average - late average
    def energy1(self, evt_num):
        early = np.average(self.data[:300, evt_num])
        late = np.average(self.data[-300:, evt_num])
        return early - late
    
    # Extract one event
    def get_event(self, index):
        i = int(index)
        if i < 0 or i > len(self.times):
            raise ValueError('Index out of range')
        return Event(self.times, self.data[:, i], i)

    # plot an energy histogram
 
    def plot_hist_on(self, ax, do_log=True):
        energies = np.empty(self.npoint)
        for i in range(self.npoint):
            energies[i] = self.energy1(i)
        ax.hist(energies, bins = 600, range=(0, 6000), log=do_log)
        ax.set(xlabel='tADC Units', ylabel='Count',
           title=self.name)
        ax.grid()
        return ax
    
    def plot_hist(self, log=True):
        fig, ax = plt.subplots(figsize=(8,6))
        self.plot_hist_on(ax, do_log=log)
        return ax
   
            

if __name__ == '__main__':
    ch1 = ChData('nopulser70V/Channel3.txt', npoint = 62729)
    fig1, ax1 = plt.subplots(figsize=(8,6))
    for i in range(2):
        ch1.plot_on(ax1, i + 1)
    energies = np.empty(ch1.npoint)
    for i in range(ch1.npoint):
        energies[i] = ch1.energy1(i)
    fig2, ax2 = plt.subplots(figsize=(8,6))
    ax2.hist(energies, bins = 600, range=(0, 6000), log=True)
    ax2.set(xlabel='tADC Units', ylabel='Count',
       title=ch1.name)
    ax2.grid()
    
    fig3, ax3 = plt.subplots(figsize=(8,6))
    ax3.hist(energies, bins = 140, range=(2200, 3600))
    ax3.set(xlabel='tADC Units', ylabel='Count',
       title=ch1.name)
    ax3.grid()

    
    