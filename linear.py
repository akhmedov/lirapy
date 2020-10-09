from scipy.constants import mu_0 as mu0
from scipy.constants import epsilon_0 as eps0
from scipy.constants import speed_of_light as c
from scipy import special as func

import numpy as np
from scipy import integrate
import matplotlib
from matplotlib import pyplot as plot
matplotlib.rcParams['text.usetex'] = True


# CONSTANTS ###################################################################

A0 = 1
radius = 1
eps = 1
mu = 1
tau0 = radius
Z0 = np.sqrt(mu0 * mu / (eps0 * eps))
nsec = c / np.sqrt(mu * eps) * 1e-9
psec = c / np.sqrt(mu * eps) * 1e-12


# TRANSIENT RESPONSE ##########################################################


def i1(rho, vt, z):

    casual2 = vt ** 2 - z ** 2  # disk edge to observer time projected to z axis
    close2 = (rho - radius) ** 2  # closest disk edge to observer time projected to rho axis
    far2 = (rho + radius) ** 2  # the farthest disk edge to observer time projected to rho axis

    if 0 <= casual2 <= close2 and rho <= radius:  # electromagnetic missile zone
        return 0.5
    elif close2 < casual2 < far2:
        top = np.sqrt(close2 * (far2 - casual2))
        bot = np.sqrt(far2 * (casual2 - close2))
        atan = np.abs(rho**2 - radius**2) * np.arctan(top/bot)
        sqrt = np.sqrt(4 * rho**2 * radius**2 - (rho**2 + radius**2 - casual2)**2)
        acos = (rho ** 2 + radius ** 2) * np.arccos((casual2 - rho ** 2 - radius ** 2) / (2 * rho * radius))
        return (acos - sqrt - 2 * atan) / (4 * np.pi * rho**2)
    else:
        return 0


def i2(rho, vt, z):

    casual2 = vt ** 2 - z ** 2
    close2 = (rho - radius) ** 2
    far2 = (rho + radius) ** 2

    if 0 <= casual2 <= close2 and rho <= radius:
        return 1
    elif close2 < casual2 < far2:
        top = casual2 + rho**2 - radius**2
        bot = 2 * rho * np.sqrt(casual2)
        return np.arccos(top/bot) / np.pi
    else:
        return 0


def i5(rho, vt, z, numeric_terms):

    casual2 = vt ** 2 - z ** 2
    close2 = (rho - radius) ** 2
    far2 = (rho + radius) ** 2

    if close2 < casual2 < far2:

        triangle = np.sqrt(casual2 - close2) * np.sqrt(far2 - casual2)
        rect = rho * (vt + z)
        zero_term = triangle / rect / np.pi

        nu = np.arange(0, 2000, 0.0001)
        i5_sum = np.zeros((nu.shape[0]), dtype=np.float)

        for m in range(1, numeric_terms+1):
            i5m = func.j1(nu * radius) * func.j1(nu * rho) * func.jn(2*m+1, nu * np.sqrt(casual2))
            i5_sum += 2 * radius * i5m * np.sqrt((vt-z)/(vt+z))**(2*m+1)

        return zero_term + (integrate.simps(i5_sum, nu) if numeric_terms != 0 else 0)

    return 0


def electric_x(vt, rho, phi, z):
    return A0 * Z0 * (i1(rho, vt, z) * np.cos(phi)**2 + (i2(rho, vt, z) - i1(rho, vt, z)) * np.sin(phi)**2) / 2


def electric_y(vt, rho, phi, z):
    return A0 * Z0 * (i1(rho, vt, z) - i2(rho, vt, z)/2) * np.sin(phi) * np.cos(phi)


def electric_z(vt, rho, phi, z):
    return 0


def magnetic_x(vt, rho, phi, z):
    return 0


def magnetic_y(vt, rho, phi, z):
    return 0


def magnetic_z(vt, rho, phi, z, numeric_terms=0):
    return - i5(rho, vt, z, numeric_terms) * np.sin(phi)


def observed_from(rho, z):
    return z if rho < radius else np.sqrt((rho - radius)**2 + z**2)


def wave_from(rho, z):
    return np.sqrt((rho - radius) ** 2 + z ** 2) + rho - rho / radius


def observed_to(rho, z):
    return np.sqrt((rho + radius)**2 + z**2)


