from math import acos, sin, isclose, pi

def cordsComplexToThetaPhi(coords):
    #coords is a tuple/list of 2 complex numbers
    if not len(coords) == 2:
        raise Exception(f"Length of input is not 2: {coords}")
    #if not isinstance(coords[0], complex) and not isinstance(coords[1], complex):
    #    raise Exception(f"Inputs are not 2 complex numbers: {coords}")

    magnitude = abs(coords[0]) ** 2 + abs(coords[1]) ** 2
    #print(f"values: {coords}")
    #print(f"coords[0]: {coords[0]}")
    #print(f"coords[1]: {coords[1]}")

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
        #print((coords[1].real) / sin(theta / 2))
        phi = acos((coords[1].real) / sin(theta / 2))

    return (theta, phi)
