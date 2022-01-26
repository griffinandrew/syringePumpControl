import time
from multiprocessing import Pool


def actuate_pump(arg):
    pump_ref, delt_vol = arg[0], arg[1]
    my_pump = ["Pump1", "Pump2", 'Pump3'][pump_ref]
    print(my_pump)
    # time.sleep(5)
    if delt_vol < 0:
        print("withdraw pump")
    elif delt_vol > 0:
        print("infuse pump")
    else:
        print("stop pump")


if __name__ == "__main__":
    pool = Pool()
    start = time.time()
    args = [(0, 0.5), (1, -0.1), (2, 0)]
    pool.map(actuate_pump, args)
    end = time.time()
    print(end-start)
