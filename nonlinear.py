from linear import i1, i2, observed_from, observed_to
from linear import A0, radius, eps, mu, Z0, nsec, psec

import numpy as np
from scipy import integrate


def i1derv(rho, vt, z):

    casual2 = vt**2 - z**2
    close2 = (rho - radius)**2
    far2 = (rho + radius)**2

    if close2 < casual2 < far2:
        one = close2**2 / casual2 * np.sqrt((far2 - casual2) * (casual2 - close2))
        two = (2 * (rho**2 + radius**2) - casual2) / np.sqrt(4 * rho**2 * radius**2 - (casual2 - rho**2 - radius**2)**2)
        return vt * (one + two) / (2 * np.pi * rho ** 2)
    else:
        return 0


def i2derv(rho, vt, z):

    casual2 = vt**2 - z**2
    close2 = (rho - radius)**2
    far2 = (rho + radius)**2

    if close2 < casual2 < far2:
        top = casual2 - rho**2 + radius**2
        bot = np.sqrt(4 * rho**2 * casual2 - (casual2 + rho**2 - radius**2)**2)
        return vt * top / bot / (np.pi * casual2)
    else:
        return 0
