from Jacob_Pump import Pump

import threading

from Jacob_Backend import Backend

Pump1 = Pump("COM3","11 PICO PLUS ELITE 3.0.7")
Pump2 = Pump("COM4","11 PICO PLUS ELITE 3.0.7")
Pump3 = Pump("COM5","11 PICO PLUS ELITE 3.0.7")


class Thread_Pump:
    def __init__(self):
        self.running = True;
        self.threads = []

    def pump_1_thread_task(self):
        self.oldVal1 = self.curVal1

        self.curVal1 = self.gui.c1.get()

        self.deltVal1 = self.curVal1 - self.oldVal1

        self.deltVol1 = 0.01 * self.deltVal1 * float(self.gui.maxvol_entry.get())

        print(str(self.deltVol1))

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
        Pump1.target_volume(str(abs(self.deltVol1)), "ml")

        if self.deltVol1 < 0:
            Pump1.withdraw_pump()
        elif self.deltVol1 > 0:
            Pump1.infuse_pump()
        else:
            Pump1.stop_pump()

    def pump_2_thread_task(self):
        self.oldVal2 = self.curVal2

        self.curVal2 = self.gui.c2.get()

        self.deltVal2 = self.curVal2 - self.oldVal2

        self.deltVol2 = 0.01 * self.deltVal2 * float(self.gui.maxvol_entry.get())

        print(str(self.deltVol2))

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
        Pump2.target_volume(str(abs(self.deltVol2)), "ml")

        if self.deltVol2 < 0:
            Pump2.withdraw_pump()
        elif self.deltVol2 > 0:
            Pump2.infuse_pump()
        else:
            Pump2.stop_pump()

    def pump_3_thread_task(self):
        self.oldVal3 = self.curVal3

        self.curVal3 = self.gui.c3.get()

        self.deltVal3 = self.curVal3 - self.oldVal3

        print(str(self.deltVol3))

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
        Pump3.target_volume(str(abs(self.deltVol3)), "ml")

        if self.deltVol3 < 0:
            Pump3.withdraw_pump()
        elif self.deltVol3 > 0:
            Pump3.infuse_pump()
        else:
            Pump3.stop_pump()

    def go(self):
        pump1_thread = threading.Thread(target=self.pump_1_thread_task)
        pump2_thread = threading.Thread(target=self.pump_2_thread_task)
        pump3_thread = threading.Thread(target=self.pump_3_thread_task)
        pump1_thread.daemon = True
        pump2_thread.daemon = True
        pump3_thread.daemon = True

        pump1_thread.start()
        pump2_thread.start()
        pump3_thread.start()
        self.threads.append(pump1_thread)
        self.threads.append(pump2_thread)
        self.threads.append(pump3_thread)

    def join_threads(threads):
        for t in threads:
            while t.isAlive():
                t.join(5)