from qiskit.circuit.quantumcircuit import QuantumCircuit
from .TestProperties import TestProperty
import random
from math import cos, sin, radians, degrees
import cmath
import numpy as np

class TestCaseGenerator:


    """
    This method generates one concrete test case and provides the exact parameters
        used to initialise the qubits

    Inputs: a TestProperty

    Output: a tuple containing the initialised test (a QantumCircuit),
        and two dictionaries, that store the theta (first one) and phi (second one)
        of each qubit in degrees

    """
    def generateTest(self, testProperties: TestProperty):

        qargs = testProperties.preconditions_q

        #Adds 2 classical bits to read the results of any assertion
        #Those bits will not interfere with the normal functioning of the program
        if testProperties.minQubits == testProperties.maxQubits:
            nbQubits = testProperties.minQubits
        else:
            nbQubits = np.random.randint(testProperties.minQubits, testProperties.maxQubits)

        qc = QuantumCircuit(nbQubits, testProperties.nbClassicalBits + 2)

        theta_init = {}
        phi_init = {}

        for key, value in qargs.items():
            #ignores the keys that are outside of the range
            if key >= nbQubits:
                continue

            #converts from degrees to radian
            randomTheta_deg = random.randint(value.minTheta, value.maxTheta)
            randomPhi_deg = random.randint(value.minPhi, value.maxPhi)

            #stores the random values generated
            theta_init[key] = randomTheta_deg
            phi_init[key] = randomPhi_deg

            randomTheta = radians(randomTheta_deg)
            randomPhi = radians(randomPhi_deg)

            value0 = cos(randomTheta/2)
            value1 = cmath.exp(randomPhi * 1j) * sin(randomTheta / 2)

            qc.initialize([value0, value1], key)

        return (qc, theta_init, phi_init)



    """
    This method runs self.generateTest to generate the specified amount of tests in
        the TestProperty

    Inputs: a TestProperty

    Outputs: a list of what self.generateTests returns (a tuple containing a QuantumCircuit,
    a dictionary for the thetas used and a dictionary for the phi used in degrees)

    """
    def generateTests(self, testProperties: TestProperty):
        return [self.generateTest(testProperties) for _ in range(testProperties.nbTests)]

