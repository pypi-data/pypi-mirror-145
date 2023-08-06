from .TestProperties import TestProperty, Qarg
from .TestCaseGeneration import TestCaseGenerator
from .TestExecutionEngine import TestExecutor
from .StatisticalAnalysisEngine import StatAnalyser
from .ExtraFunctions import thetaPhiToStateVector
from qiskit import QuantumCircuit
from math import cos, radians



"""
Inputs:
    - list of quantum circuits
    - function to filter the quantum circuits (that takes as input a QuantumCircuit)

Outputs:
    - tuple of 2 values:
        0. a list storing the indexes of the tests that passed the filtering process
        1. another list storing the tests that passed the filtering
"""
def getFilteredInfo(inputTests, filter_qc):
    if filter_qc != None:
        filteredNumbered = list(filter(lambda x: filter_qc(x[1]), enumerate(inputTests)))
        filteredIndexes = [x[0] for x in filteredNumbered]
        filteredTests = [x[1] for x in filteredNumbered]
    else:
        filteredIndexes = range(len(inputTests))
        filteredTests = inputTests
    return (filteredIndexes, filteredTests)




class QiskitPropertyTest():
    """
    This method handles all the required data to evaluate the equality between two qubits

    INPUTS:
        - qu0: int = the index of the first qubit to compare
        - qu1: int = the index of the second qubit to compare
        - qu0_pre: boolean = whether the first qubit should be compared
            before running quantumFunction()
        - qu1_pre: boolean = whether the second qubit should be compared
            before running quantumFunction()
        - basis: str = the basis in which the measurements can take place
        - filter_qc: function[QuantumCircuit => bool] or None = function applied
            to a qc that filters out tests based on an input criterion

    OUTPUTS:
        - List of the results for each test:
            ~ A result is a tuple containg a boolean (the result of one test),
            the thetas and the phis used to initialise the first and the second qubits
    """
    def assertEqualData(self, qu0, qu1, qu0_pre, qu1_pre, basis, filter_qc):

        generatedTests = [qc.copy() for qc, theta, phi in self.initTests]

        filteredIndexes, filteredTests = getFilteredInfo(generatedTests, filter_qc)

        #executes the tests twice faster if they're on the same circuit, but only possible if both pre values are the same
        if qu0_pre == qu1_pre:
            #Applies the function to the generated tests only if they are both sampled after running the full program
            if not qu0_pre and not qu1_pre:
                for circuit in generatedTests:
                    self.quantumFunction(circuit)

            dataFromExec = TestExecutor().runTestsAssertEqual(filteredTests, self.testProperty.nbTrials, \
                self.testProperty.nbMeasurements, qu0, qu1, self.testProperty.nbClassicalBits, \
                self.testProperty.nbClassicalBits + 1, basis, self.testProperty.backend)

            testResults = StatAnalyser().testAssertEqual(self.testProperty.p_value, dataFromExec)

            #gets the theta/phi each qubit was initialised with
            qu0Params = [(self.initTests[index][1].get(qu0, 0),
                self.initTests[index][2].get(qu0, 0)) for index in filteredIndexes]
            qu1Params = [(self.initTests[index][1].get(qu1, 0),
                self.initTests[index][2].get(qu1, 0)) for index in filteredIndexes]
            params = tuple(zip(qu0Params, qu1Params))

            testResultsWithInit = tuple(zip(testResults, params))

        else:
            for circuit in generatedTests:
                self.quantumFunction(circuit)

            generatedTestPre = [x[0].copy() for x in self.initTests]
            filteredTestsPre = [generatedTestPre[index] for index in filteredIndexes]


            if not qu0_pre:
                tests_qu0 = filteredTests
                tests_qu1 = filteredTestsPre
            else:
                tests_qu0 = filteredTestsPre
                tests_qu1 = filteredTests


            #can reuse testAssertEqual with data from 2 runTestsAssertProbability zipped together
            dataFrom_qu0 = TestExecutor().runTestsAssertProbability(tests_qu0, self.testProperty.nbTrials, \
                self.testProperty.nbMeasurements, qu0, self.testProperty.nbClassicalBits + 1, basis, self.testProperty.backend)
            dataFrom_qu1 = TestExecutor().runTestsAssertProbability(tests_qu1, self.testProperty.nbTrials, \
                self.testProperty.nbMeasurements, qu1, self.testProperty.nbClassicalBits + 1, basis, self.testProperty.backend)


            formattedData = tuple(zip(dataFrom_qu0, dataFrom_qu1))
            testResults = StatAnalyser().testAssertEqual(self.testProperty.p_value, formattedData)

            #gets the theta/phi each qubit was initialised with
            qu0Params = [(self.initTests[index][1].get(qu0, 0),
                self.initTests[index][2].get(qu0, 0)) for index in filteredIndexes]
            qu1Params = [(self.initTests[index][1].get(qu1, 0),
                self.initTests[index][2].get(qu1, 0)) for index in filteredIndexes]
            params = tuple(zip(qu0Params, qu1Params))

            testResultsWithInit = tuple(zip(testResults, params))

        return testResultsWithInit



    """
    This method is a wrapper around assertEqualData that outputs the results
    to the users

    INPUTS:
        - qu0: int = the index of the first qubit to compare
        - qu1: int = the index of the second qubit to compare
        - qu0_pre: boolean = whether the first qubit should be compared
            before running quantumFunction()
        - qu1_pre: boolean = whether the second qubit should be compared
            before running quantumFunction()
        - basis: str = the basis in which the measurements can take place
        - filter_qc: function[QuantumCircuit => bool] or None = function applied
            to a qc that filters out tests based on an input criterion

    OUTPUTS:
        - List of the results for each test:
            ~ A result is a tuple containg a boolean (the result of one test),
            the thetas and the phis used to initialise the first and the second qubits
    """
    def assertEqual(self, qu0, qu1, qu0_pre=False, qu1_pre=False, basis="z", filter_qc=None):
        results = self.assertEqualData(qu0, qu1, qu0_pre, qu1_pre, basis, filter_qc)

        print(f"AssertEqual({qu0}{'_pre' if qu0_pre else ''}, {qu1}{'_pre' if qu1_pre else ''}) results using basis {basis.upper()}:")

        failed = False
        nbFailed = 0
        for testIndex, testResult in enumerate(results):
            if not testResult[0]:
                failed = True
                nbFailed += 1
                print(f"Test at index {testIndex} failed with qubits initialised to:")
                print(f"qu0: Theta = {testResult[1][0][0]} Phi = {testResult[1][0][1]}")
                print(f"qu1: Theta = {testResult[1][1][0]} Phi = {testResult[1][1][1]}")

        if failed:
            print(f"Not all tests have succeeded: {len(results) - nbFailed} / {len(results)} succeeded\n")
        else:
            print(f"All {len(results)} tests have succeeded!\n")

        return results


    """
    This method is a wrapper around assertEqualData that outputs the results
    to the users
    The "Not" is evaluated by negating all booleans returned by assertEqualData

    INPUTS:
        - qu0: int = the index of the first qubit to compare
        - qu1: int = the index of the second qubit to compare
        - qu0_pre: boolean = whether the first qubit should be compared
            before running quantumFunction()
        - qu1_pre: boolean = whether the second qubit should be compared
            before running quantumFunction()
        - basis: str = the basis in which the measurements can take place
        - filter_qc: function[QuantumCircuit => bool] or None = function applied
            to a qc that filters out tests based on an input criterion

    OUTPUTS:
        - List of the results for each test:
            ~ A result is a tuple containg a boolean (the result of one test),
            the thetas and the phis used to initialise the first and the second qubits
    """
    def assertNotEqual(self, qu0, qu1, qu0_pre=False, qu1_pre=False, basis="z", filter_qc=None):
        oppositeResults = self.assertEqualData(qu0, qu1, qu0_pre, qu1_pre, basis, filter_qc)

        results = [(not x[0], x[1]) for x in oppositeResults]

        print(f"AssertNotEqual({qu0}{'_pre' if qu0_pre else ''}, {qu1}{'_pre' if qu1_pre else ''}) results using basis {basis.upper()}:")

        failed = False
        nbFailed = 0
        for testIndex, testResult in enumerate(results):
            if not testResult[0]:
                failed = True
                nbFailed += 1
                print(f"Test at index {testIndex} failed with qubits initialised to:")
                print(f"qu0: Theta = {testResult[1][0][0]} Phi = {testResult[1][0][1]}")
                print(f"qu1: Theta = {testResult[1][1][0]} Phi = {testResult[1][1][1]}")

        if failed:
            print(f"Not all tests have succeeded: {len(results) - nbFailed} / {len(results)} succeeded\n")
        else:
            print(f"All {len(results)} tests have succeeded!\n")

        return results




    """
    This method handles all the required data to evaluate whether two qubits are entangled

    INPUTS:
        - qu0: int = the index of the first qubit to compare
        - qu1: int = the index of the second qubit to compare
        - basis: str = the basis in which the measurements can take place
        - filter_qc: function[QuantumCircuit => bool] or None = function applied
            to a qc that filters out tests based on an input criterion

    OUTPUTS:
        - List of the results for each test:
            ~ A result is a tuple containg a boolean (the result of one test),
            the thetas and the phis used to initialise the first and the second qubits
    """
    def assertEntangledData(self, qu0, qu1, basis, filter_qc):

        generatedTests = [qc.copy() for qc, theta, phi in self.initTests]

        for generatedTest in generatedTests:
            self.quantumFunction(generatedTest)

        filteredIndexes, filteredTests = getFilteredInfo(generatedTests, filter_qc)


        dataFromExec = TestExecutor().runTestsAssertEntangled(filteredTests,
                                                              self.testProperty.nbTrials,
                                                              self.testProperty.nbMeasurements,
                                                              qu0,
                                                              qu1,
                                                              self.testProperty.nbClassicalBits,
                                                              self.testProperty.nbClassicalBits + 1,
                                                              basis,
                                                              self.testProperty.backend)

        testResults = StatAnalyser().testAssertEntangled(self.testProperty.p_value, dataFromExec)


        qu0Params = [(self.initTests[index][1].get(qu0, 0),
            self.initTests[index][2].get(qu0, 0)) for index in filteredIndexes]
        qu1Params = [(self.initTests[index][1].get(qu1, 0),
            self.initTests[index][2].get(qu1, 0)) for index in filteredIndexes]
        params = tuple(zip(qu0Params, qu1Params))

        testResultsWithInit = tuple(zip(testResults, params))

        return testResultsWithInit


    """
    This method is a wrapper of assertEntangledData that outputs the results to the user

    INPUTS:
        - qu0: int = the index of the first qubit to compare
        - qu1: int = the index of the second qubit to compare
        - basis: str = the basis in which the measurements can take place
        - filter_qc: function[QuantumCircuit => bool] or None = function applied
            to a qc that filters out tests based on an input criterion

    OUTPUTS:
        - List of the results for each test:
            ~ A result is a tuple containg a boolean (the result of one test),
            the thetas and the phis used to initialise the first and the second qubits
    """
    def assertEntangled(self, qu0, qu1, basis="z", filter_qc=None):
        results = self.assertEntangledData(qu0, qu1, basis, filter_qc)

        print(f"AssertEntangled({qu0}, {qu1}) results using basis {basis.upper()}:")

        failed = False
        nbFailed = 0
        for testIndex, testResult in enumerate(results):
            if not testResult[0]:
                failed = True
                nbFailed += 1
                print(f"Test at index {testIndex} failed with qubits initialised to:")
                print(f"qu0: Theta = {testResult[1][0][0]} Phi = {testResult[1][0][1]}")
                print(f"qu1: Theta = {testResult[1][1][0]} Phi = {testResult[1][1][1]}")

        if failed:
            print(f"Not all tests have succeeded: {len(results) - nbFailed} / {len(results)} succeeded\n")
        else:
            print(f"All {len(results)} tests have succeeded!\n")


        return results


    """
    This method is a wrapper of assertEntangledData that outputs the results to the user
    The result booleans are negated for the "Not" evaluation

    INPUTS:
        - qu0: int = the index of the first qubit to compare
        - qu1: int = the index of the second qubit to compare
        - basis: str = the basis in which the measurements can take place
        - filter_qc: function[QuantumCircuit => bool] or None = function applied
            to a qc that filters out tests based on an input criterion

    OUTPUTS:
        - List of the results for each test:
            ~ A result is a tuple containg a boolean (the result of one test),
            the thetas and the phis used to initialise the first and the second qubits
    """

    def assertNotEntangled(self, qu0, qu1, basis="z", filter_qc=None):
        oppositeResults = self.assertEntangledData(qu0, qu1, basis, filter_qc)

        results = [(not x[0], x[1]) for x in oppositeResults]

        print(f"AsserNotEntangled({qu0}, {qu1}) results using basis {basis.upper()}:")

        failed = False
        nbFailed = 0
        for testIndex, testResult in enumerate(results):
            if not testResult[0]:
                failed = True
                nbFailed += 1
                print(f"Test at index {testIndex} failed with qubits initialised to:")
                print(f"qu0: Theta = {testResult[1][0][0]} Phi = {testResult[1][0][1]}")
                print(f"qu1: Theta = {testResult[1][1][0]} Phi = {testResult[1][1][1]}")

        if failed:
            print(f"Not all tests have succeeded: {len(results) - nbFailed} / {len(results)} succeeded\n")
        else:
            print(f"All {len(results)} tests have succeeded!\n")


        return results



    """
    This method evaluates wether a given qubit is in state |0> with a given probability

    INPUTS:
        - qu0: int = the index of the qubit to test
        - expectedProba: float = expected probability of the qubit to be in state |0>
        - qu0_pre: bool = whether the data will be sampled before the application of the quantumFunction
        - basis: str = the basis in which the measurements can take place
        - filter_qc: function[QuantumCircuit => bool] or None = function applied
            to a qc that filters out tests based on an input criterion

    OUTPUTS:
        - List of the results for each test:
            ~ A result is a tuple containg a boolean (the result of one test),
            the thetas and the phis used to initialise the qubit
    """
    def assertProbabilityData(self, qu0, expectedProba, qu0_pre, basis, filter_qc):

        expectedProbas = [expectedProba for _ in range(self.testProperty.nbTests)]

        generatedTests = [qc.copy() for qc, theta, phi in self.initTests]

        #Only apply the functions if specified
        if not qu0_pre:
            for generatedTest in generatedTests:
                self.quantumFunction(generatedTest)


        filteredIndexes, filteredTests = getFilteredInfo(generatedTests, filter_qc)


        dataFromExec = TestExecutor().runTestsAssertProbability(filteredTests,
                                                                self.testProperty.nbTrials,
                                                                self.testProperty.nbMeasurements,
                                                                qu0,
                                                                self.testProperty.nbClassicalBits + 1,
                                                                basis,
                                                                self.testProperty.backend)

        testResults = StatAnalyser().testAssertProbability(self.testProperty.p_value, expectedProbas, dataFromExec)

        qu0Params = [(self.initTests[index][1].get(qu0, 0),
            self.initTests[index][2].get(qu0, 0)) for index in filteredIndexes]

        testResultsWithInit = tuple(zip(testResults, qu0Params))

        return testResultsWithInit


    """
    This method is a wrapper around assertprobabilitydata that outputs the results
    to the user

    inputs:
        - qu0: int = the index of the qubit to test
        - expectedproba: float = expected probability of the qubit to be in state |0>
        - qu0_pre: bool = whether the data will be sampled before the application of the quantumfunction
        - basis: str = the basis in which the measurements can take place
        - filter_qc: function[quantumcircuit => bool] or none = function applied
            to a qc that filters out tests based on an input criterion

    outputs:
        - list of the results for each test:
            ~ a result is a tuple containg a boolean (the result of one test),
            the thetas and the phis used to initialise the qubit
    """
    def assertProbability(self, qu0, expectedProba, qu0_pre=False, basis="z", filter_qc=None):
        results = self.assertProbabilityData(qu0, expectedProba, qu0_pre, basis, filter_qc)

        print(f"AssertProbability({qu0}{'_pre' if qu0_pre else ''}, {expectedProba}) results using basis {basis.upper()}:")

        failed = False
        nbFailed = 0
        for testIndex, testResult in enumerate(results):
            if not testResult[0]:
                failed = True
                nbFailed += 1
                print(f"Test at index {testIndex} failed with qubits initialised to:")
                print(f"qu0: Theta = {testResult[1][0]} Phi = {testResult[1][1]}")

        if failed:
            print(f"Not all tests have succeeded: {len(results) - nbFailed} / {len(results)} succeeded\n")
        else:
            print(f"All {len(results)} tests have succeeded!\n")


        return results




    """
    This method is a wrapper around assertProbabilityData that outputs the results
    to the user
    It negates the boolean values

    INPUTS:
        - qu0: int = the index of the qubit to test
        - expectedProba: float = expected probability of the qubit to be in state |0>
        - qu0_pre: bool = whether the data will be sampled before the application of the quantumFunction
        - basis: str = the basis in which the measurements can take place
        - filter_qc: function[QuantumCircuit => bool] or None = function applied
            to a qc that filters out tests based on an input criterion

    OUTPUTS:
        - List of the results for each test:
            ~ A result is a tuple containg a boolean (the result of one test),
            the thetas and the phis used to initialise the qubit
    """
    def assertNotProbability(self, qu0, expectedProba, qu0_pre=False, basis="z", filter_qc=None):
        oppositeResults = self.assertProbabilityData(qu0, expectedProba, qu0_pre, basis, filter_qc)

        results = [(not x[0], x[1]) for x in oppositeResults]

        print(f"AssertNotProbability({qu0}{'_pre' if qu0_pre else ''}, {expectedProba}) results using basis {basis.upper()}:")

        failed = False
        nbFailed = 0
        for testIndex, testResult in enumerate(results):
            if not testResult[0]:
                failed = True
                nbFailed += 1
                print(f"Test at index {testIndex} failed with qubits initialised to:")
                print(f"qu0: Theta = {testResult[1][0]} Phi = {testResult[1][1]}")

        if failed:
            print(f"Not all tests have succeeded: {len(results) - nbFailed} / {len(results)} succeeded\n")
        else:
            print(f"All {len(results)} tests have succeeded!\n")


        return results




    """
    This method asserts that a qubit's state has teleported from "sent" to "received"

    inputs:
        - sent: int = the index of the first qubit to test
        - received: int = the index of the second qubit to test
        - basis: str = the basis in which the measurements can take place
        - filter_qc: function[quantumcircuit => bool] or none = function applied
            to a qc that filters out tests based on an input criterion

    outputs:
        - list of the results for each test:
            ~ a result is a tuple containg a boolean (the result of one test),
            the thetas and the phis used to initialise the qubit
    """
    def assertTeleportedData(self, sent, received, basis, filter_qc):

        generatedTests = [qc.copy() for qc, theta, phi in self.initTests]

        for generatedTest in generatedTests:
            self.quantumFunction(generatedTest)


        filteredIndexes, filteredTests = getFilteredInfo(generatedTests, filter_qc)


        expectedProbas = []
        for qc, thetas, phis in self.initTests:
            expectedProba = cos(radians(thetas[sent]) / 2) ** 2
            expectedProbas.append(expectedProba)

        dataFromReceived = TestExecutor().runTestsAssertProbability(filteredTests,
                                                                    self.testProperty.nbTrials,
                                                                    self.testProperty.nbMeasurements,
                                                                    received,
                                                                    self.testProperty.nbClassicalBits + 1,
                                                                    basis,
                                                                    self.testProperty.backend)

        testResults = StatAnalyser().testAssertProbability(self.testProperty.p_value, expectedProbas, dataFromReceived)

        qu0Params = [(self.initTests[index][1].get(sent, 0),
            self.initTests[index][2].get(sent, 0)) for index in filteredIndexes]
        qu1Params = [(self.initTests[index][1].get(received, 0),
            self.initTests[index][2].get(received, 0)) for index in filteredIndexes]
        params = tuple(zip(qu0Params, qu1Params))

        testResultsWithInit = tuple(zip(testResults, params))

        return testResultsWithInit



    def assertTeleported(self, sent, received, basis="z", filter_qc=None):
        results = self.assertTeleportedData(sent, received, basis, filter_qc)

        print(f"AssertTeleported({sent}, {received}) results using basis {basis.upper()}:")

        failed = False
        nbFailed = 0
        for testIndex, testResult in enumerate(results):
            if not testResult[0]:
                failed = True
                nbFailed += 1
                print(f"Test at index {testIndex} failed with qubits initialised to:")
                print(f"sent: Theta = {testResult[1][0][0]} Phi = {testResult[1][0][1]}")

        if failed:
            print(f"Not all tests have succeeded: {len(results) - nbFailed} / {len(results)} succeeded\n")
        else:
            print(f"All {len(results)} tests have succeeded!\n")

        return results



    def assertNotTeleported(self, sent, received, basis="z", filter_qc=None):
        oppositeResults = self.assertTeleportedData(sent, received, basis, filter_qc)

        results = [(not x[0], x[1]) for x in oppositeResults]

        print(f"AssertTeleported({sent}, {received}) results using basis {basis.upper()}:")

        failed = False
        nbFailed = 0
        for testIndex, testResult in enumerate(results):
            if not testResult[0]:
                failed = True
                nbFailed += 1
                print(f"Test at index {testIndex} failed with qubits initialised to:")
                print(f"sent: Theta = {testResult[1][0][0]} Phi = {testResult[1][0][1]}")

        if failed:
            print(f"Not all tests have succeeded: {len(results) - nbFailed} / {len(results)} succeeded\n")
        else:
            print(f"All {len(results)} tests have succeeded!\n")

        return results



    def assertStateData(self, qu0, theta, phi, isRadian, qu0_pre, filter_qc):

        generatedTests = [qc.copy() for qc, theta, phi in self.initTests]

        #Only apply the functions if specified
        if not qu0_pre:
            for generatedTest in generatedTests:
                self.quantumFunction(generatedTest)


        filteredIndexes, filteredTests = getFilteredInfo(generatedTests, filter_qc)



        dataFromExec = TestExecutor().runTestsAssertState(filteredTests,
                                                          self.testProperty.nbTrials,
                                                          self.testProperty.nbMeasurements,
                                                          qu0,
                                                          self.testProperty.nbClassicalBits + 1,
                                                          self.testProperty.backend)


        testCircuit = QuantumCircuit(1, 1)
        testCircuit.initialize(thetaPhiToStateVector(theta, phi, isRadian), 0)
        testCircuits = [testCircuit.copy() for _ in range(len(filteredTests))]
        dataFromTestCircuit = TestExecutor().runTestsAssertState(testCircuits,
                                                                 self.testProperty.nbTrials,
                                                                 self.testProperty.nbMeasurements,
                                                                 0,
                                                                 0,
                                                                 self.testProperty.backend)

        testResultsZ = StatAnalyser().testAssertEqual(self.testProperty.p_value,
                tuple(zip(dataFromExec[0], dataFromTestCircuit[0])))
        testResultsY = StatAnalyser().testAssertEqual(self.testProperty.p_value,
                tuple(zip(dataFromExec[1], dataFromTestCircuit[1])))
        testResultsX = StatAnalyser().testAssertEqual(self.testProperty.p_value,
                tuple(zip(dataFromExec[2], dataFromTestCircuit[2])))

        testResults = [testResultsZ[index] and testResultsY[index] and testResultsX[index] for index in range(len(filteredTests))]


        if filter_qc == None:
            qu0Params = [(x[1].get(qu0, 0), x[2].get(qu0, 0)) for x in self.initTests]
        else:
            qu0Params = [(self.initTests[index][1].get(qu0, 0), self.initTests[index][2].get(qu0, 0)) for index in self.indexNotFilteredOut]

        testResultsWithInit = tuple(zip(testResults, qu0Params))

        return testResultsWithInit




    def assertState(self, qu0, theta, phi, isRadian=False, qu0_pre=False, filter_qc=None):

        results = self.assertStateData(qu0, theta, phi, isRadian, qu0_pre, filter_qc)

        print(f"AssertState({qu0}{'_pre' if qu0_pre else ''}, {theta}, {phi}) results:")

        failed = False
        nbFailed = 0
        for testIndex, testResult in enumerate(results):
            if not testResult[0]:
                failed = True
                nbFailed += 1
                print(f"Test at index {testIndex} failed with qubits initialised to:")
                print(f"qu0: Theta = {testResult[1][0]} Phi = {testResult[1][1]} degrees")

        if failed:
            print(f"Not all tests have succeeded: {len(results) - nbFailed} / {len(results)} succeeded\n")
        else:
            print(f"All {len(results)} tests have succeeded!\n")

        return results


    def assertNotState(self, qu0, theta, phi, isRadian=False, qu0_pre=False, filter_qc=None):

        oppositeResults = self.assertStateData(qu0, theta, phi, isRadian, qu0_pre, filter_qc)

        results = [(not x[0], x[1]) for x in oppositeResults]

        print(f"AssertNotState({qu0}{'_pre' if qu0_pre else ''}, {theta}, {phi}) results:")

        failed = False
        nbFailed = 0
        for testIndex, testResult in enumerate(results):
            if not testResult[0]:
                failed = True
                nbFailed += 1
                print(f"Test at index {testIndex} failed with qubits initialised to:")
                print(f"qu0: Theta = {testResult[1][0]} Phi = {testResult[1][1]} degrees")

        if failed:
            print(f"Not all tests have succeeded: {len(results) - nbFailed} / {len(results)} succeeded\n")
        else:
            print(f"All {len(results)} tests have succeeded!\n")

        return results



    def assertMostCommonData(self,
                               outcome,
                               filter_qc):

        if isinstance(outcome, str):
            outcome = outcome[::-1]
        else:
            outcome = [x[::-1] for x in outcome]

        generatedTests = [qc.copy() for qc, theta, phi in self.initTests]

        for generatedTest in generatedTests:
            self.quantumFunction(generatedTest)

        filteredIndexes, filteredTests = getFilteredInfo(generatedTests, filter_qc)

        dataFromExec = TestExecutor().runTestsAssertMostProbable(filteredTests,
                self.testProperty.nbMeasurements, self.testProperty.backend)

        results = StatAnalyser().testAssertMostCommon(dataFromExec, outcome)

        return results


    def assertMostCommon(self,
                         outcome,
                         filter_qc=None):

        results = self.assertMostCommonData(outcome, filter_qc)

        print(f"AssertMostCommon({outcome}) results:")

        failed = False
        nbFailed = 0
        for testIndex, testResult in enumerate(results):
            if not testResult:
                failed = True
                nbFailed += 1
                print(f"Test at index {testIndex} failed")

        if failed:
            print(f"Not all tests have succeeded: {len(results) - nbFailed} / {len(results)} succeeded\n")
        else:
            print(f"All {len(results)} tests have succeeded!\n")

        return results



    #Default functions that will usually overwritten by the user
    def property(self):
        return TestProperty()
    def quantumFunction(self, qc):
        pass
    def assertions(self):
        pass


    def run(self):
        print(f"Running tests for {type(self).__name__}:\n")

        self.testProperty = self.property()

        self.initTests = TestCaseGenerator().generateTests(self.testProperty)

        self.assertions()

        print(f"Tests for {type(self).__name__} finished\n")

    def runTests(self):
        self.run()
