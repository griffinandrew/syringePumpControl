from Jacob_Pump import Pump
import warnings

Pump3 = Pump("COM3","11 PICO PLUS ELITE 3.0.7") #Pump("COM3","11 ELITE I/W Single 3.0.7")
Pump2 = Pump("COM4","11 PICO PLUS ELITE 3.0.7")
Pump1 = Pump("COM5","11 PICO PLUS ELITE 3.0.7")

# Define a class that communicates the values from the GUI to the pumps when the GO button is pushed
class Backend:

    def __init__(self, gui):

        # Call in values from the GUI
        self.gui = gui

        # Initialize syringe settings
        self.syringe_settings = {}

        # Set slider values to 0
        self.oldVal1 = 0
        self.curVal1 = 0

        self.oldVal2 = 0
        self.curVal2 = 0

        self.oldVal3 = 0
        self.curVal3 = 0

    def set_initial_parameters(self):
        for k, v in self.syringe_settings.items():
            print(f"Setting initial syringe {k} value to {v}")

        # Check that each pump is properly connected
        Pump1.check_pump("11 PICO PLUS ELITE 3.0.7")
        Pump2.check_pump("11 PICO PLUS ELITE 3.0.7")
        Pump3.check_pump("11 PICO PLUS ELITE 3.0.7")

        # Define pump parameters for Pump 1
        Pump1.syringe_vol(str(self.syringe_settings["vol"]))
        Pump1.syringe_diam(str(self.syringe_settings["diam"]))
        Pump1.infuse_rate(str(self.syringe_settings["rate"]), "ml/min")
        Pump1.withdraw_rate(str(self.syringe_settings["rate"]), "ml/min")

        # Define pump parameters for Pump 2
        Pump2.syringe_vol(str(self.syringe_settings["vol"]))
        Pump2.syringe_diam(str(self.syringe_settings["diam"]))
        Pump2.infuse_rate(str(self.syringe_settings["rate"]), "ml/min")
        Pump2.withdraw_rate(str(self.syringe_settings["rate"]), "ml/min")

        # Define pump parameters for Pump 3
        Pump3.syringe_vol(str(self.syringe_settings["vol"]))
        Pump3.syringe_diam(str(self.syringe_settings["diam"]))
        Pump3.infuse_rate(str(self.syringe_settings["rate"]), "ml/min")
        Pump3.withdraw_rate(str(self.syringe_settings["rate"]), "ml/min")

    def buttonPush(self):

        if not self.syringe_settings:
            # try:
            self.syringe_settings = {"rate": float(self.gui.rate_entry.get()),
                                     "vol": float(self.gui.vol_entry.get()),
                                     "diam": float(self.gui.diam_entry.get()),
                                     "num_pump": float(self.gui.varPump.get())}
            self.set_initial_parameters()

            # except Exception as e:
            # print(e)
            # print("Invalid format received for the parameters. Try again with numbers!")

        else:
            if (self.syringe_settings['rate'] != float(self.gui.rate_entry.get()) or
                    self.syringe_settings['vol'] != float(self.gui.vol_entry.get()) or
                    self.syringe_settings['diam'] != float(self.gui.diam_entry.get())):
                warnings.warn("GUI currently does not support changing syringe settings during the experiment.")

        # Slide all the current slider values to the old slider values
        self.oldVal1 = self.curVal1
        self.oldVal2 = self.curVal2
        self.oldVal3 = self.curVal3

        # Set all current slider values equal to values from the GUI
        self.curVal1 = self.gui.c1.get()
        self.curVal2 = self.gui.c2.get()
        self.curVal3 = self.gui.c3.get()

        # Set the values for percent change in volume from each slider
        deltVal1 = self.curVal1 - self.oldVal1
        deltVal2 = self.curVal2 - self.oldVal2
        deltVal3 = self.curVal3 - self.oldVal3

        # Multiply by the max volume per channel and divide by 100 to get the absolute
        # change in volume for each channel
        deltVol1 = 0.01 * deltVal1 * float(self.gui.maxvol_entry.get())
        deltVol2 = 0.01 * deltVal2 * float(self.gui.maxvol_entry.get())
        deltVol3 = 0.01 * deltVal3 * float(self.gui.maxvol_entry.get())

        # Define other GUI parameters
        self.rate = float(self.gui.rate_entry.get())
        self.vol = float(self.gui.vol_entry.get())
        self.diam = float(self.gui.diam_entry.get())
        self.numPump = float(self.gui.varPump.get())

        # Print volume changes for each channel as a sanity check
        print("parameters set to: ")
        print(str(deltVol1), str(deltVol2), str(deltVol3))

        Pump1.c_volume()
        Pump1.ci_volume()
        Pump1.cw_volume()
        Pump1.target_volume(str(abs(deltVol1)), "ml")

        # Clear previous pump parameters for Pump 2
        Pump2.c_volume()
        Pump2.ci_volume()
        Pump2.cw_volume()
        Pump2.target_volume(str(abs(deltVol2)), "ml")

        # Clear previous pump parameters for Pump 3
        Pump3.c_volume()
        Pump3.ci_volume()
        Pump3.cw_volume()
        Pump3.target_volume(str(abs(deltVol3)), "ml")

        # Check that each pump is properly connected
        #Pump1.check_pump("11 PICO PLUS ELITE 3.0.7")
        #Pump2.check_pump("11 PICO PLUS ELITE 3.0.7")
        #Pump3.check_pump("11 PICO PLUS ELITE 3.0.7")

        # Set the pump parameters for Pump 1
        #Pump1.c_volume()
        #Pump1.ci_volume()
        #Pump1.cw_volume()
        #Pump1.syringe_vol(str(self.vol))
        #Pump1.syringe_diam(str(self.diam))
        #Pump1.infuse_rate(str(self.rate), "ml/min")
        #Pump1.withdraw_rate(str(self.rate), "ml/min")
        #Pump1.target_volume(str(abs(deltVol1)), "ml")

        # Set the pump parameters for Pump 2
        #Pump2.c_volume()
        #Pump2.ci_volume()
        #Pump2.cw_volume()
        #Pump2.syringe_vol(str(self.vol))
        #Pump2.syringe_diam(str(self.diam))
        #Pump2.infuse_rate(str(self.rate), "ml/min")
        #Pump2.withdraw_rate(str(self.rate), "ml/min")
        #Pump2.target_volume(str(abs(deltVol2)), "ml")

        # Set the pump parameters for Pump 3
        #Pump3.c_volume()
        #Pump3.ci_volume()
        #Pump3.cw_volume()
        #Pump3.syringe_vol(str(self.vol))
        #Pump3.syringe_diam(str(self.diam))
        #Pump3.infuse_rate(str(self.rate), "ml/min")
        #Pump3.withdraw_rate(str(self.rate), "ml/min")
        #Pump3.target_volume(str(abs(deltVol3)), "ml")

        # Actuate each pump
        if deltVol1 < 0:
            Pump1.withdraw_pump()
        elif deltVol1 > 0:
            Pump1.infuse_pump()
        else:
            Pump1.stop_pump()

        if deltVol2 < 0:
            Pump2.withdraw_pump()
        elif deltVol2 > 0:
            Pump2.infuse_pump()
        else:
            Pump2.stop_pump()
            
        if deltVol3 < 0:
            Pump3.withdraw_pump()
        elif deltVol3 > 0:
            Pump3.infuse_pump()
        else:
            Pump3.stop_pump()
                           



