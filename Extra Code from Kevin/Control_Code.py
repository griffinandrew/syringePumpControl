import pump
import serial
import Jacob_GUI
#import time

gui11 = Jacob_GUI.GUI()
p11 = pump.Pump()


p11.check_pump()
p11.syringe_type("50", "28.5")
p11.c_volume()
p11.infuse_rate("20", "ml/min")
p11.withdraw_rate("20", "ml/min")
p11.target_volume("1", "ml")
p11.infuse_pump()

gui11()
