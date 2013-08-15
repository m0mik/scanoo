#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Scanoo Com Rx
# Author: Mike Jameson M0MIK
# Generated: Thu Aug 15 11:47:44 2013
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import ConfigParser
import math
import osmosdr
import threading
import time
import wx

class scanoo_com_rx(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Scanoo Com Rx")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self._cfg_center_freq_config = ConfigParser.ConfigParser()
        self._cfg_center_freq_config.read(".scanoo")
        try: cfg_center_freq = self._cfg_center_freq_config.getfloat("main", "center_freq")
        except: cfg_center_freq = int(100e6)
        self.cfg_center_freq = cfg_center_freq
        self._cfg_samp_rate_config = ConfigParser.ConfigParser()
        self._cfg_samp_rate_config.read(".scanoo")
        try: cfg_samp_rate = self._cfg_samp_rate_config.getfloat("main", "samp_rate")
        except: cfg_samp_rate = 10e6
        self.cfg_samp_rate = cfg_samp_rate
        self._cfg_blocked_freq_list_config = ConfigParser.ConfigParser()
        self._cfg_blocked_freq_list_config.read(".scanoo")
        try: cfg_blocked_freq_list = self._cfg_blocked_freq_list_config.get("main", "blocked_freq_list")
        except: cfg_blocked_freq_list = ""
        self.cfg_blocked_freq_list = cfg_blocked_freq_list
        self.center_freq = center_freq = cfg_center_freq
        self.txt_blocked_freq_list = txt_blocked_freq_list = cfg_blocked_freq_list
        self.samp_rate = samp_rate = cfg_samp_rate
        self._cfg_channel_click_freq_config = ConfigParser.ConfigParser()
        self._cfg_channel_click_freq_config.read(".scanoo")
        try: cfg_channel_click_freq = self._cfg_channel_click_freq_config.getfloat("main", "channel_click_freq")
        except: cfg_channel_click_freq = int(center_freq)
        self.cfg_channel_click_freq = cfg_channel_click_freq
        self._cfg_ch_step_size_config = ConfigParser.ConfigParser()
        self._cfg_ch_step_size_config.read(".scanoo")
        try: cfg_ch_step_size = self._cfg_ch_step_size_config.getfloat("main", "ch_step_size")
        except: cfg_ch_step_size = 6.25e3
        self.cfg_ch_step_size = cfg_ch_step_size
        self.bin_bw = bin_bw = int(1e3)
        self.fft_len = fft_len = int(samp_rate/bin_bw)
        self.channel_click_freq = channel_click_freq = cfg_channel_click_freq
        self.ch_step_size = ch_step_size = cfg_ch_step_size
        self.blocked_freq_list = blocked_freq_list = [int(blocked_freq) for blocked_freq in txt_blocked_freq_list.split()]
        self.bin_floor = bin_floor = int(50e3/bin_bw)
        self.fft_signal_level = fft_signal_level = [0.0]*(fft_len)
        self.channel_click_freq_rounded = channel_click_freq_rounded = (round(float(channel_click_freq) / ch_step_size, 0) * ch_step_size)
        self.blocked_bin_list = blocked_bin_list = [int(math.floor(float(((blocked_freq-(center_freq-(samp_rate/2)))/bin_bw))/bin_floor)*bin_floor) for blocked_freq in blocked_freq_list]
        self.spectrum_sense_button = spectrum_sense_button = 0
        self.max_bin_index = max_bin_index = int(fft_signal_level.index(max([i for j, i in enumerate(fft_signal_level) if (int(math.floor(float(j)/bin_floor)*bin_floor) not in blocked_bin_list )])))
        self.left_edge_freq = left_edge_freq = center_freq-(samp_rate/2)
        self.channel_freq = channel_freq = channel_click_freq_rounded if ((channel_click_freq_rounded < (center_freq + samp_rate/2)) and (channel_click_freq_rounded > (center_freq - samp_rate/2))) else center_freq
        self.audio_samp_rate = audio_samp_rate = 48e3
        self.quad_samp_rate = quad_samp_rate = audio_samp_rate*4
        self.bin_index = bin_index = max_bin_index if spectrum_sense_button else ((channel_freq - left_edge_freq)/bin_bw)
        self.max_channel_freq = max_channel_freq = int(left_edge_freq+(bin_bw*bin_index))
        self.channel_samp_rate = channel_samp_rate = (quad_samp_rate*4)
        self._cfg_volume_config = ConfigParser.ConfigParser()
        self._cfg_volume_config.read(".scanoo")
        try: cfg_volume = self._cfg_volume_config.getint("main", "volume")
        except: cfg_volume = 1
        self.cfg_volume = cfg_volume
        self._cfg_squelch_threshold_config = ConfigParser.ConfigParser()
        self._cfg_squelch_threshold_config.read(".scanoo")
        try: cfg_squelch_threshold = self._cfg_squelch_threshold_config.getfloat("main", "squelch_threshold")
        except: cfg_squelch_threshold = 15
        self.cfg_squelch_threshold = cfg_squelch_threshold
        self._cfg_rf_gain_config = ConfigParser.ConfigParser()
        self._cfg_rf_gain_config.read(".scanoo")
        try: cfg_rf_gain = self._cfg_rf_gain_config.getint("main", "rf_gain")
        except: cfg_rf_gain = 15
        self.cfg_rf_gain = cfg_rf_gain
        self._cfg_modulation_config = ConfigParser.ConfigParser()
        self._cfg_modulation_config.read(".scanoo")
        try: cfg_modulation = self._cfg_modulation_config.getint("main", "modulation")
        except: cfg_modulation = 0
        self.cfg_modulation = cfg_modulation
        self._cfg_if_gain_config = ConfigParser.ConfigParser()
        self._cfg_if_gain_config.read(".scanoo")
        try: cfg_if_gain = self._cfg_if_gain_config.getint("main", "if_gain")
        except: cfg_if_gain = 15
        self.cfg_if_gain = cfg_if_gain
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
        self._cfg_bb_gain_config = ConfigParser.ConfigParser()
        self._cfg_bb_gain_config.read(".scanoo")
        try: cfg_bb_gain = self._cfg_bb_gain_config.getint("main", "bb_gain")
        except: cfg_bb_gain = 15
        self.cfg_bb_gain = cfg_bb_gain
        self.volume = volume = cfg_volume
        self.txt_max_channel_freq = txt_max_channel_freq = max_channel_freq
        self.squelch_threshold = squelch_threshold = cfg_squelch_threshold
        self.spectrum_sense_rate = spectrum_sense_rate = 2
        self.rf_gain = rf_gain = cfg_rf_gain
        self.quad_decim = quad_decim = int(channel_samp_rate/quad_samp_rate)
        self.modulation = modulation = cfg_modulation
        self.lo_offset = lo_offset = -((samp_rate/2) * 1.25)
        self.if_gain = if_gain = cfg_if_gain
        self.gui_sizes = gui_sizes = [1024,400]
        self.gui_refresh_rate = gui_refresh_rate = 2**4
        self.gui_ref_level = gui_ref_level = -55
        self.gui_fft_size = gui_fft_size = 2**10
        self.gui_average = gui_average = 0.1
        self.func_quad_avg_mag_sqrd = func_quad_avg_mag_sqrd = 0
        self.combined_ch_bins = combined_ch_bins = int(channel_samp_rate/bin_bw)
        self.ch_width = ch_width = min(cfg_ch_width,(quad_samp_rate*0.99))
        self.ch_trans = ch_trans = min(cfg_ch_trans,int(quad_samp_rate*0.99))
        self.bb_gain = bb_gain = cfg_bb_gain
        self.audio_decim = audio_decim = int(quad_samp_rate/audio_samp_rate)

        ##################################################
        # Blocks
        ##################################################
        self.probe_avg_mag_sqrd = analog.probe_avg_mag_sqrd_c(-100, 1)
        self.nb_controls = self.nb_controls = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.nb_controls.AddPage(grc_wxgui.Panel(self.nb_controls), "squelch")
        self.nb_controls.AddPage(grc_wxgui.Panel(self.nb_controls), "gain")
        self.nb_controls.AddPage(grc_wxgui.Panel(self.nb_controls), "modulation")
        self.nb_controls.AddPage(grc_wxgui.Panel(self.nb_controls), "freq")
        self.nb_controls.AddPage(grc_wxgui.Panel(self.nb_controls), "bandwidth")
        self.nb_controls.AddPage(grc_wxgui.Panel(self.nb_controls), "volume")
        self.nb_controls.AddPage(grc_wxgui.Panel(self.nb_controls), "samp_rate")
        self.nb_controls.AddPage(grc_wxgui.Panel(self.nb_controls), "spectrum_sense")
        self.GridAdd(self.nb_controls, 2, 0, 1, 1)
        _volume_sizer = wx.BoxSizer(wx.VERTICAL)
        self._volume_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(5).GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	label='volume',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._volume_slider = forms.slider(
        	parent=self.nb_controls.GetPage(5).GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	minimum=0,
        	maximum=100,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.nb_controls.GetPage(5).GridAdd(_volume_sizer, 0, 0, 1, 1)
        _squelch_threshold_sizer = wx.BoxSizer(wx.VERTICAL)
        self._squelch_threshold_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(0).GetWin(),
        	sizer=_squelch_threshold_sizer,
        	value=self.squelch_threshold,
        	callback=self.set_squelch_threshold,
        	label='squelch_threshold',
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
        self.nb_controls.GetPage(0).GridAdd(_squelch_threshold_sizer, 0, 0, 1, 1)
        self._spectrum_sense_button_chooser = forms.button(
        	parent=self.nb_controls.GetPage(7).GetWin(),
        	value=self.spectrum_sense_button,
        	callback=self.set_spectrum_sense_button,
        	label="spectrum sense",
        	choices=[0,1],
        	labels=["Disabled","Enabled"],
        )
        self.nb_controls.GetPage(7).GridAdd(self._spectrum_sense_button_chooser, 0, 0, 1, 1)
        self._samp_rate_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(6).GetWin(),
        	value=self.samp_rate,
        	callback=self.set_samp_rate,
        	label='samp_rate',
        	converter=forms.float_converter(),
        )
        self.nb_controls.GetPage(6).GridAdd(self._samp_rate_text_box, 0, 0, 1, 1)
        _rf_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._rf_gain_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(1).GetWin(),
        	sizer=_rf_gain_sizer,
        	value=self.rf_gain,
        	callback=self.set_rf_gain,
        	label='rf_gain',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._rf_gain_slider = forms.slider(
        	parent=self.nb_controls.GetPage(1).GetWin(),
        	sizer=_rf_gain_sizer,
        	value=self.rf_gain,
        	callback=self.set_rf_gain,
        	minimum=0,
        	maximum=50,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.nb_controls.GetPage(1).GridAdd(_rf_gain_sizer, 0, 0, 1, 1)
        self.nb_gfx = self.nb_gfx = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.nb_gfx.AddPage(grc_wxgui.Panel(self.nb_gfx), "Fine Tune FFT")
        self.nb_gfx.AddPage(grc_wxgui.Panel(self.nb_gfx), "Rough Tune FFT")
        self.nb_gfx.AddPage(grc_wxgui.Panel(self.nb_gfx), "Fine Tune Waterfall")
        self.nb_gfx.AddPage(grc_wxgui.Panel(self.nb_gfx), "Rough Tune Waterfall")
        self.GridAdd(self.nb_gfx, 0, 0, 1, 1)
        self._modulation_chooser = forms.radio_buttons(
        	parent=self.nb_controls.GetPage(2).GetWin(),
        	value=self.modulation,
        	callback=self.set_modulation,
        	label="Modulation",
        	choices=[0,1,2],
        	labels=["AM","NBFM","WBFM"],
        	style=wx.RA_HORIZONTAL,
        )
        self.nb_controls.GetPage(2).GridAdd(self._modulation_chooser, 0, 0, 1, 1)
        _if_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._if_gain_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(1).GetWin(),
        	sizer=_if_gain_sizer,
        	value=self.if_gain,
        	callback=self.set_if_gain,
        	label='if_gain',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._if_gain_slider = forms.slider(
        	parent=self.nb_controls.GetPage(1).GetWin(),
        	sizer=_if_gain_sizer,
        	value=self.if_gain,
        	callback=self.set_if_gain,
        	minimum=0,
        	maximum=50,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.nb_controls.GetPage(1).GridAdd(_if_gain_sizer, 0, 1, 1, 1)
        def _func_quad_avg_mag_sqrd_probe():
        	while True:
        		val = self.probe_avg_mag_sqrd.unmuted()
        		try: self.set_func_quad_avg_mag_sqrd(val)
        		except AttributeError, e: pass
        		time.sleep(1.0/(spectrum_sense_rate*1.1))
        _func_quad_avg_mag_sqrd_thread = threading.Thread(target=_func_quad_avg_mag_sqrd_probe)
        _func_quad_avg_mag_sqrd_thread.daemon = True
        _func_quad_avg_mag_sqrd_thread.start()
        _ch_width_sizer = wx.BoxSizer(wx.VERTICAL)
        self._ch_width_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(4).GetWin(),
        	sizer=_ch_width_sizer,
        	value=self.ch_width,
        	callback=self.set_ch_width,
        	label='ch_width',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._ch_width_slider = forms.slider(
        	parent=self.nb_controls.GetPage(4).GetWin(),
        	sizer=_ch_width_sizer,
        	value=self.ch_width,
        	callback=self.set_ch_width,
        	minimum=int(1e3),
        	maximum=int(quad_samp_rate*0.99),
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.nb_controls.GetPage(4).GridAdd(_ch_width_sizer, 0, 0, 1, 1)
        _ch_trans_sizer = wx.BoxSizer(wx.VERTICAL)
        self._ch_trans_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(4).GetWin(),
        	sizer=_ch_trans_sizer,
        	value=self.ch_trans,
        	callback=self.set_ch_trans,
        	label='ch_trans',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._ch_trans_slider = forms.slider(
        	parent=self.nb_controls.GetPage(4).GetWin(),
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
        self.nb_controls.GetPage(4).GridAdd(_ch_trans_sizer, 0, 1, 1, 1)
        self._center_freq_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(3).GetWin(),
        	value=self.center_freq,
        	callback=self.set_center_freq,
        	label='center_freq',
        	converter=forms.float_converter(),
        )
        self.nb_controls.GetPage(3).GridAdd(self._center_freq_text_box, 0, 0, 1, 1)
        self.blocks_probe_signal_vx_fft = blocks.probe_signal_vf(fft_len)
        _bb_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._bb_gain_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(1).GetWin(),
        	sizer=_bb_gain_sizer,
        	value=self.bb_gain,
        	callback=self.set_bb_gain,
        	label='bb_gain',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._bb_gain_slider = forms.slider(
        	parent=self.nb_controls.GetPage(1).GetWin(),
        	sizer=_bb_gain_sizer,
        	value=self.bb_gain,
        	callback=self.set_bb_gain,
        	minimum=0,
        	maximum=50,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.nb_controls.GetPage(1).GridAdd(_bb_gain_sizer, 0, 2, 1, 1)
        self.wxgui_waterfallsink2_0_1 = waterfallsink2.waterfall_sink_c(
        	self.nb_gfx.GetPage(3).GetWin(),
        	baseband_freq=center_freq,
        	dynamic_range=50,
        	ref_level=gui_ref_level,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=2**10,
        	fft_rate=2**3,
        	average=True,
        	avg_alpha=0.25,
        	title="Rough Tune Waterfall",
        	size=(gui_sizes),
        )
        self.nb_gfx.GetPage(3).GridAdd(self.wxgui_waterfallsink2_0_1.win, 0, 0, 1, 1)
        def wxgui_waterfallsink2_0_1_callback(x, y):
        	self.set_center_freq(x)
        
        self.wxgui_waterfallsink2_0_1.set_callback(wxgui_waterfallsink2_0_1_callback)
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.nb_gfx.GetPage(2).GetWin(),
        	baseband_freq=center_freq,
        	dynamic_range=50,
        	ref_level=gui_ref_level,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=2**10,
        	fft_rate=2**3,
        	average=True,
        	avg_alpha=0.25,
        	title="Fine Tune Waterfall",
        	size=(gui_sizes),
        )
        self.nb_gfx.GetPage(2).GridAdd(self.wxgui_waterfallsink2_0.win, 0, 0, 1, 1)
        def wxgui_waterfallsink2_0_callback(x, y):
        	self.set_channel_click_freq(x)
        
        self.wxgui_waterfallsink2_0.set_callback(wxgui_waterfallsink2_0_callback)
        self.wxgui_fftsink2_1_0_0_1 = fftsink2.fft_sink_c(
        	self.nb_gfx.GetPage(0).GetWin(),
        	baseband_freq=center_freq,
        	y_per_div=5,
        	y_divs=10,
        	ref_level=gui_ref_level,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=gui_fft_size,
        	fft_rate=gui_refresh_rate,
        	average=True,
        	avg_alpha=gui_average,
        	title="Fine Tune FFT",
        	peak_hold=False,
        	win=window.hamming,
        	size=(gui_sizes),
        )
        self.nb_gfx.GetPage(0).GridAdd(self.wxgui_fftsink2_1_0_0_1.win, 0, 0, 1, 1)
        def wxgui_fftsink2_1_0_0_1_callback(x, y):
        	self.set_channel_click_freq(x)
        
        self.wxgui_fftsink2_1_0_0_1.set_callback(wxgui_fftsink2_1_0_0_1_callback)
        self.wxgui_fftsink2_1_0_0_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=max_channel_freq,
        	y_per_div=5,
        	y_divs=10,
        	ref_level=20,
        	ref_scale=2.0,
        	sample_rate=channel_samp_rate,
        	fft_size=gui_fft_size,
        	fft_rate=gui_refresh_rate,
        	average=True,
        	avg_alpha=gui_average,
        	title="Click to Fine Tune",
        	peak_hold=False,
        	size=(gui_sizes),
        )
        self.GridAdd(self.wxgui_fftsink2_1_0_0_0.win, 1, 0, 1, 1)
        def wxgui_fftsink2_1_0_0_0_callback(x, y):
        	self.set_channel_click_freq(x)
        
        self.wxgui_fftsink2_1_0_0_0.set_callback(wxgui_fftsink2_1_0_0_0_callback)
        self.wxgui_fftsink2_1_0_0 = fftsink2.fft_sink_c(
        	self.nb_gfx.GetPage(1).GetWin(),
        	baseband_freq=center_freq,
        	y_per_div=5,
        	y_divs=10,
        	ref_level=gui_ref_level,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=gui_fft_size,
        	fft_rate=gui_refresh_rate,
        	average=True,
        	avg_alpha=gui_average,
        	title="Rough Tune FFT",
        	peak_hold=False,
        	win=window.hamming,
        	size=(gui_sizes),
        )
        self.nb_gfx.GetPage(1).GridAdd(self.wxgui_fftsink2_1_0_0.win, 0, 0, 1, 1)
        def wxgui_fftsink2_1_0_0_callback(x, y):
        	self.set_center_freq(x)
        
        self.wxgui_fftsink2_1_0_0.set_callback(wxgui_fftsink2_1_0_0_callback)
        self._txt_max_channel_freq_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(7).GetWin(),
        	value=self.txt_max_channel_freq,
        	callback=self.set_txt_max_channel_freq,
        	label="max_channel_freq",
        	converter=forms.str_converter(),
        )
        self.nb_controls.GetPage(7).GridAdd(self._txt_max_channel_freq_text_box, 0, 1, 1, 1)
        self._txt_blocked_freq_list_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(7).GetWin(),
        	value=self.txt_blocked_freq_list,
        	callback=self.set_txt_blocked_freq_list,
        	label="Blocked Freqs",
        	converter=forms.str_converter(),
        )
        self.nb_controls.GetPage(7).GridAdd(self._txt_blocked_freq_list_text_box, 0, 2, 1, 50)
        self.osmosdr_source_0 = osmosdr.source( args="nchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(1, 0)
        self.osmosdr_source_0.set_iq_balance_mode(1, 0)
        self.osmosdr_source_0.set_gain_mode(0, 0)
        self.osmosdr_source_0.set_gain(rf_gain, 0)
        self.osmosdr_source_0.set_if_gain(if_gain, 0)
        self.osmosdr_source_0.set_bb_gain(bb_gain, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.modulation_selector_out = grc_blks2.selector(
        	item_size=gr.sizeof_float*1,
        	num_inputs=3,
        	num_outputs=1,
        	input_index=modulation,
        	output_index=0,
        )
        self.modulation_selector_in_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*fft_len,
        	num_inputs=1,
        	num_outputs=2,
        	input_index=0,
        	output_index=spectrum_sense_button and not func_quad_avg_mag_sqrd,
        )
        self.modulation_selector_in = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=1,
        	num_outputs=3,
        	input_index=0,
        	output_index=modulation,
        )
        self.fft_vxx_0_0 = fft.fft_vcc(combined_ch_bins, False, (), True, 1)
        self.fft_vxx_0 = fft.fft_vcc(fft_len, True, (), True, 1)
        def _fft_signal_level_probe():
        	while True:
        		val = self.blocks_probe_signal_vx_fft.level()
        		try: self.set_fft_signal_level(val)
        		except AttributeError, e: pass
        		time.sleep(1.0/(spectrum_sense_rate))
        _fft_signal_level_thread = threading.Thread(target=_fft_signal_level_probe)
        _fft_signal_level_thread.daemon = True
        _fft_signal_level_thread.start()
        self.fft_filter_xxx_0_0_0_0 = filter.fft_filter_ccc(quad_decim, (firdes.low_pass_2(1, channel_samp_rate, ch_width, ch_trans, 40, firdes.WIN_HAMMING, 6.76)), 1)
        self.dc_blocker_xx_0 = filter.dc_blocker_cc(2**10, False)
        self._channel_click_freq_text_box = forms.text_box(
        	parent=self.nb_controls.GetPage(3).GetWin(),
        	value=self.channel_click_freq,
        	callback=self.set_channel_click_freq,
        	label='channel_click_freq',
        	converter=forms.float_converter(),
        )
        self.nb_controls.GetPage(3).GridAdd(self._channel_click_freq_text_box, 0, 1, 1, 1)
        self._ch_step_size_chooser = forms.drop_down(
        	parent=self.nb_controls.GetPage(3).GetWin(),
        	value=self.ch_step_size,
        	callback=self.set_ch_step_size,
        	label='ch_step_size',
        	choices=[1e3, 2.5e3, 5e3, 6.25e3, 8.33e3, 12.5e3, 25e3, 50e3,100e3, 200e3],
        	labels=["1e3", "2.5e3", "5e3", "6.25e3", "8.33e3", "12.5e3", "25e3", "50e3","100e3", "200e3"],
        )
        self.nb_controls.GetPage(3).GridAdd(self._ch_step_size_chooser, 0, 2, 1, 1)
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, combined_ch_bins)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, fft_len)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, combined_ch_bins)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_len)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*fft_len)
        self.blocks_multiply_const_vxx_1_1_0 = blocks.multiply_const_vff((volume, ))
        self.blocks_multiply_const_vxx_1_1 = blocks.multiply_const_vcc((1 if (int(modulation) == 0) else 0, ))
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_vcc((1 if (int(modulation) == 2) else 0, ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((1 if (int(modulation) == 1) else 0, ))
        self.blocks_keep_m_in_n_0_0 = blocks.keep_m_in_n(gr.sizeof_gr_complex, combined_ch_bins, fft_len, int(bin_index-(float(combined_ch_bins)/2)))
        self.blocks_complex_to_mag_0_0 = blocks.complex_to_mag(fft_len)
        self.audio_sink_0_0 = audio.sink(int(audio_samp_rate*0.97), "", True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=quad_samp_rate,
        	audio_decimation=audio_decim,
        )
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(squelch_threshold, 0.001, 0, False)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=int(audio_samp_rate),
        	quad_rate=int(quad_samp_rate),
        	tau=75e-6,
        	max_dev=5e3,
        )
        self.analog_feedforward_agc_cc_0 = analog.feedforward_agc_cc(1024, 1)
        self.analog_am_demod_cf_0 = analog.am_demod_cf(
        	channel_rate=quad_samp_rate,
        	audio_decim=audio_decim,
        	audio_pass=3000,
        	audio_stop=3500,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_keep_m_in_n_0_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_keep_m_in_n_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_vector_to_stream_0_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.fft_filter_xxx_0_0_0_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.wxgui_waterfallsink2_0, 0))
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.wxgui_fftsink2_1_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_1, 0), (self.analog_am_demod_cf_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.analog_nbfm_rx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.modulation_selector_out, 0), (self.blocks_multiply_const_vxx_1_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_1_0, 0), (self.audio_sink_0_0, 0))
        self.connect((self.analog_wfm_rcv_0, 0), (self.modulation_selector_out, 2))
        self.connect((self.analog_nbfm_rx_0, 0), (self.modulation_selector_out, 1))
        self.connect((self.analog_am_demod_cf_0, 0), (self.modulation_selector_out, 0))
        self.connect((self.modulation_selector_in, 2), (self.blocks_multiply_const_vxx_1_0, 0))
        self.connect((self.modulation_selector_in, 1), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.modulation_selector_in, 0), (self.blocks_multiply_const_vxx_1_1, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.wxgui_waterfallsink2_0_1, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.wxgui_fftsink2_1_0_0_1, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.wxgui_fftsink2_1_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.dc_blocker_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self.blocks_probe_signal_vx_fft, 0))
        self.connect((self.fft_vxx_0, 0), (self.modulation_selector_in_0, 0))
        self.connect((self.modulation_selector_in_0, 1), (self.blocks_complex_to_mag_0_0, 0))
        self.connect((self.modulation_selector_in_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.analog_feedforward_agc_cc_0, 0), (self.modulation_selector_in, 0))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.probe_avg_mag_sqrd, 0))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.analog_feedforward_agc_cc_0, 0))
        self.connect((self.fft_filter_xxx_0_0_0_0, 0), (self.analog_pwr_squelch_xx_0, 0))


