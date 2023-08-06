import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from astropy.convolution import convolve, Box1DKernel

from pysyd import functions
from pysyd import models
from pysyd import utils


def set_plot_params():
    """
    Sets the matplotlib parameters.

    Returns
    -------
    None

    """

    plt.style.use('dark_background')
    plt.rcParams.update({
        'agg.path.chunksize': 10000,
        'mathtext.fontset': 'stix',
        'figure.autolayout': True,
        'lines.linewidth': 1,
        'axes.titlesize': 18.0,
        'axes.labelsize': 16.0,
        'axes.linewidth': 1.25,
        'axes.formatter.useoffset': False,
        'xtick.major.size': 10.0,
        'xtick.minor.size': 5.0,
        'xtick.major.width': 1.25,
        'xtick.minor.width': 1.25,
        'xtick.direction': 'inout',
        'ytick.major.size': 10.0,
        'ytick.minor.size': 5.0,
        'ytick.major.width': 1.25,
        'ytick.minor.width': 1.25,
        'ytick.direction': 'inout',
    })


def time_series(star, notebook=True):

    fig = plt.figure("%s time series"%star.name, figsize=(10,6))
    ax = plt.subplot(1,1,1)
    ax.plot(star.time, star.flux, 'w-')
    ax.set_xlim([min(star.time), max(star.time)])
    ax.tick_params(axis='both', which='minor', length=10, width=1.25, direction='inout')
    ax.tick_params(axis='both', which='major', length=15, width=1.25, direction='inout')  
    ax.tick_params(labelsize=22)
    plt.xlabel(r'$\rm Time \,\, [days]$', fontsize=28)
    plt.ylabel(r'$\rm Normalized \,\, flux$', fontsize=28)
    plt.tight_layout()
    if notebook:
        with open('lc.pickle','wb') as f:
            pickle.dump(fig, f)
    if not star.params['show']:
        plt.close()


def frequency_series(star, notebook=True):

    fig = plt.figure("%s power spectrum"%star.name, figsize=(10,6))
    ax = plt.subplot(1,1,1)
    ax.plot(star.frequency, star.power, 'w-')
    ax.set_xlim([min(star.frequency), max(star.frequency)])
    ax.tick_params(axis='both', which='minor', length=10, width=1.25, direction='inout')
    ax.tick_params(axis='both', which='major', length=15, width=1.25, direction='inout')  
    ax.tick_params(labelsize=22)
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.xlabel(r'$\rm Frequency \,\, [\mu Hz]$', fontsize=28)
    plt.ylabel(r'$\rm Power \,\, [ppm^2 \, \mu Hz^{-1}]$', fontsize=28)
    plt.tight_layout()
    if notebook:
        with open('ps.pickle','wb') as f:
            pickle.dump(fig, f)
    if not star.params['show']:
        plt.close()


def dnu_comparison(star, methods=[['M','A','D'],['MC','AC','DC']], markers=['o','D','^'],
                   colors=['#FF9408','#00A9E0','g']):

    sig = 0.35*star.exp_dnu/2.35482 
    weights = 1./(sig*np.sqrt(2.*np.pi))*np.exp(-(star.lag-star.exp_dnu)**2./(2.*sig**2))
    new_weights = weights/max(weights)
    weighted_acf = star.auto*weights

    fig = plt.figure("Dnu trials for %s"%star.name, figsize=(12, 12))

    for ii, each in enumerate(methods):

        ax1 = fig.add_subplot(2, 2, ii*2+1)
        ax1.plot(star.lag, star.auto, 'w-', zorder=0, linewidth=1.)
        ax1.plot(star.lag, new_weights, c='yellow', linestyle=':', zorder = 0, linewidth = 1.0)
        ax1.axvline(star.exp_dnu, color='red', linestyle=':', linewidth=1.5, zorder=5)
        ax1.set_ylabel(r'$\rm ACF$')
        ax1.set_xlabel(r'$\rm Frequency \,\, separation \,\, [\mu Hz]$')
        ax1.set_xlim([min(star.lag), max(star.lag)])
        ax1.set_ylim([min(star.auto)-0.05*(max(star.auto)-min(star.auto)), max(star.auto)+0.1*(max(star.auto)-min(star.auto))])

        ax2 = fig.add_subplot(2, 2, ii*2+2)
        ax2.plot(star.lag, weighted_acf, 'w-', zorder=0, linewidth=1.)
        ax2.axvline(star.exp_dnu, color='red', linestyle=':', linewidth=1.5, zorder=5)
        ax2.set_yticks([])
        ax2.set_yticklabels([])
        ax2.set_xlabel(r'$\rm Frequency \,\, separation \,\, [\mu Hz]$')
        ax2.set_xlim([min(star.lag), max(star.lag)])
        ax2.set_ylim([min(weighted_acf)-0.05*(max(weighted_acf)-min(weighted_acf)), max(weighted_acf)+0.1*(max(weighted_acf)-min(weighted_acf))])

        for m, method in enumerate(each):
            if method[-1] != 'C':
                closest=False
            star.initial_dnu(method=method[0], closest=closest)
            star.get_acf_cutout(test=True)
            ax1.scatter(star.peaks_l, star.peaks_a, s=30.0, edgecolor=colors[m], marker=markers[m], facecolor='none', linewidths=1.0, label=r'$\rm %s$'%method)
            ax1.axvline(star.best_lag, color=colors[m], linestyle='--', linewidth=2.5, zorder=2)
            ax1.axvline(min(star.zoom_lag), linestyle=':', color=colors[m], linewidth=0.75, zorder=2)
            ax1.axvline(max(star.zoom_lag), linestyle=':', color=colors[m], linewidth=0.75, zorder=2)
            for lag in star.peaks_l:
                ax2.axvline(lag, linestyle='--', color=colors[m], linewidth=0.75, zorder=2, dashes=(5,5))
            ax2.axvline(star.best_lag, color=colors[m], linestyle='--', linewidth=2.5, zorder=2, dashes=(10,10))
            ax2.axvspan(min(star.zoom_lag), max(star.zoom_lag), color=colors[m], alpha=0.5, zorder=0)
        ax1.legend(fontsize=24, loc='upper right', scatteryoffsets=[0.5], handletextpad=0.25, markerscale=1.5, handlelength=0.75, labelspacing=0.3, columnspacing=0.1)
    plt.tight_layout()
    if star.params['save']:
        plt.savefig(os.path.join(star.params[star.name]['path'],'dnu_comparisons.png'), dpi=300)
    if not star.params['show']:
        plt.close()
