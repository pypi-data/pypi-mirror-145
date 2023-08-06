from math import acos, sin, degrees, degrees, isclose
from scipy import stats
from qiskit.quantum_info import entanglement_of_formation
import numpy as np

class StatAnalyser:

    """
    Inputs: a desired p-value and a list of 1 element for each test, each element
        being a list of 2 elements, one for each measured qubit (so 2 qubits that are to be compared)
        and those elements contain probabilities (the probabilities of measuring a qubit in the
        state |0> over a trial)

    Returns a list of booleans, one for each generated test

    Uses 2-sample t-test to evaluate whether the distributions are statistically similar
    The null hypothesis is that the two states are equal
    """
    def testAssertEqual(self,
                        p_value,
                        data):
        testResults = []
        for testIndex in range(len(data)):
            if np.array_equal(data[testIndex][0], data[testIndex][1]):
                testResults.append(True)
                continue

            t, stat_p = stats.ttest_ind(data[testIndex][0], data[testIndex][1])
            testResults.append(p_value <= stat_p)

        return testResults


    def testAssertEntangled(self,
                            p_value,
                            data):
        #print(testResults)
        testResults = []
        for testIndex in range(len(data)):
            totalEntanglement = 0
            for trialResult in data[testIndex]:
                #print(np.sqrt(trialResult))
                totalEntanglement += entanglement_of_formation(np.sqrt(trialResult))
                #print(entanglement_of_formation(np.sqrt(trialResult)))
            totalEntanglement /= len(data[testIndex])
            #print(f"total entanglement: {totalEntanglement}")
            testResults.append(totalEntanglement >= 1 - p_value)

        return testResults


    """
    Using one-sample t-test
    The Null hypothesis is that the sample was taken with the same probability as the argument
    """
    def testAssertProbability(self,
                              p_value,
                              expectedProbas,
                              data):

        testResults = []

        for testIndex in range(len(data)):
            if np.all(data[testIndex] == data[testIndex][0]):
                testResults.append(isclose(data[testIndex][0], expectedProbas[testIndex], abs_tol=0.01))
                continue

            t, stat_p = stats.ttest_1samp(data[testIndex], expectedProbas[testIndex])

            testResults.append(p_value <= stat_p)

            #print(stat_p)

        return testResults



 #   def testAssertTransformed(self, thetaMin, thetaMax, phiMin, phiMax, testStatevectors):

 #       results = []
 #       for statevector in testStatevectors:

 #           realPart0 = float(statevector[0].real)

 #           thetaRad = acos(realPart0) * 2

 #           #print(f"thata degrees from statevector: {degrees(thetaRad)}")

 #           if sin(thetaRad / 2) == 0:
 #               raise Exception("Division by 0")

 #           phiRad1 = acos(float(statevector[1].real) / sin(thetaRad / 2))
 #           #phiRad2 = asin(float(testStatevector[1].imag) / sin(thetaRad / 2))

 #           #print(f"values from statevectors: {degrees(thetaRad)}, {degrees(phiRad1)}")

 #           results.append(degrees(thetaRad) >= thetaMin - 0.001 and degrees(thetaRad) <= thetaMax + 0.001 and \
 #                          degrees(phiRad1) >= phiMin - 0.001 and degrees(phiRad1) <= phiMax + 0.001)

 #       return results


    def testAssertState(self,
                        p_value,
                        data,
                        expectedData):
        #print(f"data: {data}\nexpectedData: {expectedData}")
        results = []

        for testIndex in range(len(data)):
            dataZ, dataY, dataX = data[testIndex]
            avgZ = np.average(dataZ[testIndex])
            avgY = np.average(dataY[testIndex])
            avgX = np.average(dataX[testIndex])
            print(f"avg Z: {avgZ}, avg Y: {avgY}, avg X: {avgX}")


        return results
