import os
from typing import Set, List, Dict


def getAllInstantiableSubclasses(parentClass):
    """

    :param parentClass: the class that all its subclasses must be returned
    :type parentClass: Type[MutationOperator]
    :return: set of MutationOperator instantiable subclasses
    :rtype: set
    """
    allInstantiableSubclasses = set()

    for subClass in parentClass.__subclasses__():
        if subClass.instantiable:
            allInstantiableSubclasses.add(subClass)
        allInstantiableSubclasses.update(getAllInstantiableSubclasses(subClass))

    return allInstantiableSubclasses


class Writer(object):
    instantiable = False
    name = "Writer"

    def __init__(self, outputPath):
        self.outputPath = outputPath
        self.extension = ".dummy"
        self.makeOutputPath()

    def makeOutputPath(self):
        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

    def createTargetFormat(self, metricValues: Dict[str, List[int]], metricLabels: List[str]) -> bytes:
        pass

    def createFinalReportTargetFormat(self, finalReport: List[list]) -> bytes:
        pass

    def write(self, filePath: str, fileContent: bytes):
        with open(filePath + self.extension, 'wb') as outputHandle:
            outputHandle.write(fileContent)


def getAllWriters() -> Set[Writer]:
    return getAllInstantiableSubclasses(Writer)
