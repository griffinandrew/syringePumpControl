from Jacob_Pump import Pump
from serial import Serial
from threading import Thread
import multiprocessing
import time

Pump1 = Pump("COM3","11 PICO PLUS ELITE 3.0.7")
Pump2 = Pump("COM4","11 PICO PLUS ELITE 3.0.7")
Pump3 = Pump("COM5","11 PICO PLUS ELITE 3.0.7")

#temp vars to store volumes that are being changed each time stored in string for print statements
vol1=""
vol2=""
vol3=""
button_push = False


chamber_1_diff = False
chamber_2_diff = False
chamber_3_diff = False

# Define a class that communicates the values from the GUI to the pumps when the GO button is pushed
class Backend:

    def __init__(self, gui):

        # Call in values from the GUI
        self.gui = gui

        # Set slider values to 0
        self.oldVal1 = 0
        self.curVal1 = 0

        self.oldVal2 = 0
        self.curVal2 = 0

        self.oldVal3 = 0
        self.curVal3 = 0

    def pump_1_thread_task(self):
        self.oldVal1 = self.curVal1

        self.curVal1 = self.gui.c1.get()

        self.deltVal1 = self.curVal1 - self.oldVal1

        self.curVol1 = 0.01 * self.curVal1 * float(self.gui.maxvol_entry.get())

        global vol1
        vol1 = str(self.curVol1)

        self.rate = float(self.gui.rate_entry.get())
        self.vol = float(self.gui.vol_entry.get())
        self.diam = float(self.gui.diam_entry.get())

        # Set the pump parameters for Pump 1
        Pump1.c_volume()
        Pump1.ci_volume()
        Pump1.cw_volume()
        Pump1.syringe_vol(str(self.vol))
        Pump1.syringe_diam(str(self.diam))
        Pump1.infuse_rate(str(self.rate), "ml/min")
        Pump1.withdraw_rate(str(self.rate), "ml/min")
        Pump1.target_volume(str(abs(self.curVol1)), "ml")

        if self.deltVal1 < 0:
            Pump1.withdraw_pump()
        elif self.deltVal1 > 0:
            Pump1.infuse_pump()
        else:
            Pump1.stop_pump()

    def pump_2_thread_task(self):
        self.oldVal2 = self.curVal2

        self.curVal2 = self.gui.c2.get()

        self.deltVal2 = self.curVal2 - self.oldVal2

        self.curVol2 = 0.01 * self.curVal2 * float(self.gui.maxvol_entry.get())

        global vol2
        vol2 = str(self.curVol2)

        self.rate = float(self.gui.rate_entry.get())
        self.vol = float(self.gui.vol_entry.get())
        self.diam = float(self.gui.diam_entry.get())

        # Set the pump parameters for Pump 2
        Pump2.c_volume()
        Pump2.ci_volume()
        Pump2.cw_volume()
        Pump2.syringe_vol(str(self.vol))
        Pump2.syringe_diam(str(self.diam))
        Pump2.infuse_rate(str(self.rate), "ml/min")
        Pump2.withdraw_rate(str(self.rate), "ml/min")
        Pump2.target_volume(str(abs(self.curVol2)), "ml")

        if self.deltVal2 < 0:
            Pump2.withdraw_pump()
        elif self.deltVal2 > 0:
            Pump2.infuse_pump()
        else:
            Pump2.stop_pump()

    def pump_3_thread_task(self):
        self.oldVal3 = self.curVal3

        self.curVal3 = self.gui.c3.get()

        self.deltVal3 = self.curVal3 - self.oldVal3

        self.curVol3 = 0.01 * self.curVal3 * float(self.gui.maxvol_entry.get())

        global vol3
        vol3 = str(self.curVol3)

        self.rate = float(self.gui.rate_entry.get())
        self.vol = float(self.gui.vol_entry.get())
        self.diam = float(self.gui.diam_entry.get())

        # Set the pump parameters for Pump 3
        Pump3.c_volume()
        Pump3.ci_volume()
        Pump3.cw_volume()
        Pump3.syringe_vol(str(self.vol))
        Pump3.syringe_diam(str(self.diam))
        Pump3.infuse_rate(str(self.rate), "ml/min")
        Pump3.withdraw_rate(str(self.rate), "ml/min")
        Pump3.target_volume(str(abs(self.curVol3)), "ml")

        if self.deltVal3 < 0:
            Pump3.withdraw_pump()
        elif self.deltVal3 > 0:
            Pump3.infuse_pump()
        else:
            Pump3.stop_pump()

    #TypeError: can't pickle _tkinter.tkapp object

    def buttonPush(self):
        global button_push
        button_push = True
        global vol1, vol2, vol3
        global val1, val2, val3
        self.gui.update_after()


    #checks all pumps when check pump button pressed
    def check_button(self):
        Pump1.check_pump("11 PICO PLUS ELITE 3.0.7")
        Pump2.check_pump("11 PICO PLUS ELITE 3.0.7")
        Pump3.check_pump("11 PICO PLUS ELITE 3.0.7")

    def display_vol_button(self):
        global vol1, vol2, vol3
        print(vol1, vol2, vol3)

