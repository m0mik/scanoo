#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: scanoo.com_rx
# Author: Mike Jameson M0MIK
# Generated: Thu Jan  8 18:56:39 2015
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import ConfigParser
import math
import random
import threading
import time
import wx

class scanoo_com_rx(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="scanoo.com_rx")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self._cfg_min_center_freq_config = ConfigParser.ConfigParser()
        self._cfg_min_center_freq_config.read(".scanoo")
        try: cfg_min_center_freq = self._cfg_min_center_freq_config.getfloat("main", "min_center_freq")
        except: cfg_min_center_freq = 118e6
        self.cfg_min_center_freq = cfg_min_center_freq
        self.min_center_freq = min_center_freq = cfg_min_center_freq
        self._cfg_samp_rate_config = ConfigParser.ConfigParser()
        self._cfg_samp_rate_config.read(".scanoo")
        try: cfg_samp_rate = self._cfg_samp_rate_config.getfloat("main", "samp_rate")
        except: cfg_samp_rate = 100e6/256
        self.cfg_samp_rate = cfg_samp_rate
        self._cfg_blocked_freq_list_config = ConfigParser.ConfigParser()
        self._cfg_blocked_freq_list_config.read(".scanoo")
        try: cfg_blocked_freq_list = self._cfg_blocked_freq_list_config.get("main", "blocked_freq_list")
        except: cfg_blocked_freq_list = ""
        self.cfg_blocked_freq_list = cfg_blocked_freq_list
        self.txt_center_freq = txt_center_freq = 5.5e6
        self.txt_blocked_freq_list = txt_blocked_freq_list = cfg_blocked_freq_list
        self.samp_rate = samp_rate = cfg_samp_rate
        self.func_center_freq = func_center_freq = [min_center_freq]
        self.center_freq_hop_button = center_freq_hop_button = 0
        self.bin_bw = bin_bw = int(1e3)
        self.fft_len = fft_len = int(float(samp_rate)/bin_bw)
        self._cfg_ch_step_size_config = ConfigParser.ConfigParser()
        self._cfg_ch_step_size_config.read(".scanoo")
        try: cfg_ch_step_size = self._cfg_ch_step_size_config.getfloat("main", "ch_step_size")
        except: cfg_ch_step_size = 6.25e3
        self.cfg_ch_step_size = cfg_ch_step_size
        self.center_freq = center_freq = int(func_center_freq[0]) if ((func_center_freq[0] > 0) and (center_freq_hop_button)) else int(txt_center_freq)
        self.blocked_freq_list = blocked_freq_list = [int(blocked_freq) for blocked_freq in txt_blocked_freq_list.split()]
        self.bin_floor = bin_floor = int(150e3/bin_bw)
        self.fft_signal_level = fft_signal_level = [0.0]*(fft_len)
        self.channel_click_freq = channel_click_freq = 5.505e6
        self.ch_step_size = ch_step_size = cfg_ch_step_size
        self.blocked_bin_list = blocked_bin_list = [int(math.floor(float(((blocked_freq-(center_freq-(samp_rate/2)))/bin_bw))/bin_floor)*bin_floor) for blocked_freq in blocked_freq_list]
        self.audio_samp_rate = audio_samp_rate = 48e3*4
        self.spectrum_sense_button = spectrum_sense_button = 0
        self.quad_samp_rate = quad_samp_rate = audio_samp_rate*1
        self.max_bin_index = max_bin_index = int(fft_signal_level.index(max([i for j, i in enumerate(fft_signal_level) if (int(math.floor(float(j)/bin_floor)*bin_floor) not in blocked_bin_list )])))
        self.left_edge_freq = left_edge_freq = center_freq - (float(samp_rate)/2)
        self.channel_click_freq_rounded = channel_click_freq_rounded = (round(float(channel_click_freq) / ch_step_size, 0) * ch_step_size)
        self.channel_samp_rate = channel_samp_rate = (quad_samp_rate*1)
        self._cfg_volume_config = ConfigParser.ConfigParser()
        self._cfg_volume_config.read(".scanoo")
        try: cfg_volume = self._cfg_volume_config.getfloat("main", "volume")
        except: cfg_volume = 1
        self.cfg_volume = cfg_volume
        self._cfg_squelch_threshold_config = ConfigParser.ConfigParser()
        self._cfg_squelch_threshold_config.read(".scanoo")
        try: cfg_squelch_threshold = self._cfg_squelch_threshold_config.getfloat("main", "squelch_threshold")
        except: cfg_squelch_threshold = -20
        self.cfg_squelch_threshold = cfg_squelch_threshold
        self._cfg_rx_gain_config = ConfigParser.ConfigParser()
        self._cfg_rx_gain_config.read(".scanoo")
        try: cfg_rx_gain = self._cfg_rx_gain_config.getfloat("main", "rx_gain")
        except: cfg_rx_gain = 15
        self.cfg_rx_gain = cfg_rx_gain
        self._cfg_modulation_config = ConfigParser.ConfigParser()
        self._cfg_modulation_config.read(".scanoo")
        try: cfg_modulation = self._cfg_modulation_config.getint("main", "modulation")
        except: cfg_modulation = 0
        self.cfg_modulation = cfg_modulation
        self._cfg_max_center_freq_config = ConfigParser.ConfigParser()
        self._cfg_max_center_freq_config.read(".scanoo")
        try: cfg_max_center_freq = self._cfg_max_center_freq_config.getfloat("main", "max_center_freq")
        except: cfg_max_center_freq = 136e6
        self.cfg_max_center_freq = cfg_max_center_freq
        self._cfg_ch_width_config = ConfigParser.ConfigParser()
        self._cfg_ch_width_config.read(".scanoo")
        try: cfg_ch_width = self._cfg_ch_width_config.getint("main", "ch_width")
        except: cfg_ch_width = int(6.25e3)
        self.cfg_ch_width = cfg_ch_width
        self._cfg_ch_trans_config = ConfigParser.ConfigParser()
        self._cfg_ch_trans_config.read(".scanoo")
        try: cfg_ch_trans = self._cfg_ch_trans_config.getint("main", "ch_trans")
        except: cfg_ch_trans = int(1e3)
        self.cfg_ch_trans = cfg_ch_trans
        self.bin_index = bin_index = max_bin_index if spectrum_sense_button else (float(channel_click_freq_rounded - left_edge_freq)/bin_bw)
        self.volume = volume = cfg_volume
        self.squelch_threshold = squelch_threshold = cfg_squelch_threshold
        self.rx_gain = rx_gain = cfg_rx_gain
        self.quad_decim = quad_decim = int(channel_samp_rate/quad_samp_rate)
        self.modulation = modulation = cfg_modulation
        self.max_channel_freq = max_channel_freq = (round(float(left_edge_freq+(bin_bw*bin_index))/ ch_step_size, 0) * ch_step_size)
        self.max_center_freq = max_center_freq = cfg_max_center_freq
        self.lo_offset = lo_offset = (samp_rate/2)*1.25
        self.gui_sizes = gui_sizes = [1250,500]
        self.gui_refresh_rate = gui_refresh_rate = 2**4
        self.gui_ref_level = gui_ref_level = -10
        self.gui_fft_size = gui_fft_size = 2**10
        self.gui_average = gui_average = 0.1
        self.func_quad_avg_mag_sqrd_unmuted = func_quad_avg_mag_sqrd_unmuted = False
        self.func_probe_rate = func_probe_rate = 1
        self.combined_ch_bins = combined_ch_bins = int(float(channel_samp_rate)/bin_bw)
        self.ch_width = ch_width = min(cfg_ch_width,((quad_samp_rate/2)*0.9))
        self.ch_trans = ch_trans = min(cfg_ch_trans,int(quad_samp_rate*0.99))
        self.center_freq_step = center_freq_step = samp_rate*0.7
        self.audio_decim = audio_decim = int(quad_samp_rate/audio_samp_rate)

        ##################################################
        # Blocks
        ##################################################
        self.nb_controls = self.nb_controls = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.nb_controls.AddPage(grc_wxgui.Panel(self.nb_controls), "Main")
        self.nb_controls.AddPage(grc_wxgui.Panel(self.nb_controls), "Spectrum Sense")
        self.GridAdd(self.nb_controls, 1, 0, 1, 1)
        _squelch_threshold_sizer = wx.BoxSizer(wx.VERTICAL)
        self._squelch_threshold_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(0).GetWin(),
        	sizer=_squelch_threshold_sizer,
        	value=self.squelch_threshold,
        	callback=self.set_squelch_threshold,
        	label="Squelch",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._squelch_threshold_slider = forms.slider(
        	parent=self.nb_controls.GetPage(0).GetWin(),
        	sizer=_squelch_threshold_sizer,
        	value=self.squelch_threshold,
        	callback=self.set_squelch_threshold,
        	minimum=-100,
        	maximum=100,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.nb_controls.GetPage(0).GridAdd(_squelch_threshold_sizer, 1, 0, 1, 1)
        self.probe_center_freq = blocks.probe_signal_vf(1)
        self.probe_avg_mag_sqrd = analog.probe_avg_mag_sqrd_c(squelch_threshold, 0.00001)
        (self.probe_avg_mag_sqrd).set_processor_affinity([1])
        _volume_sizer = wx.BoxSizer(wx.VERTICAL)
        self._volume_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(0).GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	label="Volume",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._volume_slider = forms.slider(
        	parent=self.nb_controls.GetPage(0).GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	minimum=0,
        	maximum=10,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.nb_controls.GetPage(0).GridAdd(_volume_sizer, 1, 3, 1, 1)
        self._samp_rate_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(0).GetWin(),
        	value=self.samp_rate,
        	callback=self.set_samp_rate,
        	label="Sample Rate",
        	converter=forms.float_converter(),
        )
        self.nb_controls.GetPage(0).GridAdd(self._samp_rate_text_box, 0, 5, 1, 2)
        _rx_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._rx_gain_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(0).GetWin(),
        	sizer=_rx_gain_sizer,
        	value=self.rx_gain,
        	callback=self.set_rx_gain,
        	label="RX Gain",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._rx_gain_slider = forms.slider(
        	parent=self.nb_controls.GetPage(0).GetWin(),
        	sizer=_rx_gain_sizer,
        	value=self.rx_gain,
        	callback=self.set_rx_gain,
        	minimum=0,
        	maximum=74,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.nb_controls.GetPage(0).GridAdd(_rx_gain_sizer, 1, 1, 1, 1)
        self.nb_gfx = self.nb_gfx = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.nb_gfx.AddPage(grc_wxgui.Panel(self.nb_gfx), "FFT Rough Tune")
        self.nb_gfx.AddPage(grc_wxgui.Panel(self.nb_gfx), "FFT Fine Tune")
        self.nb_gfx.AddPage(grc_wxgui.Panel(self.nb_gfx), "FFT Zoom")
        self.nb_gfx.AddPage(grc_wxgui.Panel(self.nb_gfx), "Waterfall Rough Tune")
        self.nb_gfx.AddPage(grc_wxgui.Panel(self.nb_gfx), "Waterfall Fine Tune")
        self.nb_gfx.AddPage(grc_wxgui.Panel(self.nb_gfx), "Waterfall Zoom")
        self.nb_gfx.AddPage(grc_wxgui.Panel(self.nb_gfx), "Scope")
        self.GridAdd(self.nb_gfx, 0, 0, 1, 1)
        self._modulation_chooser = forms.radio_buttons(
        	parent=self.nb_controls.GetPage(0).GetWin(),
        	value=self.modulation,
        	callback=self.set_modulation,
        	label="Modulation",
        	choices=[0,1,2,3,4],
        	labels=["AM","FM","LSB","USB","CW"],
        	style=wx.RA_HORIZONTAL,
        )
        self.nb_controls.GetPage(0).GridAdd(self._modulation_chooser, 0, 2, 1, 2)
        self._min_center_freq_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(1).GetWin(),
        	value=self.min_center_freq,
        	callback=self.set_min_center_freq,
        	label="Min Center Freq",
        	converter=forms.float_converter(),
        )
        self.nb_controls.GetPage(1).GridAdd(self._min_center_freq_text_box, 2, 1, 1, 1)
        self._max_channel_freq_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(1).GetWin(),
        	value=self.max_channel_freq,
        	callback=self.set_max_channel_freq,
        	label="Locked On Freq (Hz)",
        	converter=forms.int_converter(),
        )
        self.nb_controls.GetPage(1).GridAdd(self._max_channel_freq_text_box, 1, 1, 1, 2)
        self._max_center_freq_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(1).GetWin(),
        	value=self.max_center_freq,
        	callback=self.set_max_center_freq,
        	label="Max Center Freq",
        	converter=forms.float_converter(),
        )
        self.nb_controls.GetPage(1).GridAdd(self._max_center_freq_text_box, 2, 2, 1, 1)
        _lo_offset_sizer = wx.BoxSizer(wx.VERTICAL)
        self._lo_offset_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(0).GetWin(),
        	sizer=_lo_offset_sizer,
        	value=self.lo_offset,
        	callback=self.set_lo_offset,
        	label='lo_offset',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._lo_offset_slider = forms.slider(
        	parent=self.nb_controls.GetPage(0).GetWin(),
        	sizer=_lo_offset_sizer,
        	value=self.lo_offset,
        	callback=self.set_lo_offset,
        	minimum=-10e6,
        	maximum=10e6,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.nb_controls.GetPage(0).GridAdd(_lo_offset_sizer, 1, 2, 1, 1)
        def _func_quad_avg_mag_sqrd_unmuted_probe():
            while True:
                val = self.probe_avg_mag_sqrd.unmuted()
                try:
                    self.set_func_quad_avg_mag_sqrd_unmuted(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (float(func_probe_rate)/1))
        _func_quad_avg_mag_sqrd_unmuted_thread = threading.Thread(target=_func_quad_avg_mag_sqrd_unmuted_probe)
        _func_quad_avg_mag_sqrd_unmuted_thread.daemon = True
        _func_quad_avg_mag_sqrd_unmuted_thread.start()
        def _func_center_freq_probe():
            while True:
                val = self.probe_center_freq.level()
                try:
                    self.set_func_center_freq(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (float(func_probe_rate)/4))
        _func_center_freq_thread = threading.Thread(target=_func_center_freq_probe)
        _func_center_freq_thread.daemon = True
        _func_center_freq_thread.start()
        _ch_width_sizer = wx.BoxSizer(wx.VERTICAL)
        self._ch_width_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(0).GetWin(),
        	sizer=_ch_width_sizer,
        	value=self.ch_width,
        	callback=self.set_ch_width,
        	label='ch_width',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._ch_width_slider = forms.slider(
        	parent=self.nb_controls.GetPage(0).GetWin(),
        	sizer=_ch_width_sizer,
        	value=self.ch_width,
        	callback=self.set_ch_width,
        	minimum=int(1e3),
        	maximum=int((quad_samp_rate/2)*0.9),
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.nb_controls.GetPage(0).GridAdd(_ch_width_sizer, 1, 4, 1, 1)
        _ch_trans_sizer = wx.BoxSizer(wx.VERTICAL)
        self._ch_trans_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(0).GetWin(),
        	sizer=_ch_trans_sizer,
        	value=self.ch_trans,
        	callback=self.set_ch_trans,
        	label='ch_trans',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._ch_trans_slider = forms.slider(
        	parent=self.nb_controls.GetPage(0).GetWin(),
        	sizer=_ch_trans_sizer,
        	value=self.ch_trans,
        	callback=self.set_ch_trans,
        	minimum=int(1e3),
        	maximum=int(quad_samp_rate*0.99),
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.nb_controls.GetPage(0).GridAdd(_ch_trans_sizer, 1, 5, 1, 1)
        self._center_freq_hop_button_chooser = forms.button(
        	parent=self.nb_controls.GetPage(1).GetWin(),
        	value=self.center_freq_hop_button,
        	callback=self.set_center_freq_hop_button,
        	label="Center Freq Hop",
        	choices=[0,1],
        	labels=["Disabled","Enabled"],
        )
        self.nb_controls.GetPage(1).GridAdd(self._center_freq_hop_button_chooser, 2, 0, 1, 1)
        self.blocks_probe_signal_vx_fft = blocks.probe_signal_vf(fft_len)
        (self.blocks_probe_signal_vx_fft).set_processor_affinity([1])
        self.wxgui_waterfallsink2_0_1_0 = waterfallsink2.waterfall_sink_c(
        	self.nb_gfx.GetPage(5).GetWin(),
        	baseband_freq=max_channel_freq,
        	dynamic_range=50,
        	ref_level=gui_ref_level,
        	ref_scale=2.0,
        	sample_rate=channel_samp_rate,
        	fft_size=2**10,
        	fft_rate=4,
        	average=True,
        	avg_alpha=0.25,
        	title="Waterfall Fine Tune",
        	size=(gui_sizes),
        )
        self.nb_gfx.GetPage(5).GridAdd(self.wxgui_waterfallsink2_0_1_0.win, 0, 0, 1, 1)
        def wxgui_waterfallsink2_0_1_0_callback(x, y):
        	self.set_channel_click_freq(x)
        
        self.wxgui_waterfallsink2_0_1_0.set_callback(wxgui_waterfallsink2_0_1_0_callback)
        self.wxgui_waterfallsink2_0_1 = waterfallsink2.waterfall_sink_c(
        	self.nb_gfx.GetPage(4).GetWin(),
        	baseband_freq=float(center_freq),
        	dynamic_range=50,
        	ref_level=gui_ref_level,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=2**10,
        	fft_rate=4,
        	average=True,
        	avg_alpha=0.25,
        	title="Waterfall Fine Tune",
        	size=(gui_sizes),
        )
        self.nb_gfx.GetPage(4).GridAdd(self.wxgui_waterfallsink2_0_1.win, 0, 0, 1, 1)
        def wxgui_waterfallsink2_0_1_callback(x, y):
        	self.set_channel_click_freq(x)
        
        self.wxgui_waterfallsink2_0_1.set_callback(wxgui_waterfallsink2_0_1_callback)
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.nb_gfx.GetPage(3).GetWin(),
        	baseband_freq=float(center_freq),
        	dynamic_range=50,
        	ref_level=gui_ref_level,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=2**10,
        	fft_rate=4,
        	average=True,
        	avg_alpha=0.25,
        	title="Waterfall Rough Tune",
        	size=(gui_sizes),
        )
        self.nb_gfx.GetPage(3).GridAdd(self.wxgui_waterfallsink2_0.win, 0, 0, 1, 1)
        def wxgui_waterfallsink2_0_callback(x, y):
        	self.set_txt_center_freq(x)
        
        self.wxgui_waterfallsink2_0.set_callback(wxgui_waterfallsink2_0_callback)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_c(
        	self.nb_gfx.GetPage(6).GetWin(),
        	title="Scope Zoom",
        	sample_rate=quad_samp_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=True,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_NORM,
        	y_axis_label="Counts",
        	size=(gui_sizes),
        )
        self.nb_gfx.GetPage(6).GridAdd(self.wxgui_scopesink2_0.win, 0, 0, 1, 1)
        self.wxgui_fftsink2_1_0_0_1_0 = fftsink2.fft_sink_c(
        	self.nb_gfx.GetPage(1).GetWin(),
        	baseband_freq=float(center_freq),
        	y_per_div=10,
        	y_divs=10,
        	ref_level=gui_ref_level,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=gui_fft_size,
        	fft_rate=gui_refresh_rate,
        	average=True,
        	avg_alpha=gui_average,
        	title="FFT Fine Tune",
        	peak_hold=False,
        	win=window.hamming,
        	size=(gui_sizes),
        )
        self.nb_gfx.GetPage(1).GridAdd(self.wxgui_fftsink2_1_0_0_1_0.win, 0, 0, 1, 1)
        def wxgui_fftsink2_1_0_0_1_0_callback(x, y):
        	self.set_channel_click_freq(x)
        
        self.wxgui_fftsink2_1_0_0_1_0.set_callback(wxgui_fftsink2_1_0_0_1_0_callback)
        self.wxgui_fftsink2_1_0_0_1 = fftsink2.fft_sink_c(
        	self.nb_gfx.GetPage(0).GetWin(),
        	baseband_freq=float(center_freq),
        	y_per_div=10,
        	y_divs=10,
        	ref_level=gui_ref_level,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=gui_fft_size,
        	fft_rate=gui_refresh_rate,
        	average=True,
        	avg_alpha=gui_average,
        	title="FFT Rough Tune",
        	peak_hold=False,
        	win=window.hamming,
        	size=(gui_sizes),
        )
        self.nb_gfx.GetPage(0).GridAdd(self.wxgui_fftsink2_1_0_0_1.win, 0, 0, 1, 1)
        def wxgui_fftsink2_1_0_0_1_callback(x, y):
        	self.set_txt_center_freq(x)
        
        self.wxgui_fftsink2_1_0_0_1.set_callback(wxgui_fftsink2_1_0_0_1_callback)
        self.wxgui_fftsink2_1_0_0_0 = fftsink2.fft_sink_c(
        	self.nb_gfx.GetPage(2).GetWin(),
        	baseband_freq=max_channel_freq,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=-10,
        	ref_scale=2.0,
        	sample_rate=quad_samp_rate,
        	fft_size=gui_fft_size,
        	fft_rate=gui_refresh_rate,
        	average=True,
        	avg_alpha=gui_average,
        	title="FFT Zoom",
        	peak_hold=False,
        	size=(gui_sizes),
        )
        self.nb_gfx.GetPage(2).GridAdd(self.wxgui_fftsink2_1_0_0_0.win, 0, 0, 1, 1)
        def wxgui_fftsink2_1_0_0_0_callback(x, y):
        	self.set_channel_click_freq(x)
        
        self.wxgui_fftsink2_1_0_0_0.set_callback(wxgui_fftsink2_1_0_0_0_callback)
        self.uhd_usrp_source_0_0_1_0 = uhd.usrp_source(
        	",".join(("addr=192.168.10.1", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0_0_1_0.set_clock_source("external", 0)
        self.uhd_usrp_source_0_0_1_0.set_time_source("external", 0)
        self.uhd_usrp_source_0_0_1_0.set_subdev_spec("A:B", 0)
        self.uhd_usrp_source_0_0_1_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0_0_1_0.set_center_freq(uhd.tune_request(center_freq, rf_freq=(center_freq + lo_offset),rf_freq_policy=uhd.tune_request.POLICY_MANUAL), 0)
        self.uhd_usrp_source_0_0_1_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0_0_1_0.set_antenna("RXB", 0)
        (self.uhd_usrp_source_0_0_1_0).set_processor_affinity([1])
        self._txt_center_freq_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(0).GetWin(),
        	value=self.txt_center_freq,
        	callback=self.set_txt_center_freq,
        	label="Center Freq",
        	converter=forms.float_converter(),
        )
        self.nb_controls.GetPage(0).GridAdd(self._txt_center_freq_text_box, 0, 0, 1, 1)
        self._txt_blocked_freq_list_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(1).GetWin(),
        	value=self.txt_blocked_freq_list,
        	callback=self.set_txt_blocked_freq_list,
        	label="Blocked Freqs (Hz, Space Separated)",
        	converter=forms.str_converter(),
        )
        self.nb_controls.GetPage(1).GridAdd(self._txt_blocked_freq_list_text_box, 0, 0, 1, 50)
        self._spectrum_sense_button_chooser = forms.button(
        	parent=self.nb_controls.GetPage(1).GetWin(),
        	value=self.spectrum_sense_button,
        	callback=self.set_spectrum_sense_button,
        	label="Spectrum Sense",
        	choices=[0,1],
        	labels=["Disabled","Enabled"],
        )
        self.nb_controls.GetPage(1).GridAdd(self._spectrum_sense_button_chooser, 1, 0, 1, 1)
        self.modulation_selector_out = grc_blks2.selector(
        	item_size=gr.sizeof_float*1,
        	num_inputs=5,
        	num_outputs=1,
        	input_index=modulation,
        	output_index=0,
        )
        (self.modulation_selector_out).set_processor_affinity([1])
        self.modulation_selector_in_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*fft_len,
        	num_inputs=1,
        	num_outputs=2,
        	input_index=0,
        	output_index=0 if (func_quad_avg_mag_sqrd_unmuted) else 1,
        )
        (self.modulation_selector_in_0).set_processor_affinity([1])
        self.modulation_selector_in = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=1,
        	num_outputs=5,
        	input_index=0,
        	output_index=modulation,
        )
        (self.modulation_selector_in).set_processor_affinity([1])
        self.fft_vxx_0_0 = fft.fft_vcc(combined_ch_bins, False, (), True, 1)
        (self.fft_vxx_0_0).set_processor_affinity([1])
        self.fft_vxx_0 = fft.fft_vcc(fft_len, True, (), True, 1)
        (self.fft_vxx_0).set_processor_affinity([1])
        def _fft_signal_level_probe():
            while True:
                val = self.blocks_probe_signal_vx_fft.level()
                try:
                    self.set_fft_signal_level(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (float(func_probe_rate)/1))
        _fft_signal_level_thread = threading.Thread(target=_fft_signal_level_probe)
        _fft_signal_level_thread.daemon = True
        _fft_signal_level_thread.start()
        self.fft_filter_xxx_0_0_0_0 = filter.fft_filter_ccc(quad_decim, ((firdes.complex_band_pass_2(1, channel_samp_rate, -ch_width, 1, ch_trans, 40, firdes.WIN_HAMMING, 6.76)) if (modulation == 2) else ((firdes.complex_band_pass_2(1, channel_samp_rate, -1, ch_width, ch_trans, 40, firdes.WIN_HAMMING, 6.76)) if (modulation == 3) else (firdes.low_pass_2(1, channel_samp_rate, ch_width, ch_trans, 40, firdes.WIN_HAMMING, 6.76)))), 1)
        self.fft_filter_xxx_0_0_0_0.declare_sample_delay(0)
        (self.fft_filter_xxx_0_0_0_0).set_processor_affinity([1])
        self._channel_click_freq_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(0).GetWin(),
        	value=self.channel_click_freq,
        	callback=self.set_channel_click_freq,
        	label="Click Freq",
        	converter=forms.float_converter(),
        )
        self.nb_controls.GetPage(0).GridAdd(self._channel_click_freq_text_box, 0, 1, 1, 1)
        self._ch_step_size_chooser = forms.drop_down(
        	parent=self.nb_controls.GetPage(0).GetWin(),
        	value=self.ch_step_size,
        	callback=self.set_ch_step_size,
        	label='ch_step_size',
        	choices=[1,10,100,1e3, 2.5e3, 5e3, 6.25e3, 8.33e3, 12.5e3, 25e3, 50e3,100e3, 200e3],
        	labels=["1","10","100","1e3", "2.5e3", "5e3", "6.25e3", "8.33e3", "12.5e3", "25e3", "50e3","100e3", "200e3"],
        )
        self.nb_controls.GetPage(0).GridAdd(self._ch_step_size_chooser, 0, 4, 1, 1)
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, combined_ch_bins)
        (self.blocks_vector_to_stream_0_0).set_processor_affinity([1])
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, fft_len)
        (self.blocks_vector_to_stream_0).set_processor_affinity([1])
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, combined_ch_bins)
        (self.blocks_stream_to_vector_0_0).set_processor_affinity([1])
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_len)
        (self.blocks_stream_to_vector_0).set_processor_affinity([1])
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*fft_len)
        (self.blocks_null_sink_0).set_processor_affinity([1])
        self.blocks_multiply_const_vxx_1_1_0 = blocks.multiply_const_vff((float(volume)/10, ))
        (self.blocks_multiply_const_vxx_1_1_0).set_processor_affinity([1])
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((0, ))
        self.blocks_keep_m_in_n_0_0 = blocks.keep_m_in_n(gr.sizeof_gr_complex, combined_ch_bins, fft_len, int(bin_index-(float(combined_ch_bins)/2)))
        (self.blocks_keep_m_in_n_0_0).set_processor_affinity([1])
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        (self.blocks_float_to_complex_0).set_processor_affinity([1])
        self.blocks_complex_to_real_2 = blocks.complex_to_real(1)
        (self.blocks_complex_to_real_2).set_processor_affinity([1])
        self.blocks_complex_to_real_1_1 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_1_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_1 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_mag_0_0 = blocks.complex_to_mag(fft_len)
        (self.blocks_complex_to_mag_0_0).set_processor_affinity([1])
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.audio_sink_0_0 = audio.sink(int(audio_samp_rate*1), "", True)
        (self.audio_sink_0_0).set_processor_affinity([1])
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(squelch_threshold, 0.001, 1, True)
        (self.analog_pwr_squelch_xx_0).set_processor_affinity([1])
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=int(audio_samp_rate),
        	quad_rate=int(quad_samp_rate),
        	tau=50e-6,
        	max_dev=5e3,
        )
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, center_freq if (not center_freq_hop_button) else (min_center_freq if ((func_center_freq[0] > max_center_freq) or (func_center_freq[0] < min_center_freq)) else (func_center_freq[0] + center_freq_step)) if (not func_quad_avg_mag_sqrd_unmuted) else center_freq)
        self.analog_am_demod_cf_0 = analog.am_demod_cf(
        	channel_rate=quad_samp_rate,
        	audio_decim=audio_decim,
        	audio_pass=12500,
        	audio_stop=25000,
        )
        (self.analog_am_demod_cf_0).set_processor_affinity([1])

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_am_demod_cf_0, 0), (self.modulation_selector_out, 0))    
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.analog_nbfm_rx_0, 0), (self.modulation_selector_out, 1))    
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.blocks_complex_to_real_1_0, 0))    
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.modulation_selector_in, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.probe_center_freq, 0))    
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self.blocks_probe_signal_vx_fft, 0))    
        self.connect((self.blocks_complex_to_real_0, 0), (self.modulation_selector_out, 2))    
        self.connect((self.blocks_complex_to_real_1, 0), (self.modulation_selector_out, 3))    
        self.connect((self.blocks_complex_to_real_1_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_complex_to_real_1_1, 0), (self.modulation_selector_out, 4))    
        self.connect((self.blocks_complex_to_real_2, 0), (self.blocks_multiply_const_vxx_1_1_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_complex_to_real_2, 0))    
        self.connect((self.blocks_keep_m_in_n_0_0, 0), (self.blocks_stream_to_vector_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.blocks_multiply_const_vxx_1_1_0, 0), (self.audio_sink_0_0, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))    
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0_0, 0))    
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_keep_m_in_n_0_0, 0))    
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.fft_filter_xxx_0_0_0_0, 0))    
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.wxgui_fftsink2_1_0_0_0, 0))    
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.wxgui_waterfallsink2_0_1_0, 0))    
        self.connect((self.fft_filter_xxx_0_0_0_0, 0), (self.analog_pwr_squelch_xx_0, 0))    
        self.connect((self.fft_filter_xxx_0_0_0_0, 0), (self.probe_avg_mag_sqrd, 0))    
        self.connect((self.fft_filter_xxx_0_0_0_0, 0), (self.wxgui_scopesink2_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.blocks_vector_to_stream_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.modulation_selector_in_0, 0))    
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_vector_to_stream_0_0, 0))    
        self.connect((self.modulation_selector_in, 0), (self.analog_am_demod_cf_0, 0))    
        self.connect((self.modulation_selector_in, 1), (self.analog_nbfm_rx_0, 0))    
        self.connect((self.modulation_selector_in, 2), (self.blocks_complex_to_real_0, 0))    
        self.connect((self.modulation_selector_in, 3), (self.blocks_complex_to_real_1, 0))    
        self.connect((self.modulation_selector_in, 4), (self.blocks_complex_to_real_1_1, 0))    
        self.connect((self.modulation_selector_in_0, 1), (self.blocks_complex_to_mag_0_0, 0))    
        self.connect((self.modulation_selector_in_0, 0), (self.blocks_null_sink_0, 0))    
        self.connect((self.modulation_selector_out, 0), (self.blocks_float_to_complex_0, 0))    
        self.connect((self.uhd_usrp_source_0_0_1_0, 0), (self.blocks_stream_to_vector_0, 0))    
        self.connect((self.uhd_usrp_source_0_0_1_0, 0), (self.wxgui_fftsink2_1_0_0_1, 0))    
        self.connect((self.uhd_usrp_source_0_0_1_0, 0), (self.wxgui_fftsink2_1_0_0_1_0, 0))    
        self.connect((self.uhd_usrp_source_0_0_1_0, 0), (self.wxgui_waterfallsink2_0, 0))    
        self.connect((self.uhd_usrp_source_0_0_1_0, 0), (self.wxgui_waterfallsink2_0_1, 0))    


    def get_cfg_min_center_freq(self):
        return self.cfg_min_center_freq

    def set_cfg_min_center_freq(self, cfg_min_center_freq):
        self.cfg_min_center_freq = cfg_min_center_freq
        self.set_min_center_freq(self.cfg_min_center_freq)

    def get_min_center_freq(self):
        return self.min_center_freq

    def set_min_center_freq(self, min_center_freq):
        self.min_center_freq = min_center_freq
        self._cfg_min_center_freq_config = ConfigParser.ConfigParser()
        self._cfg_min_center_freq_config.read(".scanoo")
        if not self._cfg_min_center_freq_config.has_section("main"):
        	self._cfg_min_center_freq_config.add_section("main")
        self._cfg_min_center_freq_config.set("main", "min_center_freq", str(self.min_center_freq))
        self._cfg_min_center_freq_config.write(open(".scanoo", 'w'))
        self._min_center_freq_text_box.set_value(self.min_center_freq)
        self.set_func_center_freq([self.min_center_freq])
        self.analog_const_source_x_0.set_offset(self.center_freq if (not self.center_freq_hop_button) else (self.min_center_freq if ((self.func_center_freq[0] > self.max_center_freq) or (self.func_center_freq[0] < self.min_center_freq)) else (self.func_center_freq[0] + self.center_freq_step)) if (not self.func_quad_avg_mag_sqrd_unmuted) else self.center_freq)

    def get_cfg_samp_rate(self):
        return self.cfg_samp_rate

    def set_cfg_samp_rate(self, cfg_samp_rate):
        self.cfg_samp_rate = cfg_samp_rate
        self.set_samp_rate(self.cfg_samp_rate)

    def get_cfg_blocked_freq_list(self):
        return self.cfg_blocked_freq_list

    def set_cfg_blocked_freq_list(self, cfg_blocked_freq_list):
        self.cfg_blocked_freq_list = cfg_blocked_freq_list
        self.set_txt_blocked_freq_list(self.cfg_blocked_freq_list)

    def get_txt_center_freq(self):
        return self.txt_center_freq

    def set_txt_center_freq(self, txt_center_freq):
        self.txt_center_freq = txt_center_freq
        self.set_center_freq(int(self.func_center_freq[0]) if ((self.func_center_freq[0] > 0) and (self.center_freq_hop_button)) else int(self.txt_center_freq))
        self._txt_center_freq_text_box.set_value(self.txt_center_freq)

    def get_txt_blocked_freq_list(self):
        return self.txt_blocked_freq_list

    def set_txt_blocked_freq_list(self, txt_blocked_freq_list):
        self.txt_blocked_freq_list = txt_blocked_freq_list
        self.set_blocked_freq_list([int(blocked_freq) for blocked_freq in self.txt_blocked_freq_list.split()])
        self._cfg_blocked_freq_list_config = ConfigParser.ConfigParser()
        self._cfg_blocked_freq_list_config.read(".scanoo")
        if not self._cfg_blocked_freq_list_config.has_section("main"):
        	self._cfg_blocked_freq_list_config.add_section("main")
        self._cfg_blocked_freq_list_config.set("main", "blocked_freq_list", str(self.txt_blocked_freq_list))
        self._cfg_blocked_freq_list_config.write(open(".scanoo", 'w'))
        self._txt_blocked_freq_list_text_box.set_value(self.txt_blocked_freq_list)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_fft_len(int(float(self.samp_rate)/self.bin_bw))
        self.set_blocked_bin_list([int(math.floor(float(((blocked_freq-(self.center_freq-(self.samp_rate/2)))/self.bin_bw))/self.bin_floor)*self.bin_floor) for blocked_freq in self.blocked_freq_list])
        self.set_left_edge_freq(self.center_freq - (float(self.samp_rate)/2))
        self.set_center_freq_step(self.samp_rate*0.7)
        self.set_lo_offset((self.samp_rate/2)*1.25)
        self.wxgui_fftsink2_1_0_0_1.set_sample_rate(self.samp_rate)
        self._samp_rate_text_box.set_value(self.samp_rate)
        self.wxgui_fftsink2_1_0_0_1_0.set_sample_rate(self.samp_rate)
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
        self.wxgui_waterfallsink2_0_1.set_sample_rate(self.samp_rate)
        self._cfg_samp_rate_config = ConfigParser.ConfigParser()
        self._cfg_samp_rate_config.read(".scanoo")
        if not self._cfg_samp_rate_config.has_section("main"):
        	self._cfg_samp_rate_config.add_section("main")
        self._cfg_samp_rate_config.set("main", "samp_rate", str(self.samp_rate))
        self._cfg_samp_rate_config.write(open(".scanoo", 'w'))
        self.uhd_usrp_source_0_0_1_0.set_samp_rate(self.samp_rate)

    def get_func_center_freq(self):
        return self.func_center_freq

    def set_func_center_freq(self, func_center_freq):
        self.func_center_freq = func_center_freq
        self.set_center_freq(int(self.func_center_freq[0]) if ((self.func_center_freq[0] > 0) and (self.center_freq_hop_button)) else int(self.txt_center_freq))
        self.analog_const_source_x_0.set_offset(self.center_freq if (not self.center_freq_hop_button) else (self.min_center_freq if ((self.func_center_freq[0] > self.max_center_freq) or (self.func_center_freq[0] < self.min_center_freq)) else (self.func_center_freq[0] + self.center_freq_step)) if (not self.func_quad_avg_mag_sqrd_unmuted) else self.center_freq)

    def get_center_freq_hop_button(self):
        return self.center_freq_hop_button

    def set_center_freq_hop_button(self, center_freq_hop_button):
        self.center_freq_hop_button = center_freq_hop_button
        self.set_center_freq(int(self.func_center_freq[0]) if ((self.func_center_freq[0] > 0) and (self.center_freq_hop_button)) else int(self.txt_center_freq))
        self._center_freq_hop_button_chooser.set_value(self.center_freq_hop_button)
        self.analog_const_source_x_0.set_offset(self.center_freq if (not self.center_freq_hop_button) else (self.min_center_freq if ((self.func_center_freq[0] > self.max_center_freq) or (self.func_center_freq[0] < self.min_center_freq)) else (self.func_center_freq[0] + self.center_freq_step)) if (not self.func_quad_avg_mag_sqrd_unmuted) else self.center_freq)

    def get_bin_bw(self):
        return self.bin_bw

    def set_bin_bw(self, bin_bw):
        self.bin_bw = bin_bw
        self.set_fft_len(int(float(self.samp_rate)/self.bin_bw))
        self.set_combined_ch_bins(int(float(self.channel_samp_rate)/self.bin_bw))
        self.set_bin_floor(int(150e3/self.bin_bw))
        self.set_blocked_bin_list([int(math.floor(float(((blocked_freq-(self.center_freq-(self.samp_rate/2)))/self.bin_bw))/self.bin_floor)*self.bin_floor) for blocked_freq in self.blocked_freq_list])
        self.set_bin_index(self.max_bin_index if self.spectrum_sense_button else (float(self.channel_click_freq_rounded - self.left_edge_freq)/self.bin_bw))
        self.set_max_channel_freq((round(float(self.left_edge_freq+(self.bin_bw*self.bin_index))/ self.ch_step_size, 0) * self.ch_step_size))

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.blocks_keep_m_in_n_0_0.set_n(self.fft_len)
        self.set_fft_signal_level([0.0]*(self.fft_len))

    def get_cfg_ch_step_size(self):
        return self.cfg_ch_step_size

    def set_cfg_ch_step_size(self, cfg_ch_step_size):
        self.cfg_ch_step_size = cfg_ch_step_size
        self.set_ch_step_size(self.cfg_ch_step_size)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.set_blocked_bin_list([int(math.floor(float(((blocked_freq-(self.center_freq-(self.samp_rate/2)))/self.bin_bw))/self.bin_floor)*self.bin_floor) for blocked_freq in self.blocked_freq_list])
        self.set_left_edge_freq(self.center_freq - (float(self.samp_rate)/2))
        self.wxgui_fftsink2_1_0_0_1.set_baseband_freq(float(self.center_freq))
        self.analog_const_source_x_0.set_offset(self.center_freq if (not self.center_freq_hop_button) else (self.min_center_freq if ((self.func_center_freq[0] > self.max_center_freq) or (self.func_center_freq[0] < self.min_center_freq)) else (self.func_center_freq[0] + self.center_freq_step)) if (not self.func_quad_avg_mag_sqrd_unmuted) else self.center_freq)
        self.wxgui_fftsink2_1_0_0_1_0.set_baseband_freq(float(self.center_freq))
        self.wxgui_waterfallsink2_0.set_baseband_freq(float(self.center_freq))
        self.wxgui_waterfallsink2_0_1.set_baseband_freq(float(self.center_freq))
        self.uhd_usrp_source_0_0_1_0.set_center_freq(uhd.tune_request(self.center_freq, rf_freq=(self.center_freq + self.lo_offset),rf_freq_policy=uhd.tune_request.POLICY_MANUAL), 0)

    def get_blocked_freq_list(self):
        return self.blocked_freq_list

    def set_blocked_freq_list(self, blocked_freq_list):
        self.blocked_freq_list = blocked_freq_list
        self.set_blocked_bin_list([int(math.floor(float(((blocked_freq-(self.center_freq-(self.samp_rate/2)))/self.bin_bw))/self.bin_floor)*self.bin_floor) for blocked_freq in self.blocked_freq_list])

    def get_bin_floor(self):
        return self.bin_floor

    def set_bin_floor(self, bin_floor):
        self.bin_floor = bin_floor
        self.set_blocked_bin_list([int(math.floor(float(((blocked_freq-(self.center_freq-(self.samp_rate/2)))/self.bin_bw))/self.bin_floor)*self.bin_floor) for blocked_freq in self.blocked_freq_list])
        self.set_max_bin_index(int(self.fft_signal_level.index(max([i for j, i in enumerate(self.fft_signal_level) if (int(math.floor(float(j)/self.bin_floor)*self.bin_floor) not in self.blocked_bin_list )]))))

    def get_fft_signal_level(self):
        return self.fft_signal_level

    def set_fft_signal_level(self, fft_signal_level):
        self.fft_signal_level = fft_signal_level
        self.set_max_bin_index(int(self.fft_signal_level.index(max([i for j, i in enumerate(self.fft_signal_level) if (int(math.floor(float(j)/self.bin_floor)*self.bin_floor) not in self.blocked_bin_list )]))))

    def get_channel_click_freq(self):
        return self.channel_click_freq

    def set_channel_click_freq(self, channel_click_freq):
        self.channel_click_freq = channel_click_freq
        self.set_channel_click_freq_rounded((round(float(self.channel_click_freq) / self.ch_step_size, 0) * self.ch_step_size))
        self._channel_click_freq_text_box.set_value(self.channel_click_freq)

    def get_ch_step_size(self):
        return self.ch_step_size

    def set_ch_step_size(self, ch_step_size):
        self.ch_step_size = ch_step_size
        self.set_channel_click_freq_rounded((round(float(self.channel_click_freq) / self.ch_step_size, 0) * self.ch_step_size))
        self._ch_step_size_chooser.set_value(self.ch_step_size)
        self.set_max_channel_freq((round(float(self.left_edge_freq+(self.bin_bw*self.bin_index))/ self.ch_step_size, 0) * self.ch_step_size))
        self._cfg_ch_step_size_config = ConfigParser.ConfigParser()
        self._cfg_ch_step_size_config.read(".scanoo")
        if not self._cfg_ch_step_size_config.has_section("main"):
        	self._cfg_ch_step_size_config.add_section("main")
        self._cfg_ch_step_size_config.set("main", "ch_step_size", str(self.ch_step_size))
        self._cfg_ch_step_size_config.write(open(".scanoo", 'w'))

    def get_blocked_bin_list(self):
        return self.blocked_bin_list

    def set_blocked_bin_list(self, blocked_bin_list):
        self.blocked_bin_list = blocked_bin_list
        self.set_max_bin_index(int(self.fft_signal_level.index(max([i for j, i in enumerate(self.fft_signal_level) if (int(math.floor(float(j)/self.bin_floor)*self.bin_floor) not in self.blocked_bin_list )]))))

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate
        self.set_quad_samp_rate(self.audio_samp_rate*1)
        self.set_audio_decim(int(self.quad_samp_rate/self.audio_samp_rate))

    def get_spectrum_sense_button(self):
        return self.spectrum_sense_button

    def set_spectrum_sense_button(self, spectrum_sense_button):
        self.spectrum_sense_button = spectrum_sense_button
        self.set_bin_index(self.max_bin_index if self.spectrum_sense_button else (float(self.channel_click_freq_rounded - self.left_edge_freq)/self.bin_bw))
        self._spectrum_sense_button_chooser.set_value(self.spectrum_sense_button)

    def get_quad_samp_rate(self):
        return self.quad_samp_rate

    def set_quad_samp_rate(self, quad_samp_rate):
        self.quad_samp_rate = quad_samp_rate
        self.set_audio_decim(int(self.quad_samp_rate/self.audio_samp_rate))
        self.set_quad_decim(int(self.channel_samp_rate/self.quad_samp_rate))
        self.set_channel_samp_rate((self.quad_samp_rate*1))
        self.set_ch_trans(min(self.cfg_ch_trans,int(self.quad_samp_rate*0.99)))
        self.set_ch_width(min(self.cfg_ch_width,((self.quad_samp_rate/2)*0.9)))
        self.wxgui_scopesink2_0.set_sample_rate(self.quad_samp_rate)
        self.wxgui_fftsink2_1_0_0_0.set_sample_rate(self.quad_samp_rate)

    def get_max_bin_index(self):
        return self.max_bin_index

    def set_max_bin_index(self, max_bin_index):
        self.max_bin_index = max_bin_index
        self.set_bin_index(self.max_bin_index if self.spectrum_sense_button else (float(self.channel_click_freq_rounded - self.left_edge_freq)/self.bin_bw))

    def get_left_edge_freq(self):
        return self.left_edge_freq

    def set_left_edge_freq(self, left_edge_freq):
        self.left_edge_freq = left_edge_freq
        self.set_bin_index(self.max_bin_index if self.spectrum_sense_button else (float(self.channel_click_freq_rounded - self.left_edge_freq)/self.bin_bw))
        self.set_max_channel_freq((round(float(self.left_edge_freq+(self.bin_bw*self.bin_index))/ self.ch_step_size, 0) * self.ch_step_size))

    def get_channel_click_freq_rounded(self):
        return self.channel_click_freq_rounded

    def set_channel_click_freq_rounded(self, channel_click_freq_rounded):
        self.channel_click_freq_rounded = channel_click_freq_rounded
        self.set_bin_index(self.max_bin_index if self.spectrum_sense_button else (float(self.channel_click_freq_rounded - self.left_edge_freq)/self.bin_bw))

    def get_channel_samp_rate(self):
        return self.channel_samp_rate

    def set_channel_samp_rate(self, channel_samp_rate):
        self.channel_samp_rate = channel_samp_rate
        self.set_combined_ch_bins(int(float(self.channel_samp_rate)/self.bin_bw))
        self.set_quad_decim(int(self.channel_samp_rate/self.quad_samp_rate))
        self.wxgui_waterfallsink2_0_1_0.set_sample_rate(self.channel_samp_rate)
        self.fft_filter_xxx_0_0_0_0.set_taps(((firdes.complex_band_pass_2(1, self.channel_samp_rate, -self.ch_width, 1, self.ch_trans, 40, firdes.WIN_HAMMING, 6.76)) if (self.modulation == 2) else ((firdes.complex_band_pass_2(1, self.channel_samp_rate, -1, self.ch_width, self.ch_trans, 40, firdes.WIN_HAMMING, 6.76)) if (self.modulation == 3) else (firdes.low_pass_2(1, self.channel_samp_rate, self.ch_width, self.ch_trans, 40, firdes.WIN_HAMMING, 6.76)))))

    def get_cfg_volume(self):
        return self.cfg_volume

    def set_cfg_volume(self, cfg_volume):
        self.cfg_volume = cfg_volume
        self.set_volume(self.cfg_volume)

    def get_cfg_squelch_threshold(self):
        return self.cfg_squelch_threshold

    def set_cfg_squelch_threshold(self, cfg_squelch_threshold):
        self.cfg_squelch_threshold = cfg_squelch_threshold
        self.set_squelch_threshold(self.cfg_squelch_threshold)

    def get_cfg_rx_gain(self):
        return self.cfg_rx_gain

    def set_cfg_rx_gain(self, cfg_rx_gain):
        self.cfg_rx_gain = cfg_rx_gain
        self.set_rx_gain(self.cfg_rx_gain)

    def get_cfg_modulation(self):
        return self.cfg_modulation

    def set_cfg_modulation(self, cfg_modulation):
        self.cfg_modulation = cfg_modulation
        self.set_modulation(self.cfg_modulation)

    def get_cfg_max_center_freq(self):
        return self.cfg_max_center_freq

    def set_cfg_max_center_freq(self, cfg_max_center_freq):
        self.cfg_max_center_freq = cfg_max_center_freq
        self.set_max_center_freq(self.cfg_max_center_freq)

    def get_cfg_ch_width(self):
        return self.cfg_ch_width

    def set_cfg_ch_width(self, cfg_ch_width):
        self.cfg_ch_width = cfg_ch_width
        self.set_ch_width(min(self.cfg_ch_width,((self.quad_samp_rate/2)*0.9)))

    def get_cfg_ch_trans(self):
        return self.cfg_ch_trans

    def set_cfg_ch_trans(self, cfg_ch_trans):
        self.cfg_ch_trans = cfg_ch_trans
        self.set_ch_trans(min(self.cfg_ch_trans,int(self.quad_samp_rate*0.99)))

    def get_bin_index(self):
        return self.bin_index

    def set_bin_index(self, bin_index):
        self.bin_index = bin_index
        self.set_max_channel_freq((round(float(self.left_edge_freq+(self.bin_bw*self.bin_index))/ self.ch_step_size, 0) * self.ch_step_size))
        self.blocks_keep_m_in_n_0_0.set_offset(int(self.bin_index-(float(self.combined_ch_bins)/2)))

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self._volume_slider.set_value(self.volume)
        self._volume_text_box.set_value(self.volume)
        self._cfg_volume_config = ConfigParser.ConfigParser()
        self._cfg_volume_config.read(".scanoo")
        if not self._cfg_volume_config.has_section("main"):
        	self._cfg_volume_config.add_section("main")
        self._cfg_volume_config.set("main", "volume", str(self.volume))
        self._cfg_volume_config.write(open(".scanoo", 'w'))
        self.blocks_multiply_const_vxx_1_1_0.set_k((float(self.volume)/10, ))

    def get_squelch_threshold(self):
        return self.squelch_threshold

    def set_squelch_threshold(self, squelch_threshold):
        self.squelch_threshold = squelch_threshold
        self._cfg_squelch_threshold_config = ConfigParser.ConfigParser()
        self._cfg_squelch_threshold_config.read(".scanoo")
        if not self._cfg_squelch_threshold_config.has_section("main"):
        	self._cfg_squelch_threshold_config.add_section("main")
        self._cfg_squelch_threshold_config.set("main", "squelch_threshold", str(self.squelch_threshold))
        self._cfg_squelch_threshold_config.write(open(".scanoo", 'w'))
        self._squelch_threshold_slider.set_value(self.squelch_threshold)
        self._squelch_threshold_text_box.set_value(self.squelch_threshold)
        self.probe_avg_mag_sqrd.set_threshold(self.squelch_threshold)
        self.analog_pwr_squelch_xx_0.set_threshold(self.squelch_threshold)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self._rx_gain_slider.set_value(self.rx_gain)
        self._rx_gain_text_box.set_value(self.rx_gain)
        self._cfg_rx_gain_config = ConfigParser.ConfigParser()
        self._cfg_rx_gain_config.read(".scanoo")
        if not self._cfg_rx_gain_config.has_section("main"):
        	self._cfg_rx_gain_config.add_section("main")
        self._cfg_rx_gain_config.set("main", "rx_gain", str(self.rx_gain))
        self._cfg_rx_gain_config.write(open(".scanoo", 'w'))
        self.uhd_usrp_source_0_0_1_0.set_gain(self.rx_gain, 0)

    def get_quad_decim(self):
        return self.quad_decim

    def set_quad_decim(self, quad_decim):
        self.quad_decim = quad_decim

    def get_modulation(self):
        return self.modulation

    def set_modulation(self, modulation):
        self.modulation = modulation
        self._cfg_modulation_config = ConfigParser.ConfigParser()
        self._cfg_modulation_config.read(".scanoo")
        if not self._cfg_modulation_config.has_section("main"):
        	self._cfg_modulation_config.add_section("main")
        self._cfg_modulation_config.set("main", "modulation", str(self.modulation))
        self._cfg_modulation_config.write(open(".scanoo", 'w'))
        self._modulation_chooser.set_value(self.modulation)
        self.modulation_selector_out.set_input_index(int(self.modulation))
        self.modulation_selector_in.set_output_index(int(self.modulation))
        self.fft_filter_xxx_0_0_0_0.set_taps(((firdes.complex_band_pass_2(1, self.channel_samp_rate, -self.ch_width, 1, self.ch_trans, 40, firdes.WIN_HAMMING, 6.76)) if (self.modulation == 2) else ((firdes.complex_band_pass_2(1, self.channel_samp_rate, -1, self.ch_width, self.ch_trans, 40, firdes.WIN_HAMMING, 6.76)) if (self.modulation == 3) else (firdes.low_pass_2(1, self.channel_samp_rate, self.ch_width, self.ch_trans, 40, firdes.WIN_HAMMING, 6.76)))))

    def get_max_channel_freq(self):
        return self.max_channel_freq

    def set_max_channel_freq(self, max_channel_freq):
        self.max_channel_freq = max_channel_freq
        self._max_channel_freq_text_box.set_value(self.max_channel_freq)
        self.wxgui_waterfallsink2_0_1_0.set_baseband_freq(self.max_channel_freq)
        self.wxgui_fftsink2_1_0_0_0.set_baseband_freq(self.max_channel_freq)

    def get_max_center_freq(self):
        return self.max_center_freq

    def set_max_center_freq(self, max_center_freq):
        self.max_center_freq = max_center_freq
        self._cfg_max_center_freq_config = ConfigParser.ConfigParser()
        self._cfg_max_center_freq_config.read(".scanoo")
        if not self._cfg_max_center_freq_config.has_section("main"):
        	self._cfg_max_center_freq_config.add_section("main")
        self._cfg_max_center_freq_config.set("main", "max_center_freq", str(self.max_center_freq))
        self._cfg_max_center_freq_config.write(open(".scanoo", 'w'))
        self._max_center_freq_text_box.set_value(self.max_center_freq)
        self.analog_const_source_x_0.set_offset(self.center_freq if (not self.center_freq_hop_button) else (self.min_center_freq if ((self.func_center_freq[0] > self.max_center_freq) or (self.func_center_freq[0] < self.min_center_freq)) else (self.func_center_freq[0] + self.center_freq_step)) if (not self.func_quad_avg_mag_sqrd_unmuted) else self.center_freq)

    def get_lo_offset(self):
        return self.lo_offset

    def set_lo_offset(self, lo_offset):
        self.lo_offset = lo_offset
        self._lo_offset_slider.set_value(self.lo_offset)
        self._lo_offset_text_box.set_value(self.lo_offset)
        self.uhd_usrp_source_0_0_1_0.set_center_freq(uhd.tune_request(self.center_freq, rf_freq=(self.center_freq + self.lo_offset),rf_freq_policy=uhd.tune_request.POLICY_MANUAL), 0)

    def get_gui_sizes(self):
        return self.gui_sizes

    def set_gui_sizes(self, gui_sizes):
        self.gui_sizes = gui_sizes

    def get_gui_refresh_rate(self):
        return self.gui_refresh_rate

    def set_gui_refresh_rate(self, gui_refresh_rate):
        self.gui_refresh_rate = gui_refresh_rate

    def get_gui_ref_level(self):
        return self.gui_ref_level

    def set_gui_ref_level(self, gui_ref_level):
        self.gui_ref_level = gui_ref_level

    def get_gui_fft_size(self):
        return self.gui_fft_size

    def set_gui_fft_size(self, gui_fft_size):
        self.gui_fft_size = gui_fft_size

    def get_gui_average(self):
        return self.gui_average

    def set_gui_average(self, gui_average):
        self.gui_average = gui_average

    def get_func_quad_avg_mag_sqrd_unmuted(self):
        return self.func_quad_avg_mag_sqrd_unmuted

    def set_func_quad_avg_mag_sqrd_unmuted(self, func_quad_avg_mag_sqrd_unmuted):
        self.func_quad_avg_mag_sqrd_unmuted = func_quad_avg_mag_sqrd_unmuted
        self.modulation_selector_in_0.set_output_index(int(0 if (self.func_quad_avg_mag_sqrd_unmuted) else 1))
        self.analog_const_source_x_0.set_offset(self.center_freq if (not self.center_freq_hop_button) else (self.min_center_freq if ((self.func_center_freq[0] > self.max_center_freq) or (self.func_center_freq[0] < self.min_center_freq)) else (self.func_center_freq[0] + self.center_freq_step)) if (not self.func_quad_avg_mag_sqrd_unmuted) else self.center_freq)

    def get_func_probe_rate(self):
        return self.func_probe_rate

    def set_func_probe_rate(self, func_probe_rate):
        self.func_probe_rate = func_probe_rate

    def get_combined_ch_bins(self):
        return self.combined_ch_bins

    def set_combined_ch_bins(self, combined_ch_bins):
        self.combined_ch_bins = combined_ch_bins
        self.blocks_keep_m_in_n_0_0.set_offset(int(self.bin_index-(float(self.combined_ch_bins)/2)))
        self.blocks_keep_m_in_n_0_0.set_m(self.combined_ch_bins)

    def get_ch_width(self):
        return self.ch_width

    def set_ch_width(self, ch_width):
        self.ch_width = ch_width
        self._cfg_ch_width_config = ConfigParser.ConfigParser()
        self._cfg_ch_width_config.read(".scanoo")
        if not self._cfg_ch_width_config.has_section("main"):
        	self._cfg_ch_width_config.add_section("main")
        self._cfg_ch_width_config.set("main", "ch_width", str(self.ch_width))
        self._cfg_ch_width_config.write(open(".scanoo", 'w'))
        self._ch_width_slider.set_value(self.ch_width)
        self._ch_width_text_box.set_value(self.ch_width)
        self.fft_filter_xxx_0_0_0_0.set_taps(((firdes.complex_band_pass_2(1, self.channel_samp_rate, -self.ch_width, 1, self.ch_trans, 40, firdes.WIN_HAMMING, 6.76)) if (self.modulation == 2) else ((firdes.complex_band_pass_2(1, self.channel_samp_rate, -1, self.ch_width, self.ch_trans, 40, firdes.WIN_HAMMING, 6.76)) if (self.modulation == 3) else (firdes.low_pass_2(1, self.channel_samp_rate, self.ch_width, self.ch_trans, 40, firdes.WIN_HAMMING, 6.76)))))

    def get_ch_trans(self):
        return self.ch_trans

    def set_ch_trans(self, ch_trans):
        self.ch_trans = ch_trans
        self._cfg_ch_trans_config = ConfigParser.ConfigParser()
        self._cfg_ch_trans_config.read(".scanoo")
        if not self._cfg_ch_trans_config.has_section("main"):
        	self._cfg_ch_trans_config.add_section("main")
        self._cfg_ch_trans_config.set("main", "ch_trans", str(self.ch_trans))
        self._cfg_ch_trans_config.write(open(".scanoo", 'w'))
        self._ch_trans_slider.set_value(self.ch_trans)
        self._ch_trans_text_box.set_value(self.ch_trans)
        self.fft_filter_xxx_0_0_0_0.set_taps(((firdes.complex_band_pass_2(1, self.channel_samp_rate, -self.ch_width, 1, self.ch_trans, 40, firdes.WIN_HAMMING, 6.76)) if (self.modulation == 2) else ((firdes.complex_band_pass_2(1, self.channel_samp_rate, -1, self.ch_width, self.ch_trans, 40, firdes.WIN_HAMMING, 6.76)) if (self.modulation == 3) else (firdes.low_pass_2(1, self.channel_samp_rate, self.ch_width, self.ch_trans, 40, firdes.WIN_HAMMING, 6.76)))))

    def get_center_freq_step(self):
        return self.center_freq_step

    def set_center_freq_step(self, center_freq_step):
        self.center_freq_step = center_freq_step
        self.analog_const_source_x_0.set_offset(self.center_freq if (not self.center_freq_hop_button) else (self.min_center_freq if ((self.func_center_freq[0] > self.max_center_freq) or (self.func_center_freq[0] < self.min_center_freq)) else (self.func_center_freq[0] + self.center_freq_step)) if (not self.func_quad_avg_mag_sqrd_unmuted) else self.center_freq)

    def get_audio_decim(self):
        return self.audio_decim

    def set_audio_decim(self, audio_decim):
        self.audio_decim = audio_decim

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable realtime scheduling."
    tb = scanoo_com_rx()
    tb.Start(True)
    tb.Wait()
