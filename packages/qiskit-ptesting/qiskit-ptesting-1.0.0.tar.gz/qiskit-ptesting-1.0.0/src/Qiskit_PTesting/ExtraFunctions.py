from math import acos, sin, isclose, pi, cos, radians
from cmath import exp

"""
INPUTS:
    - coords: list[complex] of two numbers/ a statevector of one qubit

OUTPUTS:
    - tuple of the theta and phi associated with the statevector
"""
def cordsComplexToThetaPhi(coords):
    if not len(coords) == 2:
        raise Exception(f"Length of input is not 2: {coords}")

    magnitude = abs(coords[0]) ** 2 + abs(coords[1]) ** 2

    if not isclose(magnitude.real, 1):
        raise Exception(f"Magnitude of vector not 1. Make sure that the sum of both squares is 1. Magnitude: {magnitude}")


    if isclose(coords[0].real, 1):
        theta = 0
        phi = 0
    elif isclose(coords[0].real, 0):
        theta = pi
        phi = 0
    else:
        theta = acos(coords[0].real) * 2
        phi = acos((coords[1].real) / sin(theta / 2))

    return (theta, phi)

#theta and phi in radian
"""
INPUTS:
    - theta float/int
    - phi: float/int
    - radian: bool

OUTPUT:
    - list of 2 elements/ the statevector that is equivalent to the theta/phi
"""
def thetaPhiToStateVector(theta, phi, radian=True):
    if not radian:
        theta = radians(theta)
        phi = radians(phi)
    return [cos(theta / 2), exp(1j * phi) * sin(theta / 2)]
