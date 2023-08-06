from math import degrees, pi
from .ExtraFunctions import cordsComplexToThetaPhi

class Qarg():
    #Look up for ways to make this cleaner
    def __init__(self,
                 arg0,
                 arg1 = None,
                 arg2 = None,
                 arg3 = None,
                 arg4 = None):
        if (isinstance(arg0, int) or isinstance(arg0, float)) \
            and (isinstance(arg1, int) or isinstance(arg1, float)) \
            and (isinstance(arg2, int) or isinstance(arg2, float)) \
            and (isinstance(arg3, int) or isinstance(arg3, float)) \
            and (arg4 == None or isinstance(arg4, bool)):

            if arg4 == None:
                arg4 = False

            self.init_theta_phi(arg0, arg1, arg2, arg3, arg4)

        elif (isinstance(arg0, list) or isinstance(arg0, tuple)) \
            and (isinstance(arg1, int) or isinstance(arg1, float) or arg1 == None) \
            and (isinstance(arg2, int) or isinstance(arg2, float) or arg2 == None) \
            and (isinstance(arg3, bool) or arg3 == None):
                if arg1 == None:
                    arg1 = 0
                if arg2 == None:
                    arg2 = 0
                if arg3 == None:
                    arg3 = False

                self.init_coords(arg0, arg1, arg2, arg3)
        elif (isinstance(arg0, str)):
            if arg0.lower() == "any":
                self.init_theta_phi(0, 360, 0, 360, False)
            elif arg0 == "+":
                self.init_theta_phi(90, 90, 0, 0, False)
            elif arg0 == "-":
                self.init_theta_phi(90, 90, 180, 180, False)
            elif arg0 == "1":
                self.init_theta_phi(180, 180, 0, 0, False)
            elif arg0 == "0":
                self.init_theta_phi(0, 0, 0, 0, False)
            else:
                raise Exception(f"Input for Qarg not recognised: {arg0}")
        else:
            raise Exception(f"Incorrect arguments for Qarg")

    def init_theta_phi(self,
                       minTheta,
                       maxTheta,
                       minPhi,
                       maxPhi,
                       radian):

        if not radian:
            #Error handling on Qarg values
            if minTheta < 0 or minTheta > 360:
                raise Exception(f"Invalid minTheta supplied, it has to be between 0 and 360 inclusive: {minTheta}")
            if maxTheta < 0 or maxTheta > 360:
                raise Exception(f"Invalid maxTheta supplied, it has to be between 0 and 360 inclusive: {maxTheta}")
            if minPhi < 0 or minPhi > 360:
                raise Exception(f"Invalid minPhi supplied, it has to be between 0 and 360 inclusive: {minPhi}")
            if maxPhi < 0 or maxPhi > 360:
                raise Exception(f"Invalid maxPhi supplied, it has to be between 0 and 360 inclusive: {maxPhi}")

            self.minTheta = minTheta
            self.maxTheta = maxTheta
            self.minPhi = minPhi
            self.maxPhi = maxPhi

        else:
            #Error handling is done through math.degrees()
            self.minTheta = degrees(minTheta)
            self.maxTheta = degrees(maxTheta)
            self.minPhi = degrees(minPhi)
            self.maxPhi = degrees(maxPhi)

    #Can initalise with 2 complex numbers and how much it can vary around
    def init_coords(self,
                    init_vect,
                    diff_theta,
                    diff_phi,
                    radian):

        (theta, phi) = cordsComplexToThetaPhi(init_vect)

        theta = round(degrees(theta))
        phi = round(degrees(phi))
        diff_theta = round(diff_theta)
        diff_phi = round(diff_phi)

        if not radian:
            self.minTheta = theta - diff_theta
            self.maxTheta = theta + diff_theta
            self.minPhi = phi - diff_phi
            self.maxPhi = phi + diff_phi
        else:
            self.minTheta = theta - degrees(diff_theta)
            self.maxTheta = theta + degrees(diff_theta)
            self.minPhi = phi - degrees(diff_phi)
            self.maxPhi = phi + degrees(diff_phi)




class TestProperty():
    def __init__(self,
                 p_value=0.01,
                 nbTests=10,
                 nbTrials=100,
                 nbMeasurements=500,
                 nbQubits=1,
                 nbClassicalBits=0,
                 qargs={},
                 backend="aer_simulator"):

        #Error handling on all values for the test property
        if p_value < 0 and p_value > 1:
            raise Exception(f"Invalid p_value supplied: {p_value}")
        elif nbTests < 1:
            raise Exception(f"Invalid amount of tests supplied: {nbTests}")
        elif nbTrials < 1:
            raise Exception(f"Invalid number of trials supplied: {nbTrials}")
        elif nbMeasurements < 1:
            raise Exception(f"Invalid number of measurements supplied: {nbMeasurements}")

        elif isinstance(nbQubits, int) and nbQubits < 1:
            raise Exception(f"Invalid number of qubits supplied: {nbQubits}")
        elif ((isinstance(nbQubits, tuple) or isinstance(nbQubits, list))) \
                and (nbQubits[0] < 1 or nbQubits[1] < nbQubits[0] or len(nbQubits) != 2):
            raise Exception(f"Invalid range of qubits supplied: {nbQubits}")

        elif nbClassicalBits < 0:
            raise Exception(f"Invalid number of classical bits supplied: {nbClassicalBits}")


        self.p_value = p_value
        self.nbTests = nbTests
        self.nbTrials = nbTrials
        self.nbMeasurements = nbMeasurements
        if isinstance(nbQubits, int):
            self.minQubits = nbQubits
            self.maxQubits = nbQubits
        elif isinstance(nbQubits, tuple) or isinstance(nbQubits, list):
            self.minQubits = nbQubits[0]
            self.maxQubits = nbQubits[1]
        self.nbClassicalBits = nbClassicalBits
        self.preconditions_q = qargs
        self.backend = backend
