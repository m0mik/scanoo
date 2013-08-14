scanoo
======

SDR receiver for GNU Radio 3.7, built with GRC.

It works by using an FFT block to split the spectrum into 1KHz slices.  These slices are then combined to make up the requested channel bandwidth.

Currently supports AM, NBFM, WBFM.
