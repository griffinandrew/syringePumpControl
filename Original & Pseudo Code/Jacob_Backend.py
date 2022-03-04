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

        self.rate = 0
        self.vol = 0
        self.diam = 0
        self.numPump = 0

        self.t_step = .5 # this is in seconds it might have to be changed not totally sure how it needs to be represented
        self.pump_step = 0   # I am getting the proper value in the the set attributes section #self.rate * self.t_step * (1 / 60) # this is wrong here I think, it will be init to 0 because rate is 0

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

        self.setVol1 = 0
        self.setVol2 = 0
        self.setVol3 = 0

    def buttonPush(self):
        self.setAttributes()
        global isRunning
        isRunning = True # this isn't used
        self.gui.update() # update makes the call to backend actuate recursively


    def actuate(self):
        #while isRunning is True:
            #time.sleep(self.t_step) # its pausing at first because this is here

            #pump 1
            self.com_cur1 = self.gui.c1.get()

            if not self.isInflating1:
                self.pos_cur1 = self.com_prev1
                val_to_set1 = self.com_cur1 - self.pos_cur1
                self.setVol1 = 0.01 * val_to_set1 * float(self.gui.maxvol_entry.get())
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
                self.pos_cur1 = self.pos_prev1 + self.pump_step # i think that this is just the infusing case  could if withdrawing this will need to be subtracted

                val_to_set1 = self.com_cur1 - self.pos_cur1
                self.setVol1 = 0.01 * val_to_set1 * float(self.gui.maxvol_entry.get())
                Pump1.target_volume(str(abs(self.setVol1)), "ml")

                if self.setVol1 < 0:
                    Pump1.withdraw_pump()
                elif self.setVol1 > 0:
                    Pump1.infuse_pump()
                else:
                    Pump1.stop_pump()

                self.com_prev1 = self.com_cur1
                self.pos_prev1 = self.pos_cur1

            # im a little confused why this condition is at the end I get it for the first iteration but after
            # that the condition will be set on the previous run which doesnt make any sense
            if self.setVol1 <= self.pump_step:
                self.isInflating1 = False
            else:
                self.isInflating1 = True


                ######end pump 1
                ####pump 2

            self.com_cur2 = self.gui.c2.get()

            if not self.isInflating2:
                self.pos_cur2 = self.com_prev2
                val_to_set2 = self.com_cur2 - self.pos_cur2
                self.setVol2 = 0.01 * val_to_set2 * float(self.gui.maxvol_entry.get())
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
                val_to_set2 = self.com_cur2 - self.pos_cur2
                self.setVol2 = 0.01 * val_to_set2 * float(self.gui.maxvol_entry.get())
                Pump2.target_volume(str(abs(self.setVol2)), "ml")

                if self.setVol2 < 0:
                    Pump2.withdraw_pump()
                elif self.setVol2 > 0:
                    Pump2.infuse_pump()
                else:
                    Pump2.stop_pump()

                self.com_prev2 = self.com_cur2
                self.pos_prev2 = self.pos_cur2

                # im a little confused why this condition is at the end I get it for the first iteration but after
                # that the condition will be set on the previous run which doesnt make any sense
            if self.setVol2 <= self.pump_step:
                self.isInflating2 = False
            else:
                self.isInflating2 = True

            print(self.isInflating2)
                ###end pump 2

                # pump3
            self.com_cur3 = self.gui.c3.get()

            if not self.isInflating3:
                self.pos_cur3 = self.com_prev3
                val_to_set3 = self.com_cur3 - self.pos_cur3
                self.setVol3 = 0.01 * val_to_set3 * float(self.gui.maxvol_entry.get())
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
                val_to_set3 = self.com_cur3 - self.pos_cur3
                self.setVol3 = 0.01 * val_to_set3 * float(self.gui.maxvol_entry.get())
                Pump3.target_volume(str(abs(self.setVol3)), "ml")

                if self.setVol3 < 0:
                    Pump3.withdraw_pump()
                elif self.setVol3 > 0:
                    Pump3.infuse_pump()
                else:
                    Pump3.stop_pump()

                self.com_prev3 = self.com_cur3
                self.pos_prev3 = self.pos_cur3

                # im a little confused why this condition is at the end I get it for the first iteration but after
                # that the condition will be set on the previous run which doesnt make any sense
            if self.setVol3 <= self.pump_step:
                self.isInflating3 = False
            else:
                self.isInflating3 = True

            print(self.isInflating3) # my theory is that this post checking is causing issues,


    def actuate1(self):

        #while isRunning is True:
            #time.sleep(self.t_step)
        #print("inflating 1 at start ")
        #print(self.isInflating1)

        Pump1.c_volume()
        Pump1.ci_volume()
        Pump1.cw_volume()
        Pump1.syringe_vol(str(self.vol))
        Pump1.syringe_diam(str(self.diam))
        Pump1.infuse_rate(str(self.rate), "ml/min")
        Pump1.withdraw_rate(str(self.rate), "ml/min")

        self.com_cur1 = self.gui.c1.get()

        if not self.isInflating1:
            self.pos_cur1 = self.com_prev1
            val_to_set1 = self.com_cur1 - self.pos_cur1
            self.setVol1 = 0.01 * val_to_set1 * float(self.gui.maxvol_entry.get())
            Pump1.target_volume(str(abs(self.setVol1)), "ml")

        else:
            self.pos_cur1 = self.pos_prev1 + self.pump_step
            val_to_set1 = self.com_cur1 - self.pos_cur1
            self.setVol1 = 0.01 * val_to_set1 * float(self.gui.maxvol_entry.get())
            Pump1.target_volume(str(abs(self.setVol1)), "ml")

        if self.setVol1 < 0:
            Pump1.withdraw_pump()
        elif self.setVol1 > 0:
            Pump1.infuse_pump()
        else:
            Pump1.stop_pump()

        self.com_prev1 = self.com_cur1
        self.pos_prev1 = self.pos_cur1
            #im a little confused why this condition is at the end I get it for the first iteration but after
            #that the condition will be set on the previous run which doesnt make any sense
        if self.setVol1 <= self.pump_step: # i need to think more about this conditonal
            self.isInflating1 = False
        else:
            self.isInflating1 = True


    def actuate2(self):

        #while isRunning is True:
            #time.sleep(self.t_step)
        #print("inflating 2 at start ")
        #print(self.isInflating2)

        # Set the pump parameters for Pump 2
        Pump2.c_volume()
        Pump2.ci_volume()
        Pump2.cw_volume()
        Pump2.syringe_vol(str(self.vol))
        Pump2.syringe_diam(str(self.diam))
        Pump2.infuse_rate(str(self.rate), "ml/min")
        Pump2.withdraw_rate(str(self.rate), "ml/min")

        self.com_cur2 = self.gui.c2.get()

       # if not self.isInflating2:

        if Pump2.pump_withdrawing is False and Pump2.pump_infusing is False: #might need to have a fix here to at the beginning check if false or true
            print("both false")
            self.pos_cur2 = self.com_prev2
            val_to_set2 = self.com_cur2 - self.pos_cur2
            self.setVol2 = 0.01 * val_to_set2 * float(self.gui.maxvol_entry.get())
            Pump2.target_volume(str(abs(self.setVol2)), "ml")


        #else: # this needs to be if pump infusing
        elif Pump2.pump_infusing is True and Pump2.pump_withdrawing is False:
            print("infusing true")
            self.pos_cur2 = self.pos_prev2 + self.pump_step # this is only the infusing case
            val_to_set2 = self.com_cur2 - self.pos_cur2
            self.setVol2 = 0.01 * val_to_set2 * float(self.gui.maxvol_entry.get())
            Pump2.target_volume(str(abs(self.setVol2)), "ml")

           # if self.setVol2 == 0: # this needs to be a slightly diffent conditional
                #Pump2.pump_withdrawing = False
                #Pump2.pump_infusing = False


        elif Pump2.pump_withdrawing is True and Pump2.pump_infusing is False:
            print("withdrawing true")
            self.pos_cur2 = self.pos_prev2 - self.pump_step # this is only the infusing case
            val_to_set2 = self.com_cur2 - self.pos_cur2
            self.setVol2 = 0.01 * val_to_set2 * float(self.gui.maxvol_entry.get())
            Pump2.target_volume(str(abs(self.setVol2)), "ml")

           # if self.setVol2 == 0:
             #   Pump2.pump_withdrawing = False
             #   Pump2.pump_infusing = False

        if self.setVol2 < 0:
            Pump2.withdraw_pump()
        elif self.setVol2 > 0:
            Pump2.infuse_pump()
        else:
            Pump2.stop_pump()

        self.com_prev2 = self.com_cur2
        self.pos_prev2 = self.pos_cur2


       #also still confused exactly why this logic works
        if self.setVol2 <= self.pump_step:
            self.isInflating2 = False

        else:
            self.isInflating2 = True

    def actuate3(self):

        #while isRunning is True:
            #time.sleep(self.t_step)

       # print("inflating 3 at start ")
       # print(self.isInflating3)

        #######################################
        #need to add this to all pumps
        Pump3.c_volume()
        Pump3.ci_volume()
        Pump3.cw_volume()
        Pump3.syringe_vol(str(self.vol))
        Pump3.syringe_diam(str(self.diam))
        Pump3.infuse_rate(str(self.rate), "ml/min")
        Pump3.withdraw_rate(str(self.rate), "ml/min")

        ###################################

        self.com_cur3 = self.gui.c3.get()

        if not self.isInflating3:
            self.pos_cur3 = self.com_prev3
            val_to_set3 = self.com_cur3 - self.pos_cur3
            self.setVol3 = 0.01 * val_to_set3 * float(self.gui.maxvol_entry.get())
            Pump3.target_volume(str(abs(self.setVol3)), "ml")

        else:
            self.pos_cur3 = self.pos_prev3 + self.pump_step
            val_to_set3 = self.com_cur3 - self.pos_cur3
            self.setVol3 = 0.01 * val_to_set3 * float(self.gui.maxvol_entry.get())
            Pump3.target_volume(str(abs(self.setVol3)), "ml")

        if self.setVol3 < 0:
            Pump3.withdraw_pump()
        elif self.setVol3 > 0:
            Pump3.infuse_pump()
        else:
            Pump3.stop_pump()

        self.com_prev3 = self.com_cur3
        self.pos_prev3 = self.pos_cur3

        if self.setVol3 <= self.pump_step:
            self.isInflating3 = False
        else:
            self.isInflating3 = True

    def setAttributes(self):

        self.rate = float(self.gui.rate_entry.get())
        self.vol = float(self.gui.vol_entry.get())
        self.diam = float(self.gui.diam_entry.get())
        self.pump_step = self.rate * self.t_step * (1 / 60)

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

    # stops all pumps
    def stop_button(self):
        Pump1.stop_pump()
        Pump2.stop_pump()
        Pump3.stop_pump()