#this will not work for current implementation
    def stop_button(self): #this should just call stop pump nyi
        global button_push
        button_push = False


'''

def buttonPush(self):

    # Slide all the current slider values to the old slider values
    self.oldVal1 = self.curVal1
    self.oldVal2 = self.curVal2
    self.oldVal3 = self.curVal3

    # Set all current slider values equal to values from the GUI
    self.curVal1 = self.gui.c1.get()
    self.curVal2 = self.gui.c2.get()
    self.curVal3 = self.gui.c3.get()

    # Set the values for percent change in volume from each slider
    self.deltVal1 = self.curVal1 - self.oldVal1
    self.deltVal2 = self.curVal2 - self.oldVal2
    self.deltVal3 = self.curVal3 - self.oldVal3

    # Multiply by the max volume per channel and divide by 100 to get the absolute
    # change in volume for each channel
    self.deltVol1 = 0.01 * self.deltVal1 * float(self.gui.maxvol_entry.get())
    self.deltVol2 = 0.01 * self.deltVal2 * float(self.gui.maxvol_entry.get())
    self.deltVol3 = 0.01 * self.deltVal3 * float(self.gui.maxvol_entry.get())

    # Define other GUI parameters
    self.rate = float(self.gui.rate_entry.get())
    self.vol = float(self.gui.vol_entry.get())
    self.diam = float(self.gui.diam_entry.get())

    # Print volume changes for each channel as a sanity check
    print(str(self.deltVol1), str(self.deltVol2), str(self.deltVol3))

    # Set the pump parameters for Pump 1
    Pump1.c_volume()
    Pump1.ci_volume()
    Pump1.cw_volume()
    Pump1.syringe_vol(str(self.vol))
    Pump1.syringe_diam(str(self.diam))
    Pump1.infuse_rate(str(self.rate), "ml/min")
    Pump1.withdraw_rate(str(self.rate), "ml/min")
    Pump1.target_volume(str(abs(self.deltVol1)), "ml")

    # Set the pump parameters for Pump 2
    Pump2.c_volume()
    Pump2.ci_volume()
    Pump2.cw_volume()
    Pump2.syringe_vol(str(self.vol))
    Pump2.syringe_diam(str(self.diam))
    Pump2.infuse_rate(str(self.rate), "ml/min")
    Pump2.withdraw_rate(str(self.rate), "ml/min")
    Pump2.target_volume(str(abs(self.deltVol2)), "ml")

    # Set the pump parameters for Pump 3
    Pump3.c_volume()
    Pump3.ci_volume()
    Pump3.cw_volume()
    Pump3.syringe_vol(str(self.vol))
    Pump3.syringe_diam(str(self.diam))
    Pump3.infuse_rate(str(self.rate), "ml/min")
    Pump3.withdraw_rate(str(self.rate), "ml/min")
    Pump3.target_volume(str(abs(self.deltVol3)), "ml")

    # Actuate each pump
    if self.deltVol1 < 0:
        Pump1.withdraw_pump()
    elif self.deltVol1 > 0:
        Pump1.infuse_pump()
    else:
        Pump1.stop_pump()

    if self.deltVol2 < 0:
        Pump2.withdraw_pump()
    elif self.deltVol2 > 0:
        Pump2.infuse_pump()
    else:
        Pump2.stop_pump()

    if self.deltVol3 < 0:
        Pump3.withdraw_pump()
    elif self.deltVol3 > 0:
        Pump3.infuse_pump()
    else:
        Pump3.stop_pump()

'''