import time
import threading
from functools import partial
#from SerialInterface import SerialInterface
import struct
import pickle
import pump
#import nidaqmx
#import daq


from sys import version_info
if version_info.major == 2:
	import Tkinter as tk
elif version_info.major == 3:
	import tkinter as tk

from tkinter import *


VERBOSE = 2  # debugger


N_CHANNEL = 4


# self.VAL_MAX =
# self.VAL_MIN = 0
SLIDER_LENGTH = 350

MIN_INTERVAL = 50 	# Serial update limit in ms


def main():
	ui_app = App(tk.Tk())


class App:

	def __init__(self, master_window):				# ###############Initializer

		self.daq = daq.Daq()
		self.daq.counter_out_channel_0("X-DAQ", "ctr0", self.daq.pulse_freq, self.daq.min_duty)
		self.daq.counter_out_channel_1("X-DAQ", "ctr1", self.daq.pulse_freq, self.daq.min_duty)
		self.daq.counter_out_channel_2("X-DAQ", "ctr2", self.daq.pulse_freq, self.daq.min_duty)
		self.daq.counter_out_channel_3("X-DAQ", "ctr3", self.daq.pulse_freq, self.daq.min_duty)

		self.VAL_MAX = self.daq.max_duty
		self.VAL_MIN = self.daq.min_duty

		self.pwm_running = False

		# initialize Global variable
		self.chVal = [0 for x in range(N_CHANNEL)]
		self.valMax = [self.VAL_MAX for i in range(N_CHANNEL)]


		# Initialize syringe pump
		self.syringe = pump.Pump()

		# Initialize daq channels

		self.daq.voltage_in_channel("X-DAQ", "ai0")

		# misc variable
		self.currentState = False   # current state of the program

		self.SerialApp = SerialInterface()

		# Window
		self.master_window = master_window

		# assign title
		self.master_window.title("MR Fluid Control System")

		# ###UI layout setup
		self.UILabel = tk.Label(self.master_window, text="Electromagnet Control Panel")
		self.UILabel.grid(row=0, column=0)

		self.spacer1 = tk.Label(self.master_window, text="")
		self.spacer1.grid(row=1, column=0)

		# state/mode Frame
		# self.smFrame = tk.Frame(self.master_window, bd=1)
		# self.smFrame.grid(row=3, column=1)

		# item Initialization
		self.spacer2 = tk.Label(self.master_window, text="")
		self.spacer2.grid(row=2, column=0)
		self.quitBtn = tk.Button(self.master_window, text="Quit", command=self.close_window)
		self.quitBtn.grid(row=3, column=0, sticky=E)
		self.zeroAllBtn = tk.Button(self.master_window, text="Zero All", command=self.zero_all)
		self.zeroAllBtn.grid(row=3, column=1)

		# Serial Frame Initialization
		self.spacer3 = tk.Label(self.master_window, text="")
		self.spacer3.grid(row=4, column=1)

		self.sfLabel = tk.Label(self.master_window, text="Serial Port Selection")
		self.sfLabel.grid(row=5, column=1, columnspan=1)

		self.serialConnectBtn = tk.Button(self.master_window, text="Connect", command=self.initialize_serial)
		self.serialConnectBtn.grid(row=6, column=1, sticky=W)

		self.serialDisconnectBtn = tk.Button(self.master_window, text="Disconnect", command=self.reset_serial, state='disabled')
		self.serialDisconnectBtn.grid(row=7, column=1, sticky=W)

		self.serialSL = tk.Label(self.master_window, text="Status:")
		self.serialSL.grid(row=6, column=2, sticky=W)

		self.serialStatusLabel = tk.Label(self.master_window, text="           ", bg='red')
		self.serialStatusLabel.grid(row=6, column=3, sticky=W)

		self.serialRefreshBtn = tk.Button(self.master_window, text="Refresh", command=self.refresh_serial)
		self.serialRefreshBtn.grid(row=7, column=2, rowspan=1)

		self.serialPort = tk.StringVar()

		# self.portlist=["PlaceHolder1", "PlaceHolder2"]
		self.SerialList = tk.OptionMenu(self.master_window, self.serialPort, "PlaceHolder1", "PlaceHolder2")
		self.SerialList.grid(row=6, column=0, columnspan=4)

		# individual Channel Frame
		self.channelsFrame = tk.Frame(self.master_window)
		self.channelsFrame.grid(row=1, column=0, columnspan=7)

		# channelsFrame Items Initialization
		self.chNameEntry = [0 for i in range(N_CHANNEL)]
		self.chNameEntryVar = [0 for i in range(N_CHANNEL)]
		self.slider = [0 for i in range(N_CHANNEL)]
		self.chValkPaLabel = [0 for i in range(N_CHANNEL)]
		self.chValEntry = [0 for i in range(N_CHANNEL)]
		self.chValEntryVar = [0 for i in range(N_CHANNEL)]
		self.setMaxBtn = [0 for i in range(N_CHANNEL)]
		self.setMinBtn = [0 for i in range(N_CHANNEL)]
		self.sliderMaxEntry = [0 for i in range(N_CHANNEL)]
		self.maxEntryVar = [0 for i in range(N_CHANNEL)]

		# Channel Frame Label
		self.nameLabel = tk.Label(self.channelsFrame, text="Name")
		self.nameLabel.grid(column=0, row=0)
		self.sliderLabel = tk.Label(self.channelsFrame, text="Slider")
		self.sliderLabel.grid(column=0, row=1)
		self.unitLabel = tk.Label(self.channelsFrame, text="mA")
		self.unitLabel.grid(column=0, row=2)
		self.entryLabel = tk.Label(self.channelsFrame, text="Entry Field")
		self.entryLabel.grid(column=0, row=3)
		self.rangeLabel = tk.Label(self.channelsFrame, text="Max Val")
		self.rangeLabel.grid(column=0, row=5)

		# initialize channel array

		for i in range(N_CHANNEL):

			# channel Name
			self.chNameEntryVar[i] = tk.StringVar()
			self.chNameEntry[i] = tk.Entry(self.channelsFrame, bg='white', width=9, bd=3,
											fg='blue', textvariable=self.chNameEntryVar[i])
			self.chNameEntry[i].grid(column=i*2+1, row=0, columnspan=2)
			self.chNameEntryVar[i].set("Channel %d"%(i+1))

			# slider
			self.slider[i] = tk.Scale(self.channelsFrame, from_=self.VAL_MAX, to=self.VAL_MIN,
										length=SLIDER_LENGTH, command=partial(self.read_val, i, 0))
			self.slider[i].set(0)
			self.slider[i].grid(column=i*2+1, row=1, columnspan=2)

			# label current in mA
			self.chValkPaLabel[i] = tk.Label(self.channelsFrame,text="%.2f"%0)
			self.chValkPaLabel[i].grid(column=i*2+1, row=2, columnspan=2)

			# Channel Value entry Field
			self.chValEntryVar[i] = tk.StringVar()
			self.chValEntry[i] = tk.Entry(self.channelsFrame, width=5, textvariable=self.chValEntryVar[i])
			self.chValEntryVar[i].set(0)
			self.chValEntry[i].grid(column=i*2+1, row=3, columnspan=2)

			# binding function key
			self.chValEntry[i].bind("<Return>", partial(self.read_val, i, 1))

			# min max btn
			self.setMinBtn[i] = tk.Button(self.channelsFrame, text="Min", command=partial(self.set_mn, i, 0),
												activebackground='blue')
			self.setMinBtn[i].grid(column=i*2+1, row=4)
			self.setMaxBtn[i] = tk.Button(self.channelsFrame, text="Max", command=partial(self.set_mn, i, 1),
												activebackground='blue')
			self.setMaxBtn[i].grid(column=(i+1)*2, row=4)

			# max field
			self.maxEntryVar[i] = tk.StringVar()
			self.sliderMaxEntry[i] = tk.Entry(self.channelsFrame, width=5, textvariable=self.maxEntryVar[i])
			self.sliderMaxEntry[i].grid(column=i*2+1, row=5, columnspan=2)
			self.maxEntryVar[i].set(self.valMax[i])

			# binding kay
			self.sliderMaxEntry[i].bind("<Return>", partial(self.set_max, i))

		# first time Function
		self.refresh_serial()  # refresh Serial List

		self.toggle_state(False)

		# ###############################################################################################
		# PUMP CONTROLS
		# ###############################################################################################

		# Spacer
		self.spacer4 = tk.Label(self.master_window, text="")
		self.spacer4.grid(row=5, column=10)

		# Pump Control Title
		self.pump_ui = tk.Label(self.master_window, text="Pump Control Panel")
		self.pump_ui.grid(row=5, column=11, sticky=W)

		# Infuse Button
		self.infuse_pump_btn = tk.Button(self.master_window, text="Infuse", command=lambda: self.syringe.infuse_pump())
		self.infuse_pump_btn.grid(row=6, column=11, sticky=W)

		# Withdraw Button
		self.withdraw_pump_btn = tk.Button(self.master_window, text="Withdraw", command=lambda: self.syringe.withdraw_pump())
		self.withdraw_pump_btn.grid(row=7, column=11, sticky=W)

		# Stop Pump Button
		self.stop_pump_btn = tk.Button(self.master_window, text="Stop Pump", command=lambda: self.syringe.stop_pump())
		self.stop_pump_btn.grid(row=8, column=11, sticky=W)

		# Infuse Rate
		self.infuse_rate_var = tk.StringVar()
		self.infuse_rate_field = tk.Entry(self.master_window, width=5, textvariable=self.infuse_rate_var)
		self.infuse_rate_var.set(0)
		self.infuse_rate_field.grid(row=6, column=12, sticky=W)

		# Infuse Unit Dropdown
		self.inf_unit_list_var = tk.StringVar()
		self.inf_unit_list = ["ml/min", "ml/s", "ml/hr", "ul/min", "ul/s", "ul/hr", "nl/min",
							  "nl/s", "nl/hr", "pl/min", "pl/s", "pl/hr"]
		self.infuse_unit_list = tk.OptionMenu(self.master_window, self.inf_unit_list_var, "ml/min", "ml/s", "ml/hr", "ul/min",
											  "ul/s", "ul/hr", "nl/min", "nl/s", "nl/hr", "pl/min", "pl/s", "pl/hr")
		self.infuse_unit_list.grid(row=6, column=13, sticky=W)

		# Set Infuse Rate Button
		self.set_inf_rate_btn = tk.Button(self.master_window, text="Set",
										  command=lambda: self.syringe.infuse_rate(self.infuse_rate_var.get(),
																				   self.inf_unit_list_var.get()))
		self.set_inf_rate_btn.grid(row=6, column=14, sticky=W)

		# Set Infuse Rate to Max Button
		self.set_inf_rate_max_btn = tk.Button(self.master_window, text="Set to Max",
										  command=lambda: self.syringe.infuse_rate("max",
																				   self.inf_unit_list_var.get()))
		self.set_inf_rate_max_btn.grid(row=6, column=15, sticky=W)

		# Withdraw Rate
		self.withdraw_rate_var = tk.StringVar()
		self.withdraw_rate_field = tk.Entry(self.master_window, width=5, textvariable=self.withdraw_rate_var)
		self.withdraw_rate_var.set(0)
		self.withdraw_rate_field.grid(row=7, column=12, sticky=W)

		# Withdraw Unit Dropdown
		self.with_unit_list_var = tk.StringVar()
		self.with_unit_list = ["ml/min", "ml/s", "ml/hr", "ul/min", "ul/s", "ul/hr", "nl/min", "nl/s",
							   "nl/hr", "pl/min", "pl/s", "pl/hr"]
		self.withdraw_unit_list = tk.OptionMenu(self.master_window, self.with_unit_list_var,
												"ml/min", "ml/s", "ml/hr", "ul/min","ul/s", "ul/hr",
												"nl/min", "nl/s", "nl/hr", "pl/min", "pl/s", "pl/hr")
		self.withdraw_unit_list.grid(row=7, column=13, sticky=W)

		# Set Withdraw Rate Button
		self.set_with_rate_btn = tk.Button(self.master_window, text="Set",
										   command=lambda: self.syringe.withdraw_rate(self.withdraw_rate_var.get(),
																					  self.with_unit_list_var.get()))
		self.set_with_rate_btn.grid(row=7, column=14, sticky=W)

		# Set Withdraw Rate to Max Button
		self.set_with_rate_max_btn = tk.Button(self.master_window, text="Set to Max",
											  command=lambda: self.syringe.withdraw_rate("max",
																					   self.with_unit_list_var.get()))
		self.set_with_rate_max_btn.grid(row=7, column=15, sticky=W)

		# Syringe Manufacturer Title
		self.syr_manuf_title = tk.Label(self.master_window, text="Manufacturer")
		self.syr_manuf_title.grid(row=8, column=12, sticky=W)

		# Syringe Manufacturer DropDown
		self.manuf_list_var = tk.StringVar()
		self.manuf_list = ["air", "bdg", "bdp", "cad", "has", "hm1", "hm2", "hm3", "hm4",
						   "hos", "ils", "nip", "sge", "smp", "tej", "top"]
		self.manufacturer_list = tk.OptionMenu(self.master_window, self.manuf_list_var,
											   "air", "bdg", "bdp", "cad", "has", "hm1", "hm2", "hm3",
											   "hm4", "hos", "ils", "nip", "sge", "smp", "tej", "top")
		self.manufacturer_list.grid(row=8, column=13, sticky=W)

		# Syringe Manufacturer Volume
		self.manuf_vol_var = tk.StringVar()
		self.manuf_vol_field = tk.Entry(self.master_window, width=5, textvariable=self.manuf_vol_var)
		self.manuf_vol_var.set(0)
		self.manuf_vol_field.grid(row=8, column=14, sticky=W)

		# Syringe Manufacturer Unit Dropdown
		self.manuf_unit_list_var = tk.StringVar()
		self.manuf_unit_list = ["ml", "ul"]
		self.manuf_unit_list = tk.OptionMenu(self.master_window, self.manuf_unit_list_var, "ml", "ul")
		self.manuf_unit_list.grid(row=8, column=15, sticky=W)

		# Set Syringe Manufacturer Button
		self.set_manuf_btn = tk.Button(self.master_window, text="Set",
										   command=lambda: self.set_manuf())
		self.set_manuf_btn.grid(row=8, column=16, sticky=W)

		# ###############################################################################################
		# Pressure Reading
		# ###############################################################################################

		# Pressure Label
		self.pressure_label = tk.Label(self.master_window, text="Pressure")
		self.pressure_label.grid(row=2, column=11)

		# Pressure Unit Dropdown
		self.pressure_unit_list_var = tk.StringVar()
		self.pressure_unit_list_var.set("V")
		self.pressure_unit_list = ["V", "psi", "bar", "mbar", "kPa", "MPa"]
		self.pressure_unit_list = tk.OptionMenu(self.master_window, self.pressure_unit_list_var, "V", "psi", "bar", "mbar",
												"kPa", "MPa")
		self.pressure_unit_list.grid(row=2, column=13, sticky=W)

		# Pressure Readout
		self.pressure_var = tk.DoubleVar()
		self.pressure = tk.Label(self.master_window, width=20, fg="red", textvariable=round(self.pressure_var.get(), 4))
		self.pressure_var.set(self.daq.read_pressure(self.pressure_unit_list_var.get()))
		self.pressure.grid(column=12, row=2)

		# ###############################################################################################
		# PWM
		# ###############################################################################################

		# On/Off PWM Button
		self.pwm_start_btn = tk.Button(self.master_window, text="PWM On/Off",
									 command=self.pwm_on_off())
		self.pwm_start_btn.grid(row=3, column=12, sticky=W)

		# PWM Status Label
		# self.serialStatusLabel = tk.Label(self.master_window, text="           ", bg='red')
		# self.serialStatusLabel.grid(row=6, column=3, sticky=W)
		self.pwm_notif = tk.Label(self.master_window, text="	", bg=self.pwm_on_off())
		self.pwm_notif.grid(row=3, column=13, sticky=W)

		# Set to Min Button
		self.pwm_min_btn = tk.Button(self.master_window, text="PWM Min", command=lambda: self.daq.update_duty_cycle_0(self.daq.min_duty))
		self.pwm_min_btn.grid(row=3, column=14, sticky=W)

		# Set to Max Button
		self.pwm_max_btn = tk.Button(self.master_window, text="PWM Max",
									 command=lambda: self.daq.update_duty_cycle_0(self.daq.max_duty))
		self.pwm_max_btn.grid(row=3, column=15, sticky=W)

		# ###############################################################################################
		# Run Loop
		# ###############################################################################################

		# print("Program initialization Complete!\n")
		self.check_pressure()
		self.master_window.mainloop()

	def timer_call(self):
		# this is a routine function call
		# update Status before set
		# set channel
		for i in range(N_CHANNEL):
			if self.chVal[i] != self.slider[i].get():
				time.sleep(MIN_INTERVAL/2000.0)
				self.set_channel(i)

				# check if some error occurred
				if not self.currentState:
					self.reset_serial()
					return

		if self.currentState:
			self.master_window.after(MIN_INTERVAL, self.timer_call)

	def set_channel(self, x):
		if self.SerialApp.getStatus():
			val = self.slider[x].get()
			if self.chVal[x] != val:
				# ################################## Serial processing ########################################
				# parity calculation
				# par = x << 10 | val
				# par ^= par >> 8
				# par ^= par >> 4
				# par ^= par >> 2
				# par ^= par >> 1
				# parity = (~par)
				#
				# c = [0, 0]
				#
				# two byte of data: channel 5bits, value 10bits, parity 1bit (set on even)
				# c[0] = struct.pack("B", (((x & 0x1F) << 3) | ((val >> 7) & 0x7)) & 0xff)
				# c[1] = struct.pack("B", (val << 1 | (parity & 0x1)) & 0xff)
				#
				# initiate communication
				# self.SerialApp.resetBuffer()
				# self.SerialApp.sentByte(b's')
				#
				# account for frequency limit, repeat until sent
				# self.SerialApp.sentBytes(c, 2)
				#
				# b = 0
				# b = self.SerialApp.readByte()

				if x == 0:
					self.daq.update_duty_cycle_0(val)
				elif x == 1:
					self.daq.update_duty_cycle_1(val)
				elif x == 2:
					self.daq.update_duty_cycle_2(val)
				elif x == 3:
					self.daq.update_duty_cycle_3(val)

				# if b == b'k':
				# 	if VERBOSE > 0:
				# 		print("Channel %d is set to %d" % (x+1, val))
				# 	self.chVal[x] = val
				# else:	 # return string mismatch
				# 	if VERBOSE > 0:
				# 		print("return string mismatch")
		else:
			self.reset_serial()
			print("Serial Not Connected!")

	def toggle_state(self, in_val):

		if not in_val:
			self.currentState = False
			print("Disable all input")
			# self.disableAllBtn.config(state='disabled')
			# self.enableAllBtn.config(state='normal')
			# self.loadBtn.config(state='normal')
			self.zeroAllBtn.config(state='disabled')
			for i in range(N_CHANNEL):
				self.slider[i].config(state='disabled')
				self.setMinBtn[i].config(state='disabled')
				self.setMaxBtn[i].config(state='disabled')
				self.chValEntry[i].config(state='disabled')
		else:
			self.currentState = True
			print("Re-enable all input")
			# self.disableAllBtn.config(state='normal')
			# self.enableAllBtn.config(state='disabled')
			# self.loadBtn.config(state='disabled')
			self.zeroAllBtn.config(state='normal')
			for i in range(N_CHANNEL):
				self.slider[i].config(state='normal')
				self.setMinBtn[i].config(state='normal')
				self.setMaxBtn[i].config(state='normal')
				self.chValEntry[i].config(state='normal')

			# initialize routine function
			self.master_window.after(MIN_INTERVAL, self.timer_call)

	def read_val(self, ind, src, dc):
		# src=0: source from slider
		# src=1: source from Entry Field
		if src == 0:
			if VERBOSE > 1:
				print("read_val Called by ch %d Slider" % (ind+1))
			self.chValEntryVar[ind].set(self.slider[ind].get())

		if src == 1:	  # source from entry field
			if VERBOSE > 1:
				print("read_val Called by ch %d Entry" % (ind+1))

			try: 		# try reading Entry field data
				set_val = int(self.chValEntryVar[ind].get())
			except ValueError:
				print("Value enter is not integer")
				set_val = self.slider[ind].get()			 # error set to Slide bar value

			if set_val > self.valMax[ind]:
				print("Value enter is not in range")
				set_val = self.valMax[ind]
			elif set_val < self.VAL_MIN:
				print("Value enter is not in range")
				set_val = self.VAL_MIN

			self.chValEntryVar[ind].set(set_val)
			self.slider[ind].set(set_val)
			
		self.chValkPaLabel[ind].config(text="%.2f"%(self.slider[ind].get()*1.9607843137))

	def set_mn(self, ind, target):
		if target == 1:
			if VERBOSE > 1:
				print("set ch %d to Max" % (ind+1))
			self.slider[ind].set(self.valMax[ind])
		else:
			if VERBOSE>1:
				print("set ch %d to Min" % (ind+1))
			self.slider[ind].set(self.VAL_MIN)

	def set_max(self, ind, dc):
		if VERBOSE > 1:
			print("change ch %d Max settting" % (ind+1))
		try:
			set_val = int(self.maxEntryVar[ind].get())
		except ValueError:
			print("Value entered is invalid")
			self.valMax[ind] = self.VAL_MAX
			self.slider[ind].config(from_=self.VAL_MAX)
			self.maxEntryVar[ind].set(self.VAL_MAX)
			return
		if self.VAL_MAX<set_val:
			print("Error, out of bound")
			self.valMax[ind] = self.VAL_MAX
			self.slider[ind].config(from_=self.VAL_MAX)
			self.maxEntryVar[ind].set(self.VAL_MAX)
		elif self.slider[ind].get() <= set_val:
			self.valMax[ind] = set_val
			self.slider[ind].config(from_=set_val)
		else:
			print("Error, smaller than current value")
			self.valMax[ind] = self.slider[ind].get()
			self.slider[ind].config(from_=self.slider[ind].get())
			self.maxEntryVar[ind].set(self.slider[ind].get())	

	def zero_all(self):
		if VERBOSE > 1:
			print("Zero all Channels")

		for i in range(N_CHANNEL):
			self.slider[i].set(self.VAL_MIN)

	def refresh_serial(self):
		print("Refreshing Serial List")
		# ports = list(serialList.comports())
		self.SerialApp.updatePortList()
		if VERBOSE > 1:
			self.SerialApp.listAllPort()
		p_list = ["" for x in range(self.SerialApp.n_portsList)]
		for i in range(self.SerialApp.n_portsList):
			p_list[i] = self.SerialApp.portsList[i].device
		self.SerialList.destroy()
		self.SerialList = tk.OptionMenu(self.master_window, self.serialPort, *p_list)
		self.SerialList.grid(row=7, column=3, columnspan=4)

	def initialize_serial(self):
		if not self.SerialApp.getStatus():
			print("Initialize Serial Conenction to %s" % self.serialPort.get())
			time.sleep(0.1)
			if self.SerialApp.connectDevice(self.serialPort.get()):
				print("Serial Connection Successful")
				self.serialDisconnectBtn.config(state='normal')
				self.serialConnectBtn.config(state='disabled')
				self.serialStatusLabel.config(bg='green')
				self.toggle_state(True)
				self.zero_all()
			else:
				self.serialStatusLabel.config(bg='red')
				self.toggle_state(False)

	def reset_serial(self):
		if self.SerialApp.getStatus():
			self.serialDisconnectBtn.config(state='disabled')
			self.serialConnectBtn.config(state='normal')
			self.serialStatusLabel.config(bg='red')
			self.SerialApp.reset()
			self.toggle_state(False)

	def close_window(self):
		self.pressure.destroy()
		self.daq.close_pwm()
		self.daq.close_voltage()
		time.sleep(1)
		self.master_window.destroy()
		raise SystemExit

	def set_manuf(self):
		self.syringe.syringe_type(self.manuf_list_var.get(), self.manuf_vol_var.get(), self.manuf_unit_list_var.get())
		self.syringe.infuse_rate(self.infuse_rate_var.get(), self.inf_unit_list_var.get())
		self.syringe.withdraw_rate(self.withdraw_rate_var.get(), self.with_unit_list_var.get())

	def check_pressure(self):
		self.pressure_var.set(self.daq.read_pressure(self.pressure_unit_list_var.get()))
		threading.Timer(0.1, self.check_pressure).start()

	def pwm_start(self):
		self.daq.write_pulses()
		self.pwm_running = True

	def pwm_stop(self):

		self.pwm_running = False

	def pwm_on_off(self):
		if not self.pwm_running:
			self.pwm_start()
			return 'green'
		elif self.pwm_running:
			self.pwm_stop()
			return 'red'



if __name__ == '__main__':
	main()
