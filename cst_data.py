import os, sys, csv
import numpy as np

OBSERVERS = 3
PORTS = 26

class Antenna:
    bigradius = 0.1684 # a
    smallradius = 0.127 # b
    focuslength = np.sqrt(bigradius**2 - smallradius**2) # c
    apperture = smallradius**2 / bigradius

def observer(observer_idx, a=Antenna.bigradius, c=Antenna.focuslength, R=Antenna.apperture):

    """
    TODO: documentation by Denis
    """

    observers = {
        1: dict(x=0, y=0, z= a + c + 1*R),
        2: dict(x=0, y=0, z= a + c + 2*R),
        3: dict(x=0, y=0, z= a + c + 3*R)
    }
    return type("", (), observers[observer_idx])()


def location(port_idx, b=Antenna.smallradius):

    """
    TODO: documentation by Denis
    """

    port_location_data = {
        1:  dict(x=b / 4, y=.1 * np.sin(np.pi / 20),       z=.1 * np.cos(np.pi / 20) + b),
        2:  dict(x=b / 8, y=.1 * np.sin(np.pi / 20),       z=.1 * np.cos(np.pi / 20) + b),
        3:  dict(x=b / 3, y=.1 * np.sin(np.pi / 20),       z=.1 * np.cos(np.pi / 20) + b),
        4:  dict(x=b / 3, y=.1 * np.sin(2 * np.pi / 20),   z=.1 * np.cos(2 * np.pi / 20) + b),
        5:  dict(x=b / 4, y=.1 * np.sin(2 * np.pi / 20),   z=.1 * np.cos(2 * np.pi / 20) + b),
        6:  dict(x=b / 8, y=.1 * np.sin(2 * np.pi / 20),   z=.1 * np.cos(2 * np.pi / 20) + b),
        7:  dict(x=b / 2, y=.1 * np.sin(2 * np.pi / 20),   z=.1 * np.cos(2 * np.pi / 20) + b),
        8:  dict(x=b / 2, y=.1 * np.sin(3 * np.pi / 20),   z=.1 * np.cos(3 * np.pi / 20) + b),
        9:  dict(x=b / 3, y=.1 * np.sin(3 * np.pi / 20),   z=.1 * np.cos(3 * np.pi / 20) + b),
        10: dict(x=b / 4, y=.1 * np.sin(3 * np.pi / 20),   z=.1 * np.cos(3 * np.pi / 20) + b),
        11: dict(x=b / 8, y=.1 * np.sin(3 * np.pi / 20),   z=.1 * np.cos(3 * np.pi / 20) + b),
        12: dict(x=b / 2, y=.1 * np.sin(np.pi / 20),       z=.1 * np.cos(np.pi / 20) + b),
        13: dict(x=b / 8, y=.1 * np.sin(4 * np.pi / 20),   z=.1 * np.cos(4 * np.pi / 20) + b), # prob data is not available
        14: dict(x=b / 4, y=.1 * np.sin(4 * np.pi / 20),   z=.1 * np.cos(4 * np.pi / 20) + b),
        15: dict(x=b / 8, y=.05 * np.sin(np.pi / 20),      z=.05 * np.cos(np.pi / 20) + b),
        16: dict(x=b / 3, y=.05 * np.sin(np.pi / 20),      z=.05 * np.cos(np.pi / 20) + b),
        17: dict(x=b / 2, y=.05 * np.sin(np.pi / 20),      z=.05 * np.cos(np.pi / 20) + b),
        18: dict(x=b / 8, y=.05 * np.sin(4 * np.pi / 20),  z=.05 * np.cos(4 * np.pi / 20) + b),
        19: dict(x=b / 3, y=.05 * np.sin(4 * np.pi / 20),  z=.05 * np.cos(4 * np.pi / 20) + b),
        20: dict(x=b / 2, y=.05 * np.sin(4 * np.pi / 20),  z=.05 * np.cos(4 * np.pi / 20) + b),
        21: dict(x=b / 8, y=.05 * np.sin(8 * np.pi / 20),  z=.05 * np.cos(8 * np.pi / 20) + b),
        22: dict(x=b / 4, y=.05 * np.sin(8 * np.pi / 20),  z=.05 * np.cos(8 * np.pi / 20) + b),
        23: dict(x=b / 8, y=.01 * np.sin(np.pi / 20),      z=.01 * np.cos(np.pi / 20) + b),
        24: dict(x=b / 3, y=.01 * np.sin(np.pi / 20),      z=.01 * np.cos(np.pi / 20) + b),
        25: dict(x=b / 8, y=.001 * np.sin(8 * np.pi / 20), z=.001 * np.cos(8 * np.pi / 20) + b),
        26: dict(x=b / 3, y=.001 * np.sin(8 * np.pi / 20), z=.001 * np.cos(8 * np.pi / 20) + b),
    }
    return type("", (), port_location_data[port_idx])()


def cst_data_exporter(file_path):

    """
    TODO: documentation by Denis
    """

    contents = open(file_path, 'r').readlines()
    for i in range(len(contents)):
        if len(contents[i]) > 5:
            if contents[i].split()[0].find('-----') != -1:
                contents = contents[i+1:]
                break
    time, func = [], []
    for line in contents:
        if len(line) > 1:
            time.append(float(line.split()[0]))
            func.append(float(line.split()[1]))
    return np.array(time), np.array(func)


def read_observer_data(observer_idx):

    """
    TODO: documentation by Denis
    """

    index, time, func = [], [], []
    parent_directory = 'observer' + str(observer_idx)
    obs = observer(observer_idx)

    for i in range(1,PORTS+1):

        if i == 13: continue
        file_name = 'ex_port' + str(i) + '.txt'
        file_path = os.path.join(parent_directory, file_name)

        if not os.path.exists(file_path):
            print('[EE]: File with path does not exit - ', file_path)
            sys.exit()

        data = cst_data_exporter(file_path)
        index.append(i)
        time.append(data[0])
        func.append(data[1])

    return index, time, func

