from Jacob_Pump import Pump
import serial
import Jacob_Pump

import time

Pump1 = Pump("COM3","11 PICO PLUS ELITE 3.0.7")
Pump2 = Pump("COM4","11 PICO PLUS ELITE 3.0.7")
Pump3 = Pump("COM5","11 PICO PLUS ELITE 3.0.7")

#temp vars to store volumes that are being changed each time stored in string for print statements
vol1=""
vol2=""
vol3=""

iteration_1 = True
iteration_2 = True
iteration_3 = True


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

        self.deltVal3 = 0
        self.deltVol3 = 0


        #doing this because everything needs to be in terms of volume
        self.oldVol1 = 0
        self.oldVol2 = 0
        self.oldVol3 = 0

        self.curVol3 = 0

    def pump_1_thread_task(self):
        global iteration_1
        if iteration_1 is False:
            x = self.start_1()
        else:
            self.start_1()
            x = 0
            iteration_1 = False

        self.rate = float(self.gui.rate_entry.get())

        vol_infused_in_time = (self.rate * x) / 60

        self.oldVal1 = self.curVal1 - float(vol_infused_in_time)

        self.curVal1 = self.gui.c1.get()

        self.deltVal1 = self.curVal1 - self.oldVal1 #deltVol is used to determine if we are withdrawing or infusing

        self.deltVol1 = 0.01 * self.deltVal1 * float(self.gui.maxvol_entry.get()) #curVol determines the target volume as a percentage of max vol

        global vol1
        #vol1 = str(self.curVol1)

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
        Pump1.target_volume(str(abs(self.deltVol1)), "ml") # target vol based off of curVol

        if self.deltVal1 < 0: #deltVal is just being used to see if withdraw or infuse
            Pump1.withdraw_pump()
        elif self.deltVal1 > 0:
            Pump1.infuse_pump()
        else:
            Pump1.stop_pump()

    def pump_2_thread_task(self):
        global iteration_2
        if iteration_2 is False: # if it is not the first iteration
            x = self.start_2()
        else:
            self.start_2()
            x = 0
            iteration_2 = False

        self.rate = float(self.gui.rate_entry.get())

        vol_infused_in_time = (self.rate * x) / 60

        self.oldVal2 = self.curVal2 - float(vol_infused_in_time)

        self.curVal2 = self.gui.c2.get()

        self.deltVal2 = self.curVal2 - self.oldVal2 #deltVol is used to determine if we are withdrawing or infusing

        self.deltVol2 = 0.01 * self.deltVal2 * float(self.gui.maxvol_entry.get()) #curVol determines the target volume as a percentage of max vol
        global vol2
        #vol2 = str(self.curVol2)

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
        Pump2.target_volume(str(abs(self.deltVol2)), "ml") # target vol based off of curVol

        if self.deltVal2 < 0: #deltVal is just being used to see if withdraw or infuse
            Pump2.withdraw_pump()
        elif self.deltVal2 > 0:
            Pump2.infuse_pump()
        else:
            Pump2.stop_pump()

    def pump_3_thread_task(self):
        global iteration_3

        #this code was added in order to get around the first iteration of calling time and having a starting point
        #we know the infused volume at this point is 0, so I just set the start time and record the vol_infused_in_time as 0
        if iteration_3 is False:
            #x = self.start_3()
            Pump3.f_t3 = time.time()
            y = self.time_diff_3() # this will be based off of previous target volume

            print("y")
            print(y)
            Pump3.s_t3 = time.time()

        else:
            y = 0
            iteration_3 = False
            Pump3.s_t3 = time.time()

        self.rate = float(self.gui.rate_entry.get())

        vol_infused_in_time = (self.rate * y) / 60 # rate times time # units r in ml/min time is in seconds so needed to correct this

        print("volume in time")
        print(vol_infused_in_time)

        #this logic is meant to take the place of checking if pump infusing/withdrawing is true or not
        if self.deltVol3 == self.curVol3:
            print("check conditional")
            print(self.deltVol3)
            print(self.curVol3)
            Pump3.pump_withdrawing = False
            Pump3.pump_infusing = False


        if Pump3.pump_infusing is True or Pump3.pump_withdrawing is True:  # this will not actually show if it is currently in either of those states
            self.oldVol3 = vol_infused_in_time
        else: # the code is never entering this step even when both are false
            self.oldVol3 = self.curVol3
        print("cur vol before")
        print(self.curVol3)

        self.curVal3 = self.gui.c3.get()

        self.curVol3 = self.curVal3 * 0.01 * float(self.gui.maxvol_entry.get())

        print("cur vol after")
        print(self.curVol3)

        self.deltVol3 = self.curVol3 - self.oldVol3  #deltVol is used to determine if we are withdrawing or infusing volume should be set to

        #print('delt val')
       # print(self.deltVal3)

        #self.deltVol3 = 0.01 * self.deltVal3 * float(self.gui.maxvol_entry.get()) #- float(vol_infused_in_time)


        global vol3
        print('delt vol')
        vol3 = str(self.deltVol3)
        print(vol3)

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

        Pump3.target_volume(str(abs(self.deltVol3)), "ml") # target vol based off of curVol

        if self.deltVol3 < 0: #deltVol is just being used to see if withdraw or infuse
            Pump3.withdraw_pump()
            #Pump3.pump_withdrawing = False # this is close but then it will never retrieve the time diff one
        elif self.deltVol3 > 0:
            Pump3.infuse_pump()
            #Pump3.pump_infusing = False
        else:
            Pump3.stop_pump()

    #TypeError: can't pickle _tkinter.tkapp object, error from trying to do multiprocessing

    def buttonPush(self):
        self.gui.update_after()

    #checks all pumps when check pump button pressed
    def check_button(self):
        Pump1.check_pump("11 PICO PLUS ELITE 3.0.7")
        Pump2.check_pump("11 PICO PLUS ELITE 3.0.7")
        Pump3.check_pump("11 PICO PLUS ELITE 3.0.7")

# displays the pump volume
    def display_vol_button(self):
        global vol1, vol2, vol3
        print(vol1, vol2, vol3)
#stops all pumps
    def stop_button(self):
        Pump1.stop_pump()
        Pump2.stop_pump()
        Pump3.stop_pump()

#starts are resposible for reteiving the amount of time it took for each pump tp actuate
#NOTE ATM starts are not being used I am calling vol_diff
    def start_1(self):
        Pump1.set_start_time1()
        x = Pump1.total_infused_time1
        return x

    def start_2(self):
        Pump2.set_start_time2()
        x = Pump2.total_infused_time2
        return x

    def start_3(self):
        Pump3.set_start_time3()
        x = Pump3.total_infused_time3
        return x

# time_diffs retreives and returns the total infused time
    def time_diff_1(self):
        Pump1.time1_diff()
        x = Pump1.total_infused_time1
        return x

    def time_diff_2(self):
        Pump2.time2_diff()
        x = Pump2.total_infused_time2
        return x

    def time_diff_3(self):
        Pump3.time3_diff()
        x = Pump3.total_infused_time3
        return x