# SUPERPOSITION PRINCIPAL #####################################################


def sinc(time, duration=tau0, periods=10):
    arg = periods * np.pi * (2*time - duration) / duration
    return np.sinc(arg) if 0 < time < duration else 0


def duhamel(vt, rho, phi, z, tr, shape):
    time = np.arange(0, vt, 1e-3)
    shape = np.gradient([shape(tau) for tau in time], time)
    convolution = [sh * tr(vt - tau, rho, phi, z) for tau, sh in zip(time, shape)]
    return integrate.simps(convolution, time)


# PLOTS #######################################################################


def ex_vs_hz(rho=radius/2, phi=-np.pi/2, z=radius):

    time = np.arange(9/10 * observed_from(rho, z), 10/9 * observed_to(rho, z), 1e-3)
    ex = [electric_x(vt, rho, phi, z) for vt in time]
    hz = [magnetic_z(vt, rho, phi, z, 0) for vt in time]

    plot.xlabel(r'$ct, R$')
    plot.plot(time, ex, label=r'$ E_x(t), V/R $', color='black', linestyle='-.')
    plot.plot(time, hz, label=r'$ H_z(t), A/R $', color='black', linestyle='-')
    plot.axvline(wave_from(rho, z), label=r'$ c t_{emm}, R $', color='gray', linestyle='--')
    plot.grid(color='lightgrey', linestyle=':', linewidth=1)
    plot.yscale('symlog')
    plot.legend()
    plot.show()


def hz_numerical(rho=radius/2, phi=-np.pi/2, z=radius):

    time = np.arange(9/10 * observed_from(rho, z), 10/9 * observed_to(rho, z), 1e-2)
    hz0 = [magnetic_z(vt, rho, phi, z, 0) for vt in time]
    hz1 = [magnetic_z(vt, rho, phi, z, 1) for vt in time]
    hz2 = [magnetic_z(vt, rho, phi, z, 2) for vt in time]
    hz3 = [magnetic_z(vt, rho, phi, z, 3) for vt in time]

    plot.xlabel(r'$ ct, R $')
    plot.ylabel(r'$ H_z(ct), A/m $')
    plot.plot(time, hz0, label=r'$ N = 0 $', color='black', linestyle='-.')
    plot.plot(time, hz1, label=r'$ N = 1 $', color='black', linestyle='--')
    plot.plot(time, hz2, label=r'$ N = 2 $', color='black', linestyle=':')
    plot.plot(time, hz3, label=r'$ N = 3 $', color='black', linestyle='-')
    plot.grid(color='lightgrey', linestyle=':', linewidth=1)
    plot.legend()
    plot.show()


def sinc_furier_zone(rho=0, phi=0, z1=9.75, z2=15):
    # t1 = np.arange(observed_from(rho, z1), tau0 + observed_to(rho, z1), 1e-3)
    # ex1 = [duhamel(vt, rho, phi, z1, electric_x, shape=sinc) for vt in t1]
    #
    # plot.xlabel(r'$ ct, R $')
    # plot.ylabel(r'$ E_x(t,z = 9.75R), V/m $')
    # plot.plot(t1, ex1, color='black', linestyle='-')
    # plot.grid(color='lightgrey', linestyle=':', linewidth=1)
    # plot.show()
    t2 = np.arange(observed_from(rho, z2), tau0 + observed_to(rho, z2), 1e-3)
    ex2 = [duhamel(vt, rho, phi, z2, electric_x, shape=sinc) for vt in t2]

    plot.xlabel(r'$ ct, R $')
    plot.ylabel(r'$ E_x(t,z = 15R), V/m $')
    plot.plot(t2, ex2, color='black', linestyle='-')
    plot.grid(color='lightgrey', linestyle=':', linewidth=1)
    plot.show()


def example(rho=2*radius, phi=3*np.pi/4, z=2*radius):
    time = np.arange(5/10 * observed_from(rho, z), 10/5 * observed_to(rho, z), 1e-3)
    ex = [electric_x(vt, rho, phi, z) for vt in time]
    plot.xlabel(r'$ct, R$')
    plot.plot(time, ex, label=r'$ E_x(t), V/R $', color='black', linestyle='-')
    plot.grid(color='lightgrey', linestyle=':', linewidth=1)
    plot.legend()
    plot.show()


if __name__ == '__main__':
    example()
