from math import acos, sin, degrees, degrees, isclose
from scipy import stats
from qiskit.quantum_info import entanglement_of_formation
import numpy as np

class StatAnalyser:

    """
    Uses 2-sample t-test to evaluate whether the distributions are statistically similar
    The null hypothesis is that the two states are equal

    INPUTS:
        - p_value: a desired p-value
        - data: a list (1 elem per test) of lists of 2 lists (1 per qubit)
            of probabilities (the probabilities of measuring a qubit in the
            state |0> over a trial)

    OUTPUTS:
        - list of bools
    """
    def testAssertEqual(self,
                        p_value,
                        data):
        results = []
        for testIndex in range(len(data)):
            if np.array_equal(data[testIndex][0], data[testIndex][1]):
                results.append(True)
                continue

            t, stat_p = stats.ttest_ind(data[testIndex][0], data[testIndex][1])
            results.append(p_value <= stat_p)

        return results


    """
    Uses the entanglement of formation

    INPUTS:
        - p_value
        - list of list of statevectors

    OUTPUT:
        - list of bools
    """
    def testAssertEntangled(self,
                            p_value,
                            data):
        results = []
        for testIndex in range(len(data)):
            totalEntanglement = 0
            for trialResult in data[testIndex]:
                totalEntanglement += entanglement_of_formation(np.sqrt(trialResult))
            totalEntanglement /= len(data[testIndex])
            results.append(totalEntanglement >= 1 - p_value)

        return results


    """
    Using one-sample t-test
    The Null hypothesis is that the sample was taken with the same probability as the argument

    INPUTS:
        - p_value
        - expectedProbas: list of expected probabilities for each test
        - data: list of lists of floats (probabilities for each trial)


    OUTPUT:
        - list of bools
    """
    def testAssertProbability(self,
                              p_value,
                              expectedProbas,
                              data):

        results = []

        for testIndex in range(len(data)):
            if np.all(data[testIndex] == data[testIndex][0]):
                results.append(isclose(data[testIndex][0], expectedProbas[testIndex], abs_tol=0.01))
                continue

            t, stat_p = stats.ttest_1samp(data[testIndex], expectedProbas[testIndex])

            results.append(p_value <= stat_p)

        return results




    """
    INPUTS:
        - data: list of dictionaries that give the counts of the measurements
        - outcome: string or list of strings that show which outcomes are expected

    OUTPUT:
        - list of bools
    """
    def testAssertMostCommon(self,
                             data,
                             outcome):

        results = []

        if isinstance(outcome, str):
            nbExpected = 1
        else:
            nbExpected = len(outcome)

        for index, testResult in enumerate(data):
            outcome_set = set(outcome)
            mostCommon_set = {x[0] for x in testResult[::-1][:nbExpected]}
            results.append(mostCommon_set == outcome_set)

        return results
