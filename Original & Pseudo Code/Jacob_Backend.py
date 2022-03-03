from Jacob_Pump import Pump
import time

Pump1 = Pump("COM3","11 PICO PLUS ELITE 3.0.7")
Pump2 = Pump("COM4","11 PICO PLUS ELITE 3.0.7")
Pump3 = Pump("COM5","11 PICO PLUS ELITE 3.0.7")


global isRunning
isRunning = False

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

        self.rate = float(self.gui.rate_entry.get())
        self.vol = float(self.gui.vol_entry.get())
        self.diam = float(self.gui.diam_entry.get())
        self.numPump = float(self.gui.varPump.get())

        self.t_step = 5 # this is in seconds it might have to be changed
        self.pump_step =  self.rate * self.t_step * (1 / 60)

        self.isInflating1 = False
        self.isInflating2 = False
        self.isInflating3 = False

        self.com_prev1 = 0
        self.com_prev2 = 0
        self.com_prev3 = 0

        self.com_cur1 = 0
        self.com_cur2 = 0
        self.com_cur3 = 0

        self.pos_cur1 = 0
        self.pos_cur2 = 0
        self.pos_cur3 = 0

        self.pos_prev1 = 0
        self.pos_prev2 = 0
        self.pos_prev3 = 0

        self.val_to_set1 = 0
        self.val_to_set2 = 0
        self.val_to_set3 = 0

        self.setVol1 = 0
        self.setVol2 = 0
        self.setVol3 = 0

    def buttonPush(self):
        self.setPumpAttributes()
        self.gui.update()
        global isRunning
        isRunning = True

    def actuatePumps(self):

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


        #lets move this to a init
        # Define other GUI parameters
        #self.rate = float(self.gui.rate_entry.get())
        #self.vol = float(self.gui.vol_entry.get())
        #self.diam = float(self.gui.diam_entry.get())
        #self.numPump = float(self.gui.varPump.get())

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


    def volumeCheck(self):

        #i'm thinking that these can just be attributes of the class in order to get around them being global

        global com_cur1, com_cur2, com_cur3
        global com_prev1, com_prev2, com_prev3

        global pos_cur1, pos_cur2, pos_cur3
        global pos_prev1, pos_prev2, pos_prev3

        global isInflating

        t_step = 5000 # this needs to be thought through because this should be .5 seconds
        pump_step = self.rate * t_step * (1/60)

        while isRunning is True:
            time.sleep(t_step) # iterate every .5 sec

            com_cur1 = self.gui.c1.get()
            com_cur2 = self.gui.c2.get()
            com_cur3 = self.gui.c3.get()

            if not isInflating:
                pos_cur1 = com_prev1
                pos_cur2 = com_prev2
                pos_cur3 = com_prev3


                # these will have to be self
                vol_to_set1 = com_cur1 - pos_cur1
                vol_to_set2 = com_cur2 - pos_cur2
                vol_to_set3 = com_cur3 - pos_cur3

                com_prev1 = com_cur1
                com_prev2 = com_cur2
                com_prev3 = com_cur3

                pos_prev1 = pos_cur1
                pos_prev2 = pos_cur2
                pos_prev3 = pos_cur3

            else:
                pos_cur1 = pos_prev1 + pump_step
                pos_cur2 = pos_prev2 + pump_step
                pos_cur3 = pos_prev3 + pump_step

                vol_to_set1 = com_cur1 - pos_cur1
                vol_to_set2 = com_cur2 - pos_cur2
                vol_to_set3 = com_cur3 - pos_cur3

                com_prev1 = com_cur1
                com_prev2 = com_cur2
                com_prev3 = com_cur3

                pos_prev1 = pos_cur1
                pos_prev2 = pos_cur2
                pos_prev3 = pos_cur3

            if vol_to_set1 <= pump_step and vol_to_set2 <= pump_step and vol_to_set3 <= pump_step:
                isInflating = False

            else:
                isInflating = True


    def VolumeCheck1(self):

        while isRunning is True:
            time.sleep(self.t_step)

            self.com_cur1 = self.gui.c1.get()

            if not self.isInflating1:
                self.pos_cur1 = self.com_prev1

                self.val_to_set1 = self.com_cur1 - self.pos_cur1

                self.setVol1 = 0.01 * self.val_to_set1 * float(self.gui.maxvol_entry.get())

                Pump1.target_volume(str(abs(self.setVol1)), "ml")

                if self.setVol1 < 0:
                    Pump1.withdraw_pump()
                elif self.setVol1 > 0:
                    Pump1.infuse_pump()
                else:
                    Pump1.stop_pump()

                self.com_prev1 = self.com_cur1

                self.pos_prev1 = self.pos_cur1

            else:
                self.pos_cur1 = self.pos_prev1 + self.pump_step


            #im a little confused why this condition is at the end I get it for the first iteration but after
            #that the condition will be set on the previous run which doesnt make any sense
            if self.setVol1 <= self.pump_step:
                self.isInflating1 = False

            else:
                self.isInflating1 = True

    def VolumeCheck2(self):

        while isRunning is True:
            time.sleep(self.t_step)

            self.com_cur2 = self.gui.c2.get()

            if not self.isInflating2:
                self.pos_cur2 = self.com_prev2

                self.val_to_set2 = self.com_cur2 - self.pos_cur2

                self.setVol2 = 0.01 * self.val_to_set2 * float(self.gui.maxvol_entry.get())

                #actuate pump here
                Pump2.target_volume(str(abs(self.setVol2)), "ml")

                if self.setVol2 < 0:
                    Pump2.withdraw_pump()
                elif self.setVol2 > 0:
                    Pump2.infuse_pump()
                else:
                    Pump2.stop_pump()



                self.com_prev2 = self.com_cur2

                self.pos_prev2 = self.pos_cur2

            else:
                self.pos_cur2 = self.pos_prev2 + self.pump_step

            # im a little confused why this condition is at the end I get it for the first iteration but after
            # that the condition will be set on the previous run which doesnt make any sense
            if self.setVol2 <= self.pump_step:
                self.isInflating2 = False

            else:
                self.isInflating2 = True


    def VolumeCheck3(self):

        while isRunning is True:
            time.sleep(self.t_step)

            self.com_cur3 = self.gui.c3.get()

            if not self.isInflating3:
                self.pos_cur3 = self.com_prev3

                self.val_to_set3 = self.com_cur3 - self.pos_cur3

                self.setVol3 = 0.01 * self.val_to_set3 * float(self.gui.maxvol_entry.get())

                Pump3.target_volume(str(abs(self.setVol3)), "ml")

                if self.setVol3 < 0:
                    Pump3.withdraw_pump()
                elif self.setVol3 > 0:
                    Pump3.infuse_pump()
                else:
                    Pump3.stop_pump()

                self.com_prev3 = self.com_cur3

                self.pos_prev3 = self.pos_cur3

            else:
                self.pos_cur3 = self.pos_prev3 + self.pump_step

            # im a little confused why this condition is at the end I get it for the first iteration but after
            # that the condition will be set on the previous run which doesnt make any sense
            if self.setVol3 <= self.pump_step:
                self.isInflating3 = False

            else:
                self.isInflating3 = True



    def setPumpAttributes(self):

        # Set the pump parameters for Pump 1
        Pump1.c_volume()
        Pump1.ci_volume()
        Pump1.cw_volume()
        Pump1.syringe_vol(str(self.vol))
        Pump1.syringe_diam(str(self.diam))
        Pump1.infuse_rate(str(self.rate), "ml/min")
        Pump1.withdraw_rate(str(self.rate), "ml/min")

        # Set the pump parameters for Pump 2
        Pump2.c_volume()
        Pump2.ci_volume()
        Pump2.cw_volume()
        Pump2.syringe_vol(str(self.vol))
        Pump2.syringe_diam(str(self.diam))
        Pump2.infuse_rate(str(self.rate), "ml/min")
        Pump2.withdraw_rate(str(self.rate), "ml/min")

        # Set the pump parameters for Pump 3
        Pump3.c_volume()
        Pump3.ci_volume()
        Pump3.cw_volume()
        Pump3.syringe_vol(str(self.vol))
        Pump3.syringe_diam(str(self.diam))
        Pump3.infuse_rate(str(self.rate), "ml/min")
        Pump3.withdraw_rate(str(self.rate), "ml/min")





    #checks all pumps when check pump button pressed
    def check_button(self):
        Pump1.check_pump("11 PICO PLUS ELITE 3.0.7")
        Pump2.check_pump("11 PICO PLUS ELITE 3.0.7")
        Pump3.check_pump("11 PICO PLUS ELITE 3.0.7")