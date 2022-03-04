# Import TKinter module to build the GUI
import tkinter as tk
from tkinter import *

from Jacob_Backend import Backend

main = tk.Tk()

# these global variables are needed so that I can continously check them, becuase they are not attributes of the GUI I must have
# them be global, otherwise they would be local variables and I would be unable to compare them across iterations
global val1, val2, val3
global ol_val1, ol_val2, ol_val3

val1 = 0
val2 = 0
val3 = 0

class GUI:
    # this function is responsible for detecting if a change has been made on the sliders every .5 seconds and tells the pump to actuate
    #if the volumes have been changed, else nothing
    def update_after(self):
        global val1, val2, val3
        global ol_val1, ol_val2, ol_val3

        ol_val1 = val1
        ol_val2 = val2
        ol_val3 = val3

        val1 = self.c1.get()
        val2 = self.c2.get()
        val3 = self.c3.get()

        #check if cural and old_val are different if they r actuate that pump
        self.check_different()

        main.after(500, self.update_after) #this function is in here because I need access to main(that why its not in backend)
        #every .5 sec it recursively calls itself and checks the values if they r diff pumps get moved

    # check if curval and old_val are different if they r, actuate that pump
    # this is really the driver of the program,
    # if the slider values are different it will run that task for the apprppritate task
    def check_different(self):
        if val1 != ol_val1:
            self.backend.pump_1_thread_task()
        if val2 != ol_val2:
            self.backend.pump_2_thread_task()
        if val3 != ol_val3:
            self.backend.pump_3_thread_task()
        #print(val1, val2, val3)


    def __init__(self):
        # Import the Backend code to communicate with the pumps
        self.backend = Backend(self)

        # Initialize sliders at 0
        self.c1 = 0
        self.c2 = 0
        self.c3 = 0

        # Initialize syringe pump parameters at 0
        self.diam = 0
        self.vol = 0
        self.rate = 0
        self.max = 0

        # Title
        self.title = Label(main, text = "Syringe Control Panel")
        self.title.grid(row = 1, column = 2)

        # Chamber 1 controls
        # ------------------#
        self.up1 = Button(main, text = "\u2B99", command = lambda: self.c1.set(self.c1.get()+1))
        self.up1.grid(row = 2, column = 1)

        self.c1 = Scale(main, from_ = 100, to = 0, length = 300, showvalue = 0, command = lambda x: self.c1_label.configure(text = "Chamber 1:" + " " + x + "%"))

        self.c1.grid(row = 3, column = 1)
        
        self.down1 = Button(main, text = "\u2B9B", command = lambda: self.c1.set(self.c1.get()-1))
        self.down1.grid(row = 4, column = 1)
        
        self.c1_label = Label(main, text = "Chamber 1:" + " " + str(self.c1.get()) + "%")
        self.c1_label.grid(row = 5, column = 1)
        # ------------------#

        # Chamber 2 controls
        # ------------------#
        self.up2 = Button(main, text = "\u2B99", command = lambda: self.c2.set(self.c2.get()+1))
        self.up2.grid(row = 2, column = 2)

        self.c2 = Scale(main, from_ = 100, to = 0, length = 300, showvalue = 0, command = lambda x: self.c2_label.configure(text = "Chamber 2:" + " " + x + "%"))
        self.c2.grid(row = 3, column = 2)
        
        self.down2 = Button(main, text = "\u2B9B", command = lambda: self.c2.set(self.c2.get()-1))
        self.down2.grid(row = 4, column = 2)
        
        self.c2_label = Label(main, text = "Chamber 2:" + " " + str(self.c2.get()) + "%")
        self.c2_label.grid(row = 5, column = 2)
        # ------------------#
        
        
        # Chamber 3 controls
        # ------------------#
        self.up3 = Button(main, text = "\u2B99", command = lambda: self.c3.set(self.c3.get()+1))
        self.up3.grid(row = 2, column = 3)

        #self.c3 = Scale(main, from_=100, to=0, length=300, showvalue=0,command=self.backend.cmd_3())
        self.c3 = Scale(main, from_ = 100, to = 0, length = 300, showvalue = 0, command = lambda x: self.c3_label.configure(text = "Chamber 3:" + " " + x + "%"))
        self.c3.grid(row = 3, column = 3)
        
        self.down3 = Button(main, text = "\u2B9B", command = lambda: self.c3.set(self.c3.get()-1))
        self.down3.grid(row = 4, column = 3)
        
        self.c3_label = Label(main, text = "Chamber 3:" + " " + str(self.c3.get()) + "%")
        self.c3_label.grid(row = 5, column = 3)
        # ------------------#

        #im going to add a textbox instead of the slider becuase the slider is causing some issues because of the update freq

        #self.c3_text = Button(main, height = 1, width = 5, text = "enter desired % of volume", command = lambda: self.c3_text.set(self.c3_text.get()))
       # self.c3_text.grid(row = 5, column = 3)

        # Go button controls
        self.go_button = Button(main, text = "Play", command = lambda: self.backend.buttonPush())
        self.go_button.grid(row = 6, column = 2)

        # Syringe settings text boxes
        # ------------------#
        self.diam_label = Label(main, text = "Syringe Diameter:    ")
        self.diam_label.grid(row = 1, column = 4)

        self.diam_entry = Entry(main, width = 5)
        self.diam_entry.grid(row = 2, column = 4, sticky = W)

        self.diamunit = Label(main, text = "[mm]")
        self.diamunit.grid(row = 2, column = 4)

        #---#
        
        self.vol_label = Label(main, text = "Syringe Volume:    ")
        self.vol_label.grid(row = 1, column = 5)
        
        self.vol_entry = Entry(main, width = 5)
        self.vol_entry.grid(row = 2, column = 5, sticky = W)

        self.volunit = Label(main, text = "[mL]")
        self.volunit.grid(row = 2, column = 5)

        #---#

        self.rate_label = Label(main, text = "Syringe Rate:           ")
        self.rate_label.grid(row = 1, column = 6)

        self.rate_entry = Entry(main, width = 5)
        self.rate_entry.grid(row = 2, column = 6, sticky = W)

        self.rateunit = Label(main, text = "[mL/min]")
        self.rateunit.grid(row = 2, column = 6)
        
        #---#

        self.maxvol_label = Label(main, text = "Max Volume:        ")
        self.maxvol_label.grid(row = 1, column = 7)

        self.maxvol_entry = Entry(main, width = 5)
        self.maxvol_entry.grid(row = 2, column = 7, sticky = W)

        self.maxvolunit = Label(main, text = "[mL]")
        self.maxvolunit.grid(row = 2, column = 7)

        #Check Button Controls#

        self.check_button = Button(main, text="Check Pumps", command=lambda: self.backend.check_button())
        self.check_button.grid(row=6, column=4)

        self.display_vol_button = Button(main, text="Display Volume", command=lambda: self.backend.display_vol_button())
        self.display_vol_button.grid(row=6, column=6)

        # Stop Button Controls#
        self.stop_button = Button(main, text="Stop Pumps", command=lambda: self.backend.stop_button())
        self.stop_button.grid(row=6, column=8)


if __name__ == "__main__":
    GUI()
    main.mainloop()
