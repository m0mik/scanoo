scanoo
======

SDR receiver for GNU Radio 3.7, built with GRC.

It works by using an FFT block to split the spectrum into 1KHz slices.  These slices are then combined to make up the requested channel bandwidth.

Currently supports AM, NBFM, WBFM.

Compatible Hardware Tested:

- Ettus Research USRP2 & WBX (http://ettus.com)
- HackRF (http://www.kickstarter.com/projects/mossmann/hackrf-an-open-source-sdr-platform)
- RTL-SDR

![ScreenShot](https://raw.github.com/m0mik/scanoo/master/apps/scanoo.com_rx.gui.png)
