from qiskit import Aer, IBMQ, transpile
from qiskit.providers.ibmq import least_busy
import numpy as np



"""
INPUTS: a string that specifies the backend to select, and a QuantumCircuit,
    used for checking requirements for IBMQ

OUTPUTS: a backend to run QuantumCircuits with

"""
def select_backend(backend, qc):
    if backend.lower() == "ibmq":
        if IBMQ.active_account() == None:
            IBMQ.load_account()
        provider = IBMQ.get_provider(hub="ibm-q")
        available_backends = provider.backends(filters=lambda x: x.configuration().n_qubits >= len(qc.qubits) and \
            not x.configuration().simulator and x.status().operational==True)

        if len(available_backends) == 0:
            raise Exception("No suitable quantum backend found")

        return least_busy(available_backends)
    else:
        return Aer.get_backend(backend)


def measureX(qc, qu0, measuredBit):
    qc.h(qu0)
    qc.measure(qu0, measuredBit)
    return qc

def measureY(qc, qu0, measuredBit):
    qc.sdg(qu0)
    qc.h(qu0)
    qc.measure(qu0, measuredBit)
    return qc


class TestExecutor:
    """
    INPUTS:
        - QuantumCircuit to run the tests
        - number of times the the qc will be run
        - number of times the qc will be measured after each run
        - the first qubit to compare
        - the second qubit to comapre
        - the bit where the first qubit will be measured in
        - the bit where the second qubit will be measured in
        - the basis of the measurement
        - the backend used to run the tests


    OUTPUT: the data of the execution of the tests, meaning
        a tuple of two numpy arrays, one for each qubit.
        Each numpy array contains a list of probabilities (float between 0 and 1)
        that the qubit was measured in state |0> during one trial
        Each trial is measured as many times as nbMeasurements specifies

    """
    def runTestAssertEqual(self,
                           qc,
                           nbTrials,
                           nbMeasurements,
                           qu0,
                           qu1,
                           measuredBit0,
                           measuredBit1,
                           basis,
                           backend):

        sim = select_backend(backend, qc)


        if basis.lower() == "x":
            measureX(qc, qu0, measuredBit0)
            measureX(qc, qu1, measuredBit1)
        elif basis.lower() == "y":
            measureY(qc, qu0, measuredBit0)
            measureY(qc, qu1, measuredBit1)
        else:
            qc.measure(qu0, measuredBit0)
            qc.measure(qu1, measuredBit1)


        qc_trans = transpile(qc, backend=sim)


        trialProbas0 = np.empty(nbTrials)
        trialProbas1 = np.empty(nbTrials)

        for trialIndex in range(nbTrials):
            result = sim.run(qc_trans, shots=nbMeasurements).result()
            counts = result.get_counts()

            nb0s_qu0 = nb0s_qu1 = 0
            for elem in counts:
                if elem[::-1][measuredBit0] == '0': nb0s_qu0 += counts[elem]
                if elem[::-1][measuredBit1] == '0': nb0s_qu1 += counts[elem]


            trialProbas0[trialIndex] = nb0s_qu0 / nbMeasurements
            trialProbas1[trialIndex] = nb0s_qu1 / nbMeasurements

        return (trialProbas0, trialProbas1)



    """
    Inputs: same as runTestAssertEqual except the first one, which is a
        list of QuantumCircuit instead of just one

    Outputs: a list of the results of runTestsAssertEqual for each test

    """
    def runTestsAssertEqual(self,
                            initialisedTests,
                            nbTrials,
                            nbMeasurements,
                            qu0,
                            qu1,
                            measuredBit0,
                            measuredBit1,
                            basis,
                            backend):
        return [self.runTestAssertEqual(qc, nbTrials, nbMeasurements, qu0, qu1, measuredBit0, measuredBit1, basis, backend)
                    for qc in initialisedTests]





    #Return for each test the recreated "statevector" of 2 bits
    def runTestAssertEntangled(self,
                               qc,
                               nbTrials,
                               nbMeasurements,
                               qu0,
                               qu1,
                               measuredBit0,
                               measuredBit1,
                               basis,
                               backend):


        sim = select_backend(backend, qc)


        if basis.lower() == "x":
            measureX(qc, qu0, measuredBit0)
            measureX(qc, qu1, measuredBit1)
        elif basis.lower() == "y":
            measureY(qc, qu0, measuredBit0)
            measureY(qc, qu1, measuredBit1)
        else:
            qc.measure(qu0, measuredBit0)
            qc.measure(qu1, measuredBit1)


        qc_trans = transpile(qc, backend=sim)


        trialVectors = np.zeros((nbTrials, 4))

        for trialIndex in range(nbTrials):
            result = sim.run(qc_trans, shots=nbMeasurements).result()
            counts = result.get_counts()

            for key, value in counts.items():
                #Has to be reversed before
                if key[0:2] == "00":
                    trialVectors[trialIndex][0] = value / nbMeasurements
                #Measures for state |01>
                elif key[0:2] == "10":
                    trialVectors[trialIndex][1] = value / nbMeasurements
                #Measures for state |10> (no typo, the order is just reversed in get_counts)
                elif key[0:2] == "01":
                    trialVectors[trialIndex][2] = value / nbMeasurements
                elif key[0:2] == "11":
                    trialVectors[trialIndex][3] = value / nbMeasurements

        return trialVectors



    def runTestsAssertEntangled(self,
                                initialisedTests,
                                nbTrials,
                                nbMeasurements,
                                qu0,
                                qu1,
                                measuredBit0,
                                measuredBit1,
                                basis,
                                backend):
        return [self.runTestAssertEntangled(qc, nbTrials, nbMeasurements, qu0, qu1, measuredBit0, measuredBit1, basis, backend)
                    for qc in initialisedTests]





    def runTestAssertProbability(self,
                                 qc,
                                 nbTrials,
                                 nbMeasurements,
                                 qu0,
                                 measuredBit,
                                 basis,
                                 backend):

        sim = select_backend(backend, qc)


        if basis.lower() == "x":
            measureX(qc, qu0, measuredBit)
        elif basis.lower() == "y":
            measureY(qc, qu0, measuredBit)
        else:
            qc.measure(qu0, measuredBit)


        qc_trans = transpile(qc, backend=sim)


        trialProbas = np.empty(nbTrials)

        for trialIndex in range(nbTrials):
            result = sim.run(qc_trans, shots = nbMeasurements).result()
            counts = result.get_counts()

            nb0s = 0
            for elem in counts:
                #Bit oredering is in the reverse order for get_count
                #(if we measure the last bit, it will get its value in index 0 of the string for some reason)
                if elem[::-1][measuredBit] == '0': nb0s += counts[elem]


            trialProba = nb0s / nbMeasurements

            trialProbas[trialIndex] = trialProba

        return trialProbas


    #Returns a tuple of tuple of bool
    #Data to collect is a tuple (one for each trial) of tuples (one for each trial) of bools (one for each measruement)
    def runTestsAssertProbability(self,
                                  initialisedTests,
                                  nbTrials,
                                  nbMeasurements,
                                  qu0,
                                  measuredBit,
                                  basis,
                                  backend):
        return [self.runTestAssertProbability(qc, nbTrials, nbMeasurements, qu0, measuredBit, basis, backend)
                    for qc in initialisedTests]






    def runTestsAssertState(self,
                            initialisedTests,
                            nbTrials,
                            nbMeasurements,
                            qu0,
                            measuredBit,
                            backend):
        tests_Y = [qc.copy() for qc in initialisedTests]
        tests_X = [qc.copy() for qc in initialisedTests]

        return (self.runTestsAssertProbability(initialisedTests, nbTrials, nbMeasurements, qu0, measuredBit, "z", backend),
                self.runTestsAssertProbability(tests_Y, nbTrials, nbMeasurements, qu0, measuredBit, "y", backend),
                self.runTestsAssertProbability(tests_X, nbTrials, nbMeasurements, qu0, measuredBit, "x", backend))