# QT sink close method reimplementation

    def get_cfg_center_freq(self):
        return self.cfg_center_freq

    def set_cfg_center_freq(self, cfg_center_freq):
        self.cfg_center_freq = cfg_center_freq
        self.set_center_freq(self.cfg_center_freq)

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

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.set_channel_freq(self.channel_click_freq_rounded if ((self.channel_click_freq_rounded < (self.center_freq + self.samp_rate/2)) and (self.channel_click_freq_rounded > (self.center_freq - self.samp_rate/2))) else self.center_freq)
        self.set_left_edge_freq(self.center_freq-(self.samp_rate/2))
        self.set_blocked_bin_list([int(math.floor(float(((blocked_freq-(self.center_freq-(self.samp_rate/2)))/self.bin_bw))/self.bin_floor)*self.bin_floor) for blocked_freq in self.blocked_freq_list])
        self._center_freq_text_box.set_value(self.center_freq)
        self._cfg_center_freq_config = ConfigParser.ConfigParser()
        self._cfg_center_freq_config.read(".scanoo")
        if not self._cfg_center_freq_config.has_section("main"):
        	self._cfg_center_freq_config.add_section("main")
        self._cfg_center_freq_config.set("main", "center_freq", str(self.center_freq))
        self._cfg_center_freq_config.write(open(".scanoo", 'w'))
        self.set_cfg_channel_click_freq(int(self.center_freq))
        self.wxgui_waterfallsink2_0.set_baseband_freq(self.center_freq)
        self.wxgui_waterfallsink2_0_1.set_baseband_freq(self.center_freq)
        self.wxgui_fftsink2_1_0_0_1.set_baseband_freq(self.center_freq)
        self.wxgui_fftsink2_1_0_0.set_baseband_freq(self.center_freq)
        self.osmosdr_source_0.set_center_freq(self.center_freq, 0)

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
        self.set_channel_freq(self.channel_click_freq_rounded if ((self.channel_click_freq_rounded < (self.center_freq + self.samp_rate/2)) and (self.channel_click_freq_rounded > (self.center_freq - self.samp_rate/2))) else self.center_freq)
        self.set_lo_offset(-((self.samp_rate/2) * 1.25))
        self.set_left_edge_freq(self.center_freq-(self.samp_rate/2))
        self.set_fft_len(int(self.samp_rate/self.bin_bw))
        self.set_blocked_bin_list([int(math.floor(float(((blocked_freq-(self.center_freq-(self.samp_rate/2)))/self.bin_bw))/self.bin_floor)*self.bin_floor) for blocked_freq in self.blocked_freq_list])
        self._samp_rate_text_box.set_value(self.samp_rate)
        self._cfg_samp_rate_config = ConfigParser.ConfigParser()
        self._cfg_samp_rate_config.read(".scanoo")
        if not self._cfg_samp_rate_config.has_section("main"):
        	self._cfg_samp_rate_config.add_section("main")
        self._cfg_samp_rate_config.set("main", "samp_rate", str(self.samp_rate))
        self._cfg_samp_rate_config.write(open(".scanoo", 'w'))
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
        self.wxgui_waterfallsink2_0_1.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_1_0_0_1.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_1_0_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_cfg_channel_click_freq(self):
        return self.cfg_channel_click_freq

    def set_cfg_channel_click_freq(self, cfg_channel_click_freq):
        self.cfg_channel_click_freq = cfg_channel_click_freq
        self.set_channel_click_freq(self.cfg_channel_click_freq)

    def get_cfg_ch_step_size(self):
        return self.cfg_ch_step_size

    def set_cfg_ch_step_size(self, cfg_ch_step_size):
        self.cfg_ch_step_size = cfg_ch_step_size
        self.set_ch_step_size(self.cfg_ch_step_size)

    def get_bin_bw(self):
        return self.bin_bw

    def set_bin_bw(self, bin_bw):
        self.bin_bw = bin_bw
        self.set_bin_index(self.max_bin_index if self.spectrum_sense_button else ((self.channel_freq - self.left_edge_freq)/self.bin_bw))
        self.set_combined_ch_bins(int(self.channel_samp_rate/self.bin_bw))
        self.set_fft_len(int(self.samp_rate/self.bin_bw))
        self.set_blocked_bin_list([int(math.floor(float(((blocked_freq-(self.center_freq-(self.samp_rate/2)))/self.bin_bw))/self.bin_floor)*self.bin_floor) for blocked_freq in self.blocked_freq_list])
        self.set_max_channel_freq(int(self.left_edge_freq+(self.bin_bw*self.bin_index)))
        self.set_bin_floor(int(50e3/self.bin_bw))

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.blocks_keep_m_in_n_0_0.set_n(self.fft_len)
        self.set_fft_signal_level([0.0]*(self.fft_len))

    def get_channel_click_freq(self):
        return self.channel_click_freq

    def set_channel_click_freq(self, channel_click_freq):
        self.channel_click_freq = channel_click_freq
        self.set_channel_click_freq_rounded((round(float(self.channel_click_freq) / self.ch_step_size, 0) * self.ch_step_size))
        self._cfg_channel_click_freq_config = ConfigParser.ConfigParser()
        self._cfg_channel_click_freq_config.read(".scanoo")
        if not self._cfg_channel_click_freq_config.has_section("main"):
        	self._cfg_channel_click_freq_config.add_section("main")
        self._cfg_channel_click_freq_config.set("main", "channel_click_freq", str(self.channel_click_freq))
        self._cfg_channel_click_freq_config.write(open(".scanoo", 'w'))
        self._channel_click_freq_text_box.set_value(self.channel_click_freq)

    def get_ch_step_size(self):
        return self.ch_step_size

    def set_ch_step_size(self, ch_step_size):
        self.ch_step_size = ch_step_size
        self.set_channel_click_freq_rounded((round(float(self.channel_click_freq) / self.ch_step_size, 0) * self.ch_step_size))
        self._cfg_ch_step_size_config = ConfigParser.ConfigParser()
        self._cfg_ch_step_size_config.read(".scanoo")
        if not self._cfg_ch_step_size_config.has_section("main"):
        	self._cfg_ch_step_size_config.add_section("main")
        self._cfg_ch_step_size_config.set("main", "ch_step_size", str(self.ch_step_size))
        self._cfg_ch_step_size_config.write(open(".scanoo", 'w'))
        self._ch_step_size_chooser.set_value(self.ch_step_size)

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

    def get_channel_click_freq_rounded(self):
        return self.channel_click_freq_rounded

    def set_channel_click_freq_rounded(self, channel_click_freq_rounded):
        self.channel_click_freq_rounded = channel_click_freq_rounded
        self.set_channel_freq(self.channel_click_freq_rounded if ((self.channel_click_freq_rounded < (self.center_freq + self.samp_rate/2)) and (self.channel_click_freq_rounded > (self.center_freq - self.samp_rate/2))) else self.center_freq)

    def get_blocked_bin_list(self):
        return self.blocked_bin_list

    def set_blocked_bin_list(self, blocked_bin_list):
        self.blocked_bin_list = blocked_bin_list
        self.set_max_bin_index(int(self.fft_signal_level.index(max([i for j, i in enumerate(self.fft_signal_level) if (int(math.floor(float(j)/self.bin_floor)*self.bin_floor) not in self.blocked_bin_list )]))))

    def get_spectrum_sense_button(self):
        return self.spectrum_sense_button

    def set_spectrum_sense_button(self, spectrum_sense_button):
        self.spectrum_sense_button = spectrum_sense_button
        self.set_bin_index(self.max_bin_index if self.spectrum_sense_button else ((self.channel_freq - self.left_edge_freq)/self.bin_bw))
        self._spectrum_sense_button_chooser.set_value(self.spectrum_sense_button)
        self.modulation_selector_in_0.set_output_index(int(self.spectrum_sense_button and not self.func_quad_avg_mag_sqrd))

    def get_max_bin_index(self):
        return self.max_bin_index

    def set_max_bin_index(self, max_bin_index):
        self.max_bin_index = max_bin_index
        self.set_bin_index(self.max_bin_index if self.spectrum_sense_button else ((self.channel_freq - self.left_edge_freq)/self.bin_bw))

    def get_left_edge_freq(self):
        return self.left_edge_freq

    def set_left_edge_freq(self, left_edge_freq):
        self.left_edge_freq = left_edge_freq
        self.set_bin_index(self.max_bin_index if self.spectrum_sense_button else ((self.channel_freq - self.left_edge_freq)/self.bin_bw))
        self.set_max_channel_freq(int(self.left_edge_freq+(self.bin_bw*self.bin_index)))

    def get_channel_freq(self):
        return self.channel_freq

    def set_channel_freq(self, channel_freq):
        self.channel_freq = channel_freq
        self.set_bin_index(self.max_bin_index if self.spectrum_sense_button else ((self.channel_freq - self.left_edge_freq)/self.bin_bw))

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate
        self.set_audio_decim(int(self.quad_samp_rate/self.audio_samp_rate))
        self.set_quad_samp_rate(self.audio_samp_rate*4)

    def get_quad_samp_rate(self):
        return self.quad_samp_rate

    def set_quad_samp_rate(self, quad_samp_rate):
        self.quad_samp_rate = quad_samp_rate
        self.set_audio_decim(int(self.quad_samp_rate/self.audio_samp_rate))
        self.set_quad_decim(int(self.channel_samp_rate/self.quad_samp_rate))
        self.set_channel_samp_rate((self.quad_samp_rate*4))
        self.set_ch_trans(min(self.cfg_ch_trans,int(self.quad_samp_rate*0.99)))
        self.set_ch_width(min(self.cfg_ch_width,(self.quad_samp_rate*0.99)))

    def get_bin_index(self):
        return self.bin_index

    def set_bin_index(self, bin_index):
        self.bin_index = bin_index
        self.set_max_channel_freq(int(self.left_edge_freq+(self.bin_bw*self.bin_index)))
        self.blocks_keep_m_in_n_0_0.set_offset(int(self.bin_index-(float(self.combined_ch_bins)/2)))

    def get_max_channel_freq(self):
        return self.max_channel_freq

    def set_max_channel_freq(self, max_channel_freq):
        self.max_channel_freq = max_channel_freq
        self.set_txt_max_channel_freq(self.max_channel_freq)
        self.wxgui_fftsink2_1_0_0_0.set_baseband_freq(self.max_channel_freq)

    def get_channel_samp_rate(self):
        return self.channel_samp_rate

    def set_channel_samp_rate(self, channel_samp_rate):
        self.channel_samp_rate = channel_samp_rate
        self.set_quad_decim(int(self.channel_samp_rate/self.quad_samp_rate))
        self.set_combined_ch_bins(int(self.channel_samp_rate/self.bin_bw))
        self.wxgui_fftsink2_1_0_0_0.set_sample_rate(self.channel_samp_rate)
        self.fft_filter_xxx_0_0_0_0.set_taps((firdes.low_pass_2(1, self.channel_samp_rate, self.ch_width, self.ch_trans, 40, firdes.WIN_HAMMING, 6.76)))

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

    def get_cfg_rf_gain(self):
        return self.cfg_rf_gain

    def set_cfg_rf_gain(self, cfg_rf_gain):
        self.cfg_rf_gain = cfg_rf_gain
        self.set_rf_gain(self.cfg_rf_gain)

    def get_cfg_modulation(self):
        return self.cfg_modulation

    def set_cfg_modulation(self, cfg_modulation):
        self.cfg_modulation = cfg_modulation
        self.set_modulation(self.cfg_modulation)

    def get_cfg_if_gain(self):
        return self.cfg_if_gain

    def set_cfg_if_gain(self, cfg_if_gain):
        self.cfg_if_gain = cfg_if_gain
        self.set_if_gain(self.cfg_if_gain)

    def get_cfg_ch_width(self):
        return self.cfg_ch_width

    def set_cfg_ch_width(self, cfg_ch_width):
        self.cfg_ch_width = cfg_ch_width
        self.set_ch_width(min(self.cfg_ch_width,(self.quad_samp_rate*0.99)))

    def get_cfg_ch_trans(self):
        return self.cfg_ch_trans

    def set_cfg_ch_trans(self, cfg_ch_trans):
        self.cfg_ch_trans = cfg_ch_trans
        self.set_ch_trans(min(self.cfg_ch_trans,int(self.quad_samp_rate*0.99)))

    def get_cfg_bb_gain(self):
        return self.cfg_bb_gain

    def set_cfg_bb_gain(self, cfg_bb_gain):
        self.cfg_bb_gain = cfg_bb_gain
        self.set_bb_gain(self.cfg_bb_gain)

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_1_1_0.set_k((self.volume, ))
        self._volume_slider.set_value(self.volume)
        self._volume_text_box.set_value(self.volume)
        self._cfg_volume_config = ConfigParser.ConfigParser()
        self._cfg_volume_config.read(".scanoo")
        if not self._cfg_volume_config.has_section("main"):
        	self._cfg_volume_config.add_section("main")
        self._cfg_volume_config.set("main", "volume", str(self.volume))
        self._cfg_volume_config.write(open(".scanoo", 'w'))

    def get_txt_max_channel_freq(self):
        return self.txt_max_channel_freq

    def set_txt_max_channel_freq(self, txt_max_channel_freq):
        self.txt_max_channel_freq = txt_max_channel_freq
        self._txt_max_channel_freq_text_box.set_value(self.txt_max_channel_freq)

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
        self.analog_pwr_squelch_xx_0.set_threshold(self.squelch_threshold)

    def get_spectrum_sense_rate(self):
        return self.spectrum_sense_rate

    def set_spectrum_sense_rate(self, spectrum_sense_rate):
        self.spectrum_sense_rate = spectrum_sense_rate

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self._rf_gain_slider.set_value(self.rf_gain)
        self._rf_gain_text_box.set_value(self.rf_gain)
        self._cfg_rf_gain_config = ConfigParser.ConfigParser()
        self._cfg_rf_gain_config.read(".scanoo")
        if not self._cfg_rf_gain_config.has_section("main"):
        	self._cfg_rf_gain_config.add_section("main")
        self._cfg_rf_gain_config.set("main", "rf_gain", str(self.rf_gain))
        self._cfg_rf_gain_config.write(open(".scanoo", 'w'))
        self.osmosdr_source_0.set_gain(self.rf_gain, 0)

    def get_quad_decim(self):
        return self.quad_decim

    def set_quad_decim(self, quad_decim):
        self.quad_decim = quad_decim

    def get_modulation(self):
        return self.modulation

    def set_modulation(self, modulation):
        self.modulation = modulation
        self.modulation_selector_out.set_input_index(int(self.modulation))
        self.blocks_multiply_const_vxx_1.set_k((1 if (int(self.modulation) == 1) else 0, ))
        self.blocks_multiply_const_vxx_1_0.set_k((1 if (int(self.modulation) == 2) else 0, ))
        self._cfg_modulation_config = ConfigParser.ConfigParser()
        self._cfg_modulation_config.read(".scanoo")
        if not self._cfg_modulation_config.has_section("main"):
        	self._cfg_modulation_config.add_section("main")
        self._cfg_modulation_config.set("main", "modulation", str(self.modulation))
        self._cfg_modulation_config.write(open(".scanoo", 'w'))
        self.blocks_multiply_const_vxx_1_1.set_k((1 if (int(self.modulation) == 0) else 0, ))
        self._modulation_chooser.set_value(self.modulation)
        self.modulation_selector_in.set_output_index(int(self.modulation))

    def get_lo_offset(self):
        return self.lo_offset

    def set_lo_offset(self, lo_offset):
        self.lo_offset = lo_offset

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self._if_gain_slider.set_value(self.if_gain)
        self._if_gain_text_box.set_value(self.if_gain)
        self._cfg_if_gain_config = ConfigParser.ConfigParser()
        self._cfg_if_gain_config.read(".scanoo")
        if not self._cfg_if_gain_config.has_section("main"):
        	self._cfg_if_gain_config.add_section("main")
        self._cfg_if_gain_config.set("main", "if_gain", str(self.if_gain))
        self._cfg_if_gain_config.write(open(".scanoo", 'w'))
        self.osmosdr_source_0.set_if_gain(self.if_gain, 0)

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

    def get_func_quad_avg_mag_sqrd(self):
        return self.func_quad_avg_mag_sqrd

    def set_func_quad_avg_mag_sqrd(self, func_quad_avg_mag_sqrd):
        self.func_quad_avg_mag_sqrd = func_quad_avg_mag_sqrd
        self.modulation_selector_in_0.set_output_index(int(self.spectrum_sense_button and not self.func_quad_avg_mag_sqrd))

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
        self._ch_width_slider.set_value(self.ch_width)
        self._ch_width_text_box.set_value(self.ch_width)
        self._cfg_ch_width_config = ConfigParser.ConfigParser()
        self._cfg_ch_width_config.read(".scanoo")
        if not self._cfg_ch_width_config.has_section("main"):
        	self._cfg_ch_width_config.add_section("main")
        self._cfg_ch_width_config.set("main", "ch_width", str(self.ch_width))
        self._cfg_ch_width_config.write(open(".scanoo", 'w'))
        self.fft_filter_xxx_0_0_0_0.set_taps((firdes.low_pass_2(1, self.channel_samp_rate, self.ch_width, self.ch_trans, 40, firdes.WIN_HAMMING, 6.76)))

    def get_ch_trans(self):
        return self.ch_trans

    def set_ch_trans(self, ch_trans):
        self.ch_trans = ch_trans
        self._ch_trans_slider.set_value(self.ch_trans)
        self._ch_trans_text_box.set_value(self.ch_trans)
        self._cfg_ch_trans_config = ConfigParser.ConfigParser()
        self._cfg_ch_trans_config.read(".scanoo")
        if not self._cfg_ch_trans_config.has_section("main"):
        	self._cfg_ch_trans_config.add_section("main")
        self._cfg_ch_trans_config.set("main", "ch_trans", str(self.ch_trans))
        self._cfg_ch_trans_config.write(open(".scanoo", 'w'))
        self.fft_filter_xxx_0_0_0_0.set_taps((firdes.low_pass_2(1, self.channel_samp_rate, self.ch_width, self.ch_trans, 40, firdes.WIN_HAMMING, 6.76)))

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self._bb_gain_slider.set_value(self.bb_gain)
        self._bb_gain_text_box.set_value(self.bb_gain)
        self._cfg_bb_gain_config = ConfigParser.ConfigParser()
        self._cfg_bb_gain_config.read(".scanoo")
        if not self._cfg_bb_gain_config.has_section("main"):
        	self._cfg_bb_gain_config.add_section("main")
        self._cfg_bb_gain_config.set("main", "bb_gain", str(self.bb_gain))
        self._cfg_bb_gain_config.write(open(".scanoo", 'w'))
        self.osmosdr_source_0.set_bb_gain(self.bb_gain, 0)

    def get_audio_decim(self):
        return self.audio_decim

    def set_audio_decim(self, audio_decim):
        self.audio_decim = audio_decim

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = scanoo_com_rx()
    tb.Start(True)
    tb.Wait()

