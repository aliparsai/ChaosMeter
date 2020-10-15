import os
from typing import Dict, List
from chaosmeter.writers.Writer import Writer


class CSVWriter(Writer):
    instantiable = True
    name = "CSV Writer"

    def __init__(self, outputPath):
        super().__init__(outputPath)
        self.extension = ".csv"

    def createTargetFormat(self, metricValues: Dict[str, List[int]], metricLabels: List[str]) -> bytes:
        fileContentLines = [';'.join(metricLabels)]

        for methodName in metricValues.keys():
            fileContentLines.append(methodName + ';' + ';'.join([str(x) for x in metricValues[methodName]]))

        fileContent = os.linesep.join(fileContentLines)
        return fileContent.encode()

    def createFinalReportTargetFormat(self, finalReport: List[list]) -> bytes:
        fileContentLines = [';'.join([str(x) for x in line]) for line in finalReport]
        fileContent = os.linesep.join(fileContentLines)
        return fileContent.encode()



