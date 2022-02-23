# Import modules for testing thread
import serial
import re

#the volume pumped in when the
#global syr_vol_real

#syr_vol_real = ''


# Create a class of functions called "Pump" to control the Harvard Apparatus Pump 11 Elite series pumps
class Pump:

    # Define the initializing function: set all values to zero or false
    def __init__(self, com, name):
        self.serial_pump = serial.Serial(com, 9600, timeout=2)
        self.svol = None
        self.sdiam = None
        self.infuse_statement = None
        self.withdraw_statement = None
        self.targetvolume_statement = None
        self.pump_infusing = False
        self.pump_withdrawing = False
        self.i_volume_statement = None
        self.s_volume_statement = None
        self.syr_vol_real = 0

    # Define a function to ensure the pump is properly connected and turn off nvram
    def check_pump(self, name):

        try:
            self.serial_pump.write(b'ver\r')
            tmp = self.serial_pump.read(1000)
            print(tmp)
            self.serial_pump.write(b'address\r')
            tmp2 = self.serial_pump.read(1000)
            print(tmp2)

            if name in tmp.decode():
                print(f"Pump {name} Connected Successfully\n")
            else:
                print(f"Problem connecting to pump {name}\n")
                
            print('Setting nvram (non-volatile RAM) to none\n')
            self.serial_pump.write(b'nvram none\r')

        except serial.serialutil.SerialException:
            print("Serial error. Check to make sure the Pump is plugged in and Serial port is not in use")

    # Define a function to set the syringe volume
    def syringe_vol(self, volume):
        self.svol = "svolume " + volume + " ml" + "\r"
        self.serial_pump.write(self.svol.encode())

    # Define a function to set the syringe diameter
    def syringe_diam(self, diameter):
        self.sdiam = "diameter " + diameter + " mm" + "\r"
        self.serial_pump.write(self.sdiam.encode())

    # Define a function to set the syringe infusion rate
    def infuse_rate(self, rate, unit):
        self.infuse_statement = "irate " + rate + " " + unit + "\r"
        self.serial_pump.write(self.infuse_statement.encode())

    # Define a function to set the syringe withdraw rate
    def withdraw_rate(self, rate, unit):
        self.withdraw_statement = "wrate " + rate + " " + unit + "\r"
        self.serial_pump.write(self.withdraw_statement.encode())

    # Define a function to set the syringe target volume
    def target_volume(self, target, unit):
        self.targetvolume_statement = "tvolume " + target + " " + unit + "\r"
        self.serial_pump.write(self.targetvolume_statement.encode())

    # Define a function that tells the pump to infuse
    def infuse_pump(self):
        #if not self.pump_infusing:
        self.serial_pump.write(b'irun\r')
        self.pump_infusing = True
        self.pump_withdrawing = False

    # Define a function that tells the pump to withdraw
    def withdraw_pump(self):
        #if not self.pump_withdrawing:
        self.serial_pump.write(b'wrun\r')
        self.pump_infusing = False
        self.pump_withdrawing = True

    # Define a function that tells the pump to stop
    def stop_pump(self):
        if self.pump_infusing or self.pump_withdrawing:
            self.serial_pump.write(b'stop\r')
            self.pump_infusing = False
            self.pump_withdrawing = False

    # Define a function that clears the infused volume value
    def ci_volume(self):
        self.civolume_statement = "civolume\r"
        self.serial_pump.write(self.civolume_statement.encode())

    # Define a function that clears the withdrawn volume value
    def cw_volume(self):
        self.cwvolume_statement = "cwvolume\r"
        self.serial_pump.write(self.cwvolume_statement.encode())

    # Define a function that clears the infused/withdrawn volume value
    def c_volume(self):
        self.cvolume_statement = "cvolume\r"
        self.serial_pump.write(self.cvolume_statement.encode())

    #function that sets or displays the syringe volume, its will always just be whatever u set it to at start up
    def s_volume(self):
        self.s_volume_statement = "svolume\r"
        self.serial_pump.write(self.s_volume_statement.encode())

    def i_volume(self):
        self.i_volume_statement = "ivolume\r"
        self.serial_pump.write(self.i_volume_statement.encode())

    def itime(self):
        self.itime_statement = "itime\r"
        self.serial_pump.write(self.itime_statement.encode())

    def syringe_volume(self):
        self.i_volume() #not sure if 100 is too small requires testing
        tmp = self.serial_pump.read(100) # if i play with the number of chars read this should improve performance

        #note that temp will appear in binary need to decode\
        x = ''
        #tmp.decode('ascii')
        tmp = str(tmp)

        #code to extract numbers and units from pumps
        for char in tmp:
            if char.isdigit():
                x = x + char
            if char is ".":
                x = x + char

        if re.search("ul", tmp):
            x = float(x) / 1000 #convert ul to ml

        elif re.search("nl", tmp):
            x = float(x) / 1000000 # convert nl to ml

        self.syr_vol_real = x