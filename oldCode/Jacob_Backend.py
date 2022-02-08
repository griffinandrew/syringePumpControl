from Jacob_Pump import Pump
from serial import Serial
import multithreading

Pump1 = Pump("COM3","11 PICO PLUS ELITE 3.0.7")
Pump2 = Pump("COM4","11 PICO PLUS ELITE 3.0.7")
Pump3 = Pump("COM5","11 PICO PLUS ELITE 3.0.7")

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


    # i believe that if i create a thread for each of pump 1-3 actions it should work concurrently

        def pump_1_thread():
            self.oldVal1 = self.curVal1
            self.curVal1 = self.gui.c1.get()
            self.deltVal1 = self.curVal1 - self.oldVal1
            self.deltVol1 = 0.01 * self.deltVal1 * float(self.gui.maxvol_entry.get())





                           
    #checks all pumps when check pump button pressed
    def check_button(self):
        Pump1.check_pump("11 PICO PLUS ELITE 3.0.7")
        Pump2.check_pump("11 PICO PLUS ELITE 3.0.7")
        Pump3.check_pump("11 PICO PLUS ELITE 3.0.7")